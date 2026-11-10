# -*- coding: utf-8 -*-
"""Pruefungen und Abnahmewerte fuer die Demodaten.

Die Pruefungen lesen die GESCHRIEBENEN CSV-Dateien zurueck, nicht das
Modell im Speicher -- so faellt auch ein Fehler im Schreiben auf.

Enthalten ist ein kleiner Nachbau der Statement-Logik des Visuals
(Levels-Pfade, synthetische Zwischensummen, Vorzeichenkonvention,
Bestands- statt Summenbildung, Formelauflösung). Damit lassen sich die
Kontrollzeilen und die Abnahmewerte wirklich nachrechnen statt sie nur
zu behaupten.
"""

import csv
import io
import os
import re

SCENARIOS = ["AC", "PY", "PL", "FC"]
# Die Werte liegen in Basiseinheiten (EUR, CHF, JPY ...). Toleranz der
# Abstimmungen in Basiseinheiten -- geschrieben wird mit zwei
# Nachkommastellen, die Rundung summiert sich ueber rund 60 Zeilen.
TOL = 5.0
MIO = 1000000.0
_REF = re.compile(r"\[([^\]]+)\]")
_TOKEN = re.compile(r"\s*(\[[^\]]+\]|[0-9]+(?:[.,][0-9]+)?|[-+*/()])")


# ---------------------------------------------------------------------------
# Einlesen
# ---------------------------------------------------------------------------
def load(out_dir):
    def rd(name):
        with io.open(os.path.join(out_dir, name), encoding="utf-8") as fh:
            return list(csv.DictReader(fh, delimiter=";"))

    dim = rd("dim-konten.csv")
    datum = rd("dim-datum.csv")
    ges = rd("dim-gesellschaft.csv")
    reg = rd("dim-region.csv")
    cur = rd("dim-waehrung.csv")
    kurse = rd("fact-kurse.csv")

    fact = {}
    months = set()
    entities = set()
    with io.open(os.path.join(out_dir, "fact-abschluss.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            fact[(r["AccountID"], r["EntityID"], r["Monat"])] = r
            months.add(r["Monat"])
            entities.add(r["EntityID"])
    return (dim, datum, ges, reg, cur, kurse, fact,
            sorted(months), sorted(entities))


def num(s):
    if s is None or s == "":
        return None
    return float(s)


# ---------------------------------------------------------------------------
# Nachbau der Statement-Logik
# ---------------------------------------------------------------------------
def level_path(row, lang="de"):
    """Pfad aus den Level-Spalten: endet bei leerem oder wiederholtem Wert."""
    cols = ["L1", "L2", "L3", "L4", "L5", "L6"]
    if lang == "en":
        cols = [c + " EN" for c in cols]
    path = []
    for c in cols:
        v = (row.get(c) or "").strip()
        if v == "":
            break
        if path and v == path[-1]:
            break
        path.append(v)
    return tuple(path)


class Statement:
    """Ein aufgeloestes Statement fuer eine Filterkombination."""

    def __init__(self, dim, fact, statement, scenario, months, entities,
                 lang="de", currency="EUR"):
        self.values = {}          # Zeilenname -> Wert
        self.by_id = {}           # AccountID -> Wert
        self.errors = []
        # EUR ist die Konzernwaehrung, LW die jeweilige Landeswaehrung
        self.column = scenario if currency == "EUR" else scenario + "_LW"
        name_col = "Name" if lang == "de" else "Name EN"
        formula_col = "FormulaDef" if lang == "de" else "FormulaDef EN"

        rows = [r for r in dim if r["Abschluss"] == statement]
        # Levels-Modus: Zeilen mit komplett leeren L-Spalten werden
        # uebersprungen (das sind die Knotenzeilen fuer Parent-Child).
        leafs = []
        for r in rows:
            path = level_path(r, lang)
            if not path:
                continue
            leafs.append((r, path))

        # Kinder je Pfad sammeln
        children = {}
        node_agg = {}
        for r, path in leafs:
            for depth in range(1, len(path)):
                children.setdefault(path[:depth], set()).add(path[:depth + 1])

        order = []
        leaf_value = {}
        for r, path in leafs:
            base = (r["RowType"] or "").lower().split()[0]
            agg = r["Zeitaggregation"]
            sign = int(r["SignConvention"])
            if base in ("account", "subtotal"):
                v = self._series_value(fact, r["AccountID"], self.column,
                                       months, entities, agg)
                leaf_value[path] = leaf_value.get(path, 0.0) + (v or 0.0) * sign
                node_agg[path] = agg
            order.append((r, path, base, agg, sign))

        # Zwischensummen von unten nach oben
        def value_of(path):
            if path in leaf_value:
                return leaf_value[path]
            total = 0.0
            for child in children.get(path, ()):
                total += value_of(child)
            leaf_value[path] = total
            return total

        for path in sorted(children, key=len, reverse=True):
            value_of(path)
        for path in list(leaf_value):
            value_of(path)

        # Namen zuordnen: synthetische Knoten heissen wie ihr Level-Wert
        for path, v in leaf_value.items():
            self.values.setdefault(path[-1], v)
        for r, path, base, agg, sign in order:
            if base in ("account", "subtotal"):
                self.by_id[r["AccountID"]] = leaf_value.get(path, 0.0)

        # Formeln und Kennzahlen in Kontenplanreihenfolge
        for r, path, base, agg, sign in order:
            if base not in ("formula", "kpi"):
                continue
            expr = r[formula_col]
            val = self._eval(expr, r[name_col])
            self.values[r[name_col]] = val
            self.by_id[r["AccountID"]] = val

    def _series_value(self, fact, account_id, column, months, entities, agg):
        """Wert eines Kontos: Fluss summiert, Bestand nimmt die letzte,
        Bestand Anfang die erste belegte Periode der Auswahl."""
        per_month = []
        for mo in months:
            total = None
            for ent in entities:
                row = fact.get((account_id, ent, mo))
                if row is None:
                    continue
                v = num(row[column])
                if v is None:
                    continue
                total = (total or 0.0) + v
            per_month.append(total)
        belegt = [v for v in per_month if v is not None]
        if not belegt:
            return None
        if agg == "Bestand":
            return belegt[-1]
        if agg == "Bestand Anfang":
            return belegt[0]
        return sum(belegt)

    def _eval(self, expr, own_name, depth=0):
        if not expr:
            return None
        if depth > 12:
            self.errors.append("cycle: %s" % own_name)
            return None
        tokens = []
        pos = 0
        while pos < len(expr):
            mo = _TOKEN.match(expr, pos)
            if not mo:
                if expr[pos].isspace():
                    pos += 1
                    continue
                self.errors.append("unparsed %r in %s" % (expr[pos:], own_name))
                return None
            tokens.append(mo.group(1))
            pos = mo.end()

        out = []
        for t in tokens:
            if t.startswith("["):
                ref = t[1:-1]
                if ref in self.by_id:
                    out.append(self.by_id[ref])
                elif ref in self.values:
                    out.append(self.values[ref])
                else:
                    self.errors.append("unknown reference [%s] in %s"
                                       % (ref, own_name))
                    return None
            elif re.match(r"^[0-9]", t):
                out.append(float(t.replace(",", ".")))
            else:
                out.append(t)

        py = []
        for t in out:
            py.append(t if isinstance(t, str) else repr(t if t is not None else 0.0))
        try:
            return eval(" ".join(py), {"__builtins__": {}}, {})
        except ZeroDivisionError:
            return None
        except Exception as exc:                       # pragma: no cover
            self.errors.append("eval %s: %s" % (own_name, exc))
            return None


# ---------------------------------------------------------------------------
# Pruefungen
# ---------------------------------------------------------------------------
def run(accounts, value_tags, paths, out_dir):
    (dim, datum, ges, reg, cur, kurse, fact,
     months, entities) = load(out_dir)
    problems = []
    notes = []

    ent_cur = {r["EntityID"]: r["Währung"] for r in ges}
    ent_name = {r["EntityID"]: r["Gesellschaft"] for r in ges}
    ent_region = {r["EntityID"]: r["Region"] for r in ges}
    rate = {(r["Währung"], r["Monat"]):
            (float(r["Kurs Durchschnitt"]), float(r["Kurs Stichtag"]))
            for r in kurse}

    all_months = months
    y2026 = [m for m in months if m.startswith("2026")]
    y2025 = [m for m in months if m.startswith("2025")]
    ytd2026 = [m for m in y2026 if m <= "2026-10"]

    # --- 1. Schluessel und Struktur ---
    ids = [r["AccountID"] for r in dim]
    if len(ids) != len(set(ids)):
        problems.append("AccountID nicht eindeutig")
    id_set = set(ids)
    for r in dim:
        if r["ParentAccountID"] and r["ParentAccountID"] not in id_set:
            problems.append("ParentAccountID %s existiert nicht"
                            % r["ParentAccountID"])

    sorts = [int(r["SortOrder"]) for r in dim]
    if len(sorts) != len(set(sorts)):
        problems.append("SortOrder nicht eindeutig")
    if any(r["SortOrder"] == "" for r in dim):
        problems.append("SortOrder hat Luecken")

    # --- 1b. Referentielle Integritaet ---
    dim_dates = {r["Datum"] for r in datum}
    dim_ents = {r["EntityID"] for r in ges}
    dim_regs = {r["RegionID"] for r in reg}
    dim_curs = {r["Währung"] for r in cur}
    missing = {"AccountID": 0, "Datum": 0, "EntityID": 0}
    with_fact = set()
    for (acc, ent, mo), row in fact.items():
        if acc not in id_set:
            missing["AccountID"] += 1
        if row["Datum"] not in dim_dates:
            missing["Datum"] += 1
        if ent not in dim_ents:
            missing["EntityID"] += 1
        with_fact.add(acc)
    for key, cnt in missing.items():
        if cnt:
            problems.append("%d Faktzeilen mit unbekanntem %s" % (cnt, key))
    if {r["RegionID"] for r in ges} - dim_regs:
        problems.append("dim-gesellschaft verweist auf unbekannte Region")
    if set(ent_cur.values()) - dim_curs:
        problems.append("dim-gesellschaft verweist auf unbekannte Waehrung %s"
                        % sorted(set(ent_cur.values()) - dim_curs))
    if {r["Währung"] for r in kurse} - dim_curs:
        problems.append("fact-kurse verweist auf unbekannte Waehrung")
    fehlende_kurse = [(c, m) for c in set(ent_cur.values()) for m in months
                      if (c, m) not in rate]
    if fehlende_kurse:
        problems.append("%d fehlende Monatskurse, z. B. %s"
                        % (len(fehlende_kurse), fehlende_kurse[:3]))
    orphan = id_set - with_fact
    if orphan:
        problems.append("%d Konten ohne jede Faktzeile: %s"
                        % (len(orphan), sorted(orphan)[:5]))
    else:
        notes.append("referentielle Integritaet: %d Faktzeilen, alle "
                     "Schluessel aufgeloest, jede Dimensionszeile belegt, "
                     "Monatskurse vollstaendig" % len(fact))

    # --- 2. Eindeutige Zeilennamen (Formelauflösung ist global) ---
    for lang, col in (("DE", "Name"), ("EN", "Name EN")):
        seen = {}
        for r in dim:
            if not level_path(r, "de" if lang == "DE" else "en"):
                continue          # Knotenzeile, im Levels-Modus unsichtbar
            seen.setdefault(r[col], []).append(r["AccountID"])
        dupes = {k: v for k, v in seen.items() if len(v) > 1}
        if dupes:
            problems.append("Zeilennamen %s mehrfach: %s"
                            % (lang, list(dupes)[:5]))

    # --- 3. Level-Pfade ohne Loecher ---
    for r in dim:
        for cols in (["L1", "L2", "L3", "L4", "L5", "L6"],
                     ["L1 EN", "L2 EN", "L3 EN", "L4 EN", "L5 EN", "L6 EN"]):
            vals = [(r.get(c) or "").strip() for c in cols]
            filled = [i for i, v in enumerate(vals) if v]
            if filled and filled != list(range(len(filled))):
                problems.append("Level-Luecke in %s (%s)"
                                % (r["AccountID"], cols[0]))

    # --- 4. Uebersetzungen vollstaendig ---
    for r in dim:
        if level_path(r, "de") and not r["Name EN"]:
            problems.append("keine Uebersetzung fuer %s" % r["Name"])
        for a, b in (("L1", "L1 EN"), ("L2", "L2 EN"), ("L3", "L3 EN"),
                     ("L4", "L4 EN")):
            if r[a] and not r[b]:
                problems.append("keine Uebersetzung fuer %s=%s" % (a, r[a]))

    # --- 5. Ruhende Konten ---
    def is_zero(v):
        n = num(v)
        return n is None or abs(n) < 1.0

    ruhend = [r["AccountID"] for r in dim
              if (r["RowType"] or "").lower().startswith("account")
              and all(is_zero(fact[(r["AccountID"], e, m)]["AC"])
                      for e in entities for m in months[:3])]
    if len(ruhend) > 20:
        problems.append("%d Konten ohne Ist-Werte, mehr als erwartet"
                        % len(ruhend))
    else:
        notes.append("%d ruhende Konten ohne Ist-Werte (Testfall "
                     "\"Nullzeilen ausblenden\")" % len(ruhend))

    # --- 6. Formeln und Kontrollzeilen rechnen, in beiden Waehrungen ---
    checked = 0
    for currency in ("EUR", "LW"):
        for lang in ("de", "en"):
            for stmt in ("GuV", "Bilanz", "Cashflow"):
                for scen in SCENARIOS:
                    for mset, label in ((all_months, "2025-2026"),
                                        (y2026, "2026"), (y2025, "2025")):
                        st = Statement(dim, fact, stmt, scen, mset, entities,
                                       lang, currency)
                        checked += 1
                        for err in st.errors:
                            problems.append("%s/%s/%s/%s/%s: %s"
                                            % (currency, lang, stmt, scen,
                                               label, err))
                        if stmt == "Bilanz":
                            key = ("Bilanzkontrolle" if lang == "de"
                                   else "Balance sheet check")
                        elif stmt == "Cashflow":
                            key = ("Kontrolle Finanzmittelfonds" if lang == "de"
                                   else "Cash reconciliation check")
                        else:
                            continue
                        v = st.values.get(key)
                        if v is None or abs(v) > TOL:
                            problems.append("%s geht nicht auf (%s/%s/%s/%s): %r"
                                            % (key, currency, lang, scen,
                                               label, v))
    notes.append("%d Statement-Kombinationen durchgerechnet (3 Aufstellungen "
                 "x 4 Szenarien x 3 Zeitraeume x DE/EN x EUR und "
                 "Landeswaehrung)" % checked)

    # --- 6b. GuV, Bilanz und Cashflow zeigen denselben Gewinn ---
    # In Landeswaehrung muessen alle drei uebereinstimmen. In EUR gilt das
    # nur fuer GuV und Cashflow (beide zum Durchschnittskurs); die
    # Eigenkapitalzeile steht zum Stichtagskurs und weicht deshalb ab --
    # das ist der Umrechnungseffekt, den IAS 21 genau so erzeugt.
    worst_ni = 0.0
    for currency in ("EUR", "LW"):
        for scen in SCENARIOS:
            for mset, label in ((y2025, "2025"), (y2026, "2026")):
                guv = Statement(dim, fact, "GuV", scen, mset, entities,
                                "de", currency)
                cfl = Statement(dim, fact, "Cashflow", scen, mset, entities,
                                "de", currency)
                a = guv.values.get("Jahresüberschuss")
                b = cfl.values.get("Jahresüberschuss der Periode")
                if a is None or b is None:
                    problems.append("Jahresueberschuss fehlt (%s/%s/%s)"
                                    % (currency, scen, label))
                    continue
                if abs(a - b) > TOL:
                    problems.append("GuV-Gewinn %.0f != Cashflow-Gewinn %.0f "
                                    "(%s/%s/%s)" % (a, b, currency, scen, label))
                worst_ni = max(worst_ni, abs(a - b))
                if currency != "LW":
                    continue
                bil = Statement(dim, fact, "Bilanz", scen, mset, entities,
                                "de", currency)
                ek = bil.values.get("Jahresüberschuss (Konzernanteil)")
                if ek is not None and b and abs(ek - b * (1 - 0.022)) > TOL:
                    problems.append("Eigenkapital-Gewinn %.0f passt nicht zu "
                                    "%.0f (%s/%s)" % (ek, b, scen, label))
    if not any("Gewinn" in p for p in problems):
        notes.append("GuV, Bilanz und Cashflow zeigen denselben "
                     "Jahresueberschuss (max. Abweichung %.2f Einheiten)"
                     % worst_ni)

    # --- 7. Bilanz je Gesellschaft und Monat, in beiden Waehrungen ---
    worst = 0.0
    for currency in ("EUR", "LW"):
        for ent in entities:
            for mo in (months[0], months[len(months) // 2], months[-1]):
                st = Statement(dim, fact, "Bilanz", "AC", [mo], [ent],
                               "de", currency)
                v = st.values.get("Bilanzkontrolle")
                if v is not None:
                    worst = max(worst, abs(v))
    if worst > TOL:
        problems.append("Bilanz je Gesellschaft/Monat weicht ab: %.2f" % worst)
    else:
        notes.append("Bilanz geht auch je einzelner Gesellschaft und "
                     "Einzelmonat auf, in EUR und Landeswaehrung "
                     "(max. Abweichung %.4f Einheiten)" % worst)

    # --- 8. Umrechnung stichprobenweise nachrechnen ---
    # Flussposten zum Durchschnittskurs, Bestandsposten zum Stichtagskurs.
    probe = [("G-rev_export", 0), ("G-admin_gehaelter", 0),
             ("B-goodwill", 1), ("B-zahlungsmittel_bank", 1)]
    worst_fx = 0.0
    n_probe = 0
    for acc, use_close in probe:
        if acc not in id_set:
            problems.append("Pruefkonto %s fehlt" % acc)
            continue
        for ent in entities:
            for mo in (ytd2026[0], ytd2026[-1]):
                row = fact.get((acc, ent, mo))
                eur, lw = num(row["AC"]), num(row["AC_LW"])
                if eur is None or lw is None or abs(lw) < 1.0:
                    continue
                k = rate[(ent_cur[ent], mo)][1 if use_close else 0]
                # relativ pruefen: der Kurs in der CSV ist gerundet, bei
                # 88 Mio. EUR schlaegt die achte Dezimalstelle noch durch
                worst_fx = max(worst_fx, abs(eur - lw / k) / max(abs(eur), 1.0))
                n_probe += 1
    if worst_fx > 1e-6:
        problems.append("Umrechnung weicht relativ um %.2e ab" % worst_fx)
    else:
        notes.append("Umrechnung nachgerechnet an %d Werten: Fluss zum "
                     "Durchschnitts-, Bestand zum Stichtagskurs "
                     "(max. relative Abweichung %.1e)" % (n_probe, worst_fx))

    # --- 9. Plausibilitaet ---
    st26 = Statement(dim, fact, "Bilanz", "AC", ytd2026, entities)
    guv26 = Statement(dim, fact, "GuV", "FC", y2026, entities)
    rev = guv26.values.get("Umsatzerlöse") or 1.0
    cash = st26.values.get("Zahlungsmittel und Zahlungsmitteläquivalente") or 0.0
    eq_ratio = st26.values.get("Eigenkapitalquote") or 0.0
    if not 0.20 <= eq_ratio <= 0.55:
        problems.append("Eigenkapitalquote unplausibel: %.1f %%"
                        % (eq_ratio * 100))
    if not 0.03 <= cash / rev <= 0.14:
        problems.append("Liquiditaetsquote unplausibel: %.1f %%"
                        % (cash / rev * 100))

    cfo = Statement(dim, fact, "Cashflow", "AC", ytd2026, entities)
    resid = cfo.values.get("Sonstige zahlungsunwirksame Posten") or 0.0
    cfo_total = cfo.values.get("Cashflow aus betrieblicher Tätigkeit") or 1.0
    if abs(resid) > abs(cfo_total) * 0.08:
        problems.append("Restposten im Cashflow zu gross: %.1f von %.1f"
                        % (resid / MIO, cfo_total / MIO))
    else:
        notes.append("Restposten im Cashflow %.1f mEUR = %.1f %% des "
                     "operativen Cashflows"
                     % (resid / MIO, resid / cfo_total * 100))
    fx_cash = cfo.values.get("Währungsbedingte Effekte auf den Finanzmittelfonds") or 0.0
    notes.append("Waehrungseffekt auf den Finanzmittelfonds %.1f mEUR "
                 "(haelt die EUR-Ueberleitung exakt)" % (fx_cash / MIO))

    # --- 10. Groessenordnung: nichts darf auf Null runden ---
    werte = [abs(num(r["AC"])) for r in fact.values()
             if num(r["AC"]) not in (None,) and abs(num(r["AC"])) > 0.5]
    werte.sort()
    p10 = werte[len(werte) // 10]
    if p10 < 1000.0:
        problems.append("10 %% der Werte unter 1.000 Einheiten (%.0f) — "
                        "das Visual zeigte sie als Null" % p10)
    else:
        notes.append("kleinster typischer Wert (10 %%-Quantil) %.0f "
                     "Basiseinheiten = %.0f TEUR, rundet also nicht auf Null"
                     % (p10, p10 / 1000.0))

    # --- 11. DataView-Budget ---
    per_stmt = {}
    for r in dim:
        per_stmt[r["Abschluss"]] = per_stmt.get(r["Abschluss"], 0) + 1
    biggest = max(per_stmt.values())
    notes.append("DataView: groesste Aufstellung %d Zeilen x %d Monate = "
                 "%d von 30.000" % (biggest, len(months), biggest * len(months)))

    # --- Bericht ---
    report = []
    report.append("Abnahmewerte PnL ChartkitchenDemoKit")
    report.append("=" * 76)
    report.append("")
    report.append("Konzern DWG Industries SE, Sitz Deutschland")
    report.append("%d Gesellschaften, %d Regionen, %d Waehrungen"
                  % (len(ges), len(reg), len(cur)))
    report.append("Zeitraum %s bis %s, Ist bis 2026-10, Forecast 2026-11/12"
                  % (months[0], months[-1]))
    report.append("")
    report.append("Die CSV-Dateien liefern BASISEINHEITEN der jeweiligen")
    report.append("Waehrung. Dieser Bericht rechnet auf mEUR um.")
    report.append("Unsuffigierte Spalten sind EUR, '_LW' ist Landeswaehrung.")
    report.append("")

    periods = [
        ("YTD Januar bis Oktober 2026 -- Ist gegen Vorjahr und Plan\n"
         "(gleiche 10 Monate in allen Spalten)", ytd2026),
        ("Geschaeftsjahr 2026, 12 Monate -- Forecast gegen Plan\n"
         "(die AC-Spalte enthaelt nur Jan-Okt, weil Nov/Dez offen sind)", y2026),
        ("Geschaeftsjahr 2025, 12 Monate -- abgeschlossen", y2025),
    ]
    for label, mset in periods:
        report.append("-" * 76)
        for line in label.split("\n"):
            report.append(line)
        report.append("-" * 76)
        g = {s: Statement(dim, fact, "GuV", s, mset, entities)
             for s in SCENARIOS}

        def block(title, st_by_scen, absolute, percent=()):
            report.append("%-44s %10s %10s %10s %10s"
                          % (title, "AC", "PY", "PL", "FC"))
            for ln in absolute:
                vals = []
                for s in SCENARIOS:
                    v = st_by_scen[s].values.get(ln)
                    vals.append("%10.1f" % (v / MIO) if v is not None
                                else "%10s" % "-")
                report.append("%-44s %s" % (ln, " ".join(vals)))
            for ln in percent:
                vals = []
                for s in SCENARIOS:
                    v = st_by_scen[s].values.get(ln)
                    vals.append("%9.1f%%" % (v * 100) if v is not None
                                else "%10s" % "-")
                report.append("%-44s %s" % (ln, " ".join(vals)))
            report.append("")

        block("Gewinn- und Verlustrechnung (mEUR)", g,
              ("Umsatzerlöse", "Umsatzkosten", "Rohertrag", "Vertriebskosten",
               "Verwaltungskosten", "Forschung & Entwicklung",
               "Sonstiges betriebliches Ergebnis", "EBITDA", "Abschreibungen",
               "EBIT", "Finanzergebnis", "EBT", "Ertragsteuern",
               "Jahresüberschuss"),
              ("Rohertragsmarge %", "EBITDA-Marge %", "EBIT-Marge %",
               "Nettomarge %"))

        b = {s: Statement(dim, fact, "Bilanz", s, mset, entities)
             for s in SCENARIOS}
        block("Bilanz zum Stichtag (mEUR)", b,
              ("Summe Anlagevermögen", "Summe Umlaufvermögen", "Summe Aktiva",
               "Summe Eigenkapital", "Summe langfristige Schulden",
               "Summe kurzfristige Schulden", "Summe Passiva",
               "Bilanzkontrolle", "Working Capital", "Nettofinanzverschuldung"),
              ("Eigenkapitalquote", "Anlagenintensität", "Verschuldungsgrad",
               "Liquidität 3. Grades"))

        c = {s: Statement(dim, fact, "Cashflow", s, mset, entities)
             for s in SCENARIOS}
        block("Kapitalflussrechnung (mEUR)", c,
              ("Cashflow aus betrieblicher Tätigkeit",
               "Cashflow aus Investitionstätigkeit",
               "Cashflow aus Finanzierungstätigkeit",
               "Veränderung des Finanzmittelfonds",
               "Währungsbedingte Effekte auf den Finanzmittelfonds",
               "Veränderung des Konsolidierungskreises",
               "Zahlungsmittelbestand am Anfang der Periode",
               "Zahlungsmittelbestand am Ende der Periode",
               "Kontrolle Finanzmittelfonds",
               "Free Cashflow", "Investitionen in das Anlagevermögen"),
              ("Cash Conversion", "CapEx-Quote"))

    # --- Umsatz je Gesellschaft, Landeswaehrung und EUR ---
    report.append("-" * 76)
    report.append("Umsatzerloese YTD Januar bis Oktober 2026 je Gesellschaft")
    report.append("Landeswaehrung in Millionen, EUR in mEUR, Ist gegen Plan")
    report.append("-" * 76)
    report.append("%-34s %-4s %11s %11s %9s %9s"
                  % ("", "Wae", "Ist (LW)", "Ist (EUR)", "Plan EUR", "Abw."))
    by_region = {}
    total_eur = 0.0
    for ent in entities:
        lw = Statement(dim, fact, "GuV", "AC", ytd2026, [ent],
                       "de", "LW").values.get("Umsatzerlöse") or 0.0
        eur = Statement(dim, fact, "GuV", "AC", ytd2026, [ent],
                        "de", "EUR").values.get("Umsatzerlöse") or 0.0
        pl = Statement(dim, fact, "GuV", "PL", ytd2026, [ent],
                       "de", "EUR").values.get("Umsatzerlöse") or 0.0
        total_eur += eur
        by_region.setdefault(ent_region[ent], []).append(
            (ent, ent_cur[ent], lw, eur, pl))
    for rg in sorted(by_region):
        rsum = sum(e for _, _, _, e, _ in by_region[rg])
        report.append("%-34s %-4s %11s %11.1f" % (rg, "", "", rsum / MIO))
        for ent, c, lw, eur, pl in sorted(by_region[rg]):
            d = (eur / pl - 1.0) * 100 if pl else 0.0
            report.append("  %-32s %-4s %11.1f %11.1f %9.1f %+8.1f %%"
                          % (ent_name[ent][:32], c, lw / MIO, eur / MIO,
                             pl / MIO, d))
    report.append("%-34s %-4s %11s %11.1f" % ("Konzern", "", "", total_eur / MIO))
    report.append("")

    # --- Waehrungseffekt: Ist zu Vorjahreskursen ---
    report.append("-" * 76)
    report.append("Waehrungseffekt auf die Umsatzerloese, YTD 2026")
    report.append("Ist in EUR gegen Ist zu den Kursen des Vorjahresmonats")
    report.append("-" * 76)
    rev_accs = [(r["AccountID"], int(r["SignConvention"])) for r in dim
                if r["Abschluss"] == "GuV" and r["L1"] == "Umsatzerlöse"
                and (r["RowType"] or "").lower().startswith("account")]
    eff_total = eur_total = cc_total = 0.0
    lines = []
    for ent in entities:
        c = ent_cur[ent]
        e_sum = cc_sum = 0.0
        for mo in ytd2026:
            lw_m = 0.0
            e_m = 0.0
            for acc, sg in rev_accs:
                row = fact.get((acc, ent, mo))
                if row is None:
                    continue
                v_lw, v_eur = num(row["AC_LW"]), num(row["AC"])
                if v_lw is not None:
                    lw_m += v_lw * sg
                if v_eur is not None:
                    e_m += v_eur * sg
            py_mo = "%04d-%s" % (int(mo[:4]) - 1, mo[5:])
            k_py = rate.get((c, py_mo), rate[(c, mo)])[0]
            e_sum += e_m
            cc_sum += lw_m / k_py
        eur_total += e_sum
        cc_total += cc_sum
        if c != "EUR":
            lines.append((ent, c, e_sum, cc_sum))
    report.append("%-34s %-4s %11s %11s %11s"
                  % ("", "Wae", "Ist EUR", "zu PY-Kurs", "Effekt"))
    for ent, c, e_sum, cc_sum in lines:
        report.append("  %-32s %-4s %11.1f %11.1f %11.1f"
                      % (ent_name[ent][:32], c, e_sum / MIO, cc_sum / MIO,
                         (e_sum - cc_sum) / MIO))
    eff_total = eur_total - cc_total
    report.append("  %-32s %-4s %11.1f %11.1f %11.1f"
                  % ("Konzern", "", eur_total / MIO, cc_total / MIO,
                     eff_total / MIO))
    report.append("")
    report.append("  Der Waehrungseffekt betraegt %.1f mEUR = %.2f Prozent"
                  % (eff_total / MIO, eff_total / cc_total * 100))
    report.append("  der Umsatzerloese. Ohne Kursveraenderung waere der")
    report.append("  Konzernumsatz also %.1f mEUR gewesen." % (cc_total / MIO))
    report.append("")

    # --- Kursuebersicht ---
    report.append("-" * 76)
    report.append("Monatskurse, Einheiten der Landeswaehrung je 1 EUR")
    report.append("-" * 76)
    report.append("%-5s %12s %12s %12s %9s"
                  % ("Wae", "Jan 2025", "Okt 2026", "Dez 2026", "Veraend."))
    for r in sorted(cur, key=lambda x: int(x["Sortierung"])):
        c = r["Währung"]
        if c == "EUR":
            continue
        a1 = rate[(c, "2025-01")][0]
        a2 = rate[(c, "2026-10")][0]
        a3 = rate[(c, "2026-12")][0]
        report.append("%-5s %12.4f %12.4f %12.4f %+8.1f %%"
                      % (c, a1, a2, a3, (a3 / a1 - 1.0) * 100))
    report.append("")
    report.append("  Ein steigender Kurs heisst: die Landeswaehrung wird")
    report.append("  schwaecher, ein EUR kauft mehr davon.")
    report.append("")

    report.append("-" * 76)
    report.append("Pruefungen")
    report.append("-" * 76)
    for n in notes:
        report.append("  ok   %s" % n)
    if problems:
        for p in problems:
            report.append("  FEHLER  %s" % p)
    else:
        report.append("  ok   keine Fehler")

    text = "\n".join(report) + "\n"
    with io.open(os.path.join(out_dir, "reconciliation.txt"), "w",
                 encoding="utf-8", newline="\r\n") as fh:
        fh.write(text)
    print(text)
    return problems
