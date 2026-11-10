# Umsetzung der Review-Synthese im Deck (story-v2.html)

Quelle: `story.html` (unverändert). Ergebnis: `story-v2.html`, 25 Folien (14 Hauptteil + 11 Appendix).

## Neue Nummerierung

| alt | neu | Folie |
|---|---|---|
| s01–s03 | 1–3 | Cover, Speaker, What we want to see |
| s04 | **4 + 5** | geteilt: 4 „Time runs as columns“, 5 „Structure runs as bars“ |
| s05 | 6 | IBCS on one page |
| s06 | 7 | P&L is a calculation |
| s07 | 8 | Modell |
| s08 | 9 | Leiter |
| s09 | 10 | Demo |
| s10 | 11 | Rechner |
| s11 | 12 | Matrix |
| s12 | – | Fabric Apps → in A8 (Appendix) zusammengeführt |
| neu | **13** | „Your decision in four numbers“ |
| neu | **14** | Schlussfolie (Thesensatz, QR, Thank you) |
| s13–s23 | 15–25 | A1–A11 |

Kapitel: Intro · What we want to see · How it fits Power BI · Demo · What it costs · **Your decision** (neu, ersetzt „What's next“) · Appendix.

## Punkte

| Punkt | umgesetzt | Anmerkung |
|---|---|---|
| F3 Arrays auf Modellzahlen (AC 10+2 null, PY 12, PL 12, FC 10 null + 301, 314) | ja | Gerundete Werte wie vorgegeben |
| F3 Farben AC #404040, PY #B3B3B3 | ja | Konstanten `C_AC`, `C_PY`, auch Legende im Chart |
| F3 Titel letzter Schritt „landing 3,433 … +1.3 %“ | ja | |
| F3 Fußzeile „Demo model DWG Industries, net revenue, million EUR“ | ja | |
| F3 Skalierung bis 316 | ja | 1 px je Mio., 340 Mio. Platz, kein Überlauf (Render geprüft) |
| F4 Fußzeile „Δ on the base scale in each chart“ | ja | auf 4b (Struktur); 4a trägt „Δ on the base scale“ |
| F4 Bildunterschrift „four companies below plan, Mobility FR with −32.3 m“ | ja | im Lead von 4b |
| F4 Bilder größer | ja | Entscheidung nach Render: **geteilt in 4a/4b**. Seitenvergleich nebeneinander hätte nur ~0.45 Skalierung gebracht (Höhe ist der Engpass, Bilder hochkant). Jetzt Text links, Bild rechts über fast die volle Folienhöhe (~0.65 Skalierung, Labels ca. 13–15 px) |
| F5 Klammern NOTATION / COMPOSITION, Karten gruppiert | ja | Reihenfolge Simplify, Unify, Check · Say, Express, Structure, Condense |
| F5 SAY-Karte „one message per page …“ | ja | |
| F5 Legende „or a scale band“ | ja | |
| F5 untere Hälfte mit Doppel-Renders gestrichen | ja | Karten dafür größer (Buchstabe 52 px, Text 26 px) |
| F5 Legende 28 px, Swatches 44×28 | ja | AC/PY-Swatches in #404040/#B3B3B3 passend zu F3 |
| F5 Fußzeile Lizenz CC BY-SA 4.0 | ja | zweizeilig |
| F6 Kicker, Titel, Unterzeile | ja | Titel einzeilig |
| F6 Satz „Δ = AC − PL …; colour carries good or bad (IBCS)“ | ja | in der Bildunterschrift |
| F6 Satz Management P&L / IFRS 18 | ja | kleine Zeile unter den vier Dingen |
| F6 Bild pbi3-group-pnl-statement-en.png | ja | Datei existierte beim Rendern noch nicht (Alt-Text sichtbar) |
| F6 Headline-Zusatz +12.8 % reported · +8.7 % organic | ja | |
| F6 versteckten Tabellenblock gelöscht | ja | |
| F6 „sign trio“ im Kartentext | teilweise | Bullet heißt jetzt „The sign.“, damit der Begriff zu „calculation“ passt; Inhalt unverändert |
| F7 Untertitel „rate table related to date and currency“ | ja | |
| F7 L1…L6, „· Unit“ entfernt | ja | |
| F7 „Star schema, one snowflake branch (region)“ | ja | |
| F7 Rule 2 „MAX per account, company and year, then summed“ | ja | |
| F7 Rule 3 neu | ja | |
| F7 Satz unter Rule 4 (Forecast-Versionen) | ja | in der Rule-4-Karte |
| F7 Trap-Satz mit Period status = Actual | ja | |
| F7 Überlauf „168“ | ja | rechte Spalte auf 210 px verbreitert, Text auf drei Zeilen |
| F7 DimCurrency an FactRates, DimRegion an DimEntity | ja | dazu Linie Date → FactRates (beschriftet „date“); gestrichelte Linie FactFinance → FactRates entfernt; „LW“ im Diagramm → „LC“ |
| F8 Klammerzeile Stack 1/2/3 + Host, 24 px, Akzent | ja | Host in Grau, weil kein Stack |
| F8 Kartentexte zwei Sätze, 26 px | ja | Titel einzeilig, damit es passt |
| F8 Sprosse 1 Copilot (paid capacity F2+/P1+) | ja | |
| F8 Sprosse 4 Zertifizierung + FabCon-Zeile | ja | FabCon-Satz als hervorgehobene Notiz (22 px) |
| F8 Sprosse 6 Preview/Build/Git | ja | |
| F8 Fußzeile „Not on the ladder …“ | ja | erste Zeile der Fußzeile; Agenten-Satz bleibt als zweite Zeile |
| F9 „Nothing prerecorded.“ gestrichen | ja | |
| F9 Bullet Day three, 10:40 | ja | Streifen mit 5 Figuren bleibt |
| F10 Zeile unter dem Chart (125 EUR/h …) | ja | „3 of 58 …“ steht stattdessen in der Fußzeile (siehe nächste Zeile) |
| F10 „tie“ → „indistinguishable within the band“ | ja | |
| F10 erster Punkt „Negotiate below ~92 EUR …“ | ja | |
| F10 „3 of 58 assumptions verified“ in die Fußzeile | ja | Fußzeile links: „3 of 58 assumptions verified: read the P10–P90 band, not the P50.“; in der Matrix-Fußzeile gestrichen |
| F10 Bild grayscale + object-position top | ja | Klasse `.calc-img` |
| F10 Lizenzanker-Satz | ja | im Punkt „Licence anchor“ |
| F11 Titel zweizeilig gekürzt | ja | „Rules in the model. Pick the rung …“, 56 px; Drei-Stacks-Satz in den Kicker verschoben |
| F11 Lead „Ratings from calculator, demo and seven reviews …“ | ja | |
| F11 Spalte Platform risk mit Zellen | ja | Punkte ergänzt (eigene Bewertung): 1 ●●○, 2 ●●●, 3 ●●○, 4 ●●○, 5a ●●○, 5b ●●○, 6 ●○○ |
| F11 Cost per reader mit Zahlen, Spaltenkopf | ja | |
| F11 IBCS fit (as shown today) | ja | 1–3 Bewertungen unverändert |
| F11 Export & audit trail, Zelle 5a rot umrandet | ja | |
| F11 Zellen 2/3 Excel-Export | teilweise | Zeile 3 wörtlich; Zeile 2 „Excel export carries the bar as text“, weil Sprosse 2 Textbalken und kein SVG nutzt |
| F11 Zeile 6 „readers need Build on the model“ | ja | in der Spalte Export & audit trail |
| F11 Punkte einfarbig 18 px in --ink | ja | per CSS (`.dots b`, `.dots b.o`), keine Teal/Rot-Kodierung mehr |
| F11 Satz „Because the rules sit in the model …“ | ja | direkt unter dem Titel, 28 px |
| F11 Fußzeile „If your board pack is a PDF …“ | ja | rechts; Legende links |
| F12 Fabric Apps in den Appendix (mit A8 zusammengeführt) | ja | Inhalt „One spec, two targets“ und Schlusssatz in A8 übernommen, Kicker „A8 · rung 6 · what's next“ |
| Neue Folie „Your decision in four numbers“ | ja | fünf Zeilen wörtlich |
| Neue Schlussfolie | ja | blaue Titel-Optik, Thesensatz 64 px, QR (von Folie Demo) 300 px, Thank you, Speaker-Zeile, Repo-Link |
| Kapitelzuordnung | ja | beide neue Folien im Kapitel „Your decision“ |
| A2 Minus Q&A / Plus paid capacity / Minus Subtotals | ja | |
| A3 Bild | ja | unverändert referenziert |
| A4 Plus UDF/1702/daxlib, Minus Service-Test, Minus UDFs | ja | |
| A5 Bild, Bildtitel, Minus Deneb 2.0, Plus FabCon | ja | Bildunterschrift angepasst („Vega-Lite specs … exports these templates“) |
| A6 Bild pbi3-group-pnl-statement-en.png, Bildtitel, T04B-Zusatz | ja | T04B-Zusatz als Bildunterschrift |
| A7 Bildunterschrift Zebra BI Trial/Preise | ja | Plus „free tier“ → „14-day trial“, Minus Preis-Satz und Fußzeile angeglichen |
| A8 Minus Build permission | ja | ersetzt die alte Git-Zeile (inhaltlich enthalten) |
| A9 Fußzeile ehrlich, Franken statt Yen | ja | „The yen problem“ → „The franc problem“; „rate table without a relationship“ im Text → „related to date and currency“ |
| A10 Satz Synthetic group / FC 10+2 | ja | |
| A11 MAX-Text, 215 m-Satz, LW → LC, AC at reporting date, Fußzeile | ja | Spaltennamen im Code (`AC LW Wert`, `Währung`) bleiben, weil sie dem Modell entsprechen; nur das Measure heißt `AC LC` |
| Global: #hud ausgeblendet, Taste H | ja | `body.hud` schaltet |
| Global: Crumb nur Kapitelname | ja | |
| Global: Fußzeilen ≥ 18 px, Fließtext ≥ 22 px | teilweise | Fußzeilen 20 px; `.success` 26 px, `.rung` 26 px, Strip-Bildunterschriften 20 px. Matrix-Begründungen 17 px (vorher 16): mehr passt in die Tabelle nicht ohne Zeilen zu streichen |
| Global: Appendix-Figuren ohne Leerraum | ja | Klasse `appx`: Figur passt sich der Bildhöhe an, rechte Spalte oben bündig |

## Nicht umgesetzt / offen

- Bilder `pbi3-group-pnl-statement-en.png` (F7, A6) fehlten beim Rendern; Platz ist reserviert.
- Die neuen Kachelbilder (A4/A5) waren beim Rendern noch in Arbeit (A5 zeigt angeschnittenen zweiten Chart im Bild selbst).
- Die Renders auf F4/F5 tragen weiter deutsche Zahlformate („+22,1M“, „in Mio.“), das ist Bildsache.

## Kontrollbilder (reviews-v2/)

v2-s01, v2-s03, v2-s04, v2-s05, v2-s06, v2-s07, v2-s08, v2-s09, v2-s10, v2-s11, v2-s12, v2-s13, v2-s14, v2-s15, v2-s16, v2-s17, v2-s18, v2-s19, v2-s20, v2-s21, v2-s22, v2-s23, v2-s24, v2-s25 (.png)
