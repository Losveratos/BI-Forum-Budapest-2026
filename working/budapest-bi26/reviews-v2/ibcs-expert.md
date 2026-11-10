# Review IBCS-Experte

Stand 2026-11-09 · Grundlage: 23 Folienbilder (s01–s23), `story.html`, `BRIEF.md`, `REVIEWS.md`, sechs Demo-Seiten und `demo-report/README.md` · Maßstab: IBCS Standards 2.0 / ISO 24896 (UN = Unify, CH = Check, SA = Say, ST = Structure, CO = Condense, EX = Express, SI = Simplify)

## Drei Dinge, die vor dem Vortrag gefixt sein müssen

1. **Gebietsschema und Einheiten der Demo auf Englisch und IBCS-Einheiten umstellen.** Ein englisches Publikum liest „Σ 2.818M“ als 2,8 Millionen statt 2,818 Milliarden. Dazu kommen „in Mio.“, Dezimalkommas („+35,5M“, „+12,8%“), „Alle“ in den Slicern der Plan-gap-Seite, die deutsche Bedienleiste des P&L-Visuals („Ansicht · Tabelle · Balken · Einheit · Dichte“, „AC Ist · PY Vorjahr · günstige Δ“, „Dokumentierte IBCS-Abweichung …“) und die deutschen Zeilen der Brauerei-GuV auf A6. Fix: Modellkultur auf en-US stellen (Desktop-Neustart nötig) oder Format-Strings je Measure mit Punkt als Dezimaltrenner. Einheit einmal in den Titel schreiben (`Revenue in mEUR`) und die Werte ohne „M“-Suffix beschriften (`662`, `+29.8`, `+4.7%`). Die Sprache im P&L-Visual auf EN stellen. Die Rung-Seiten 1–3 zeigen zehnstellige Euro-Beträge (`2.817.623.779`). IBCS erlaubt höchstens 4 Ziffern in Tabellen, also Format `#,0.0,,` → `2,817.6` mEUR.
2. **Drei Notationsbrüche auf Demo-Seiten beheben, die live gezeigt werden.** (a) Rung 1: Im Balkendiagramm ist PL hellgrau gefüllt. Hellgrau ist in IBCS das Zeichen für PY, das Publikum liest also „AC vs PY“. AC ist blau-teal statt dunkelgrau. (b) Rung 2: Negative ΔPL-Textbalken laufen wie positive nach rechts, die Nulllinie fehlt (Cost of sales −49.7 zeigt nach rechts). (c) Rung 4 Deneb: Der PL-Umriss liegt deckungsgleich unter AC und ist in 8 von 10 Monaten unsichtbar. Die Struktur (Gesellschaften) steht als Säulen statt als Balken, und positive ΔPL-Beschriftungen stehen unter der Achse („+5.4M“) oder im Balken („+30M“). Dazu ist die günstige Farbe uneinheitlich: Rung 1 und Plan gap sind teal, Rung 2–4 grün. UNIFY verlangt eine Farbe für alles.
3. **Sachfehler in Text und Zahlen tilgen.** (a) Plan-gap-Seite, Untertitel: „so the two companies below plan stand out“. Vier Gesellschaften liegen unter Plan (Mobility FR, Automation CH, Mobility AU, Digital JP). Neu: „…so the four companies below plan stand out, Mobility FR with −32.3 m“. (b) A6 (Brauerei-GuV, s18): Die PL-Rohertragsmarge ist mit 67.5 % ausgewiesen. Gerechnet sind es 12 137.75 / 18 056.00 = **67.2 %**, die Abweichung beträgt also −0.4 pp statt −0.7 pp. Das ist derselbe Fehlertyp, den der Controller am 7.11. auf Folie 6 gefunden hat; auf A6 ist er geblieben. Fix: Render ersetzen, am besten durch dieselbe Konzern-GuV in T04B, englisch und in mEUR. (c) Folie 4, Fußzeile „One visual, two directions, one scale“: Auf der Plan-gap-Seite haben die beiden Charts nicht dieselbe Skala (gemessen ≈ 0.43 px/mEUR gegen 1.53 px/mEUR, Faktor ≈ 3.6, ohne Skalenband). Neu: „One visual, two directions, Δ on the base scale in each chart“, oder in beiden Charts ein Skalenband bei 100 mEUR setzen.

## Befunde (priorisiert, max. 12)

**1 · Folie 6 (s06)** · Die Empfehlung vom 7.11. („eine GuV ist für IBCS eine Rechnung, kein Sonderfall der Struktur“) ist nicht umgesetzt: Die Folie heißt weiter „A P&L is structure with rules“ und „Structure analysis, but the rows are not equal“.
Fix: Kicker „The special case“ → „Not a ranking“. Titel: **„A P&L is a calculation, not a structure“**. Unterzeile: „IBCS treats it as a calculation scheme: operators (+ − =), subtotals, a vertical calculation waterfall, never sorted by size. It needs a hierarchy, formulas and a sign.“ Der Rest der Folie (vier Dinge) passt dazu.
Beleg: IBCS EX, Vertikaler Wasserfall (a) „Calculation waterfall“ für Rechenschemata (P&L), ohne horizontales Gegenstück; Tabellen mit Rechenzeilen und Operatoren.

**2 · Folien 4/5 und Plan-gap-Seite** · Die Skalen der beiden Charts einer Seite weichen ohne Markierung um den Faktor ≈ 3.6 voneinander ab. Auf der Deneb-Seite sind es ≈ 2.1 (316 mEUR auf 252 px gegen 662 mEUR auf 248 px). Das widerspricht der eigenen CHECK-Karte „same scale“.
Fix: Entweder beide Charts auf einen gemeinsamen Maximalwert fixieren (die Monatssäulen werden dann kürzer, das ist ehrlich) oder in beiden ein Skalenband bei 100 mEUR mit hellem Hintergrund zeichnen. Sprechertext: „Within one chart Δ is on the base scale; across charts the band shows the factor.“
Beleg: CH 3.1 / UN 5.2 (gleiche Einheit → gleiche Skala auf einer Seite, sonst Skalenband), ISO 24896.

**3 · Alle Demo-Seiten, Kacheltitel** · Die Titel sind einzeilig und deskriptiv-technisch („Revenue by month, AC columns with PL outline and ΔPL on the same scale, EUR“). Das „Wer“ fehlt, das „Wann“ fehlt, der Seitenfilter Monate 1–10 ist unsichtbar, und die Einheit „EUR“ passt nicht zu den Labels in M/bn.
Fix (Bildschirmform, eine Zeile mit `|`): `DWG Industries SE | Revenue in mEUR, by company, sorted by AC (↓) | Jan..Oct 2026 AC and PL and ΔPL`. Die Seitenbeschreibung oben (grauer Fließtext) durch eine Kernbotschaft ersetzen, z. B. „Revenue +1.3% above plan; four of nine companies miss it, Mobility FR alone by −32 m“. Den Wert dann im Chart mit blauer Ellipse markieren.
Beleg: UN 2.2 (Titel: wer/was/wann, „&“ vs „and“, Zeitspannen `Jan..Oct`), SA (Botschaft als Satz, im Visual hervorgehoben).

**4 · Demo gesamt** · FC kommt in keinem Demo-Visual vor. Der Seitenfilter schneidet auf Monate 1–10. Folie 3 und Folie 6 versprechen aber „forecast hatched where actuals stop“.
Fix: Auf der Deneb-Seite oder im Zeit-Chart von Plan gap die Zeitreihe ohne Monatsfilter als `Jan..Dec 2026 AC&FC and PL and ΔPL` zeigen: Nov/Dec schraffiert, ΔPL in Nov/Dec ebenfalls schraffiert. Der Filter „Monate 1–10“ gilt nur für Seiten mit reinem AC. Das ist die Szene, in der IBCS-Notation ihren Wert zeigt.
Beleg: UN 3.2 (FC schraffiert; Varianz-Füllung folgt dem Minuenden), UN 2.2 (`AC&FC`).

**5 · Folie 11 (Matrix) und Folie 8** · „IBCS fit“ mischt Zertifizierung und Konformität. 5b bekommt ●●● „IBCS-certified“, Deneb ●●● „anything you can spec“, obwohl die Deneb-Seite der Demo PL unsichtbar zeichnet und Struktur als Säulen. Fabric Apps bekommen ●●● ohne Demo-Beleg.
Fix: Spalte umbenennen in „IBCS fit (as shown today)“. 5b-Zelle: „certified software; conformity still the author's job“. Deneb: ●●○ „anything you spec, if you spec it“. Fabric Apps: ●●○ „same React ports, not shown“. Auf Folie 10 „IBCS certificate mandatory“ präzisieren: „IBCS-certified software mandatory“. Vorschlag für die IBCS-Unterkriterien siehe unten (Szenario-Notation, Δ auf Basisskala, Skalengleichheit über Visuals, GuV als Rechnung, Titel/Einheiten, Tabellen).
Beleg: Die IBCS-Zertifizierung prüft Software oder Berichtsvorlagen, nicht jeden Bericht. REVIEWS.md, IBCS-Punkt 5.

**6 · Folie 10 (Rechner-Chart)** · Die Ansätze sind rot (Paid), grün (Open source), blau und gelb eingefärbt. In einem Vortrag, der Rot und Grün gerade als „ungünstig/günstig“ eingeführt hat, liest das Publikum „Paid = schlecht, Open source = gut“.
Fix: Alle vier Bänder grau (P10–P90 hellgrau, P50-Strich dunkelgrau), Kategoriennamen schwarz. Wenn etwas hervorgehoben werden soll, dann nur der Gleichstand Paid/Open source mit blauer Ellipse. Im Rechner selbst die Farbe ebenfalls neutralisieren oder die Kategoriefarben dokumentieren.
Beleg: SI (keine dekorativen Farben), UN 4.1 (Rot/Grün sind für Geschäftswirkung reserviert).

**7 · Folie 5 (IBCS on one page)** · Die SUCCESS-Karten stehen ohne die v2-Gruppierung da. Lizenzlücke: Die Folie bearbeitet CC-BY-SA-Inhalt, die Bearbeitung fällt damit unter dieselbe Lizenz. Außerdem sind Rechteinhaber der Standards (IBCS Association) und Markeninhaber (IBCS Institute) nicht getrennt.
Fix: Über den Karten zwei Klammern, „NOTATION: Simplify · Unify · Check“ und „COMPOSITION: Say · Express · Structure · Condense“ (Reihenfolge der Karten entsprechend). Fußzeile: „SUCCESS cards adapted from the IBCS® Standards 2.0 by the IBCS Association, CC BY-SA 4.0 (ibcs.com/standards); this slide is shared under the same licence · IBCS® is a registered trademark of the IBCS Institute“. SAY-Karte: „one message per page, as a sentence above it, highlighted in the chart“ (IBCS spricht von Seite/Visual, nicht von jedem Chart). Legende „Δ on the base scale, or a marked factor“ → „Δ on the base scale, or a scale band“: IBCS kennt Skalenband und Lupe, keinen Faktor-Hinweis.
Beleg: IBCS 2.0, Gliederung NOTATION/COMPOSITION; CC BY-SA 4.0 Abschnitt 3(b); UN 5.2.

**8 · Plan-gap-Seite, Folien 4/5 (Struktur-Chart)** · Die Gesellschaften stehen weder nach Größe sortiert noch gruppiert (Industries US 482 unter Automation CZ 141), und die Reihenfolge weicht von Rung 1–3 ab (dort AC↓). Eine Summenzeile fehlt; Σ steht nur im Kopf.
Fix: Im ChartKitchen-Visual nach AC absteigend sortieren und das im Titel nennen („sorted by AC (↓)“), oder nach Segment gruppieren mit Zwischenabstand. Für die Botschaft „wo sitzt die Lücke“ geht auch eine Sortierung nach ΔPL. Eine Total-Zeile mit größerem Abstand unten ergänzen. Dieselbe Reihenfolge auf allen Rung-Seiten.
Beleg: UN 4.3 (Ranking-Pfeil im Titel), ST 1 (konsistente Elemente).

**9 · Plan-gap-Seite, ΔPL %- und ΔPY %-Pins** · Die Pin-Köpfe sind teal/rot gefärbt. Nach IBCS 2.0 trägt der Kopf die Szenario-Füllung des Minuenden (AC = gefüllt dunkel); die Nadel trägt die Bewertungsfarbe. Das eigene P&L-Visual (T04B, s18) macht es richtig (dunkle Quadrate), ChartKitchen nicht: zwei Notationen beim selben Hersteller.
Fix: In ChartKitchen den Pin-Kopf AC-dunkel füllen, bei FC-Minuend schraffiert, bei PL umrandet; die Nadel bleibt teal/rot.
Beleg: UN 4.1 (relative Abweichung: Pin, Kopf mit Szenario-Füllung des Minuenden).

**10 · Group-P&L-Seite (Folie 6, Demo)** · T03A zeigt ΔPY/ΔPL nur als schwarze Zahlen. Weil Kosten positiv angezeigt werden, sieht „+49.7“ bei Cost of sales genauso aus wie „+35.5“ bei Net revenue, obwohl das eine ungünstig und das andere günstig ist. Genau das Vorzeichen-Problem, das die Folie erklärt, ist im Bild nicht sichtbar. Titelzeile 3 ist Prosa.
Fix: In der Demo T04B (integrierte ΔPL-Balken und ΔPL-%-Pins) für die Konzern-GuV zeigen oder in T03A die Abweichungszahlen einfärben. Titel: `Income statement in mEUR` / `Jan..Oct 2026 PY, PL, AC, ΔPY, ΔPL`.
Beleg: UN 4.1 (Abweichungszahlen in Tabellen dürfen nach Wirkung gefärbt werden), UN 2.2.

**11 · Folie 3 vs Demo** · Die Schemazahlen (Jan 262, Jan..Oct 2 884) weichen vom Demo-Report ab (Jan 245, Jan..Oct 2 818). Die Farben passen auch nicht: Navy #0F1E2E und PY bläulich #9AA5B1 gegen #404040/#B3B3B3 in den Renders auf Folie 4.
Fix: Die Arrays `AC/PY/PL/FC` in `story.html` aus dem Demo-Modell nehmen (Jan..Oct AC wie Plan gap, Nov/Dec FC, FY AC&FC = 3 440 laut reconciliation.txt). AC `#404040`, PY `#B3B3B3`. Dann zeigt Folie 3 dieselbe Zeitreihe, die eine Folie später als Render erscheint.
Beleg: UN 1 (gleiche Bedeutung, gleiches Aussehen).

**12 · Rung-Matrizen 1–3** · Die GuV erscheint als flache Liste von L1-Zeilen mit „Total“ am Ende. Es gibt keine Zwischensummen (Net revenue → Gross profit → EBITDA → EBIT → Net income), und „Total“ ist in Wahrheit das Ergebnis nach Steuern. Die Spaltenköpfe sind technisch („AC signed“), die Spaltenfolge in Rung 1 ist AC, PY, PL.
Fix: „Total“ als „Net income“ beschriften (Matrix › Zwischensummen › Zeilenbeschriftung). Köpfe „PY · PL · AC · ΔPL · ΔPL%“ in dieser Reihenfolge. Optional eine Berichtszeilen-Tabelle mit Zwischensummen über `SWITCH`/Calculation Group; das ist genau der Aufwand, den „Rules: in DAX“ meint, und lässt sich live erzählen.
Beleg: UN 4.1 (Reihenfolge PY → PL → AC), EX (Rechenschema mit Zwischensummen).

## Je Demo-Seite: was fehlt zur Notation (Tabelle Sprosse × Kriterium)

Legende: ✓ erfüllt · ◐ teilweise · ✗ fehlt/falsch · – nicht anwendbar

| Kriterium | R1 Pure PBI | R2 DAX text | R3 SVG | R4 Deneb | 5a Plan gap (ChartKitchen) | 5a Group P&L (P&L Statement) |
|---|---|---|---|---|---|---|
| AC gefüllt dunkel | ✗ teal-blau | ◐ nur Sparkline | ✓ | ✓ | ✓ | ✓ (Kopfmarker) |
| PY hellgrau | ✓ (Zeit-Chart) | – | – | – | ✓ überlappt | ✓ (Kopfmarker) |
| PL Umriss | ✗ grau gefüllt = PY | – | ✓ Sparkline | ✗ deckungsgleich, unsichtbar | ✓ versetzt | ✓ (Kopfmarker) |
| FC schraffiert | ✗ nicht gezeigt | ✗ | ✗ | ✗ (Filter Monate 1–10) | ✗ (Filter) | ✗ (Filter) |
| Δ-Farbe einheitlich | ◐ teal | ◐ grün | ◐ grün | ◐ grün | ◐ teal | ✗ keine Farbe in T03A |
| Negatives Δ nach links/unten, Nulllinie | ✗ Datenbalken überdecken Zahlen | ✗ alles nach rechts | ✓ | ✓ | ✓ | – |
| Δ auf Basisskala im Chart | ✗ keine Δ-Grafik | – | ◐ eigene Skala je Spalte | ✓ | ✓ | – |
| Achse kodiert Referenz (PY grau / PL doppelt) | ✗ | ✗ | ✗ | ✗ dünne Linie | ✓ | – |
| ΔPL%-Pins mit Szenario-Kopf | ✗ | ✗ | ✗ | ✗ | ◐ Kopf farbig statt AC | ✓ in T04B (A6) |
| Gleiche Skala über Visuals der Seite | ✗ M vs bn | – | ✗ Sparklines je Zeile skaliert | ✗ Faktor ≈ 2.1 | ✗ Faktor ≈ 3.6 | – |
| Labels ≤ 3/4 Ziffern, Einheit im Titel | ✗ 10 Ziffern | ✗ 10 Ziffern | ✗ Tabelle 10, SVG 3 | ◐ M/k gemischt | ◐ „Mio.“ + Dezimalkomma | ◐ „million EUR“, Dezimalkomma |
| Titel wer / was / wann | ✗ | ✗ | ✗ | ✗ | ◐ wer fehlt | ✓ (Kernbotschaft + 3 Zeilen) |
| Kernbotschaft + Hervorhebung | ✗ | ✗ | ✗ | ✗ | ✗ (Text sachlich falsch) | ◐ Satz ja, Hervorhebung nein |
| Struktur als Balken, sortiert | ✓ AC↓ | ✓ AC↓ (Tabelle) | ✓ AC↓ (Tabelle) | ✗ Säulen, unsortiert | ✗ unsortiert | – |
| GuV als Rechnung (Operatoren, Zwischensummen) | ✗ flach, „Total“ | ✗ | ✗ | – | – | ✓ |
| Sprache EN | ✓ | ✓ | ✓ | ✓ | ✗ „Alle“ | ✗ UI deutsch |

**Konkrete Änderungen je Seite, nach Aufwand**

- **Rung 1 Pure Power BI (≈ 1 h, größter Hebel fürs Publikum):** Zeit-Chart: AC `#404040`, PY `#B3B3B3`, Datenbeschriftung an, Y-Achse und Gitter aus, Titel wie Befund 3. Balken-Chart: PL-Serie mit 100 % transparenter Füllung und dunklem Rahmen (Spalten/Balken › Rahmen, in aktuellen Desktop-Versionen prüfen; falls nicht vorhanden, PL mittelgrau statt hellgrau und im Titel benennen). Matrix: Format `#,0.0,,` + Titel „in mEUR“, Spaltenfolge PY · PL · AC · ΔPL · ΔPL%. ΔPL ein zweites Mal als Spalte „ΔPL bar“ mit Datenbalken „Nur Balken anzeigen“, getrennten Farben für positiv/negativ und Achse in der Mitte, damit die Zahl nicht mehr überdeckt wird. Optional ein flaches Säulen-Chart ΔPL unter dem Zeit-Chart mit per fx fixierter Achse (Min/Max = Skala des Basischarts). Damit gibt es eine Abweichungsleiste auf Basisskala ganz ohne Code, eine gute Live-Pointe: „core gets further than you think“.
- **Rung 2 DAX only (≈ 1 h):** Balken-Measure um eine Mittelachse bauen: negativ `REPT(" ", n-k) & REPT("█", k) & "│" & REPT(" ", n)`, positiv `REPT(" ", n) & "│" & REPT("█", k) & REPT(" ", n-k)`, Schrift Consolas. Total-Balken in der Bewertungsfarbe statt Navy. Zahlen in mEUR. Die Sparklines sind je Zeile auf das eigene Maximum skaliert: entweder gemeinsame Skala über `ALLSELECTED` oder Spaltenkopf „month pattern, indexed per row“. Digital JP zeigt Lücken in Jan/Feb, Daten prüfen.
- **Rung 3 SVG (≈ 2 h):** Spalte `ΔPL% SVG` als Pin (dünne Linie in Bewertungsfarbe + dunkles Quadrat als AC-Kopf) neben dem ΔPL-Balken. Die Achse im ΔPL-SVG als Doppellinie (zwei 1-px-Linien im Abstand 2 px) zeichnen, so steht dort „vs PL“. Die Sparklines „AC vs PL“ auf eine gemeinsame Skala über alle Gesellschaften stellen (Max über `ALLSELECTED('dim-gesellschaft')`); Digital JP wird dann klein, das ist richtig so. Tabellenzahlen in mEUR mit einer Nachkommastelle, damit Tabelle und SVG-Label (−49.7) dieselbe Einheit haben.
- **Rung 4 Deneb (≈ 2–3 h, in Vega-Lite gut machbar):** PL als eigene `bar`-Ebene mit `xOffset` (+⅓ Bandbreite) hinter AC zeichnen (überlappte Gruppierung, wie ChartKitchen). Das Gesellschafts-Chart auf horizontale Balken drehen (`x`/`y` tauschen), nach AC↓ sortieren (`sort: "-x"`). ΔPL-Labels mit `dy` nach Vorzeichen setzen (positiv über, negativ unter dem Balken). Die ΔPL-Achse als zwei `rule`-Ebenen im Abstand 2 px zeichnen (PL-Referenz). Beide Charts per `scale.domain` auf dasselbe Maximum oder ein Skalenband setzen. Labels `format: ",.0f"` in mEUR. Für FC: Zeitreihe Jan..Dec AC&FC, Nov/Dec weiß mit Umriss und diagonalen Streifen (Vega-Lite hat kein natives Muster; Workaround über eine zusätzliche Ebene mit schrägen `rule`-Strichen, geclippt auf die Säule).
- **5a Plan gap ChartKitchen (≈ 30 min):** Sortierung AC↓, Total-Zeile, Titel `DWG Industries SE | Revenue in mEUR | Jan..Oct 2026 AC and PL and ΔPL`, Untertitel „four companies“, Pin-Köpfe AC-dunkel, Skalenband in beiden Charts, Slicer-Locale EN.
- **5a Group P&L (≈ 15 min):** Visual-Sprache EN, Einheit „mEUR“, Template T04B statt T03A in der Demo (oder T03A mit eingefärbten Abweichungen). Einmal ohne Monatsfilter Ganzjahr AC&FC vs PL zeigen, damit die Schraffur live erscheint.

**Kriterien, die der Stack-Vergleich aus IBCS-Sicht enthalten sollte** (statt einer einzigen Spalte „IBCS fit“, z. B. als „Definition of Done“-Checkliste je Rung in der Demo):

1. Szenario-Notation vollständig (AC/PY/PL/FC inkl. Schraffur und Umriss, auch im Δ-Element)
2. Absolute Abweichung auf Basisskala, Achse kodiert die Referenz
3. Relative Abweichung als Pin mit Szenario-Kopf, `N/A` bei negativer Basis
4. Gleiche Skala über mehrere Visuals einer Seite bzw. Skalenband (für jede Plattform die schwierigste Anforderung)
5. GuV als Rechnung: Hierarchie, Zwischensummen, Operatoren, Vorzeichen-Trio
6. Titel, Einheiten und Zahlenformat nach UN 2 (dynamisch aus den Filtern)
7. Kernbotschaft und Hervorhebung möglich (Ellipse, Annotation)
8. Zeitfenster YTD `_Oct` und Ganzjahr AC&FC aus einem Modell
9. Export, der die Notation erhält (PDF/PPT, Abos), denn ein IBCS-Bericht wird verteilt

## Was gut ist und bleiben soll

- **Folie 3 (Aufbau AC → PY → PL → FC):** didaktisch das stärkste IBCS-Chart im Deck. Überlappte Gruppierung, PL-Umriss, FC-Schraffur, „AC&FC“ im letzten Titel korrekt mit „&“. Die Ganzjahreszahl 3 440 vs 3 510 / −2.0 % stimmt rechnerisch.
- **Folie 4 und die Plan-gap-Seite:** Δ jetzt wirklich auf Basisskala (+22.1 / 245 = 9.0 %, nachgerechnet). PL versetzt umrandet, PY hellgrau hinter AC, ΔPY-Achse hellgrau, ΔPL-Achse als Doppellinie, Pins und Balken in drei Ebenen ausgerichtet (CO 4). Die Kritik vom 7.11. ist sauber umgesetzt.
- **Group P&L (T03A):** Kernbotschaft als Satz über dem Titel, dreizeiliger Titel, Spaltenfolge PY · PL · AC · ΔPY · ΔPL, Szenario-Marker in den Spaltenköpfen (grau, Umriss, gefüllt), Operatoren + − =, Marge in pp, schmales Leerzeichen als Tausendertrenner. Das ist lehrbuchnah.
- **A6 (T04B):** integrierter ΔPL-Wasserfall und Pins mit dunklen Köpfen, Achsenhinweis „double line = PL“. So sieht ISO-konforme Abweichungsdarstellung aus, sobald die Marge korrigiert und die Sprache englisch ist.
- **Ehrlichkeit:** „We are not members and not certified“, „teal as documented deviation“, Markenhinweis auf jeder Demo-Seite, Offenlegung der eigenen Visuals, Bildunterschriften wie „No plan outline, no variance panel, no scenario notation“. Das schützt vor dem Vorwurf der Vereinnahmung, bitte beibehalten.
- **Das Modell (Folie 7, A10/A11):** Vorzeichen-Trio in der Dimension, „empty not zero“, FY-Skalar. Das ist die Voraussetzung dafür, dass jede Sprosse dieselbe Bewertungsfarbe richtig setzt. Aus IBCS-Sicht das eigentliche Argument des Vortrags.
