# Budapest BI Forum 2026 · Session-Brief

## Offizielle Fakten (budapestbi.hu, Stand 2026-11-07)

| Feld | Wert |
|---|---|
| Titel | Finance Reporting in Power BI: One Model, Three Visual Stacks Compared |
| Tag | Dienstag, 17. November 2026, vor Ort (Danubius Hotel Helia) |
| Format | **40-minute talk** laut budapestbi.hu; der Sessionize-Abstract sagt „60-minute session" → mit Orga klären |
| Sprache | Englisch |
| Tags | Power BI & Fabric · DataViz · Finance Analytics |
| Seite | https://budapestbi.hu/bi26/sessions/finance-reporting-in-power-bi-one-model-three-visual-stacks-compared/ |
| Material-Repo | https://github.com/Losveratos/BI-Forum-Budapest-2026 |

## Abstract (wörtlich)

> Finance reporting always asks the same questions: AC vs PY, PL and FC, MTD/YTD/FY, Local vs Company Currency, current rate vs budget rate — on real data volumes.
>
> This designs a lean Power BI model that handles all of it, then walks through the same dashboard implemented three ways: Core Visuals with SVG, Deneb, and a paid custom visual.
>
> Compare IBCS fit, performance, cost, maintainability, and self-service in the age of AI — honest trade-offs.

## Was der Abstract verspricht (Checkliste)

1. Ein schlankes Modell für AC/PY/PL/FC, MTD/YTD/FY, Lokal- vs. Konzernwährung, Ist-Kurs vs. Budgetkurs, echte Datenmengen
2. **Dasselbe** Dashboard dreimal: Core Visuals + SVG · Deneb · bezahltes Custom Visual
3. Vergleich: IBCS-Fit · Performance · Kosten · Wartbarkeit · Self-Service mit KI, ehrlich

## Vorhandenes Material (Desktop)

| Was | Wo | Nutzen für die Session |
|---|---|---|
| Budapest BI Forum.Report (10 Seiten, 85 Visuals) + PnL ChartkitchenDemoKit.SemanticModel | `PnL Demo\` | Modell-Story komplett: 9 Firmen, 7 Währungen, AC/PY/PL/FC, FC_FY-Skalar, SignConvention, IAS 21/IAS 7. Stack 3 (Custom Visual) fertig; seit 08.11. je eine Seite für Sprosse 1–4 (Core, DAX-Text, SVG-Measures, Deneb). Doku: `working/budapest-bi26/demo-report/README.md` |
| Vortragsnotizen zu den 6 Seiten | `PnL Demo\Budapest\README.md` | Was auf jeder Seite zu sagen ist, inkl. der Modell-Fallen (SUM vs MAX, 10 vs 12 Monate) |
| Deneb-Beispiele | `Daten WG Knowlegde Kitchen\deneb-test\` | Stack 2 Startpunkt |
| SVG-Visual-Skill, Waterfall-HTML, PBI-IBCS-Testbed | `Daten WG Knowlegde Kitchen\` | Stack 1 Startpunkt |
| Visual-Standards-Rechner + Monte-Carlo | `Downloads\`, Knowledge Kitchen | Kosten-Argument |
| ChartKitchen/P&L-Doku DE/EN, Showcase-Videos | `PnL Demo\`, Knowledge Kitchen | Stack 3 Belege |
| Folienvorlage BI26 (Exo 2, Dark/Light, Card-Layouts) | `material/bi26_template.pptx` | Pflichtrahmen: Titel, Sponsoren, Bio |

## Nicht diese Session

`material/andere-sessions/` enthält den Mockup-Brief (Human-to-Agent) und den FabCon-CFP. Sie gehören zu anderen Einreichungen.

## Folien-Deck (Stand 2026-11-07, `story.html`, 1920×1080)

Bedienung: → / Leertaste / Klick rechts = weiter (erst Statement, dann Inhalt, dann Aufbauschritte) · ← = zurück · O oder Esc = pyramidale Übersicht mit Gruppen, Klick auf Thumbnail zoomt hinein · Home / End.

| # | Folie | Bild | Status |
|---|---|---|---|
| 1 | Cover (BI26-Look) | – | steht |
| 2 | Michael: Foto groß, QR Repo, QR LinkedIn, Links | assets/michael-tenner.webp | steht |
| 3 | What do we want to see: AC → PY → PL → FC in vier Schritten | schematisch (SVG) | Demo-Zahlen |
| 4 | … in structure and in time | Plan-gap-Kacheln aus Desktop, 3×, EN, Δ auf Basisskala | steht |
| 5 | IBCS on one page + Struktur-vs-Zeit-Beispiel | dieselben Plan-gap-Kacheln | steht |
| 6 | P&L als Spezialfall | Group P&L aus Desktop, 3× (2407 px) | steht |
| 7 | Modell: Sternschema, vier Regeln | SVG | steht |
| 8 | Stack-Leiter 1–6 | – | steht |
| 9 | Demo-Platzhalter, GitHub-QR, vier Report-Seiten | Desktop-Screenshots Sprosse 1–4 + Plan gap | steht (Desktop EN, Zahlenformat de-DE) |
| 10 | Rechner live, Finance-Preset, Link zum Rechner | Rechner-Screenshot EN | Share-Link mit Preset ablegen |
| 11 | Summary: bewertete Matrix, sechs Kriterien, Avoid-when, These als Titel | – | Bewertungen bestätigt 07.11. |
| 12 | What's next: Fabric Apps | – | steht |
| A1 | Rechner: warum Paid und Open Source gleichauf | Rechner-Screenshot | steht |
| A2–A4 | Pure Power BI · DAX only · DAX+SVG+UDF | Demo-Report-Seiten 1–3 | steht |
| A5 | Deneb/HTML | Demo-Report Seite 4 (Deneb, Basisskala), Link zum Business Chart Builder | steht |
| A6 | Custom Visual open | P&L T04B | steht |
| A7 | Custom Visual paid | Zebra BI Working-Capital-Dashboard | steht; P&L-Seite in Zebra noch offen |
| A8 | Fabric Apps | Vertriebs-App | steht |
| A9 | Währung: Kursarten, Franken-Beispiel, Budgetkurs im Modell, FX-Effekt gezeigt | assets/demo-fx-close.png | steht (Stand 10.11.) |
| A10 | Modellbau: Generator, sieben CSVs, Umrechnung im Generator, Reconciliation, dwg check | – | steht |
| A11 | DAX: Rollen-Measures, Vorzeichen-Blöcke, FY-Skalar, LW-Guard, Stichtag | – | aus fact-abschluss.tmdl |

Assets liegen in `working/budapest-bi26/assets/`. Desktop-Seiten wurden mit `pbir desktop screenshot` aus Power BI Desktop geholt (nach Daten-Refresh), Rechner-Bilder headless aus `visual-standards-rechner.html?lang=en`.

Stand 09.11.: `story-v2.html` (25 Folien) nach sieben Expertenreviews, Synthese in REVIEWS.md, Umsetzungsliste in `reviews-v2/UMSETZUNG-DECK.md`; Modell und Report angepasst (Period-Status-Flag, EUR m, Teal, Datenstand, Deneb mit Chart-Builder-Vorlagen, UDF-Bibliothek PowerofBI.IBCS auf Sprosse 3, Modellkultur en-US). Anleitung UDF mit neuer Karte und Button-Slicer: `demo-report/udf-ibcs-anleitung.md`.

Offen: 40 oder 60 Minuten · Seite „Card and slicer“ (UDF-Bilder in Karte/Button-Slicer unbestätigt) · ChartKitchen-Renders mit deutschem Zahlenformat · Zebra-P&L-Seite · „Vega kommt nach Power BI" verifizieren · Speaker-Card trägt „Daten.-WG".

Reviews der vier Expert-Agenten mit Umsetzungsstand: `REVIEWS.md`. Übersicht (Taste O) jetzt als Story von links nach rechts, sechs Akte, Appendix darunter.

Alle URLs im Deck sind klickbar (Rechner mit ?lang=en, GitHub, LinkedIn, Kitchen, ibcs.com, Chart Builder). 21 Folien.

Renders in 3×: `pbir desktop screenshot "<Report>" --all --scale 3 --settle 1500 --output-dir <dir>` nach Daten-Refresh in Desktop; Kacheln per PIL zugeschnitten (Koordinaten ×3 der 1317-px-Aufnahme). ChartKitchen ab 1.52 zeichnet Δ-Panels auf Basisskala und markiert jede Vergrößerung mit Faktor und Skalenband.
