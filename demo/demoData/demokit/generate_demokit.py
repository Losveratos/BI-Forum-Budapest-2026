# -*- coding: utf-8 -*-
"""Generator fuer die Demodaten des PnL ChartkitchenDemoKit.

Erzeugt im eigenen Verzeichnis:

    dim-konten.csv        Kontenplan GuV + Bilanz + Cashflow, DE und EN
    dim-datum.csv         Datumsdimension 1.1.2025 - 31.12.2026, tagesgenau
    dim-gesellschaft.csv  7 Gesellschaften
    dim-region.csv        3 Regionen
    fact-abschluss.csv    Werte je Konto x Gesellschaft x Monat
    reconciliation.txt    Abnahmewerte und Pruefergebnisse

Aufruf:  python generate_demokit.py
Seed ist fest, der Lauf ist byte-identisch reproduzierbar.
"""

import csv
import datetime as dt
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coa_guv import GUV, TRANSLATIONS_GUV
from coa_bilanz_cf import BILANZ, CASHFLOW, TRANSLATIONS_BILANZ_CF
import dims
import engine
from dims import (CURRENCIES, ENTITIES, KONZERNWAEHRUNG, REGIONS, SEGMENTS,
                  build_calendar, month_end, month_sequence)

OUT = os.path.dirname(os.path.abspath(__file__))
TODAY = dt.date(2026, 10, 30)

# Der Motor rechnet in Millionen, ausgeliefert werden BASISEINHEITEN der
# jeweiligen Waehrung (EUR, CHF, JPY ...). Das Visual skaliert selbst:
# seine Einstellung "unit" teilt den Rohwert durch 1e3, 1e6 oder 1e9.
# Lieferte man schon Millionen, zeigte es bei unit = "m" ueberall 0,0.
UNIT = 1000000.0

TRANSLATIONS = {}
TRANSLATIONS.update(TRANSLATIONS_GUV)
TRANSLATIONS.update(TRANSLATIONS_BILANZ_CF)

STATEMENTS = [
    ("GuV", "Income statement", "G", GUV),
    ("Bilanz", "Balance sheet", "B", BILANZ),
    ("Cashflow", "Cash flow statement", "C", CASHFLOW),
]

# Kontonummernkreise je Hauptblock -- nur Kosmetik, damit die Konten
# aussehen wie aus einem echten Hauptbuch.
NUMBER_BASE = {
    "Umsatzerlöse": 400000, "Umsatzkosten": 500000, "Vertriebskosten": 600000,
    "Verwaltungskosten": 650000, "Forschung & Entwicklung": 700000,
    "Sonstiges betriebliches Ergebnis": 750000, "Abschreibungen": 800000,
    "Finanzergebnis": 850000, "Ertragsteuern": 900000,
    "Anlagevermögen": 100000, "Umlaufvermögen": 120000,
    "Eigenkapital": 200000, "Langfristige Schulden": 220000,
    "Kurzfristige Schulden": 240000,
    "Betriebliche Tätigkeit": 300000, "Investitionstätigkeit": 320000,
    "Finanzierungstätigkeit": 340000,
}

# Fussnoten auf einzelnen Zeilen
COMMENTS = {
    "cogs_mat_elektronik": (
        "① Halbleiter-Spotkäufe März bis Mai 2026: Allokationsengpass bei "
        "zwei Vorlieferanten, Mehrkosten rund 26 % auf die Materialgruppe.",
        "① Semiconductor spot purchases March to May 2026: allocation "
        "shortage at two suppliers, around 26 % extra cost on this material group."),
    "cogs_seefracht": (
        "② Seefrachtraten im vierten Quartal 2025 um rund 72 % über Plan "
        "(Umleitung Kap der Guten Hoffnung).",
        "② Ocean freight rates roughly 72 % above plan in Q4 2025 "
        "(Cape of Good Hope diversion)."),
    "admin_public_cloud": (
        "③ Public-Cloud-Kosten wachsen 2026 monatlich um gut 5 %; "
        "Gegenmaßnahmen ab dem ersten Quartal 2027 beschlossen.",
        "③ Public cloud cost grows by a good 5 % per month in 2026; "
        "countermeasures approved for Q1 2027."),
    "fin_fx": (
        "④ Währungsverlust Juni 2026 bei DWG Energy do Brasil aus der "
        "Abwertung des BRL, einmalig -6,8 mEUR.",
        "④ Foreign exchange loss in June 2026 at DWG Energy do Brasil from "
        "the BRL devaluation, one-off -6.8 mEUR."),
    "rev_lizenz": (
        "⑤ Einmaliger Lizenzerlös September 2026 bei DWG Automation GmbH "
        "aus einem Portfolio-Verkauf, 11,0 mEUR.",
        "⑤ One-off licence revenue in September 2026 at DWG Automation GmbH "
        "from a portfolio sale, 11.0 mEUR."),
    "da_impair_goodwill": (
        "⑥ Wertminderung auf den Geschäfts- oder Firmenwert von Mobility "
        "Solutions, Dezember 2025, 21,0 mEUR.",
        "⑥ Impairment of the goodwill of Mobility Solutions, "
        "December 2025, 21.0 mEUR."),
    "bilanzkontrolle": (
        "⑦ Kontrollzeile: Summe Aktiva minus Summe Passiva muss in jeder "
        "Filterkombination 0 ergeben.",
        "⑦ Control row: total assets less total equity and liabilities must "
        "be 0 for every filter combination."),
    "cf_kontrolle": (
        "⑧ Kontrollzeile: Endbestand minus Anfangsbestand minus "
        "Fondsveränderung minus Währungs- und Konsolidierungseffekte = 0.",
        "⑧ Control row: closing balance less opening balance less net change "
        "less currency and consolidation effects = 0."),
    "cf_bestand_anfang": (
        "⑨ Bestandszeile mit RowType \"Account opening\": zeigt den Wert der "
        "ERSTEN Periode der Auswahl, nicht die Summe.",
        "⑨ Stock row with RowType \"Account opening\": shows the value of the "
        "FIRST period in the selection, not the sum."),
    "cf_sonstige_zahlungsunwirksam": (
        "⑩ Restposten: zahlungsunwirksame Eigenkapitalbewegungen (OCI) und "
        "Rundung. Hält die Überleitung exakt.",
        "⑩ Residual: non-cash movements in equity (OCI) and rounding. "
        "Keeps the reconciliation exact."),
}


def translate(text):
    if text == "":
        return ""
    return TRANSLATIONS.get(text, text)


_REF = re.compile(r"\[([^\]]+)\]")


def translate_formula(formula):
    """Referenzen in einer Formel auf die englischen Zeilennamen umstellen."""
    if not formula:
        return ""
    return _REF.sub(lambda mo: "[" + translate(mo.group(1)) + "]", formula)


def parse_rowtype(raw):
    """RowType-Text in (Basistyp, Zeitaggregation) zerlegen.

    Das Visual liest Tokens wie "stock" und "opening" aus demselben Feld;
    der Text geht unveraendert in die CSV, hier brauchen wir nur die
    Ableitung fuer die Spalte Zeitaggregation.
    """
    parts = raw.lower().split()
    if "opening" in parts:
        return parts[0], "Bestand Anfang"
    if "stock" in parts:
        return parts[0], "Bestand"
    return parts[0], "Summe"


# ---------------------------------------------------------------------------
# Kontenplan aufbauen
# ---------------------------------------------------------------------------
class Account:
    __slots__ = ("id", "parent", "statement_de", "statement_en", "levels_de",
                 "levels_en", "name_de", "name_en", "rowtype", "base_type",
                 "aggregation", "sign", "display_invert", "variance_invert",
                 "formula_de", "formula_en", "tag", "sort", "number",
                 "comment_de", "comment_en", "is_node")

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


def build_accounts():
    """Liefert (accounts, value_tags).

    accounts    alle Zeilen der Dimension, inklusive der expliziten
                Knotenzeilen fuer den Parent-Child-Modus
    value_tags  die Tags, zu denen der Motor Werte liefert
    """
    accounts = []
    value_tags = {}          # tag -> statement_de
    sort = 0
    counters = {}

    for stmt_de, stmt_en, prefix, rows in STATEMENTS:
        # Knotenzeilen fuer den Parent-Child-Modus: ein Eintrag je
        # Hierarchiepfad, in der Reihenfolge des ersten Auftretens.
        node_order = []
        node_seen = set()
        for row in rows:
            l1, l2, l3, l4 = row[0], row[1], row[2], row[3]
            path = tuple(x for x in (l1, l2, l3, l4) if x)
            if len(path) <= 1:
                continue
            for depth in range(1, len(path)):
                key = path[:depth]
                if key not in node_seen:
                    node_seen.add(key)
                    node_order.append(key)

        node_id = {}
        for key in node_order:
            node_id[key] = "%s-N%d" % (prefix, len(node_id) + 1)

        # erst die Blatt- und Strukturzeilen in Kontenplanreihenfolge
        pending_nodes = dict.fromkeys(node_order)
        out_rows = []
        for row in rows:
            (l1, l2, l3, l4, rowtype_raw, sign, di, vi, formula, tag) = row
            path = tuple(x for x in (l1, l2, l3, l4) if x)
            # Knotenzeilen unmittelbar vor ihrem ersten Kind einfuegen
            for depth in range(1, len(path)):
                key = path[:depth]
                if key in pending_nodes:
                    del pending_nodes[key]
                    out_rows.append(("node", key, row))
            out_rows.append(("leaf", path, row))

        for kind, path, row in out_rows:
            (l1, l2, l3, l4, rowtype_raw, sign, di, vi, formula, tag) = row
            base_type, aggregation = parse_rowtype(rowtype_raw)

            if kind == "node":
                name_de = path[-1]
                parent = node_id[path[:-1]] if len(path) > 1 else ""
                sort += 10
                node_rowtype = "Subtotal stock" if aggregation == "Bestand" \
                    else "Subtotal"
                accounts.append(Account(
                    id=node_id[path], parent=parent,
                    statement_de=stmt_de, statement_en=stmt_en,
                    levels_de=("", "", "", "", "", ""),
                    levels_en=("", "", "", "", "", ""),
                    name_de=name_de, name_en=translate(name_de),
                    rowtype=node_rowtype, base_type="subtotal",
                    aggregation=aggregation,
                    sign=1, display_invert="false", variance_invert="false",
                    formula_de="", formula_en="", tag="",
                    sort=sort - 5, number="",
                    comment_de="", comment_en="", is_node=True))
                continue

            sort += 10
            levels_de = (l1, l2, l3, l4, "", "")
            levels_en = tuple(translate(x) for x in levels_de)
            name_de = path[-1] if path else l1
            parent = node_id[path[:-1]] if len(path) > 1 else ""

            if base_type == "account":
                base = NUMBER_BASE.get(l1, 990000)
                counters[l1] = counters.get(l1, 0) + 1
                number = "%d" % (base + counters[l1] * 10)
            else:
                number = ""

            cm = COMMENTS.get(tag, ("", ""))
            accounts.append(Account(
                id="%s-%s" % (prefix, tag), parent=parent,
                statement_de=stmt_de, statement_en=stmt_en,
                levels_de=levels_de, levels_en=levels_en,
                name_de=name_de, name_en=translate(name_de),
                rowtype=rowtype_raw, base_type=base_type,
                aggregation=aggregation,
                sign=sign,
                display_invert="true" if di else "false",
                variance_invert="true" if vi else "false",
                formula_de=formula, formula_en=translate_formula(formula),
                tag=tag, sort=sort, number=number,
                comment_de=cm[0], comment_en=cm[1], is_node=False))

            if base_type == "account":
                value_tags[tag] = stmt_de

    return accounts, value_tags


# ---------------------------------------------------------------------------
# Szenariopfade
# ---------------------------------------------------------------------------
def build_scenario_paths(agg_by_tag):
    """dict[entity_id][scenario][(y, m)] -> dict[tag] -> Wert in Landeswährung.

    Die EUR-Werte liegen je Monat unter dem Schlüssel "_eur".
    """
    paths = {}
    for e in engine.entities():
        paths[e.id] = {s: engine.build_statements(e, s, agg_by_tag)
                       for s in ("AC", "PL", "FC")}
    return paths


def value_of(path, ym, tag, eur):
    """Einzelwert eines Kontos, in EUR oder in Landeswährung."""
    p = path.get(ym)
    if p is None:
        return None
    src = p["_eur"] if eur else p
    return src.get(tag)


def fy_value(path, year, tag, aggregation, first_ym, eur):
    """Jahreswert eines Kontos: Fluss = Summe, Bestand = Dezemberwert,
    Bestand Anfang = Januarwert (bzw. erster konsolidierter Monat)."""
    months = [ym for ym in ((year, m) for m in range(1, 13))
              if ym >= first_ym]
    vals = [v for v in (value_of(path, ym, tag, eur) for ym in months)
            if v is not None]
    if not vals:
        return None
    if aggregation == "Bestand":
        return vals[-1]
    if aggregation == "Bestand Anfang":
        return vals[0]
    return sum(vals)


# ---------------------------------------------------------------------------
# CSV schreiben
# ---------------------------------------------------------------------------
def write_csv(name, header, rows):
    path = os.path.join(OUT, name)
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";", lineterminator="\r\n",
                       quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        w.writerows(rows)
    return path


DIM_KONTEN_HEADER = [
    "AccountID", "ParentAccountID", "Kontonummer",
    "Abschluss", "Statement",
    "Name", "Name EN",
    "L1", "L2", "L3", "L4", "L5", "L6",
    "L1 EN", "L2 EN", "L3 EN", "L4 EN", "L5 EN", "L6 EN",
    "SortOrder", "RowType", "Zeitaggregation",
    "FormulaDef", "FormulaDef EN",
    "SignConvention", "DisplayInvert", "VarianceInvert",
    "Kommentar", "Comment EN",
]


def write_dim_konten(accounts):
    rows = []
    for a in accounts:
        rows.append([
            a.id, a.parent, a.number, a.statement_de, a.statement_en,
            a.name_de, a.name_en,
            a.levels_de[0], a.levels_de[1], a.levels_de[2],
            a.levels_de[3], a.levels_de[4], a.levels_de[5],
            a.levels_en[0], a.levels_en[1], a.levels_en[2],
            a.levels_en[3], a.levels_en[4], a.levels_en[5],
            a.sort, a.rowtype, a.aggregation,
            a.formula_de, a.formula_en,
            a.sign, a.display_invert, a.variance_invert,
            a.comment_de, a.comment_en,
        ])
    return write_csv("dim-konten.csv", DIM_KONTEN_HEADER, rows)


def write_dim_datum():
    cal = build_calendar(2025, 2026, engine.LAST_ACTUAL, TODAY)
    rows = [[r[c] for c in dims.DATE_COLUMNS] for r in cal]
    return write_csv("dim-datum.csv", dims.DATE_COLUMNS, rows), len(rows)


DIM_GES_HEADER = [
    "EntityID", "Gesellschaft", "Company", "Kurzname", "Short name",
    "RegionID", "Region", "Region EN", "Land", "Country", "ISO",
    "SegmentID", "Segment", "Segment EN", "Währung", "Währung Name",
    "Währung Name EN", "IstKonzernwährung", "Rechtsform",
    "Mitarbeiter", "Erstkonsolidierung", "Konsolidierungsart",
    "Consolidation method", "Sortierung",
]


def write_dim_gesellschaft():
    region_names = {r[0]: (r[2], r[3]) for r in REGIONS}
    region_code = {r[0]: r[1] for r in REGIONS}
    cons_en = {"Vollkonsolidierung": "Full consolidation",
               "Vollkonsolidierung (Zukauf)": "Full consolidation (acquisition)"}
    cur_names = {c[0]: (c[1], c[2]) for c in CURRENCIES}
    rows = []
    for i, e in enumerate(ENTITIES):
        (eid, name, short, region, land_de, land_en, iso, seg, cur, legal,
         rev, staff, first_cons, cons) = e
        cur_de, cur_en = cur_names[cur]
        rows.append([
            eid, name, name, short, short,
            region, region_code[region], region_names[region][1],
            land_de, land_en, iso,
            seg, SEGMENTS[seg][0], SEGMENTS[seg][1],
            cur, cur_de, cur_en,
            "true" if cur == KONZERNWAEHRUNG else "false",
            legal, staff, first_cons, cons,
            cons_en.get(cons, cons), (i + 1) * 10,
        ])
    return write_csv("dim-gesellschaft.csv", DIM_GES_HEADER, rows), len(rows)


DIM_REGION_HEADER = ["RegionID", "Region", "Region DE", "Region EN",
                     "Sortierung", "Hauptsitz", "Zeitzone", "Gesellschaften"]


def write_dim_region():
    count = {}
    for e in ENTITIES:
        count[e[3]] = count.get(e[3], 0) + 1
    rows = []
    for (rid, code, de, en, sort, hq, tz) in REGIONS:
        rows.append([rid, code, de, en, sort, hq, tz, count.get(rid, 0)])
    return write_csv("dim-region.csv", DIM_REGION_HEADER, rows), len(rows)


DIM_WAEHRUNG_HEADER = ["Währung", "Name", "Name EN", "Symbol",
                       "Nachkommastellen", "IstKonzernwährung", "Sortierung"]


def write_dim_waehrung():
    rows = []
    for (iso, de, en, sym, dec, sort) in CURRENCIES:
        rows.append([iso, de, en, sym, dec,
                     "true" if iso == KONZERNWAEHRUNG else "false", sort])
    return write_csv("dim-waehrung.csv", DIM_WAEHRUNG_HEADER, rows), len(rows)


FACT_KURSE_HEADER = ["Währung", "Datum", "Monat", "Jahr", "Periode",
                     "PeriodeSort", "Kurs Durchschnitt", "Kurs Stichtag",
                     "Kurs Budget"]


def budget_rate(iso, year):
    """Budgetkurs (v3): fester Kurs je Währung und Jahr, Landeswährung je
    1 EUR. Regel: Mittel der Durchschnittskurse Oktober bis Dezember des
    Vorjahres; für das erste ausgelieferte Jahr (2025, ohne Vorjahr in der
    Kurstabelle) der Durchschnittskurs Januar. EUR = 1. Rein deskriptiv:
    die Faktenwerte bleiben zum Ist-Durchschnittskurs umgerechnet."""
    if iso == KONZERNWAEHRUNG:
        return 1.0
    if year <= engine.FIRST_OUT[0]:
        return engine.FX_RATES[(iso, (year, 1))][0]
    q4 = [engine.FX_RATES[(iso, (year - 1, m))][0] for m in (10, 11, 12)]
    return sum(q4) / 3.0


def write_fact_kurse():
    """Monatskurse in Einheiten der Landeswährung je 1 EUR."""
    rows = []
    for (iso, de, en, sym, dec, sort) in CURRENCIES:
        for (y, m) in month_sequence(engine.FIRST_OUT, engine.LAST_OUT):
            avg, close = engine.FX_RATES[(iso, (y, m))]
            rows.append([
                iso, month_end(y, m).isoformat(), "%04d-%02d" % (y, m), y,
                "%s %02d" % (dims.MONTH_DE_SHORT[m - 1], y % 100),
                y * 100 + m, "%.8f" % avg, "%.8f" % close,
                "%.8f" % budget_rate(iso, y),
            ])
    return write_csv("fact-kurse.csv", FACT_KURSE_HEADER, rows), len(rows)


# Unsuffigierte Spalten sind Konzernwährung (EUR), "_LW" ist Landeswährung.
FACT_HEADER = ["AccountID", "EntityID", "Datum", "Monat",
               "AC", "AC_LW", "PY", "PY_LW", "PL", "PL_LW", "FC", "FC_LW",
               "FC_FY", "FC_FY_LW", "PL_FY", "PL_FY_LW"]


def fmt(v):
    """In Basiseinheiten der Währung, zwei Nachkommastellen."""
    if v is None:
        return ""
    return "%.2f" % (v * UNIT)


def write_fact(accounts, paths):
    months = month_sequence(engine.FIRST_OUT, engine.LAST_OUT)
    ents = engine.entities()
    rows = []
    zero = ["0"] * 12

    for a in accounts:
        for e in ents:
            ac_path = paths[e.id]["AC"]
            pl_path = paths[e.id]["PL"]
            fc_path = paths[e.id]["FC"]
            for (y, m) in months:
                datum = month_end(y, m).isoformat()
                monat = "%04d-%02d" % (y, m)
                head = [a.id, e.id, datum, monat]

                if (y, m) < e.first_ym:
                    # vor der Erstkonsolidierung gibt es die Gesellschaft nicht
                    rows.append(head + [""] * 12)
                    continue
                if a.base_type != "account":
                    # Struktur-, Formel- und Trennzeilen brauchen Faktzeilen,
                    # damit sie im DataView bleiben; die Werte rechnet das
                    # Visual selbst aus den Kindern bzw. der Formel.
                    rows.append(head + zero)
                    continue

                tag = a.tag
                vals = []
                for eur in (True, False):
                    ac = value_of(ac_path, (y, m), tag, eur)
                    if (y, m) > engine.LAST_ACTUAL:
                        ac = None                   # offene Monate: kein Ist
                    py = value_of(ac_path, (y - 1, m), tag, eur)
                    if (y - 1, m) < e.first_ym:
                        py = None                   # kein Vorjahr (Zukauf)
                    vals.append((ac, py,
                                 value_of(pl_path, (y, m), tag, eur),
                                 value_of(fc_path, (y, m), tag, eur),
                                 fy_value(fc_path, y, tag, a.aggregation,
                                          e.first_ym, eur),
                                 fy_value(pl_path, y, tag, a.aggregation,
                                          e.first_ym, eur)))
                (eur_ac, eur_py, eur_pl, eur_fc, eur_fcfy, eur_plfy) = vals[0]
                (lw_ac, lw_py, lw_pl, lw_fc, lw_fcfy, lw_plfy) = vals[1]
                rows.append(head + [
                    fmt(eur_ac), fmt(lw_ac), fmt(eur_py), fmt(lw_py),
                    fmt(eur_pl), fmt(lw_pl), fmt(eur_fc), fmt(lw_fc),
                    fmt(eur_fcfy), fmt(lw_fcfy),
                    fmt(eur_plfy), fmt(lw_plfy),
                ])
    return write_csv("fact-abschluss.csv", FACT_HEADER, rows), len(rows)


# v3: Monatsabschluss-Szene. Genau eine Nachbuchung nach dem Close am
# Arbeitstag 3: Mobility FR löst im Oktober 2026 eine Rückstellung auf,
# +4,0 Mio. EUR Ertrag (Konto mit SignConvention +1, Rohwert positiv).
# Fließt NICHT in fact-abschluss; das Modell addiert sie nur, wenn der
# Schalter 'close-status' auf "Incl. day-3 adjustment" steht.
FACT_NACHBUCHUNG_HEADER = ["AccountID", "EntityID", "Datum", "Monat",
                           "AC Wert", "AC LW Wert", "Text"]


def write_fact_nachbuchung():
    rows = [["G-oth_rst_aufloesung", "1300", "2026-10-31", "2026-10",
             fmt(4.0), fmt(4.0),     # fmt rechnet Mio. in Basiseinheiten um
             "Release of warranty provision (day-3 adjustment, Oct 2026)"]]
    return (write_csv("fact-nachbuchung.csv", FACT_NACHBUCHUNG_HEADER, rows),
            len(rows))


if __name__ == "__main__":
    import checks

    accounts, value_tags = build_accounts()
    agg_by_tag = {a.tag: a.aggregation for a in accounts if a.tag}
    paths = build_scenario_paths(agg_by_tag)

    write_dim_konten(accounts)
    (_, n_dates) = write_dim_datum()
    (_, n_ents) = write_dim_gesellschaft()
    (_, n_regs) = write_dim_region()
    (_, n_curs) = write_dim_waehrung()
    (_, n_rates) = write_fact_kurse()
    (_, n_facts) = write_fact(accounts, paths)
    write_fact_nachbuchung()

    print("dim-konten.csv        %5d Zeilen" % len(accounts))
    print("dim-datum.csv         %5d Zeilen" % n_dates)
    print("dim-gesellschaft.csv  %5d Zeilen" % n_ents)
    print("dim-region.csv        %5d Zeilen" % n_regs)
    print("dim-waehrung.csv      %5d Zeilen" % n_curs)
    print("fact-kurse.csv        %5d Zeilen" % n_rates)
    print("fact-abschluss.csv   %6d Zeilen" % n_facts)
    print()
    checks.run(accounts, value_tags, paths, OUT)
