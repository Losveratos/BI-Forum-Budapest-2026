# -*- coding: utf-8 -*-
"""Schreibt die TMDL-Dateien des semantischen Modells passend zu den
erzeugten CSV-Dateien.

Warum ein Generator und nicht von Hand: das Modell hat fuenf Tabellen mit
rund hundert Spalten, deren Typen genau zu den CSV-Spalten passen muessen.
Einmal beschrieben, laesst sich das Modell nach jedem Datenlauf in einem
Schritt neu verdrahten.

Aufruf:  python build_model_tmdl.py
Danach:  te validate -m "PnL ChartkitchenDemoKit.SemanticModel" --errors-only
"""

import csv
import hashlib
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
MODEL = os.path.join(PROJECT, "PnL ChartkitchenDemoKit.SemanticModel", "definition")
DEMO_PATH = HERE + "\\"

TAB = "\t"


def guid(*parts):
    """Stabile lineageTags, damit Wiederholungslaeufe keine Diffs erzeugen."""
    h = hashlib.sha1(("demokit|" + "|".join(parts)).encode("utf-8")).hexdigest()
    return "%s-%s-4%s-8%s-%s" % (h[0:8], h[8:12], h[13:16], h[17:20], h[20:32])


def read_header(name):
    with io.open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return next(csv.reader(fh, delimiter=";"))


# ---------------------------------------------------------------------------
# Typzuordnung je Tabelle: Spaltenname -> (dataType, m-Typ)
# Alles, was hier nicht steht, ist Text.
# ---------------------------------------------------------------------------
INT = ("int64", "Int64.Type")
DBL = ("double", "type number")
DATE = ("dateTime", "type date")
TXT = ("string", "type text")

TYPES = {
    "dim-konten": {"SortOrder": INT, "SignConvention": INT},
    "dim-datum": {
        "Datum": DATE, "Monatsende": DATE, "DatumKey": INT, "Jahr": INT,
        "HalbjahrNr": INT, "QuartalNr": INT, "MonatNr": INT,
        "PeriodeSort": INT, "Tag": INT, "TagImJahr": INT, "TagImMonat": INT,
        "WochentagNr": INT, "Woche": INT, "Relatives Jahr": INT,
        "Relativer Monat": INT,
    },
    "dim-gesellschaft": {"Mitarbeiter": INT, "Sortierung": INT},
    "dim-region": {"Sortierung": INT, "Gesellschaften": INT},
    "fact-abschluss": {
        "Datum": DATE,
        "AC": DBL, "AC_LW": DBL, "PY": DBL, "PY_LW": DBL,
        "PL": DBL, "PL_LW": DBL, "FC": DBL, "FC_LW": DBL,
        "FC_FY": DBL, "FC_FY_LW": DBL, "PL_FY": DBL, "PL_FY_LW": DBL,
    },
    "dim-waehrung": {"Nachkommastellen": INT, "Sortierung": INT},
    "fact-kurse": {
        "Datum": DATE, "Jahr": INT, "PeriodeSort": INT,
        "Kurs Durchschnitt": DBL, "Kurs Stichtag": DBL,
    },
}

# Schluesselspalte je Dimension
KEYS = {"dim-datum": "Datum", "dim-waehrung": "Währung"}

# Zahlenformat der Double-Spalten je Tabelle
DBL_FORMAT = {"fact-abschluss": "#,##0", "fact-kurse": "#,##0.0000"}

# Spalten, die im Bericht nichts zu suchen haben
HIDDEN = {
    "fact-abschluss": {"AC", "AC_LW", "PY", "PY_LW", "PL", "PL_LW",
                       "FC", "FC_LW", "FC_FY", "FC_FY_LW",
                       "PL_FY", "PL_FY_LW"},
    "dim-datum": {"DatumKey"},
}

# Spalte -> Anzeigeordner
FOLDERS = {
    "fact-kurse": {
        "Jahr": "Periode", "Monat": "Periode", "Periode": "Periode",
        "PeriodeSort": "Periode", "Datum": "Periode",
    },
    "dim-waehrung": {"Nachkommastellen": "Details", "Symbol": "Details",
                     "Name EN": "Details", "IstKonzernwährung": "Details",
                     "Sortierung": "Details"},
    "dim-konten": {
        "L1": "Levels DE", "L2": "Levels DE", "L3": "Levels DE",
        "L4": "Levels DE", "L5": "Levels DE", "L6": "Levels DE",
        "L1 EN": "Levels EN", "L2 EN": "Levels EN", "L3 EN": "Levels EN",
        "L4 EN": "Levels EN", "L5 EN": "Levels EN", "L6 EN": "Levels EN",
        "RowType": "Steuerung", "Zeitaggregation": "Steuerung",
        "FormulaDef": "Steuerung", "FormulaDef EN": "Steuerung",
        "SignConvention": "Steuerung", "DisplayInvert": "Steuerung",
        "VarianceInvert": "Steuerung", "SortOrder": "Steuerung",
        "Kommentar": "Fußnoten", "Comment EN": "Fußnoten",
        "ParentAccountID": "Steuerung", "Kontonummer": "Steuerung",
    },
    "dim-datum": {
        "Monat Lang": "Monat", "Monat Kurz": "Monat",
        "Month Long": "Monat", "Month Short": "Monat",
        "Periode": "Monat", "Period": "Monat", "PeriodeSort": "Monat",
        "MonatNr": "Monat", "Monat": "Monat",
        "Wochentag": "Tag", "Weekday": "Tag", "Wochentag Kurz": "Tag",
        "Weekday Short": "Tag", "WochentagNr": "Tag", "Tag": "Tag",
        "TagImJahr": "Tag", "TagImMonat": "Tag", "IstWerktag": "Tag",
        "IstMonatsletzter": "Tag", "ISO-Woche": "Woche", "Woche": "Woche",
        "Quartal": "Jahr und Quartal", "QuartalNr": "Jahr und Quartal",
        "JahrQuartal": "Jahr und Quartal", "Halbjahr": "Jahr und Quartal",
        "HalbjahrNr": "Jahr und Quartal", "Jahr": "Jahr und Quartal",
        "Periodenstatus": "Status", "Period Status": "Status",
        "IstIstPeriode": "Status", "IstAbgeschlossen": "Status",
        "Relatives Jahr": "Status", "Relativer Monat": "Status",
        "Monatsende": "Monat",
    },
    "dim-gesellschaft": {
        "Company": "Englisch", "Short name": "Englisch",
        "Region EN": "Englisch", "Country": "Englisch",
        "Segment EN": "Englisch", "Consolidation method": "Englisch",
    },
}

# Sortierspalten: Spalte -> Spalte, nach der sortiert wird
SORT_BY = {
    "fact-kurse": {"Periode": "PeriodeSort"},
    "dim-waehrung": {"Währung": "Sortierung", "Name": "Sortierung"},
    "dim-datum": {
        "Monat Lang": "MonatNr", "Monat Kurz": "MonatNr",
        "Month Long": "MonatNr", "Month Short": "MonatNr",
        "Periode": "PeriodeSort", "Period": "PeriodeSort",
        "Wochentag": "WochentagNr", "Weekday": "WochentagNr",
        "Wochentag Kurz": "WochentagNr", "Weekday Short": "WochentagNr",
    },
    "dim-gesellschaft": {"Gesellschaft": "Sortierung", "Kurzname": "Sortierung",
                        "Company": "Sortierung", "Short name": "Sortierung",
                        "Segment": "SegmentID", "Segment EN": "SegmentID"},
    "dim-konten": {},
    "dim-region": {"Region": "Sortierung", "Region DE": "Sortierung",
                   "Region EN": "Sortierung"},
}

DESCRIPTIONS = {
    "dim-waehrung": {
        "Währung": "ISO-Code. Schlüssel zur Kurstabelle.",
        "Nachkommastellen": "Übliche Stellenzahl der Währung — JPY hat 0.",
        "IstKonzernwährung": "Nur der Euro ist die Konzernwährung.",
    },
    "fact-kurse": {
        "Währung": "ISO-Code der Landeswährung.",
        "Kurs Durchschnitt": "Durchschnittskurs des Monats, Einheiten der "
                             "Landeswährung je 1 EUR. Für Erfolgsposten "
                             "und Zahlungsströme.",
        "Kurs Stichtag": "Kurs am Monatsletzten, Einheiten der "
                         "Landeswährung je 1 EUR. Für Bilanzposten.",
        "Datum": "Monatsletzter, Bezug zur Datumsdimension.",
    },
    "dim-konten": {
        "AccountID": "Technischer Schlüssel. Präfix G = GuV, B = Bilanz, "
                     "C = Cashflow, N = Knotenzeile für den Parent-Child-Modus.",
        "ParentAccountID": "Nur für den Parent-Child-Modus. Im Levels-Modus "
                           "NICHT binden, sonst ignoriert das Visual L1 bis L6.",
        "Abschluss": "GuV, Bilanz oder Cashflow. Gehört auf einen Slicer — "
                     "damit wählt man die Aufstellung aus.",
        "Statement": "Englische Entsprechung zu Abschluss.",
        "Name": "Zeilenname, deutsch. Formeln in FormulaDef verweisen auf "
                "genau diese Namen.",
        "Name EN": "Zeilenname, englisch. Passt zu FormulaDef EN.",
        "RowType": "Zeilentyp plus Bestandstoken: \"Account stock\" nimmt den "
                   "Wert der letzten Periode statt der Summe, "
                   "\"Account opening\" den der ersten.",
        "Zeitaggregation": "Aus RowType abgeleitet: Summe, Bestand oder "
                           "Bestand Anfang. Die Measures mit dem Zusatz "
                           "Stichtag werten diese Spalte aus.",
        "FormulaDef": "Formel einer Zwischen- oder Kennzahlenzeile, "
                      "Referenzen in eckigen Klammern auf Zeilennamen.",
        "SortOrder": "Dichte Reihenfolge in Zehnerschritten. Lücken vermeiden "
                     "— eine Zeile ohne Wert fällt auf den DataView-Index "
                     "zurück und sortiert falsch.",
        "SignConvention": "Wird vor Summen und Formeln anmultipliziert.",
        "DisplayInvert": "Zeile mit umgekehrtem Vorzeichen anzeigen, damit "
                         "Kostenzeilen positiv erscheinen.",
        "VarianceInvert": "Weniger ist besser — Abweichung unter Plan wird grün.",
    },
    "dim-datum": {
        "Datum": "Monatsletzter der Periode. Der Faktbezug liegt auf diesem Tag.",
        "Periodenstatus": "Ist, Forecast oder Plan — je Monat.",
        "IstAbgeschlossen": "Monat liegt vollständig vor dem Stichtag 30.10.2026.",
        "Relativer Monat": "Abstand in Monaten zum Stichtag, 0 = Oktober 2026.",
    },
    "dim-gesellschaft": {
        "EntityID": "Schlüssel zur Faktentabelle.",
        "Währung": "Funktionale Währung der Gesellschaft. Diese Spalte "
                   "gehört auf einen Währungsslicer — sie filtert die "
                   "Gesellschaften und damit die Fakten.",
        "Erstkonsolidierung": "Erster Monat im Konsolidierungskreis. "
                              "DWG Digital Services KK kommt erst 2026-04 "
                              "hinzu und hat deshalb kein Vorjahr.",
    },
    "dim-region": {
        "RegionID": "Schlüssel zu dim-gesellschaft — ein Schneeflocken-Ast, "
                    "Region filtert über die Gesellschaft auf die Fakten.",
    },
    "fact-abschluss": {
        "Monat": "Periodenschlüssel als Text JJJJ-MM. Diese Spalte gehört in "
                 "die Rolle \"Period\" des Visuals.",
        "AC": "Ist in EUR, Basiseinheiten. Die Spalten ohne Zusatz sind "
              "Konzernwährung, die mit \"_LW\" Landeswährung.",
        "AC_LW": "Ist in der Landeswährung der Gesellschaft, Basiseinheiten.",
        "Datum": "Monatsletzter, Bezug zur Datumsdimension.",
        "FC_FY": "Jahresskalar, auf jeder Monatszeile des Jahres gleich. "
                 "Nur mit MAX aggregieren, nie mit SUM.",
        "PL_FY": "Jahresskalar, auf jeder Monatszeile des Jahres gleich. "
                 "Nur mit MAX aggregieren, nie mit SUM.",
    },
}

TABLE_DESC = {
    "dim-waehrung": "Die sieben Währungen des Konzerns. Konzernwährung ist "
                    "der Euro. Hängt an der Kurstabelle, nicht an den "
                    "Gesellschaften — siehe Kommentar bei RELATIONSHIPS.",
    "fact-kurse": "Monatskurse je Währung, in Einheiten der Landeswährung "
                  "je 1 EUR. Durchschnittskurs für Erfolgsposten und "
                  "Zahlungsströme, Stichtagskurs für Bilanzposten (IAS 21). "
                  "Die Umrechnung ist in der Faktentabelle bereits "
                  "vollzogen; diese Tabelle macht sie nachvollziehbar.",
    "dim-konten": "Kontenplan für alle drei Rechenwerke. Die Spalte "
                  "Abschluss wählt zwischen GuV, Bilanz und Cashflow; "
                  "L1 bis L6 tragen die Hierarchie in Deutsch, L1 EN bis "
                  "L6 EN dieselbe in Englisch.",
    "dim-datum": "Datumsdimension, tagesgenau vom 1.1.2025 bis 31.12.2026. "
                 "Als Datumstabelle markiert, Schlüssel ist Datum.",
    "dim-gesellschaft": "Sieben Gesellschaften des Konzerns DWG Industries SE "
                        "mit Region, Land, Segment und Konsolidierungsinfo.",
    "dim-region": "Drei Regionen. Hängt an dim-gesellschaft, nicht direkt an "
                  "den Fakten.",
    "fact-abschluss": "Werte je Konto, Gesellschaft und Monat in mEUR. "
                      "Szenarien AC (Ist), PY (Vorjahr), PL (Plan), "
                      "FC (Forecast) plus die Jahresskalare FC_FY und PL_FY.",
}

# Spalten, die als Measure-Quelle dienen und darum anders heissen muessen
# als das Measure (sonst PFE_XL_MEASURE_COLUMN_ALREADY_EXIST beim Laden).
RENAME = {"AC": "AC Wert", "PY": "PY Wert", "PL": "PL Wert", "FC": "FC Wert",
          "AC_LW": "AC LW Wert", "PY_LW": "PY LW Wert",
          "PL_LW": "PL LW Wert", "FC_LW": "FC LW Wert"}


def m_partition(table, csv_name, header):
    """Power-Query-Partition, die am Parameter DemoPfad haengt."""
    types = TYPES.get(table, {})
    casts = ", ".join(
        '{"%s", %s}' % (c, types.get(c, TXT)[1]) for c in header)
    return (
        "{T}partition {t} = m\n"
        "{T}{T}mode: import\n"
        "{T}{T}source =\n"
        "{T}{T}{T}{T}let\n"
        "{T}{T}{T}{T}    Quelle = Csv.Document(File.Contents(DemoPfad & \"{f}\"), "
        "[Delimiter = \";\", Columns = {n}, Encoding = 65001, "
        "QuoteStyle = QuoteStyle.Csv]),\n"
        "{T}{T}{T}{T}    Header = Table.PromoteHeaders(Quelle, "
        "[PromoteAllScalars = true]),\n"
        "{T}{T}{T}{T}    Typen = Table.TransformColumnTypes(Header, {{{c}}}, \"en-US\")\n"
        "{T}{T}{T}{T}in\n"
        "{T}{T}{T}{T}    Typen\n"
    ).format(T=TAB, t=table, f=csv_name, n=len(header), c=casts)


def quote(name):
    """TMDL-Name quoten, wenn er Sonderzeichen enthaelt."""
    if all(ch.isalnum() or ch == "_" for ch in name):
        return name
    return "'%s'" % name


def column_block(table, col, header):
    types = TYPES.get(table, {})
    dtype = types.get(col, TXT)[0]
    target = RENAME.get(col, col) if table == "fact-abschluss" else col
    lines = []
    desc = DESCRIPTIONS.get(table, {}).get(col)
    if desc:
        for part in wrap(desc, 68):
            lines.append("%s/// %s" % (TAB, part))
    lines.append("%scolumn %s" % (TAB, quote(target)))
    lines.append("%s%sdataType: %s" % (TAB, TAB, dtype))
    if KEYS.get(table) == col:
        lines.append("%s%sisKey" % (TAB, TAB))
    if col in HIDDEN.get(table, ()):
        lines.append("%s%sisHidden" % (TAB, TAB))
    if dtype == "int64":
        lines.append("%s%sformatString: 0" % (TAB, TAB))
    elif dtype == "double":
        lines.append("%s%sformatString: %s"
                     % (TAB, TAB, DBL_FORMAT.get(table, "#,##0.0")))
    elif dtype == "dateTime":
        lines.append("%s%sformatString: yyyy-mm-dd" % (TAB, TAB))
    folder = FOLDERS.get(table, {}).get(col)
    if folder:
        lines.append("%s%sdisplayFolder: %s" % (TAB, TAB, folder))
    lines.append("%s%slineageTag: %s" % (TAB, TAB, guid(table, col)))
    sort_by = SORT_BY.get(table, {}).get(col)
    if sort_by:
        lines.append("%s%ssortByColumn: %s" % (TAB, TAB, quote(sort_by)))
    summarize = "sum" if (dtype == "double" and table == "fact-abschluss") else "none"
    lines.append("%s%ssummarizeBy: %s" % (TAB, TAB, summarize))
    lines.append("%s%ssourceColumn: %s" % (TAB, TAB, col))
    lines.append("")
    lines.append("%s%sannotation SummarizationSetBy = %s"
                 % (TAB, TAB, "Automatic" if summarize == "none" else "User"))
    if dtype == "dateTime":
        lines.append("")
        lines.append("%s%sannotation UnderlyingDateTimeDataType = Date" % (TAB, TAB))
    return "\n".join(lines) + "\n"


def wrap(text, width):
    words = text.split()
    out, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


# ---------------------------------------------------------------------------
# Measures
# ---------------------------------------------------------------------------
SIMPLE_MEASURES = [
    ("AC", "SUM ( 'fact-abschluss'[AC Wert] )", "Szenarien (EUR)",
     "Ist in Konzernwährung EUR. Erfolgsposten zum Durchschnittskurs des "
     "Monats, Bilanzposten zum Stichtagskurs. Bestandszeilen regelt das "
     "Visual selbst über das Token \"stock\" in RowType."),
    ("PY", "SUM ( 'fact-abschluss'[PY Wert] )", "Szenarien (EUR)",
     "Vorjahr in EUR, monatsgenau verschoben. Für 2026 ist PY gleich dem "
     "Ist 2025 — jeweils zum Kurs des damaligen Monats."),
    ("PL", "SUM ( 'fact-abschluss'[PL Wert] )", "Szenarien (EUR)",
     "Plan in EUR."),
    ("FC", "SUM ( 'fact-abschluss'[FC Wert] )", "Szenarien (EUR)",
     "Forecast in EUR: Ist für die geschlossenen Monate, Hochrechnung für "
     "November und Dezember 2026."),
]

# Landeswährung: nur sinnvoll, solange genau eine Währung im Filter ist.
# CHF und JPY zu addieren ergibt keine Zahl, die etwas bedeutet, darum
# liefert die Measure dann BLANK statt einer irreführenden Summe.
LW_DAX = """IF (
    HASONEVALUE ( 'dim-gesellschaft'[Währung] ),
    SUM ( 'fact-abschluss'[{col}] )
)"""

LW_MEASURES = [("AC LW", "AC LW Wert", "Ist"), ("PY LW", "PY LW Wert", "Vorjahr"),
               ("PL LW", "PL LW Wert", "Plan"), ("FC LW", "FC LW Wert", "Forecast")]

FY_MEASURES = [
    ("FC FY", "FC_FY", "Jahresskalare",
     "Forecast für das ganze Geschäftsjahr in EUR. Der Wert steht identisch "
     "auf jeder Monatszeile, deshalb MAX je Gesellschaft und Jahr statt SUM."),
    ("PL FY", "PL_FY", "Jahresskalare",
     "Plan für das ganze Geschäftsjahr in EUR, gleiche Logik wie FC FY."),
    ("FC FY LW", "FC_FY_LW", "Jahresskalare",
     "Forecast für das Geschäftsjahr in Landeswährung."),
    ("PL FY LW", "PL_FY_LW", "Jahresskalare",
     "Plan für das Geschäftsjahr in Landeswährung."),
]

# ChartKitchen braucht vorzeichenrichtige Kennzahlen: die Spalte
# SignConvention wendet nur das P&L-Visual an, ein nacktes SUM addierte
# Erlösschmälerungen statt sie abzuziehen. Die Blöcke summieren sich
# genau deshalb zu EBITDA, weil das Vorzeichen die Richtung trägt.
SIGNED_DAX = """CALCULATE (
    SUMX (
        'fact-abschluss',
        'fact-abschluss'[{col}] * RELATED ( 'dim-konten'[SignConvention] )
    ),
    KEEPFILTERS ( 'dim-konten'[L1 EN] {pred} )
)"""

EBITDA_BLOCKS = ('IN {{ "Net revenue", "Cost of sales", "Selling expenses", '
                 '"Administrative expenses", "Research & development", '
                 '"Other operating result" }}')

SIGNED_MEASURES = [
    ("Revenue", '= "Net revenue"',
     "Umsatzerlöse als Skalar, Erlösschmälerungen korrekt abgezogen. "
     "Für ChartKitchen und Karten — das P&L-Visual braucht sie nicht, "
     "es rechnet das Vorzeichen selbst."),
    ("EBITDA", EBITDA_BLOCKS,
     "EBITDA als Skalar: die Summe der sechs operativen GuV-Blöcke. Geht "
     "auf, weil SignConvention die Kosten negativ trägt. Formelzeilen "
     "fließen nicht ein, sie liegen in der Faktentabelle auf 0."),
]
SIGNED_SCENARIOS = [("AC", "AC Wert"), ("PY", "PY Wert"),
                    ("PL", "PL Wert"), ("FC", "FC Wert")]

RATE_MEASURES = [
    ("Durchschnittskurs", "AVERAGE ( 'fact-kurse'[Kurs Durchschnitt] )",
     "Kurse",
     "Mittlerer Durchschnittskurs der gewählten Monate, Einheiten der "
     "Landeswährung je 1 EUR. Für Erfolgsposten und Zahlungsströme.",
     "#,##0.0000"),
    ("Stichtagskurs",
     "LASTNONBLANKVALUE ( 'dim-datum'[Datum], "
     "MAX ( 'fact-kurse'[Kurs Stichtag] ) )", "Kurse",
     "Kurs am letzten Tag der Auswahl, Einheiten der Landeswährung je "
     "1 EUR. Für Bilanzposten.", "#,##0.0000"),
]

STOCK_MEASURES = [
    ("AC", "AC Wert"), ("PY", "PY Wert"),
    ("PL", "PL Wert"), ("FC", "FC Wert"),
]


def measure_block(name, dax, folder, desc, fmt="#,##0.0"):
    """fmt=None laesst formatString weg -- fuer Textmeasures."""
    lines = []
    for part in wrap(desc, 68):
        lines.append("%s/// %s" % (TAB, part))
    if "\n" in dax:
        lines.append("%smeasure %s =" % (TAB, quote(name)))
        for ln in dax.strip("\n").split("\n"):
            lines.append("%s%s%s%s" % (TAB, TAB, TAB, ln))
    else:
        lines.append("%smeasure %s = %s" % (TAB, quote(name), dax))
    if fmt:
        lines.append("%s%sformatString: %s" % (TAB, TAB, fmt))
    lines.append("%s%sdisplayFolder: %s" % (TAB, TAB, folder))
    lines.append("%s%slineageTag: %s" % (TAB, TAB, guid("measure", name)))
    lines.append("")
    return "\n".join(lines) + "\n"


FY_DAX = """VAR _Scope =
    SUMMARIZE (
        'fact-abschluss',
        'fact-abschluss'[AccountID],
        'fact-abschluss'[EntityID],
        'dim-datum'[Jahr]
    )
RETURN
    SUMX ( _Scope, CALCULATE ( MAX ( 'fact-abschluss'[{col}] ) ) )"""

STOCK_DAX = """VAR _Fluss =
    CALCULATE (
        SUM ( 'fact-abschluss'[{col}] ),
        KEEPFILTERS ( 'dim-konten'[Zeitaggregation] = "Summe" )
    )
VAR _Erste = CALCULATE ( MIN ( 'fact-abschluss'[Datum] ), REMOVEFILTERS ( 'dim-konten' ) )
VAR _Letzte = CALCULATE ( MAX ( 'fact-abschluss'[Datum] ), REMOVEFILTERS ( 'dim-konten' ) )
VAR _Bestand =
    CALCULATE (
        SUM ( 'fact-abschluss'[{col}] ),
        KEEPFILTERS ( 'dim-konten'[Zeitaggregation] = "Bestand" ),
        'fact-abschluss'[Datum] = _Letzte
    )
VAR _Anfang =
    CALCULATE (
        SUM ( 'fact-abschluss'[{col}] ),
        KEEPFILTERS ( 'dim-konten'[Zeitaggregation] = "Bestand Anfang" ),
        'fact-abschluss'[Datum] = _Erste
    )
RETURN
    _Fluss + _Bestand + _Anfang"""

FILTERINFO_DAX = """VAR _Wae =
    IF (
        HASONEVALUE ( 'dim-gesellschaft'[Währung] ),
        VALUES ( 'dim-gesellschaft'[Währung] ),
        "EUR"
    )
VAR _Ges =
    IF (
        ISFILTERED ( 'dim-gesellschaft'[Gesellschaft] ),
        CONCATENATEX (
            VALUES ( 'dim-gesellschaft'[Kurzname] ),
            'dim-gesellschaft'[Kurzname],
            ", ",
            'dim-gesellschaft'[Kurzname]
        ),
        "Konzern"
    )
VAR _Reg =
    IF (
        ISFILTERED ( 'dim-region'[Region] ),
        " · " & CONCATENATEX (
            VALUES ( 'dim-region'[Region] ),
            'dim-region'[Region],
            ", ",
            'dim-region'[Region]
        ),
        ""
    )
VAR _Von = MIN ( 'fact-abschluss'[Monat] )
VAR _Bis = MAX ( 'fact-abschluss'[Monat] )
VAR _Per = " · " & IF ( _Von = _Bis, _Von, _Von & " bis " & _Bis )
RETURN
    _Ges & _Reg & _Per & " · " & _Wae"""


def fact_measures():
    out = []
    for name, dax, folder, desc in SIMPLE_MEASURES:
        out.append(measure_block(name, dax, folder, desc, "#,##0"))
    for name, col, label in LW_MEASURES:
        out.append(measure_block(
            name, LW_DAX.format(col=col), "Szenarien (Landeswährung)",
            "%s in der Landeswährung der Gesellschaft. Liefert BLANK, "
            "sobald mehr als eine Währung im Filter liegt — eine Summe "
            "über CHF und JPY wäre bedeutungslos." % label, "#,##0"))
    for name, col, folder, desc in FY_MEASURES:
        out.append(measure_block(name, FY_DAX.format(col=col), folder, desc,
                                 "#,##0"))
    for base, pred, desc in SIGNED_MEASURES:
        for scen, col in SIGNED_SCENARIOS:
            out.append(measure_block(
                "%s %s" % (base, scen),
                SIGNED_DAX.format(col=col, pred=pred.format()),
                "ChartKitchen (vorzeichenrichtig)",
                "%s — Szenario %s. %s" % (base, scen, desc), "#,##0"))
    for scen, col in STOCK_MEASURES:
        out.append(measure_block(
            "%s Stichtag" % scen, STOCK_DAX.format(col=col), "Bestandssicher",
            "Wie %s, aber bestandsrichtig: Bilanzzeilen werden nicht über die "
            "Perioden summiert, sondern mit dem Wert des Stichtags gezeigt. "
            "Für Karten und Matrizen außerhalb des P&L-Visuals — das Visual "
            "selbst braucht das nicht." % scen, "#,##0"))
    out.append(measure_block(
        "Filterinfo", FILTERINFO_DAX, "Beschriftung",
        "Textmeasure für die Rolle \"Filter info\" des Visuals: zeigt "
        "Gesellschaft, Region und Zeitraum in der Fußzeile. Muss Text "
        "liefern, Zahlen würden unformatiert ausgegeben.", fmt=None))
    return "".join(out)


# ---------------------------------------------------------------------------
# Dateien schreiben
# ---------------------------------------------------------------------------
def write(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(text)


def table_file(table, csv_name):
    header = read_header(csv_name)
    parts = []
    for part in wrap(TABLE_DESC[table], 72):
        parts.append("/// %s\n" % part)
    parts.append("table %s\n" % quote(table))
    if table == "dim-datum":
        parts.append("%sdataCategory: Time\n" % TAB)
    parts.append("%slineageTag: %s\n" % (TAB, guid("table", table)))
    parts.append("\n")
    if table == "fact-abschluss":
        parts.append(fact_measures())
    if table == "fact-kurse":
        for name, dax, folder, desc, fmt in RATE_MEASURES:
            parts.append(measure_block(name, dax, folder, desc, fmt))
    for col in header:
        parts.append(column_block(table, col, header))
        parts.append("\n")
    parts.append(m_partition(table, csv_name, header))
    parts.append("\n")
    parts.append("%sannotation PBI_ResultType = Table\n" % TAB)
    return "".join(parts)


TABLES = [
    ("dim-konten", "dim-konten.csv"),
    ("dim-datum", "dim-datum.csv"),
    ("dim-gesellschaft", "dim-gesellschaft.csv"),
    ("dim-region", "dim-region.csv"),
    ("dim-waehrung", "dim-waehrung.csv"),
    ("fact-kurse", "fact-kurse.csv"),
    ("fact-abschluss", "fact-abschluss.csv"),
]

# dim-waehrung haengt bewusst NICHT an dim-gesellschaft: sonst entstuende
# der Ring dim-datum -> fact-kurse -> dim-waehrung -> dim-gesellschaft ->
# fact-abschluss -> dim-datum, und Power BI laesst keinen geschlossenen
# Beziehungsring zu. Nach Waehrung filtert man ueber die Spalte
# dim-gesellschaft[Währung]; dim-waehrung bedient die Kurstabelle.
RELATIONSHIPS = [
    ("fact-abschluss.AccountID", "dim-konten.AccountID", None),
    ("fact-abschluss.Datum", "dim-datum.Datum", None),
    ("fact-abschluss.EntityID", "dim-gesellschaft.EntityID", None),
    ("dim-gesellschaft.RegionID", "dim-region.RegionID", None),
    ("fact-kurse.Datum", "dim-datum.Datum", None),
    ("fact-kurse.Währung", "dim-waehrung.Währung", None),
]


def main():
    os.makedirs(os.path.join(MODEL, "tables"), exist_ok=True)

    # alte Tabellendateien entfernen, die es nicht mehr gibt
    keep = {"%s.tmdl" % t for t, _ in TABLES}
    for fn in os.listdir(os.path.join(MODEL, "tables")):
        if fn.endswith(".tmdl") and fn not in keep:
            os.remove(os.path.join(MODEL, "tables", fn))
            print("entfernt  tables/%s" % fn)

    for table, csv_name in TABLES:
        path = os.path.join(MODEL, "tables", "%s.tmdl" % table)
        write(path, table_file(table, csv_name))
        print("tables/%s.tmdl" % table)

    # expressions.tmdl -- der eine Ort fuer den Datenpfad
    expr = (
        "/// Ordner mit allen Demo-CSVs. Einziger Ort, an dem der Pfad steht —\n"
        "/// bei einer Ordnerverschiebung nur hier anpassen.\n"
        'expression DemoPfad = "%s" meta [IsParameterQuery=true, Type="Text", '
        "IsParameterQueryRequired=true]\n"
        "%slineageTag: %s\n"
        "\n"
        "%sannotation PBI_NavigationStepName = Navigation\n"
        "\n"
        "%sannotation PBI_ResultType = Text\n"
        % (DEMO_PATH.replace("\\", "\\"), TAB, guid("expression", "DemoPfad"),
           TAB, TAB)
    )
    write(os.path.join(MODEL, "expressions.tmdl"), expr)
    print("expressions.tmdl")

    rel = []
    for i, (frm, to, extra) in enumerate(RELATIONSHIPS, 1):
        rel.append("relationship %s\n" % guid("rel", frm, to))
        rel.append("%sfromColumn: %s\n" % (TAB, frm))
        rel.append("%stoColumn: %s\n" % (TAB, to))
        rel.append("\n")
    write(os.path.join(MODEL, "relationships.tmdl"), "".join(rel).rstrip() + "\n")
    print("relationships.tmdl")

    order = '","'.join(t for t, _ in TABLES)
    model = (
        "model Model\n"
        "%sculture: de-DE\n"
        "%sdefaultPowerBIDataSourceVersion: powerBI_V3\n"
        "%ssourceQueryCulture: de-DE\n"
        "%svalueFilterBehavior: independent\n"
        "%sdataAccessOptions\n"
        "%s%slegacyRedirects\n"
        "%s%sreturnErrorValuesAsNull\n"
        "\n"
        "annotation __PBI_TimeIntelligenceEnabled = 0\n"
        "\n"
        "annotation PBI_ProTooling = [\"DevMode\"]\n"
        "\n"
        'annotation PBI_QueryOrder = ["DemoPfad","%s"]\n'
        "\n"
        % (TAB, TAB, TAB, TAB, TAB, TAB, TAB, TAB, TAB, order)
    )
    for t, _ in TABLES:
        model += "ref table %s\n" % quote(t)
    model += "\nref cultureInfo en-US\n"
    write(os.path.join(MODEL, "model.tmdl"), model)
    print("model.tmdl")


if __name__ == "__main__":
    main()
