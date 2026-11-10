# Review Controller

Rolle: Konzern-Controller (Management Reporting, Abschluss am dritten Arbeitstag, Plan/Forecast, Kommentierung, Power-BI-Power-User ohne Entwicklerrolle). Grundlage: 23 Folienbilder (s01–s23), `story.html`, `BRIEF.md`, `REVIEWS.md` (7.11.), Demo-Seiten in `assets/`, `demo-report/README.md`, dazu ein Blick in das TMDL des Demo-Modells (`PnL Demo\PnL ChartkitchenDemoKit.SemanticModel`).
Hinweis zur Nummerierung: Die Bewertungsmatrix steht im aktuellen Deck auf **Folie 11** (Folie 10 ist der Rechner). Ich beziehe mich auf die Nummern der Bilder s01–s23.

**Stand der Controller-Punkte vom 7.11.**

| Punkt vom 7.11. | Stand 9.11. |
|---|---|
| Kosten je Leser, Folie 10 Richtung/Widerspruch | erledigt (176-Aussage korrigiert, Preset konsistent) |
| Audit nur Fußnote | erledigt: Matrix-Spalte „Export & audit“ (Folie 11) |
| Folie 3 „Where do we land?“ ohne Zahl | laut REVIEWS.md im letzten Aufbauschritt erledigt (im Bild s03 nur Schritt 1 sichtbar) |
| Brauerei-Margen falsch | erledigt (DWG-Seite auf Folie 6) |
| Datenstand-Stempel | **nur behauptet** (Folie 9), auf den Sprossen-Seiten fehlt er |
| Monatsabschluss-Szene (Buchung korrigieren, alle Stacks zeigen neue Zahl) | **offen** |
| Lokal- vs. Konzernwährung, Ist- vs. Budgetkurs | **nur Appendix A9 (s21), im Demo-Modell nicht gebaut**: kein Budgetkurs in `fact-kurse`, kein `AC @BUD`, keine FX-Zeile |
| Was ein Fachanwender ohne IT ändern kann | **offen**, fehlt in der Matrix |
| Rechner budgetreif (eigener Stundensatz, PBI-Lizenzen, Capacity, Angebote statt Listenpreise) | **teilweise**: Preise als „unverified“ markiert, Plattformlizenzen und Capacity weiter nicht erwähnt |
| Forecast-Versionen, PY-Restatement, Konsolidierung | **offen**, nicht erwähnt |

## Drei Dinge, die vor dem Vortrag gefixt sein müssen

1. **Die Monatsabschluss-Szene bauen (seit 7.11. offen).** Ohne sie bleibt „One Model“ eine Behauptung. Die risikoarme Variante braucht keinen Live-Refresh: Der Generator schreibt eine zusätzliche Buchung (z. B. Mobility FR, Oktober, Rückstellungsauflösung +4,0 m EUR in „Other operating result“) mit `BookingStatus = "Day-3 adjustment"`, alle anderen Zeilen bekommen `"Closed"`. Auf jeder Seite liegt ein synchronisierter Slicer „Booking status“ (Sync Slicers). In der Demo schaltet man ihn um, und **alle sechs Seiten** zeigen denselben neuen ΔPL bei Mobility FR (−32,3 → −28,3 m) und dasselbe neue Ergebnis. Dazu ändert sich der Stempel (siehe 2.). Das dauert 90 Sekunden und belegt die These des Abschlusstitels besser als jede Folie.
2. **Folie 9 verspricht „Every page states its data-as-of“, die Sprossen-Seiten 1–4 halten das nicht ein.** Dort fehlen Zeitraum, Datenstand und Einheit, die Zahlen stehen in vollen EUR mit neun Stellen (`2.817.623.779`). Fix: Eine Stempel-Measure auf jede Seite unter den Titel, z. B.
   `Data as of = "DWG Industries · AC Jan–" & FORMAT(MAX('fact-abschluss'[Monat]), "mmm yyyy") & " · PL/FC to Dec · EUR m · " & SELECTEDVALUE('fact-abschluss'[BookingStatus], "all bookings")`
   (die vorhandene Measure `Filterinfo` ist deutsch, „Konzern“ und „bis“, und taugt nicht für die Bühne). Für die Matrix-Measures `AC/PY/PL signed` und `ΔPL` das Format `#,0.0,,;-#,0.0,,` bzw. `+#,0.0,,;-#,0.0,,` setzen und die Titel auf „EUR m“ ändern.
3. **Die Landung zeigen: Keine Demo-Seite zeigt Forecast oder Gesamtjahr.** Alle Seiten zeigen nur Januar bis Oktober kumuliert. Im November will ich aber wissen, wo das Jahr landet (AC+FC vs. PL FY), und Folie 3 stellt genau diese Frage. Die Measures `Revenue AC&FC`, `FC FY`, `PL FY` und `FC flag` liegen schon im Modell. Fix: Auf der Seite „Group P&L“ das Template mit FC/FY-Spalte zeigen (live umschalten, 30 Sekunden). Auf der Deneb-Seite Nov/Dez als schraffierte FC-Säulen ergänzen, der Page-Filter bleibt dabei für die YTD-Kacheln. Falls das nicht mehr klappt, sagen Sie es offen: *„YTD only today; the FY landing is the same model with `FC FY`.“*

## Befunde (priorisiert, max. 12)

1. **Demo (Folie 9), alle Sprossen** · Es fehlt die Szene, die mich als Anwender überzeugt: Ich sehe nie, was am dritten Arbeitstag passiert, wenn eine Zahl falsch ist. · Fix: die Szene aus „Drei Dinge“ Nr. 1. Sprechtext: *„Day three, 10:40. France books a 4 million release. I flip one slicer, and every rung shows the same new number, because none of them owns a number.“* Danach ein Satz zu Sign-off: *„Who signs off? Whoever owns the model, not whoever drew the chart.“*

2. **Sprossen-Seiten 1–3 (s14–s16, demo-rung1–3)** · Das ist keine GuV, sondern eine Liste der L1-Zeilen mit einer unbeschrifteten Zeile „Total“. Rohertrag, EBITDA und Margen fehlen, und „Total“ ist in Wahrheit der Jahresüberschuss. · Fix: In den drei Matrizen die Gesamtzeile in „Net income“ umbenennen (Row subtotals › Label). Beim Vorführen auf die Zeile zeigen und sagen: *„This is where core visuals stop: no gross profit, no EBITDA, no margin, unless I build a P&L line table or a calculation group.“* So wird Folie 6 („Four things a bar chart never knew“) in der Demo sichtbar, statt nur behauptet.

3. **Sprossen-Seiten 1–4, Zahlenformat** · Im selben Bericht stehen vier Einheitskonventionen nebeneinander: volle EUR mit deutschen Trennzeichen (Sprossen 1–3), „0,1bn“ in der Balkengrafik von Sprosse 1, „M/k“ in Deneb, „mEUR“ mit Komma im P&L-Visual. · Fix: alles auf EUR m mit einer Nachkommastelle (Format siehe „Drei Dinge“ Nr. 2). Das Dezimalkomma kommt aus der Modellkultur de-DE. Entweder den Satz auf Folie 9 anpassen (*„Numbers in German format: the model culture is de-DE“*) oder die Kultur auf en-US stellen; dafür ist ein Desktop-Neustart nötig.

4. **Folie 11, Matrix** · Aus Anwendersicht fehlen die Kriterien, nach denen ich im Abschluss tatsächlich auswähle. „Export & audit“ vermischt außerdem zwei Fragen. · Fix: „Export & audit“ in **„PPT/PDF export“** und **„Logic auditable“** teilen. Dazu zwei neue Spalten mit diesem Vorschlag:
   - **„Controller changes it alone“** (Spaltentitel, Bildunterschrift, Ebene, Einheit, neue Kontenzeile): 1 ●●● · 2 ●●○ (Measure-Änderung braucht Modellrechte) · 3 ●○○ · 4 ●○○ (Spec) · 5a ●●● (Template, Ebene, kEUR/mEUR per Klick) · 5b ●●● · 6 ●○○ (App-Code)
   - **„Comment on a variance“** (je Zelle, Monat und Gesellschaft, nicht je Visual): 1–4 ●○○ (nur Service-Kommentar am Visual) · 5a ●●○ (Kommentar je Konto aus der Dimension, statisch) · 5b ●●● (Zebra-Kommentare; Speicherort prüfen) · 6 ●●○ (baubar, aber App-Code)
   Weitere Kandidaten, falls Platz bleibt: Drill/Aufklappen, Excel-Export der Zeilen, „Time to fix on close day“.

5. **Folie 11, Zeile 5a, und die Seiten „Group P&L“ und „Plan gap“** · Die zwei überzeugendsten Demo-Seiten stammen vom eigenen, nicht zertifizierten Visual. Sie lassen sich im Service weder nach PowerPoint/PDF exportieren noch abonnieren, und das steht nur in einer Matrixzelle. Für meinen Monatsbericht ist das ein K.-o.-Kriterium. · Fix: In der Demo direkt nach der Group-P&L-Seite sagen: *„This one does not export to PowerPoint in the Service. If your board pack is a PDF, this rung is out, or you go paid or Deneb.“* Danach (wie vom Power-BI-Experten schon am 7.11. gefordert) einmal „Export → PDF“ im Service zeigen: Sprosse 1 und Deneb kommen mit, 5a nicht.

6. **Sprosse 4 Deneb (s17, demo-rung4)** · Die Seite zeigt nur Umsatz und keine GuV. Die ΔPL-Labels der großen positiven Abweichungen liegen auf dem Balken und sind unlesbar („+30M“, „+33M“ bei Automation DE/Energy DE), dazu wird „371M“ bei Mobility FR vom PL-Rahmen überschnitten. · Fix: Text-Layer mit `dy` unter die Nulllinie bzw. über den Balken verschieben (`baseline: "top"`, `dy: 4` für positive Werte, analog zu den negativen). Sprechtext: *„Deneb draws the chart; the statement stays in a matrix or a P&L visual.“* In der Matrix (Folie 11) gehört bei 4 der Zusatz „no statement layout“ in die Zelle „IBCS fit“, sonst wirkt ●●● zu großzügig.

7. **Appendix A9 (s21) und Abstract** · Die Folie liest sich, als könne das Demo-Modell „AC @BUD“, „FX effect“ und einen „rate view“-Slicer. Im TMDL gibt es aber nur Durchschnitts- und Stichtagskurs, keinen Budgetkurs und keine FX-Zeile. Der Abstract verspricht „current rate vs budget rate“. · Fix: entweder bauen (Spalte `Kurs Budget` in `fact-kurse`, Measures `AC @BUD`, `FX effect`, Slicer „Rate view“) und 60 Sekunden mit Gesellschaft „Digital JP“ zeigen: AC LW wächst, EUR schrumpft, FX-Zeile erklärt die Differenz. Oder den Fußtext ehrlich ändern: *„Pattern from the finance-data-model skill, variant B; the demo model ships average and closing rates only.“*

8. **Folie 3 (s03)** · Die Monatswerte des Einstiegscharts (Jan 262, Σ ≈ 2.884 m) passen nicht zum Demo-Report (Jan 245, Σ 2.818 m auf Folie 4 und in allen Sprossen). Ein Controller vergleicht genau solche Zahlen. · Fix: die Report-Werte übernehmen: 245 · 259 · 295 · 287 · 297 · 308 · 251 · 251 · 316 · 309 (Σ 2.818). Fußzeile: *„DWG Industries demo model, EUR m“* statt „Demo numbers“.

9. **Appendix A6 (s18) und Seite „Group P&L“ (Folie 6)** · „Same P&L page“ stimmt nicht: A6 zeigt die Brauerei (deutsch, kEUR, Jan–Sep) statt DWG. Die DWG-Seite hat deutsche Bedienelemente („Ansicht“, „Einheit“, „Dichte“, „günstige Δ“, „Dokumentierte IBCS-Abweichung“), der Plan-gap-Slicer zeigt „Alle“, die Sprossen-Seiten zeigen „All“. · Fix: Sprache des P&L-Visuals auf EN stellen, A6 durch einen DWG-Render mit T04B ersetzen, die Slicer-Beschriftung vereinheitlichen.

10. **Forecast-Version wechseln** · Das Modell kennt genau eine FC-Version. Im Plan/Forecast-Prozess vergleiche ich aber FC Sep gegen FC Okt, und PY-Restatements kommen ebenfalls nicht vor. · Fix: kein Umbau vor dem 17.11. Ein Satz auf Folie 7 unter Rule 4 genügt: *„Forecast versions and restated PY are one more column or a version dimension in the fact; the visuals do not change.“* Damit ist die Frage aus dem Publikum vorweg beantwortet.

11. **Folie 10 (s10) und A1 (s13)** · Der Rechner bleibt für meine Budgetfrage zu theoretisch: „1,500 scenarios, P10–P90“, „3 of 58 assumptions verified“, ohne Power-BI-Pro/PPU-Lizenzen und Capacity und ohne meinen Stundensatz. · Fix: in den Live-Teil eine Zeile aufnehmen: *„Plug in your readers, authors and hourly rate; Power BI licences and capacity are the same for all rungs and left out on purpose.“* „3 of 58 verified“ von der Hauptfolie in die Fußzeile verschieben. Wenn Zeit ist, live einen Wert aus dem Publikum eintippen (Leserzahl).

12. **Reihenfolge Folien 3–8** · Die Reihenfolge Zeit → IBCS → GuV-Sonderfall → Modell → Leiter → Demo → Rechner → Ausblick ist für mich im Kern logisch. Die IBCS-Seite (Folie 5) kommt aber vor meinem Problem, der GuV, und kostet Aufmerksamkeit bei denen, die IBCS kennen. · Fix: Folie 6 (P&L) direkt hinter Folie 4 ziehen, Folie 5 auf 60 Sekunden kürzen („the notation has a name“) oder als Brücke hinter Folie 6 setzen. Der Bogen lautet dann: Was will ich sehen → warum die GuV schwer ist → Notation → Modell → Leiter.

**Zu theoretisch für Praktiker (Auswahl, mit Ersatz):**
- „Rules: in your head / in DAX / in the spec / inside the visual“ (Folie 8): gut gedacht, aber abstrakt. Ersatz: „**Who changes a row label on close day?** You / a DAX author / a Vega author / you, via template / nobody but the app dev.“
- „Agents write Vega well“, „Copilot builds it today“: Für mich zählt, ob *ich* es ändern kann, nicht ein Agent. Mit der neuen Spalte aus Befund 4 belegen.
- „35 h learning per template builder“, „Maintenance 12/30/48 % per year“, „Core +209 % at twenty models“: Ohne Bezugsgröße (wovon 12 %?) ist das nicht verwertbar. Entweder in Stunden je Jahr für 5 Seiten umrechnen oder in den Appendix.
- „Ten actual months against twelve plan months“ (Folie 7): richtig und wichtig, aber erst in der Demo verständlich. Dort zeigen: Page-Filter kurz entfernen, ΔPL springt.

## Tauglichkeit je Demo-Seite für den Monatsbericht

Bewertet ist die **Seite, wie sie heute im Demo-Report steht**, nicht das theoretische Potenzial des Stacks. „Kommentar“ meint einen Kommentar an der Abweichung (Konto × Gesellschaft × Monat), nicht den Service-Kommentar am Visual. „–“ = keine DWG-Seite vorhanden, nicht beurteilbar.

| Sprosse / Seite | Kommentar | Drill / Aufklappen | Export PPT/PDF | Filter / Slicer | Sortierung | Zwischen- und Gesamtsummen | Vorzeichen | Zahlenformat / Einheit | Datenstand | Monat · YTD · FY+FC | Selbst pflegbar ohne Entwickler |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Pure Power BI | nein | teilweise (Hierarchie möglich, nur L1 gebaut) | ja | ja | ja (Sortierspalte) | teilweise (nur „Total“, kein EBITDA) | ja | nein (volle EUR, „bn“ vs. „M“) | nein | nein (nur YTD) | ja |
| 2 DAX only | nein | teilweise | ja | ja | ja | teilweise | ja | nein | nein | nein | teilweise (Measures brauchen Modellrechte) |
| 3 SVG + UDF | nein | teilweise | teilweise (rastert, im Service testen) | ja | ja | teilweise | ja | nein | nein | nein | nein |
| 4 Deneb | nein | nein | ja (zertifiziert) | ja | teilweise (im Spec) | nein (keine GuV) | ja | teilweise (M/k, Labels überlappen) | nein | nein | nein |
| 5a Custom open: Group P&L + Plan gap | teilweise (statisch je Konto) | ja (Ebenen 1/2/3/Alle) | **nein** (nicht zertifiziert) | ja | ja (Dimensionsreihenfolge) | ja | ja | ja (kEUR/mEUR per Klick) | teilweise (Zeitraum im Titel, kein Refresh-Stempel) | teilweise (YTD gezeigt, FC/FY möglich, nicht gezeigt) | ja |
| 5b Custom paid (Zebra) | ja (laut Folie, nicht gezeigt) | ja | ja | ja | ja | ja | ja | ja | – | – | ja |
| 6 Fabric App | – | ja (Zoom, Small Multiples) | nein | ja | – | – | – | – | – | – | nein |

Lesart für den Vortrag: Heute besteht keine Sprosse alle elf Kriterien. 5a kommt am nächsten, scheitert aber am Export, also genau an dem Punkt, der für ein Board-Pack zählt. Diese ehrliche Lücke ist ein starker Satz für Folie 11.

## Was gut ist und bleiben soll

- **„The model answers the questions. The visuals only draw them.“** (Folie 7) und die vier Regeln, vor allem „empty not zero“ und „Full year is a scalar, MAX then SUM“. Das ist genau die Falle, in die jeder Controller schon gelaufen ist. Unbedingt behalten.
- **Das Vorzeichen-Trio** (SignConvention, DisplayInvert, VarianceInvert) und der Satz „One wrong and an overrun turns green“. Damit ist Praxis in einer Zeile gesagt.
- **ΔPL konsistent über alle Seiten** (+35,5 m Umsatz, −32,3 m Mobility FR, −14,2 m Rohertrag). Wo die Zahlen übereinstimmen, wirkt „One Model“. Die Szene aus Befund 1 baut darauf auf.
- **Plan-gap-Seite** mit Δ auf Basisskala und markiertem Miss bei Mobility FR. Das ist die Seite, die ich am Montag selbst haben will.
- **„Avoid when“** je Sprosse (A2–A8). Diese Zeilen sind entscheidungsfähig, mehr davon und weniger Prozentannahmen.
- **Der Yen-Satz** (A9): „grows in JPY and shrinks in EUR. Both statements are true.“ Er gehört in den Hauptteil, sobald das Modell ihn zeigen kann.
- **„Fast, and invisible to your auditors“** (Folie 12, Fabric Apps). Das ist die richtige Warnung, direkt an das Publikum gerichtet.
- **Offenlegung** (eigene Visuals, „prices unverified“, „Indication, not a quote“). Das schafft Vertrauen bei Finanzleuten.
