# -*- coding: utf-8 -*-
"""Rewrites the 'Budapest demo' measure block in fact-abschluss.tmdl (v2 after the seven reviews).
Run from anywhere: python -I -X utf8 budapest_measures.py
"""
import re, uuid, io, sys
BASE = r"C:\Users\MichaelTenner\Desktop\PnL Demo\PnL ChartkitchenDemoKit.SemanticModel\definition"
p = BASE + r"\tables\fact-abschluss.tmdl"
s = io.open(p, encoding="utf-8").read()
start = s.index("\t/// ")
# locate the start of the Budapest block: the first measure with displayFolder Budapest demo
idx = s.index("displayFolder: Budapest demo")
start = s.rfind("\n\t/// ", 0, idx)
# walk back over consecutive /// lines
while True:
    prev = s.rfind("\n\t/// ", 0, start - 1)
    if prev != -1 and s[prev:start].count("\n") == 1:
        start = prev
    else:
        break
start += 1
end = s.index("\tcolumn AccountID")
old = s[start:end]
tags = {m.group(1): m.group(2) for m in re.finditer(r"measure '?([^'=\n]+?)'? =.*?lineageTag: ([0-9a-f-]{36})", old, re.S)}
def tag(n): return tags.get(n) or str(uuid.uuid4())
T = "\t"
def m(name, desc, dax_lines, fmt=None, extra=None):
    out = [f"{T}/// {d}" for d in desc]
    q = f"'{name}'" if re.search(r"[^A-Za-z0-9_]", name) else name
    if len(dax_lines) == 1:
        out.append(f"{T}measure {q} = {dax_lines[0]}")
    else:
        out.append(f"{T}measure {q} =")
        out += [f"{T}{T}{T}{l}" for l in dax_lines]
    if fmt: out.append(f"{T}{T}formatString: {fmt}")
    out.append(f"{T}{T}displayFolder: Budapest demo")
    out.append(f"{T}{T}lineageTag: {tag(name)}")
    if extra: out += [f"{T}{T}{e}" for e in extra]
    out.append("")
    return "\n".join(out)

FM = "#,##0.0;-#,##0.0;-"
FD = "+#,##0.0;-#,##0.0;-"
FP = "+0.0%;-0.0%;-"
ACT = "KEEPFILTERS ( 'dim-datum'[Period Status] = \"Actual\" )"
SVG_HEAD = "\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='\" & _W & \"' height='\" & _H & \"' viewBox='0 0 \" & _W & \" \" & _H & \"'>\""
def F(x): return f"FORMAT ( {x}, \"0.0\", \"en-US\" )"

blocks = []
for sc, col, lab in [("AC", "AC Wert", "Ist"), ("PY", "PY Wert", "Vorjahr"), ("PL", "PL Wert", "Plan"), ("FC", "FC Wert", "Forecast")]:
    blocks.append(m(f"{sc} signed",
        [f"GuV only. {lab} vorzeichenrichtig: Kontenzeilen mal SignConvention, nur RowType \"account\"",
         "und Statement \"Income statement\". Erlöse positiv, Kosten negativ, damit Core-Visuals ohne",
         "Vorzeichen-Wissen auskommen. Ergebnis in Mio. EUR (durch 1.000.000 geteilt)."],
        ["CALCULATE (", "    SUMX (", "        VALUES ( 'dim-konten'[SignConvention] ),",
         f"        'dim-konten'[SignConvention] * CALCULATE ( SUM ( 'fact-abschluss'[{col}] ) )", "    ) / 1000000,",
         "    KEEPFILTERS ( 'dim-konten'[RowType] = \"account\" ),",
         "    KEEPFILTERS ( 'dim-konten'[Statement] = \"Income statement\" )", ")"], FM))
blocks.append(m("ΔPL", ["Abweichung Ist gegen Plan, vorzeichenrichtig: positiv ist gut. Plan nur für Monate mit",
    "Ist (Period Status = Actual), damit ohne Seitenfilter nicht 10 Ist- gegen 12 Planmonate stehen."],
    ["VAR _Ac = [AC signed]", f"VAR _Pl = CALCULATE ( [PL signed], {ACT} )", "RETURN", "    IF ( NOT ISBLANK ( _Ac ), _Ac - _Pl )"], FD))
blocks.append(m("ΔPL %", ["Abweichung Ist gegen Plan in Prozent des Plans der Ist-Monate."],
    ["DIVIDE ( [ΔPL], ABS ( CALCULATE ( [PL signed], " + ACT + " ) ) )"], FP))
blocks.append(m("ΔPY", ["Abweichung Ist gegen Vorjahr, vorzeichenrichtig: positiv ist gut. Vorjahr nur für Ist-Monate."],
    ["VAR _Ac = [AC signed]", f"VAR _Py = CALCULATE ( [PY signed], {ACT} )", "RETURN", "    IF ( NOT ISBLANK ( _Ac ), _Ac - _Py )"], FD))
blocks.append(m("ΔPY %", ["Abweichung Ist gegen Vorjahr in Prozent des Vorjahres der Ist-Monate."],
    ["DIVIDE ( [ΔPY], ABS ( CALCULATE ( [PY signed], " + ACT + " ) ) )"], FP))
blocks.append(m("ΔPL (bar)", ["Kopie von ΔPL für eine eigene Datenbalken-Spalte in der Core-Matrix (Sprosse 1), damit der",
    "Balken die Zahl nicht überdeckt."], ["[ΔPL]"], FD))
blocks.append(m("ΔPL bar (text)", ["Sprosse 2, nur DAX: Abweichungsbalken aus Unicode-Blöcken, skaliert auf die größte Abweichung",
    "der sichtbaren Zeilen (Summenzeile auf 10 Blöcke begrenzt). Links vom Trennstrich negativ,",
    "rechts positiv. Monospace-Schrift im Visual nötig."],
    ["VAR _D = [ΔPL]", "VAR _Max =",
     "    MAXX ( ALLSELECTED ( 'dim-konten'[L1 EN], 'dim-konten'[L1 Sort] ), ABS ( [ΔPL] ) )",
     "VAR _N = MIN ( 10, ROUND ( DIVIDE ( ABS ( _D ), _Max, 0 ) * 10, 0 ) )",
     "VAR _Neg = REPT ( \" \", 10 - _N ) & REPT ( \"█\", _N )",
     "VAR _Pos = REPT ( \"█\", _N ) & REPT ( \" \", 10 - _N )",
     "RETURN", "    IF (", "        ISBLANK ( _D ),", "        BLANK (),",
     "        IF ( _D < 0, _Neg & \"│\" & REPT ( \" \", 10 ), REPT ( \" \", 10 ) & \"│\" & _Pos )", "    )"]))
blocks.append(m("Revenue sparkline (text)", ["Sprosse 2, nur DAX: Umsatz je Monat als Unicode-Säulen, ein Zeichen je Monat (PeriodeSort,",
    "damit Jahr und Monat eindeutig sind), skaliert auf den höchsten Monat der Zeile."],
    ["VAR _Months = VALUES ( 'dim-datum'[PeriodeSort] )", "VAR _Max = MAXX ( _Months, [Revenue AC] )", "RETURN",
     "    CONCATENATEX (", "        _Months,", "        VAR _V = [Revenue AC]",
     "        VAR _I = ROUND ( DIVIDE ( _V, _Max, 0 ) * 7, 0 ) + 1", "        RETURN",
     "            IF ( ISBLANK ( _V ), \" \", MID ( \"▁▂▃▄▅▆▇█\", _I, 1 ) ),", "        \"\",",
     "        'dim-datum'[PeriodeSort]", "    )"]))
blocks.append(m("ΔPL status", ["Sprosse 2, nur DAX: Farbcode für bedingte Formatierung. Teal (dokumentierte IBCS-Abweichung",
    "wie in ChartKitchen) bei günstiger, Rot bei ungünstiger Abweichung."],
    ["SWITCH (", "    TRUE (),", "    ISBLANK ( [ΔPL] ), BLANK (),", "    [ΔPL] >= 0, \"#2E8B7A\",", "    \"#C0392B\"", ")"]))
blocks.append(m("Revenue AC&FC", ["Sprosse 4, Deneb-Vorlage: Ist für Monate mit Period Status Actual, Forecast für Forecast-",
    "Monate, als eine Reihe für AC&FC-Säulen gegen den Plan-Umriss. Robust auf jeder Ebene."],
    ["CALCULATE ( [Revenue AC], " + ACT + " )",
     "    + CALCULATE ( [Revenue FC], KEEPFILTERS ( 'dim-datum'[Period Status] = \"Forecast\" ) )"], "#,##0"))
for nm, src in [("Revenue AC&FC mEUR", "Revenue AC&FC"), ("Revenue AC mEUR", "Revenue AC"), ("Revenue PY mEUR", "Revenue PY"), ("Revenue PL mEUR", "Revenue PL")]:
    blocks.append(m(nm, [f"{src} in Millionen EUR für Core-Charts, Tabellen und Deneb (Feldname ohne Klammern, weil Deneb", "Felder mit Klammern nicht per Ausdruck lesen kann)."], [f"DIVIDE ( [{src}], 1000000 )"], "#,##0.0"))
blocks.append(m("FC flag", ["Sprosse 4, Deneb-Vorlage: 1 für Forecast-Monate (Period Status = Forecast), sonst 0. Steuert",
    "Umriss und Strichelung der FC-Säulen in der Vega-Lite-Vorlage."],
    ["IF ( SELECTEDVALUE ( 'dim-datum'[Period Status] ) = \"Forecast\", 1, 0 )"], "0"))
line = lambda off: ("\"<line x1='\" & ( _Mid " + off + " ) & \"' y1='0' x2='\" & ( _Mid " + off + " ) & \"' y2='\" & _H & \"' stroke='%23404040' stroke-width='1'/>\"")
blocks.append(m("ΔPL SVG", ["Sprosse 3, SVG-Measure: Abweichungsbalken auf Basisskala mit Doppellinie als Plan-Referenz,",
    "Teal gut, Rot schlecht, Wert in Mio. EUR als Label. Datenkategorie ImageUrl, in der Matrix als",
    "Bild. Balken auf die Zellbreite begrenzt, Koordinaten mit en-US-Format."],
    ["VAR _D = [ΔPL]", "VAR _Max =",
     "    MAXX ( ALLSELECTED ( 'dim-konten'[L1 EN], 'dim-konten'[L1 Sort] ), ABS ( [ΔPL] ) )",
     "VAR _W = 160", "VAR _H = 18", "VAR _Mid = _W / 2",
     "VAR _Len = MIN ( 1, DIVIDE ( ABS ( _D ), _Max, 0 ) ) * ( _Mid - 44 )",
     "VAR _X = IF ( _D < 0, _Mid - _Len, _Mid )",
     "VAR _Col = IF ( _D >= 0, \"%232E8B7A\", \"%23C0392B\" )",
     "VAR _Lbl = FORMAT ( _D, \"+#,##0.0;-#,##0.0\", \"en-US\" )",
     "VAR _LblX = IF ( _D < 0, _Mid + 5, _Mid - 5 )",
     "VAR _Anchor = IF ( _D < 0, \"start\", \"end\" )",
     "VAR _Svg =", "    " + SVG_HEAD,
     "        & " + line("- 1.5"),
     "        & " + line("+ 1.5"),
     "        & \"<rect x='\" & " + F("_X") + " & \"' y='3' width='\" & " + F("_Len") + " & \"' height='\" & ( _H - 6 ) & \"' fill='\" & _Col & \"'/>\"",
     "        & \"<text x='\" & _LblX & \"' y='13' font-family='Segoe UI' font-size='10' text-anchor='\" & _Anchor & \"' fill='%23222'>\" & _Lbl & \"</text>\"",
     "        & \"</svg>\"", "RETURN", "    IF ( ISBLANK ( _D ), BLANK (), _Svg )"], None, ["dataCategory: ImageUrl"]))
blocks.append(m("Revenue AC vs PL SVG", ["Sprosse 3, SVG-Measure: Umsatz je Monat als Säulen (AC gefüllt) mit Plan-Umriss, 160 px breit,",
    "ein Slot je Monat (PeriodeSort), skaliert auf den höchsten Wert der Zeile. Datenkategorie ImageUrl."],
    ["VAR _Months = VALUES ( 'dim-datum'[PeriodeSort] )", "VAR _Max =",
     "    MAXX ( _Months, MAX ( [Revenue AC], [Revenue PL] ) )",
     "VAR _W = 160", "VAR _H = 28", "VAR _N = COUNTROWS ( _Months )", "VAR _Slot = DIVIDE ( _W, _N )",
     "VAR _Bars =", "    CONCATENATEX (", "        _Months,",
     "        VAR _I = RANKX ( _Months, 'dim-datum'[PeriodeSort], , ASC ) - 1",
     "        VAR _Ac = DIVIDE ( [Revenue AC], _Max ) * ( _H - 2 )",
     "        VAR _Pl = DIVIDE ( [Revenue PL], _Max ) * ( _H - 2 )",
     "        VAR _X = _I * _Slot + 1", "        VAR _Bw = _Slot - 3", "        RETURN",
     "            \"<rect x='\" & " + F("_X") + " & \"' y='\" & " + F("_H - _Ac") + " & \"' width='\" & " + F("_Bw") + " & \"' height='\" & " + F("_Ac") + " & \"' fill='%23404040'/>\"",
     "                & \"<rect x='\" & " + F("_X") + " & \"' y='\" & " + F("_H - _Pl") + " & \"' width='\" & " + F("_Bw") + " & \"' height='\" & " + F("_Pl") + " & \"' fill='none' stroke='%23404040' stroke-width='1'/>\",",
     "        \"\",", "        'dim-datum'[PeriodeSort]", "    )", "RETURN", "    IF (",
     "        ISBLANK ( [Revenue AC] ),", "        BLANK (),",
     "        " + SVG_HEAD + " & _Bars & \"</svg>\"", "    )"], None, ["dataCategory: ImageUrl"]))
blocks.append(m("Data as of", ["Datenstand-Stempel für jede Demo-Seite (Karte unter dem Titel): letzter Ist-Monat, Plan- und",
    "Forecast-Version, Einheit, Vorzeichenkonvention."],
    ["VAR _LastAct =", "    CALCULATE (", "        MAX ( 'dim-datum'[Monatsende] ),",
     "        REMOVEFILTERS ( 'dim-datum' ),", "        'dim-datum'[Period Status] = \"Actual\"", "    )", "RETURN",
     "    \"DWG Industries · actuals to \" & FORMAT ( _LastAct, \"mmm yyyy\", \"en-US\" )",
     "        & \" · plan v2026-1 and forecast 10+2 to Dec 2026 · EUR m · variances signed, positive is favourable\""]))

new = "".join(b + "\n" for b in blocks)
s = s[:start] + new + s[end:]
io.open(p, "w", encoding="utf-8").write(s)

mp = BASE + r"\model.tmdl"
# culture stays de-DE: Desktop refuses to change Culture on an existing model
gp = BASE + r"\tables\dim-gesellschaft.tmdl"
gs = io.open(gp, encoding="utf-8").read().replace("/// Sieben Gesellschaften", "/// Neun Gesellschaften", 1)
io.open(gp, "w", encoding="utf-8").write(gs)
print("measures written:", len(blocks), "old block chars:", len(old), "new:", len(new))
