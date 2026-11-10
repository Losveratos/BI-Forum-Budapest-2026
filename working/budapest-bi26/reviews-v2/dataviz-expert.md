# Review Data-Viz-Experte

Stand 09.11.2026 · Grundlage: s01–s23 (1920×1080), `story.html` (CSS), die vier Demo-Seiten in `assets/`, BRIEF.md und REVIEWS.md vom 7.11.
Folien-Nummern hier = Bildnummern s01–s23 (der Rechner ist jetzt Folie 10, die Matrix Folie 11).

**Messannahme für „letzte Reihe":** Leinwand 4–5 m breit, letzte Reihe 15 m. Dann ist 1 px etwa 2,3 mm. Daraus folgen diese Mindestgrößen: Fließtext ≥ 28 px, Sekundärtext ≥ 22 px, Fußzeile und Quellen ≥ 18 px. Beschriftung **in** Screenshots braucht effektiv ≥ 16 px auf der Folie. Alles unter 12 px ist von hinten Textur, kein Text.

## Drei Dinge, die vor dem Vortrag gefixt sein müssen

1. **Die Renders auf Folie 4 und 5 sind inhaltlich jetzt richtig, aber zu klein.** Die Basisskala stimmt und der Text ist englisch. Weil das Bild hochkant mit `object-fit:contain` in eine 820 px breite Karte gesetzt wird, belegt es nur ~420 × 500 px. Monatsnamen und Werte landen bei **8–9 px**, auf Folie 5 bei **5–6 px**. Der Fix „Folienbreite, Labels ab 16 px" aus dem Review vom 7.11. ist damit nicht erreicht. → Zeit-Render im **Querformat** neu aufnehmen (Visual in Desktop auf 1600 × 700 ziehen, `--scale 2`). Auf Folie 4 die zwei Charts **untereinander** statt nebeneinander setzen oder je Chart eine Folie. Auf Folie 5 die Bilder streichen (siehe Befund 3).
2. **Das Ende verpufft.** Die Matrix (Folie 11) trägt die These und ist der stärkste Abschluss. Danach kommt Fabric Apps (Folie 12) mit „Thank you · questions?" als 20-px-Fußzeile, und der Saal geht mit einem Ausblick statt mit der Botschaft. → Fabric Apps vor die Matrix oder in den Appendix (A8 existiert schon). Danach eine **Schlussfolie**: Thesensatz 64 px, QR zum Repo 300 px, „Thank you" groß.
3. **Die Matrix ist von hinten nicht lesbar und doppelt kodiert.** 56 Zellen, Begründungen in 16 px `#475569`, Punkte als Glyphen (22 px Schrift, ~11 px Durchmesser). Teal und Rot sind im Deck die IBCS-Farben für *günstig/ungünstig*, hier bedeuten sie *Bewertung*. Grau gegen Teal fällt im Validator durch: Normalsicht-ΔE 12,6 (< 15), Kontrast 2,98:1. → Punkte einfarbig in `--ink`, 18 px gefüllte Kreise per CSS statt Glyphen. Nur K.-o.-Zellen bekommen eine rote Umrandung mit Wort („knock-out"). `table.sc small` auf 18 px, Spalte „Avoid when" in die Sprecher-Notizen verschieben. So gewinnt die Tabelle ~190 px Breite für die anderen Spalten.

## Befunde (priorisiert, max. 12)

1. **Folie 4 / 5** · Die Labels in den ChartKitchen-Renders sind 5–9 px groß (siehe oben). · Querformat-Render; auf Folie 4 `.cols.c2` → `grid-template-columns:1fr` oder je Chart eine eigene Folie; Bildunterschrift (`.cap`) auf eine Zeile kürzen, damit das Bild Höhe bekommt.

2. **Folie 11 (Matrix)** · Bewertungsfarben kollidieren mit der IBCS-Semantik, die Punkte sind zu klein, und der Titel braucht drei Zeilen (232 px Höhe), weil `h2.t{max-width:26ch}` greift. · Punkte als `<span class=dot>` mit `width:18px;height:18px;border-radius:50%`, gefüllt in `--ink` und leer mit 2 px Rand. Titel auf zwei Zeilen: „Rules in the model. Rung by who pays and maintains." oder für diese Folie `max-width:34ch`. Lead-Zeile „Draft ratings, confirmed by demo and calculator" widerspricht sich (Entwurf *oder* bestätigt) → „Ratings from calculator, demo and four reviews".

3. **Folie 5** · Zeigt dieselben zwei Renders wie Folie 4, nur noch kleiner (≈ 330 px breit). Der Saal sieht die Doppelung und keine neue Information. · Untere Hälfte streichen. Dafür die Legendenzeile auf 28 px und 44 × 28 px Swatches vergrößern und die SUCCESS-Karten auf zwei Zeilen à 4/3 mit 24-px-Text setzen. Oder die Legende als Overlay direkt auf Folie 4 legen und Folie 5 auf die SUCCESS-Karten beschränken.

4. **Folie 6** · Der P&L-Screenshot zeigt Text in 6–8 px, die **deutsche** Visual-Toolbar („ANSICHT", „EINHEIT", „DICHTE", „Nullzeilen aus", „Balken", „Baum"), einen Desktop-Scrollbalken rechts und abgeschnittene untere Zeilen. · Neu aufnehmen mit ausgeblendeter Toolbar, nur Kopf plus „Product revenue" bis „Gross profit" (≈ 15 Zeilen) bei `--scale 3`, zugeschnitten auf 900 × 560. Ziel: Zahlen ≥ 16 px auf der Folie.

5. **Folie 10 (Rechner)** · Das Chart ist ein Screenshot mit 13–14-px-Achsen und -Untertiteln („Flexible · off the shelf"). Es führt vier neue Kategoriefarben ein (Lachs, Mint, Blau, Gelb), die mit nichts im Deck korrespondieren. „Paid" in Lachsrot liest sich wie „ungünstig". · Chart als SVG im Deck nachzeichnen: vier Zeilen, P10–P90-Band in `--py`, P50-Strich in `--ink`, Werte 28 px direkt am Band, Achse 20 px. Ohne Farbe pro Ansatz, die Zeile trägt die Identität. Rund 120 px Leerraum unter der Achse wegnehmen (`object-position:center` → `top`).

6. **Zwei Zähler je Folie (wie am 7.11. bemängelt, nicht umgesetzt)** · `.crumb` oben rechts („slide 2 of 3", 20 px) plus `#hud` unten rechts („4 / 23", 16 px, `#777` → 4,3:1). Dazu kommt die Kapitelleiste. · `#hud{display:none}` im Vortragsmodus (Taste H zum Einblenden). Crumb behalten, aber nur das Kapitel ohne „slide x of y": die Kapitelleiste zeigt den Fortschritt schon.

7. **Folie 8 (Leiter) und der Titel „Three Visual Stacks"** · Die Zuordnung sechs Sprossen → drei Stacks steht erst auf Folie 11 als Nebensatz. Auf Folie 8 sucht der Saal die „drei". Pro Karte stehen 40–60 Wörter in 23 px Grau. · Über den Karten eine Klammerzeile mit 24 px, fett, in Akzentfarbe: „Stack 1 · Core + SVG" über 1–3, „Stack 2 · Deneb" über 4, „Stack 3 · Custom visual" über 5, „Host" über 6. Kartentext auf zwei Sätze kürzen (`.rung p` 26 px); die Details liegen ohnehin im Appendix A2–A8. Unten sind 120 px frei, Platz genug.

8. **Demo-Seiten Sprosse 1–3** · Die Tabellen belegen 35–45 % der Kartenhöhe, darunter liegen ~550 px leere weiße Fläche. Zahlen stehen mit vollen Euro-Stellen und de-DE-Trennzeichen („2.817.623.779", „0,1bn") auf einer englischen Seite. · Format `#,0.0,,"M"` in **en-US** (Modellkultur oder Format-String), dann bleiben 5 statt 13 Zeichen. Schrift der Matrix auf 14 pt (Desktop), Zeilenabstand `rowPadding` 6. Die Karte auf Tabellenhöhe kürzen und darunter das zweite Visual oder einen „data as of"-Stempel setzen. Die Slicer-Spalte (280 px, 5 × „All") als eine Kopfzeile oben quer anlegen, dann gewinnen die Visuals 300 px Breite.

9. **Demo-Seite Sprosse 1** · Die Data Bars im ΔPL-Feld liegen **über** den Zahlen („+35.51▇7.892", „−49.74▇3.361"), die Werte sind nicht lesbar. · Data Bars nur in einer eigenen Spalte („ΔPL bar") oder „Show bar only" verwenden, die Zahl in eine eigene Spalte.

10. **Demo-Seiten: Farbe für „günstig" uneinheitlich** · Sprosse 1 und ChartKitchen nutzen Teal (`#2E8B7A`), Sprosse 2–4 ein Grün (`#3F8F3F`-artig). Folie 5 sagt ausdrücklich „teal as the documented favourable colour". Der Vergleich „dasselbe Dashboard, vier Stacks" verliert so an Glaubwürdigkeit. · In DAX-Statusmeasure, SVG-Measure und Deneb-Spec dieselbe Hex `#2E8B7A` setzen (Deneb: `pbiColor` aus dem Theme oder Konstante im `config`).

11. **Demo-Seite Sprosse 4 (Deneb)** · Die ΔPL-Monatsbalken sind auf Basisskala 2–5 px hoch, also ehrlich, aber von hinten unsichtbar. Labels haben 9 px. „371M" sitzt im PL-Umriss, „+30M"/„+33M" überlagern die Balken. Die Firmen sind anders sortiert als auf Sprosse 1–3 (Industries US an Position 7 statt 3). · Firmenachse wie auf den anderen Seiten nach AC absteigend sortieren (`sort: {field: "AC", order: "descending"}`). Labels mit `dy` aus den Marks herausziehen, `fontSize` 12 im Visual. Zweites Δ-Panel „×5" mit Skalenband, wie es Folie 5 selbst erlaubt („or a marked factor").

12. **Appendix-Crops** · A5 (s17) schneidet das Firmen-Chart nach der Überschrift ab, darunter sind ~220 px leer. A4 (s16) kündigt „AC columns with PL outline" an, der Ausschnitt zeigt sie nicht. A1 (s13) zeigt denselben Text zweimal (Screenshot links, Karte rechts), links bleiben ~250 px leer. A8 (s20) zeigt eine deutsche App-Oberfläche in 7 px. · A5 mit `assets/demo-rung4-deneb.png`, Ausschnitt x 340–1940 / y 130–1040. A4 auf beide Visuals zuschneiden (x 340–1940, y 130–640). Auf A1 den Screenshot streichen und die Karte über die volle Breite setzen. Auf A8 eine englische App-Ansicht verwenden oder die Bildunterschrift mit dem Hinweis „German UI" versehen.

## Folie für Folie

| Nr | Note | Problem |
|---|---|---|
| 1 Cover | 1 | – |
| 2 Speaker | 1 | – |
| 3 What we want to see | 2 | Zahlenbruch (262 vs. 245 Mio. im Render, besser die Demo-Zahlen); Aufbauschritte 2–4 nicht als Bild geprüft |
| 4 Time and structure | 4 | Labelgröße |
| 5 IBCS on one page | 3 | Doppelung |
| 6 P&L structure with rules | 4 | Screenshot |
| 7 Model | 2 | Überlauf („168" ragt aus FactRates-Box, x≈995) |
| 8 Ladder | 3 | Stack-Zuordnung |
| 9 Demo | 2 | Thumbnails (238 px, nur Dekor) |
| 10 Calculator | 3 | Fremdpalette |
| 11 Matrix | 3 | Dichte |
| 12 Fabric Apps | 3 | Reihenfolge |
| 13 A1 | 4 | Doppelung |
| 14 A2 | 3 | Mini-Screenshot |
| 15 A3 | 2 | Leerfläche |
| 16 A4 | 3 | Zuschnitt |
| 17 A5 | 4 | Zuschnitt |
| 18 A6 | 1 | – |
| 19 A7 | 3 | Auflösung |
| 20 A8 | 3 | Sprache |
| 21 A9 | 1 | – |
| 22 A10 | 2 | Textmenge |
| 23 A11 | 2 | Code 17 px |

Demo-Seiten als Visualisierung: Sprosse 1 **3** (überlagerte Data Bars, volle Euro), Sprosse 2 **3** (55 % leer; die gebrochene Digital-JP-Sparkline ist aber ein guter Demo-Moment für „fragile"), Sprosse 3 **3** (Mini-Säulen ohne Vergleich zwischen Firmen, Digital JP rechtsbündig verschoben, Δ-Labels 7 px), Sprosse 4 **2** (bestes Layout, Sortierung und Labels nachziehen).

## Was gut ist und bleiben soll

- **Statement-Titel durchgehend.** Fast jede Folie sagt ihre These als Überschrift („Every rung works. Each one pays differently.", „The model answers the questions. The visuals only draw them."). Das ist die Dramaturgie, die trägt.
- **Folie 3 als Aufbau in vier Schritten** bleibt das beste Chart im Deck: dünne Säulen, direkte Werte in 19 px, aktive Karte mit Akzentkante und ausgegraute nächste Schritte. Statement-first und Fragment-Reveal passen hier genau.
- **Die Basisskala ist umgesetzt.** Die Renders auf 4/5 und Deneb A5 zeigen Δ maßstabsgetreu, und die Bildunterschrift rechnet es vor („+22 M is exactly nine percent of the 245 M column"). Das hat der Saal so noch selten gesehen. Es fehlt nur die Größe.
- **Matrix als bewertete Tabelle mit „Avoid when"** statt 28 Prosa-Zellen: richtiger Schritt. Die These steht als Überschrift, das hat das Review vom 7.11. verlangt.
- **Kartensystem und Farben sind ruhig und konsistent:** `--ink` `#0F1E2E` auf `#FAFAF7`, Akzent `#C25A2D` nur für Kicker, Kanten und Zähler, `--soft` `#475569` (7,4:1). Das BI-Orange `#FF9819` bleibt auf den dunklen Folien 1–2. Diese Trennung ist vertretbar (auf hellem Grund fiele `#FF9819` beim Kontrast durch) und soll so bleiben.
- **Appendix-Raster PLUS / MINUS / AVOID WHEN** mit Bild links ist gut für die Fragerunde. A6 (P&L T04B) ist die beste Bildfolie im Deck, und A9 (Währungstabelle in 24 px) ist von hinten lesbar.
- **Offenlegung, Trademark und Quellen in den Fußzeilen** bei 20 px sind sauber gelöst.
