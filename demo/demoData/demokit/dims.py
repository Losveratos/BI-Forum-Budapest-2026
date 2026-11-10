# -*- coding: utf-8 -*-
"""Stammdaten-Dimensionen des PnL ChartkitchenDemoKit:
Regionen, Gesellschaften, Währungen, Wechselkurse und die Datumsdimension.

Fiktiver Konzern "DWG Industries SE" mit Sitz in Deutschland -- neun
Gesellschaften in drei Regionen, acht Währungen. Alle Namen sind frei
erfunden, die Kursniveaus sind plausibel gewählt, aber keine echten
Marktdaten.
"""

import datetime as dt
import hashlib
import math

# ---------------------------------------------------------------------------
# Regionen
# ---------------------------------------------------------------------------
# (RegionID, Kuerzel, Name DE, Name EN, Sortierung, Hauptsitz, Zeitzone)
REGIONS = [
    ("R-EMEA", "EMEA", "Europa, Nahost & Afrika", "Europe, Middle East & Africa",
     10, "Stuttgart", "UTC+01:00"),
    ("R-AM", "Americas", "Amerika", "Americas",
     20, "Chicago", "UTC-06:00"),
    ("R-APAC", "APAC", "Asien-Pazifik", "Asia-Pacific",
     30, "Singapur", "UTC+08:00"),
]

# ---------------------------------------------------------------------------
# Segmente
# ---------------------------------------------------------------------------
SEGMENTS = {
    "IA": ("Industrial Automation", "Industrial Automation"),
    "ES": ("Energiesysteme", "Energy Systems"),
    "MS": ("Mobilitätslösungen", "Mobility Solutions"),
    "DS": ("Digitale Dienste", "Digital Services"),
}

# ---------------------------------------------------------------------------
# Währungen
# ---------------------------------------------------------------------------
# (ISO, Name DE, Name EN, Symbol, Nachkommastellen, Sortierung)
CURRENCIES = [
    ("EUR", "Euro", "Euro", "€", 2, 10),
    ("CHF", "Schweizer Franken", "Swiss franc", "CHF", 2, 20),
    ("PLN", "Polnischer Zloty", "Polish zloty", "zł", 2, 30),
    ("CZK", "Tschechische Krone", "Czech koruna", "Kč", 2, 40),
    ("USD", "US-Dollar", "US dollar", "$", 2, 50),
    ("AUD", "Australischer Dollar", "Australian dollar", "A$", 2, 60),
    ("JPY", "Japanischer Yen", "Japanese yen", "¥", 0, 70),
]

KONZERNWAEHRUNG = "EUR"

# Kursniveau in Einheiten der Landeswährung je 1 EUR, am Anfang (2023-12)
# und am Ende (2026-12) des Rechenzeitraums. Dazwischen wird geometrisch
# interpoliert und mit einer glatten Welle plus Rauschen überlagert.
#   CHF, PLN und CZK werten gegenüber dem Euro auf (Kurs fällt),
#   USD leicht ab, AUD deutlicher, JPY am stärksten.
FX_PATH = {
    "EUR": (1.0, 1.0, 0.000),
    "CHF": (0.955, 0.895, 0.012),
    "PLN": (4.360, 4.190, 0.018),
    "CZK": (25.20, 24.30, 0.015),
    "USD": (1.085, 1.125, 0.021),
    "AUD": (1.645, 1.735, 0.024),
    "JPY": (161.0, 188.0, 0.026),
}

# ---------------------------------------------------------------------------
# Gesellschaften
# ---------------------------------------------------------------------------
# EntityID, Name, Kurzname, RegionID, Land DE, Land EN, ISO-Land, Segment,
# Währung, Rechtsform, Umsatz FY2026 in mEUR (Konzernsicht, brutto),
# Mitarbeiter, Erstkonsolidierung (JJJJ-MM), Konsolidierungsart
ENTITIES = [
    ("1100", "DWG Automation GmbH", "Automation DE", "R-EMEA",
     "Deutschland", "Germany", "DE", "IA", "EUR", "GmbH",
     820.0, 3180, "2024-01", "Vollkonsolidierung"),
    ("1200", "DWG Energy Systems AG", "Energy DE", "R-EMEA",
     "Deutschland", "Germany", "DE", "ES", "EUR", "AG",
     690.0, 2540, "2024-01", "Vollkonsolidierung"),
    ("1300", "DWG Mobility Solutions S.A.S.", "Mobility FR", "R-EMEA",
     "Frankreich", "France", "FR", "MS", "EUR", "S.A.S.",
     480.0, 1880, "2024-01", "Vollkonsolidierung"),
    ("1400", "DWG Automation Schweiz AG", "Automation CH", "R-EMEA",
     "Schweiz", "Switzerland", "CH", "IA", "CHF", "AG",
     260.0, 640, "2024-01", "Vollkonsolidierung"),
    ("1500", "DWG Energy Polska sp. z o.o.", "Energy PL", "R-EMEA",
     "Polen", "Poland", "PL", "ES", "PLN", "sp. z o.o.",
     210.0, 1120, "2024-01", "Vollkonsolidierung"),
    ("1600", "DWG Automation Czechia s.r.o.", "Automation CZ", "R-EMEA",
     "Tschechien", "Czechia", "CZ", "IA", "CZK", "s.r.o.",
     180.0, 980, "2024-01", "Vollkonsolidierung"),
    ("2100", "DWG Industries North America Inc.", "Industries US", "R-AM",
     "Vereinigte Staaten", "United States", "US", "IA", "USD", "Inc.",
     610.0, 1860, "2024-01", "Vollkonsolidierung"),
    ("3100", "DWG Mobility Australia Pty Ltd", "Mobility AU", "R-APAC",
     "Australien", "Australia", "AU", "MS", "AUD", "Pty Ltd",
     190.0, 430, "2024-01", "Vollkonsolidierung"),
    # Zukauf April 2026 -- kein Vorjahr, Sparkline mit Luecke
    ("3200", "DWG Digital Services KK", "Digital JP", "R-APAC",
     "Japan", "Japan", "JP", "DS", "JPY", "KK",
     120.0, 410, "2026-04", "Vollkonsolidierung (Zukauf)"),
]

# Segment-Profile: steuern Margen und Bilanzstruktur je Gesellschaft.
# Alle Werte sind Verhältnisse und damit währungsunabhängig.
#   gm      Rohertragsmarge (Ziel)
#   sell    Vertriebskosten in % vom Netto-Umsatz
#   admin   Verwaltungskosten in % vom Netto-Umsatz
#   rnd     F&E in % vom Netto-Umsatz
#   dio     Vorratsreichweite in Tagen (bezogen auf Umsatzkosten)
#   dso     Forderungslaufzeit in Tagen
#   dpo     Verbindlichkeitenlaufzeit in Tagen
#   capex   Investitionen in % vom Netto-Umsatz
#   ppe     Sachanlagenintensität (Sachanlagen in % vom Jahresumsatz)
#   season  Monatsgewichte Jan..Dez (Summe 12.0)
SEGMENT_PROFILE = {
    "IA": dict(gm=0.360, sell=0.092, admin=0.058, rnd=0.052,
               dio=78, dso=62, dpo=54, capex=0.034, ppe=0.30,
               season=[0.90, 0.94, 1.09, 1.00, 1.03, 1.08,
                       0.88, 0.86, 1.07, 1.05, 1.03, 1.07]),
    "ES": dict(gm=0.318, sell=0.078, admin=0.054, rnd=0.041,
               dio=96, dso=74, dpo=62, capex=0.042, ppe=0.38,
               season=[0.84, 0.89, 1.06, 0.98, 1.02, 1.12,
                       0.92, 0.88, 1.06, 1.08, 1.06, 1.09]),
    "MS": dict(gm=0.288, sell=0.086, admin=0.051, rnd=0.064,
               dio=68, dso=58, dpo=66, capex=0.048, ppe=0.34,
               season=[0.93, 0.97, 1.08, 1.02, 1.05, 1.04,
                       0.80, 0.84, 1.09, 1.08, 1.05, 1.05]),
    "DS": dict(gm=0.612, sell=0.148, admin=0.082, rnd=0.118,
               dio=12, dso=48, dpo=38, capex=0.021, ppe=0.09,
               season=[0.96, 0.96, 1.04, 0.99, 1.00, 1.03,
                       0.97, 0.97, 1.02, 1.02, 1.01, 1.03]),
}


# ---------------------------------------------------------------------------
# Wechselkurse
# ---------------------------------------------------------------------------
def _fx_jitter(*parts):
    key = "fx-demokit|" + "|".join(str(p) for p in parts)
    h = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") / float(1 << 64) * 2.0 - 1.0


def _spot(currency, month_index, total_months):
    """Kassakurs (Landeswährung je 1 EUR) am Ende von Monat month_index."""
    start, end, amp = FX_PATH[currency]
    if start == end:
        return 1.0
    t = month_index / float(total_months)
    base = start * (end / start) ** t                      # geometrischer Trend
    wave = 1.0 + amp * 0.55 * math.sin(2.0 * math.pi * (t * 1.7 + 0.3))
    noise = 1.0 + amp * 0.35 * _fx_jitter(currency, month_index)
    return base * wave * noise


def build_fx_rates(first_ym, last_ym):
    """dict[(currency, (year, month))] -> (Durchschnittskurs, Stichtagskurs).

    Durchschnittskurs für Ertrags- und Aufwandsposten sowie Zahlungsströme,
    Stichtagskurs für Bilanzposten -- so verlangt es IAS 21.
    """
    months = month_sequence(first_ym, last_ym)
    total = len(months) - 1
    out = {}
    for cur in FX_PATH:
        prev = _spot(cur, -1, total) if cur != "EUR" else 1.0
        for i, ym in enumerate(months):
            close = _spot(cur, i, total) if cur != "EUR" else 1.0
            avg = (prev + close) / 2.0
            if cur != "EUR":
                avg *= 1.0 + FX_PATH[cur][2] * 0.08 * _fx_jitter(cur, ym, "avg")
            out[(cur, ym)] = (avg, close)
            prev = close
    return out


def fx_base_rate(rates, currency, year):
    """Durchschnittskurs eines Jahres -- Basis, um die in EUR geplanten
    Umsatzziele in Landeswährung umzurechnen."""
    vals = [a for (c, (y, m)), (a, _) in rates.items()
            if c == currency and y == year]
    return sum(vals) / len(vals) if vals else 1.0


# ---------------------------------------------------------------------------
# Datumsdimension
# ---------------------------------------------------------------------------
MONTH_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"]
MONTH_DE_SHORT = ["Jan", "Feb", "Mrz", "Apr", "Mai", "Jun",
                  "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
MONTH_EN_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAY_DE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
              "Freitag", "Samstag", "Sonntag"]
WEEKDAY_DE_SHORT = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
WEEKDAY_EN = ["Monday", "Tuesday", "Wednesday", "Thursday",
              "Friday", "Saturday", "Sunday"]
WEEKDAY_EN_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

DATE_COLUMNS = [
    "Datum", "DatumKey", "Jahr", "Halbjahr", "HalbjahrNr", "Quartal",
    "QuartalNr", "JahrQuartal", "MonatNr", "Monat", "Monat Lang",
    "Monat Kurz", "Month Long", "Month Short", "Periode", "Period",
    "PeriodeSort", "Monatsende", "Tag", "TagImJahr", "TagImMonat",
    "Wochentag", "Weekday", "Wochentag Kurz", "Weekday Short",
    "WochentagNr", "ISO-Woche", "Woche", "IstWerktag", "IstMonatsletzter",
    "Periodenstatus", "Period Status", "Relatives Jahr", "Relativer Monat",
    "IstIstPeriode", "IstAbgeschlossen",
]


def month_end(year, month):
    """Letzter Kalendertag des Monats."""
    if month == 12:
        return dt.date(year, 12, 31)
    return dt.date(year, month + 1, 1) - dt.timedelta(days=1)


def build_calendar(first_year, last_year, last_actual_ym, today):
    """Tagesgenaue Datumsdimension von 1.1.<first_year> bis 31.12.<last_year>."""
    rows = []
    d = dt.date(first_year, 1, 1)
    end = dt.date(last_year, 12, 31)
    la_year, la_month = last_actual_ym
    last_actual_idx = la_year * 12 + la_month

    while d <= end:
        y, m = d.year, d.month
        midx = y * 12 + m
        me = month_end(y, m)
        quarter = (m - 1) // 3 + 1
        half = 1 if m <= 6 else 2
        iso_year, iso_week, iso_wd = d.isocalendar()
        is_actual = midx <= last_actual_idx

        if is_actual:
            status_de, status_en = "Ist", "Actual"
        elif y == last_year:
            status_de, status_en = "Forecast", "Forecast"
        else:
            status_de, status_en = "Plan", "Plan"

        rows.append({
            "Datum": d.isoformat(),
            "DatumKey": y * 10000 + m * 100 + d.day,
            "Jahr": y,
            "Halbjahr": "H%d %d" % (half, y),
            "HalbjahrNr": half,
            "Quartal": "Q%d" % quarter,
            "QuartalNr": quarter,
            "JahrQuartal": "%d-Q%d" % (y, quarter),
            "MonatNr": m,
            "Monat": "%04d-%02d" % (y, m),
            "Monat Lang": MONTH_DE[m - 1],
            "Monat Kurz": MONTH_DE_SHORT[m - 1],
            "Month Long": MONTH_EN[m - 1],
            "Month Short": MONTH_EN_SHORT[m - 1],
            "Periode": "%s %02d" % (MONTH_DE_SHORT[m - 1], y % 100),
            "Period": "%s %02d" % (MONTH_EN_SHORT[m - 1], y % 100),
            "PeriodeSort": y * 100 + m,
            "Monatsende": me.isoformat(),
            "Tag": d.day,
            "TagImJahr": d.timetuple().tm_yday,
            "TagImMonat": d.day,
            "Wochentag": WEEKDAY_DE[iso_wd - 1],
            "Weekday": WEEKDAY_EN[iso_wd - 1],
            "Wochentag Kurz": WEEKDAY_DE_SHORT[iso_wd - 1],
            "Weekday Short": WEEKDAY_EN_SHORT[iso_wd - 1],
            "WochentagNr": iso_wd,
            "ISO-Woche": "%04d-KW%02d" % (iso_year, iso_week),
            "Woche": iso_week,
            "IstWerktag": "true" if iso_wd <= 5 else "false",
            "IstMonatsletzter": "true" if d == me else "false",
            "Periodenstatus": status_de,
            "Period Status": status_en,
            "Relatives Jahr": y - today.year,
            "Relativer Monat": midx - (today.year * 12 + today.month),
            "IstIstPeriode": "true" if is_actual else "false",
            "IstAbgeschlossen": "true" if me < dt.date(today.year, today.month, 1) else "false",
        })
        d += dt.timedelta(days=1)
    return rows


def month_sequence(first_ym, last_ym):
    """Liste von (Jahr, Monat) von first_ym bis last_ym, beide inklusive."""
    out = []
    y, m = first_ym
    ly, lm = last_ym
    while (y, m) <= (ly, lm):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out
