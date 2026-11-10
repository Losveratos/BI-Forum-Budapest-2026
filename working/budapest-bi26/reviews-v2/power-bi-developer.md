# Review Power BI Developer

Stand 09.11.2026. Grundlage: 23 Folienbilder, `story.html`, `BRIEF.md`, `REVIEWS.md`, Demo-README, TMDL von `PnL ChartkitchenDemoKit.SemanticModel` und PBIR von `Budapest BI Forum.Report` (nur gelesen). Fakten gegen Microsoft Learn und Herstellerseiten geprüft, Quellen am Ende.

## Drei Dinge, die vor dem Vortrag gefixt sein müssen

1. **Die Deneb-Seite rechnet bei den Gesellschaften 10 Monate Ist gegen 12 Monate Plan.** Seit dem 09.11., 02:30 bindet `r4companies` die Measure `Revenue AC&FC` = `IF(ISBLANK([Revenue AC]), [Revenue FC], [Revenue AC])`. Auf Gesellschaftsebene ist AC nie leer, also kommt nur Jan–Okt Ist, gegen `Revenue PL` über 12 Monate. Die Seite `4 Deneb` hat außerdem keinen Seitenfilter (die Sprossen 1–3 filtern MonatNr 1–10). Jede Gesellschaft liegt damit rund 15–17 % unter Plan und ist rot. Das ist genau die Falle, vor der Folie 7 warnt, und im Saal fällt es in Sekunden auf, sobald Rung 3 Mobility FR als einzigen Ausreißer zeigt. Fix: Measure monatsweise auswerten (DAX unter Befund 1), danach neuer Screenshot. A5 und das Vorschaubild auf Folie 9 zeigen noch die alte Spec vom 08.11.
2. **A6 zeigt eine falsche Rohertragsmarge, deutsche Zeilen und ein anderes Modell.** In `pnl-t04b-en.webp` steht PL-Marge 67,5 %, ΔPL −0,7 pp. Aus den Zahlen auf derselben Folie ergibt sich 12.137,75 / 18.056,00 = **67,2 %**, ΔPL also −0,4 pp. Das ist derselbe Fehler, den das Controller-Review am 7.11. auf Folie 6 gefunden hat. Er sitzt jetzt im Appendix und betrifft ausgerechnet das eigene Visual, dessen Stärke laut Folie 6 die Formelzeilen sind. Dazu kommen deutsche Zeilen (Fassbier, Umsatzerlöse), Jan–Sep und die Brauerei statt DWG Industries, obwohl der Titel „One Model“ verspricht. Fix: T04B mit P&L Statement 1.7 auf dem DWG-Modell in Englisch neu rendern (die Group-P&L-Seite rechnet richtig: 33,3 / 34,4 / 33,5 %).
3. **„+ UDF“ ist im Demo-Modell nicht möglich.** In `database.tmdl` steht `compatibilityLevel: 1606`, UDFs brauchen 1702. Im Modell gibt es keine einzige `function`. Sprosse 3 heißt auf Folie 8, 11 und A4 aber „SVG measures + UDF“, und A4 nennt „IBCS function packages on DaxLib“ ohne Namen (am 7.11. schon bemängelt, nicht umgesetzt). Fix: Modell auf 1702 heben, DaxLib.SVG (Jake Duddy) oder PowerofBI.IBCS installieren und `ΔPL SVG` durch einen Funktionsaufruf ersetzen. Das ist dann zugleich der stärkste Wartbarkeitsmoment der Demo. Wer das nicht mehr schafft, schreibt „SVG measures (UDF-ready)“ und sagt, dass das Modell auf 1606 steht.

## Befunde (priorisiert, max. 12)

**1 · Folie 9, A5 / Seite „4 Deneb“** · `Revenue AC&FC` ist nicht über Monate additiv, und die Seite hat keinen Zeitfilter. Darum vergleicht `r4companies` Teilzeitraum gegen Gesamtjahr, und die Zahlen widersprechen „Same P&L page, same numbers“ auf Folie 9.
Fix (DAX, `te set … -p expression=-`):
```dax
Revenue AC&FC =
SUMX (
    VALUES ( 'dim-datum'[Monatsende] ),
    VAR _Ac = [Revenue AC]
    RETURN IF ( ISBLANK ( _Ac ), [Revenue FC], _Ac )
)
```
`FC flag` auf Gesellschaftsebene ist immer 0. Beim Gesellschaften-Chart den Untertitel deshalb auf „AC Jan–Oct & FC Nov–Dec vs PL FY“ setzen. Im Monats-Chart heißt das Label „ΔPL % YTD“, kumuliert werden aber auch die FC-Monate: umbenennen in „ΔPL % cumulative (AC&FC)“. Titel und Untertitel der Spec sind fest kodiert („DWG Industries“, „2026“) und bleiben stehen, wenn live der Company-Slicer oder das Jahr wechselt. Entweder `Filterinfo` als Feld mitgeben und daraus den Titel bauen, oder den Titel aus der Spec entfernen und eine Textbox mit `Filterinfo` darüber setzen. Danach A5 neu aufnehmen (beide Visuals, nicht abgeschnitten) und README Rung 4 aktualisieren. `dBase`-Spec und „one layer“ stimmen nicht mehr.

**2 · A6** · Margenzeile falsch (67,5 statt 67,2 %), deutsch, falsches Modell (Details unter „Drei Dinge“ Nr. 2).
Fix: Bild ersetzen. Wenn die Zeit nicht reicht, kann vorerst die vorhandene, korrekte Group-P&L (`pbi3-group-pnl-statement.png`) mit Bildunterschrift „template T03A on the demo model“ einspringen. Im P&L-Statement-Repo prüfen, ob ältere Versionen Margen als Mittel der Monatsmargen statt als Quotient der Summen rechnen. Wer die alte Version im Einsatz hat, bekommt sonst die Frage im Q&A.

**3 · Folie 8, 11, A4 (Sprosse 3)** · UDF-Aussage ohne Beleg im Modell, DaxLib-Paket unbenannt (siehe „Drei Dinge“ Nr. 3).
Fix für A4, Plus-Zeile 1: „DAX user-defined functions GA since June 2026 (compatibility level 1702); SVG and IBCS packages on daxlib.org: DaxLib.SVG, PowerofBI.IBCS“. Minus-Zeile ergänzen: „UDFs: no display folders, no translations, no inherited OLS“. Die Einschränkung „Cannot combine UDFs with translations“ steht auf Learn und trifft jedes Finance-Modell mit DE/EN-Captions. Das Demo-Modell hat zwar `cultures`, aber leer, ist also nicht betroffen.
Quelle: Microsoft Learn, DAX user-defined functions (Considerations and limitations; „compatibility level 1702 … GA … June 2026“).

**4 · Folie 4, A2–A4, Live-Demo** · Das Modell hat `culture: de-DE`. Der englische Vortrag zeigt deshalb „2.817.623.779“, „−1.874.847.799“ und „Σ 2.818M“. Für dieses Publikum liest sich „2.818M“ als 2,8 Millionen. In derselben Matrix zeigt das SVG-Label „+35.5“ (en-US), daneben steht „+35.517.892“ (de-DE).
Fix: In `model.tmdl` `culture: en-US` setzen und Desktop neu starten (bei Modellen mit `cultures` gibt es kein Hot-Reload). Die Format Strings der Budapest-Measures auf Millionen umstellen: `AC signed`/`PY signed`/`PL signed` mit `#,0.0,,;-#,0.0,,;-`, `ΔPL`/`ΔPY` mit `+#,0.0,,;-#,0.0,,;-`, Spaltenköpfe „AC EUR m“ usw. Danach alle Rung-Screenshots neu aufnehmen. Dabei ist die Zahlenformatierung nach dem Wechsel der Anwendungssprache noch de-DE, das sagt das README selbst.

**5 · Folie 7, A11** · Das Deck widerspricht sich bei Zeitintelligenz, und die eigene Regel wird per Klick gepflegt. Folie 7 und A11 Karte 1 sagen „no time intelligence in the model … the visual cuts month, YTD and FY“, die Fußzeile von A11 sagt „time intelligence … stay in the model“. Für die Sprossen 1–4 stimmt beides nicht, dort schneidet ein **hart kodierter Seitenfilter MonatNr 1–10** auf drei Seiten (auf der vierten fehlt er). Im Novemberabschluss muss jemand drei Seitenfilter von Hand ändern, also „rules in your head“.
Fix 1, neue Fußzeile A11: „Currency translation and security stay in the model. Time windows: the custom visual cuts them itself; on rungs 1–4 one model flag does it.“
Fix 2, eine berechnete Spalte statt drei Seitenfiltern:
```dax
'dim-datum'[Actual closed] =
'dim-datum'[Datum]
    <= MAXX (
        FILTER ( ALL ( 'fact-abschluss' ), NOT ISBLANK ( 'fact-abschluss'[AC Wert] ) ),
        'fact-abschluss'[Datum]
    )
```
Seitenfilter auf allen Rung-Seiten wird `Actual closed = TRUE`, mit `pbir add filter` setzen. Folie 7, Fußzeile neu: „Trap every rung inherits: ten actual months against twelve plan months. One flag in the date table prevents it.“

**6 · Folie 8, 11, A5 (Sprosse 4)** · Drei Fakten stimmen so nicht.
a) Unter „Deneb (Vega) · HTML: Microsoft-certified visuals“ ist **HTML Content nicht zertifiziert**, zertifiziert ist nur „HTML Content (lite)“ ohne externe URLs. Fix Folie 8: „Deneb and HTML Content (lite) are Microsoft-certified; full HTML Content is not.“
b) „Deneb 2.0 changes the template format“ erzeugt unnötig Angst. v2 ist ein eigenes, zertifiziertes Visual mit neuer AppSource-ID, v1 bleibt „indefinitely“ zertifiziert, bestehende Berichte laufen weiter, und migriert wird über Export als v1-Template und Import in v2. Fix A5 Minus: „Deneb 2.0 is a separate certified visual; v1 stays certified, migration via template export/import“. In Matrix-Zelle 4 / Maintainability „2.0 format change“ ersetzen durch „v2 = new visual, opt-in“.
c) Die Vega-Ankündigung fehlt im Deck ganz. Laut Autor ist gesichert, dass Microsoft auf der FabCon Vega nativ für Power BI angekündigt hat. Das ändert Sprosse 4 vom „Community-Visual“ zur Richtung, in die Microsoft selbst geht, und sollte deshalb drinstehen. Ich habe dazu **keine öffentliche Microsoft-Quelle gefunden** (Learn, Power-BI-Blog). Belegbar ist nur, dass Fabric-Apps-Data-Apps Vega-Lite als empfohlenen Chart-Pfad nutzen, mit Cross-Highlighting für Microsofts eigene Vega-Lite-Visuals (Tabular Editor, „Fabric Apps explained“). Fix: auf Folie 8, Sprosse 4 eine Zeile mit genauer Quelle: „Microsoft announced native Vega(-Lite) for Power BI at FabCon <Ort, Session-Code>; no date yet. Specs written today stay portable.“ Ohne Session-Code oder Link lieber mündlich sagen und nicht auf die Folie.
Quellen: AppSource-Listings HTML Content / HTML Content (lite); deneb.guide Annual Round-Up; tabulareditor.com „Fabric Apps explained“.

**7 · A2, Folie 8, Folie 11 (Sprosse 1)** · Zwei Fakten falsch oder unvollständig.
a) „legacy card and Q&A retire 02/2027“: Nur Q&A geht im Februar 2027. Die Legacy-Card bleibt „for backward compatibility … continue to render without changes“. Fix A2 Minus: „Deprecation is not zero: Q&A goes away in February 2027.“
b) „Copilot builds and edits it today“ stimmt, aber nur mit bezahlter Kapazität F2+/P1+ oder einer Fabric Copilot capacity, nicht auf Trial, nicht in Sovereign Clouds. Fix Folie 11, Sprosse 1, Self-service: „Copilot builds it (F2+/P1+)“. Folie 8: „Copilot can build and edit it today (paid capacity)“.
c) Weiter unbelegt seit 7.11.: „SVG … can come up blank in the Service; card regressions in 2025“ (A4). Entweder Community-Thread oder Known-Issue-ID dazuschreiben oder auf „test every SVG measure in the Service before release“ kürzen.
Quellen: Learn „Use Power BI Q&A“ (Feb 2027), Learn „Create a card visual“ (Legacy single/multi card), Learn „Copilot for Power BI overview“ (Requirements).

**8 · Folie 10, 11, A7 (Sprosse 5b)** · Preisanker und Zebra-Aussagen halten den Herstellerseiten nicht stand.
Zebra BI listet für Power BI **keinen Free-Plan**, nur eine 14-Tage-Testversion. Die Single-User-Gratisversion gilt für Zebra BI for Office. Die Bildunterschrift „Zebra BI ships a free tier for Power BI“ ist deshalb falsch. Listenpreise laut zebrabi.com: Starter €696/Jahr für bis zu 10 Nutzer (erstes Jahr €504), Business €3.240/Jahr für bis zu 50, das sind **rund €65–70 je Nutzer und Jahr** und nicht 170. Inforiver listet $5–10 je Nutzer und Monat. Das IBCS-Zertifikat im Lumel-Umfeld steht auf ibcs.com für „Lumel EPM“ (08/2025). Nicht jedes Inforiver-Visual ist automatisch gemeint.
Fix A7 Bildunterschrift: „Zebra BI for Power BI: 14-day trial, then team plans (list: about €65–70 per user and year at 10–50 users).“ A7 Fußzeile: „prices from vendor pages, 11/2026; quotes differ“. Folie 10: „Licence anchor 33, 80 or 170 EUR“ entweder gegen die Listenpreise neu setzen oder mit „anchors include support, add-ons and enterprise tiers“ erklären. Matrix 5b „tips at 176 readers“ nach dem neuen Anker neu rechnen.
Quellen: zebrabi.com/pricing, inforiver.com/pricing, ibcs.com (Lumel EPM).

**9 · Folie 8, 11, 12, A8 (Sprosse 6)** · Die Fabric-Apps-Zeile lässt die Governance-Fakten weg, die Controller und Admins zuerst fragen.
Für Data Apps braucht jeder Leser **Build- und Read-Recht auf das Semantic Model**, nicht nur Read wie beim Bericht, dazu die Tenant-Settings „Fabric apps (preview)“ und „Semantic Model Execute Queries REST API“. Fabric Apps ist Preview, regional eingeschränkt und steht nicht in der Learn-Liste der Git-unterstützten Items. Laut FabCon-Barcelona-Recap (Tabular Editor) sollen Pro/PPU Fabric Apps abdecken. Damit wäre „capacity“ als Kostenargument bald überholt.
Fix Matrix, Zeile 6: Export & audit „readers need Build on the model“. Cost: „capacity today; Pro/PPU announced“. Folie 8: „Preview. Thin capacity“ ersetzen durch „Preview, some regions, readers need Build permission, no Git sync yet“. A8 Minus, eine Zeile ergänzen: „Every reader needs Build permission on the semantic model“.
Quellen: Learn „What is Fabric Apps (Preview)?“, Learn „Create an app connected to a semantic model“ (Prerequisites), Learn „Git integration – supported items“, tabulareditor.com FabCon Barcelona 2026 Recap.

**10 · Folie 9, 11, Abstract** · Die Performance-Bewertung ist nicht gemessen, und das Demo-Modell ist zu klein, um sie zu zeigen.
`fact-abschluss` hat 63.936 Zeilen. Der Abstract verspricht „real data volumes“. Folie 9 verspricht Performance Analyzer live, „who is still fast?“. Bei 64k Zeilen kommen alle Sprossen unter 100 ms DAX zurück, und Sprosse 3 steht in der Matrix trotzdem auf ●○○ („CU unmeasured“). Die Live-Zahlen widersprechen also der eigenen Tabelle.
Fix: (a) Generator mit Skalierungsfaktor laufen lassen (z. B. 50 Gesellschaften × Kostenstellen, 10–20 Mio. Zeilen), als zweites Modell `…_large`, und je Seite einmal kalt und warm messen (DAX Studio Server Timings: SE/FE getrennt), Zahlen in die Matrix. (b) Wenn das nicht mehr geht, Folie 9 auf „Performance Analyzer on screen: render time per stack; the model is small on purpose, DAX time is not the differentiator here“ ändern und Sprosse 3 Performance auf ●●○ „string building per cell, measure before scaling“.
DAX-Muster, das ein Entwickler im Publikum anspricht: Alle `* signed`-Measures und `Revenue/EBITDA *` iterieren mit `SUMX ( 'fact-abschluss', … * RELATED ( … ) )` über die Faktentabelle. Bei echten Volumen ist das Formula-Engine-Last. Besser über die zwei Vorzeichenwerte iterieren:
```dax
AC signed =
CALCULATE (
    SUMX ( VALUES ( 'dim-konten'[SignConvention] ), 'dim-konten'[SignConvention] * [AC] ),
    KEEPFILTERS ( 'dim-konten'[RowType] = "account" )
)
```

**11 · A11, Modell-Hygiene** · Einige Stellen im Modell würde ein Entwickler im Publikum kommentieren.
- `EBITDA AC/PY/PL/FC` filtern eine hart kodierte Liste englischer `L1 EN`-Texte, obwohl `dim-konten[FormulaDef EN]` die Formel schon kennt. Die Regel steht damit zweimal im Modell, und eine Umbenennung in der Kontendimension bricht EBITDA still. Fix: Flag-Spalte `'dim-konten'[In EBITDA]` (aus FormulaDef oder im Generator) und `KEEPFILTERS ( 'dim-konten'[In EBITDA] )`. Dasselbe gilt für `Revenue *` mit `"Net revenue"`: auf einen Schlüssel filtern (L1 Sort oder Kontonummer), nicht auf den Anzeigetext.
- Die `///`-Beschreibung von `ΔPL SVG` steht vor `Revenue AC&FC`. Die Measure hat dadurch zwei Beschreibungen, `ΔPL SVG` hat keine. Mit `te set "fact-abschluss/ΔPL SVG" -p "description=…"` nachziehen, `te validate`.
- `Revenue sparkline (text)`: `ROUND(…*7,0)` liefert 0–7, `MAX(_I,1)` macht aus 0 und 1 dasselbe Zeichen, und „█“ (Position 8) wird nie erreicht. Fix: `MID ( "▁▂▃▄▅▆▇█", ROUND ( DIVIDE ( _V, _Max ) * 7, 0 ) + 1, 1 )`.
- Die Farben der Sprossen 1–3 (`#3F8F3F` grün) und von ChartKitchen (teal) unterscheiden sich, obwohl Folie 5 teal als dokumentierte Günstig-Farbe nennt. Für „same notation“ in `ΔPL status` und den SVG-Measures dasselbe Teal verwenden.
- Export & audit (Folie 11, Sprossen 2 und 3): „Export data“ nach Excel liefert für SVG- und Unicode-Spalten Data-URI- bzw. Blockzeichen-Strings. Das fragt jeder Controller. In die Zelle schreiben: „Excel export carries the SVG text, not the bar“.
- FC FY / PL FY (A11 Karte 3): Zu erwarten ist die Frage, warum der Jahreswert auf jeder Monatszeile steht und nicht in einer Tabelle auf Jahresebene. Antwort vorbereiten (z. B. „the visual needs FY on the month grain; a year-grain fact would be cleaner for other consumers“).

**12 · Folie 8 (Leiter), Lücken** · Drei Optionen, nach denen ein Finance-Publikum fragt, fehlen weiterhin: Paginated Reports (Abschlusspaket, PDF, Abos, Report Builder), Excel live am Semantic Model (Analyze in Excel, Cube-Formeln: der echte Arbeitsplatz vieler Controller) und Visual Calculations. Letztere stehen auf Folie 8 in Sprosse 1, kommen in der Demo aber nicht vor.
Fix: Fußzeile Folie 8 ergänzen: „Not on the ladder, same model underneath: paginated reports for the close pack, Excel connected to the model for controllers.“ Auf Seite „1 Pure Power BI“ ΔPL % als Visual Calculation statt Measure zeigen (`ΔPL % = DIVIDE([AC signed]-[PL signed], ABS([PL signed]))`). Das kostet 30 Sekunden und belegt die Aussage.

## Was gut ist und bleiben soll

- **Eine Seite je Sprosse, gleiches Layout, gleiche Slicer.** Das ist die richtige Versuchsanordnung, sie macht den Vergleich ehrlich und live zeigbar.
- **Sign trio und `* signed`-Measures** trennen Vorzeichenlogik sauber von der Darstellung. `ΔPL` mit „positiv = gut“ und das Format `+#,##0;-#,##0;-` sind genau, was Core-Visuals brauchen.
- **`ALLSELECTED('dim-konten'[L1 EN], 'dim-konten'[L1 Sort])`** fürs Skalieren, **`FORMAT(x,"0.0","en-US")`** in SVG-Koordinaten und **`%23` statt `#`** zeigen gelöste Praxisprobleme. Ein Satz dazu in der Demo bringt Glaubwürdigkeit bei den Entwicklern.
- **`AC LW` mit `HASONEVALUE` auf Währung** (blank statt sinnloser Summe) und Regel 1 „empty not zero“ sind starke, kurze Modellregeln.
- **Umsetzung der 7.11.-Reviews ist größtenteils gelungen:** IntelliSense-Aussage gestrichen, Org-Store-Hinweis korrekt (Learn bestätigt: Org-Visuals ohne PPT-Export und Abos, zudem nicht in Report Server), Report Server mit Herstellerschlüssel, „Microsoft-certified“ und „IBCS-certified“ getrennt, Leiter umbenannt, Matrix mit Bewertung und Avoid-when, Plan-gap-Kacheln auf Basisskala (Folie 4: +22,1 M zu 245 M = 9,0 % rechnet). Q&A 02/2027, UDF-GA 06/2026 und „no display folders, no inherited OLS“ sind gegen Learn korrekt.
- **Folie 11 als Abschlussthese** und „Nothing in this table always wins“: bleiben.
- **A10 mit Generator, fixem Seed und reconciliation.txt**: Das beantwortet die Frage „sind die Zahlen echt?“, bevor sie gestellt wird.

## Demo-Empfehlung (Ablauf in Minuten)

Annahme 40 Minuten: Folien 1–8 in 13 Minuten, Demo 15 Minuten, Folien 10–12 in 7 Minuten, 5 Minuten Fragen. Desktop läuft schon, alle Seiten wurden vorher zweimal geöffnet (warm), Deneb ist geladen, „Apply external changes“ ist erledigt, Performance Analyzer ist geöffnet und geleert, Zoom 125 %, ein Lesezeichen „Reset slicers“ ist angelegt.

| Min | Seite | Live zeigen | Vorab erledigt |
|---|---|---|---|
| 0:00–1:00 | Plan gap (Sprosse 5) | Definition of Done ansagen: PL-Umriss, FC-Schraffur, ΔPL auf Basisskala, Vorzeichen-Trio, YTD/FY. Die vier Rung-Seiten werden daran gemessen | – |
| 1:00–2:30 | 1 Pure Power BI | Matrix, rot/grün, keine Umrisse. ΔPL % als Visual Calculation in 30 s anlegen (Befund 12) | Measures in EUR m (Befund 4) |
| 2:30–3:30 | 2 DAX only | Unicode-Balken; Schrift kurz auf proportional umstellen, Balken zerfallen, zurück | – |
| 3:30–6:00 | 3 SVG + UDF | Matrix zeigen, dann TMDL-Ansicht: `ΔPL SVG` vor und nach dem UDF-Aufruf (20 Zeilen → 1 Zeile). Farbe in der Funktion ändern, beide SVG-Spalten ändern sich mit | Modell auf 1702, DaxLib-Paket installiert (Befund 3) |
| 6:00–9:00 | 4 Deneb | Monats-Chart mit FC-Schraffur, dann Gesellschaften. Editor öffnen, eine Zahl in der Spec ändern (Balkenbreite), Apply. Satz: „this is text in Git“ | Measure-Fix (Befund 1), Titel dynamisch |
| 9:00–11:30 | Group P&L (Sprosse 5a) | Vorlage T03A → T04B wechseln, Ebene 2 → 3. Gesellschaft Mobility FR wählen: auf allen Seiten dieselbe −32 M | – |
| 11:30–13:00 | Performance Analyzer | Eine Seite je Stack refreshen, DAX-Zeit gegen Visual-Display-Zeit vorlesen. Ehrlich sagen: „small model, render time is the difference“ | Werte vorher einmal notiert, als Spickzettel |
| 13:00–15:00 | Rechner | Finance-Preset per Link öffnen, Leserzahl 150 → 400 ziehen, der Gewinner kippt | Share-Link mit Preset als Lesezeichen |

Nicht live: Fabric App (Netz, Kapazität, Login; Screenshot A8 reicht), Copilot (Kapazität, Latenz, nicht deterministisch), Zebra BI (kein Modell-Seite vorhanden; A7 als Bild).

Bei 60 Minuten zusätzlich: Monatsabschluss-Szene (eine Buchung im CSV ändern, Refresh, alle Seiten zeigen neues EBITDA, 4 Min.), Fabric App live (3 Min.), Zebra-Seite auf dem DWG-Modell, falls bis dahin gebaut (3 Min.).

**Live-Risiken und Gegenmaßnahmen**
- **Deneb kommt aus AppSource** und braucht beim ersten Laden Netz. Hotel-WLAN ist kein Plan. Report am Vortag und am Morgen öffnen. Für den Notfall eine Kopie des Reports mit Deneb als importierter `.pbiviz` (privates Visual) auf dem Laptop.
- **Desktop hält das Modell im Speicher.** Nach dem Culture-Wechsel (Befund 4) ist ein Neustart Pflicht. Nach dem letzten `te`/`pbir`-Eingriff Desktop schließen, öffnen und alle Seiten durchklicken. Nicht aus Desktop speichern, solange externe Änderungen offen sind.
- **Slicer-Zustand:** Ein vergessener Company-Filter aus der Probe verfälscht jede Seite. Vor dem Start „Reset slicers“ auslösen.
- **Performance Analyzer** zeigt beim ersten Refresh Kaltwerte. Jede Seite einmal vorher refreshen und die Messung beim zweiten Mal vorlesen.
- **Backup:** Bildschirmaufnahme des kompletten Demo-Ablaufs (15 Min.) lokal, in der Präsentation per Taste erreichbar. Folie 9 verspricht „Nothing prerecorded“: den Satz streichen, dann steht keine Zusage im Raum, die im Notfall bricht.

## Quellen

- Microsoft Learn, DAX user-defined functions (GA Juni 2026, Kompatibilitätslevel 1702, Limitations inkl. Translations/Display Folders/OLS): https://learn.microsoft.com/dax/best-practices/dax-user-defined-functions
- Microsoft Learn, Q&A geht im Februar 2027: https://learn.microsoft.com/power-bi/natural-language/power-bi-tutorial-q-and-a
- Microsoft Learn, Card visual (Legacy-Card bleibt verfügbar): https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-card
- Microsoft Learn, Copilot Requirements (F2+/P1+, kein Trial, keine Sovereign Clouds) und „Create and edit reports with Copilot“: https://learn.microsoft.com/power-bi/create-reports/copilot-introduction · https://learn.microsoft.com/power-bi/create-reports/copilot-create-reports
- Microsoft Learn, Organizational visuals (kein PPT-Export, keine Abos, nicht in Report Server): https://learn.microsoft.com/power-bi/developer/visuals/power-bi-custom-visuals-organization
- Microsoft Learn, Fabric Apps (Preview, Regionen) und Data-App-Template (Build + Read, Execute-Queries-Tenant-Setting): https://learn.microsoft.com/fabric/apps/overview · https://learn.microsoft.com/fabric/apps/data-apps-template
- Microsoft Learn, Git integration supported items (Fabric Apps nicht gelistet): https://learn.microsoft.com/fabric/cicd/git-integration/intro-to-git-integration
- Deneb v2 (separates Visual, v1 bleibt zertifiziert, Migration per Template): https://deneb.guide/blog/2024-2025-summary
- HTML Content (lite) zertifiziert, HTML Content nicht: https://appsource.microsoft.com/en-us/product/power-bi-visuals/coacervolimited1596856650797.htmlcontent_certified
- Fabric Apps und Vega-Lite, FabCon-Barcelona-Recap (Pro/PPU): https://tabulareditor.com/blog/fabric-apps-explained-visualization-as-code-in-a-data-app-dashboard · https://tabulareditor.com/blog/fabcon-barcelona-2026-recap
- DaxLib.SVG / PowerofBI.IBCS: https://evaluationcontext.github.io/daxlib.svg · https://www.sqlbi.com/blog/marco/2025/12/12/introducing-dax-lib-the-app-store-for-dax-user-defined-functions/
- Zebra BI Preise und IBCS-Zertifikat: https://zebrabi.com/pricing/ · Inforiver: https://inforiver.com/pricing · Lumel EPM IBCS-zertifiziert: https://www.ibcs.com/?p=73528
- Nicht gefunden: eine öffentliche Microsoft-Quelle zu „Vega nativ in Power BI“ (Suche in Learn, Power-BI-Blog und Feature Summaries März–Okt 2026, Stand 09.11.).
