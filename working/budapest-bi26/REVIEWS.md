# Vier Expert-Reviews des Decks (2026-11-07)

Vier Opus-Agenten haben die 19 Folienbilder und den Zeitplan begutachtet, in der Rolle IBCS-Experte, Data-Viz-Experte, Power-BI-Experte und Konzern-Controller. Annahme: Demos laufen und werden gezeigt. Unten die Punkte, die mehrfach kamen, dann je Rolle das Wesentliche. Was davon schon im Deck korrigiert ist, steht in der letzten Tabelle.

## Was alle vier getroffen hat

1. **Abweichungen in den ChartKitchen-Renders sind nicht auf Basisskala.** Gemessen: Zeit-Render ΔPL etwa 3-fach, Struktur-Render ΔPY etwa 1,8-fach vergrößert, ohne Skalenband. Widerspricht der eigenen CHECK-Karte. Lösung: in ChartKitchen mit Basisskala oder Skalenband neu rendern, englisch, in Folienbreite. Bis dahin ehrliche Bildunterschrift.
2. **Folie 9 widerspricht sich.** Gleichstand bei 150 Lesern, „ab 176 Lesern" und „Break-even 1:11 bis 1:22" zeigen in drei Richtungen. Dazu war die Richtung der 176-Aussage falsch: ab 176 Lesern wird die Lizenz je Kopf teurer als der günstigste Stunden-Ansatz, nicht billiger.
3. **Brauerei-P&L auf Folie 6 rechnet falsch** (Rohertragsmarge 67,1 % statt 66,8 %). Ein Controller in Reihe drei merkt das.
4. **Drei Stacks im Titel, sechs Sprossen, vier Rechner-Ansätze, sieben Matrix-Zeilen.** Die Zuordnung muss einmal gezeigt werden.
5. **Bezahltes Visual fehlt** (A7 Platzhalter), obwohl der Abstract es verspricht.

## IBCS-Experte

- SAY-Karte: IBCS hält den Titel neutral, die Botschaft steht als eigener Satz über dem Chart und ist im Chart hervorgehoben.
- STRUCTURE: „comparable" → „MECE". „Δ immer neben dem Wert" ist keine IBCS-Regel; besser „Varianz-Tiers am Basischart ausgerichtet".
- IBCS 2.0 gruppiert SUCCESS in NOTATION (Simplify, Unify, Check) und COMPOSITION (Say, Express, Structure, Condense).
- Publikum wird fragen: IBCS hat drei Achsen (Zeit, Struktur, Szenario). Eine GuV ist für IBCS eine Rechnung, als vertikaler Wasserfall gezeigt, kein Sonderfall der Struktur.
- „Zertifikat Pflicht → Paid": zertifizierte Software macht keinen Bericht konform, offene Stacks können konform liefern.
- Fehlende Zeilen: „IBCS® is a registered trademark of the IBCS Institute", CC BY-SA 4.0 für SUCCESS-Inhalte, Offenlegung eigener Visuals auf Folie 4 bis 7.
- Zeit-Render: Botschaft „YTD +171 K€" ist Gesamtjahr AC&FC vs PL, nicht YTD.

## Data-Viz-Experte

- Folie 3 ist das beste Chart (Aufbau in vier Schritten). Labels sitzen auf dem PL-Umriss, unklar ob AC oder PL.
- Folien 4 und 5: Dokumentations-Renders auf 7 bis 10 px geschrumpft, deutsch, grün links, teal rechts. Schlechtestes Chart: Zeit-Render Folie 4. Fix: englisch, Folienbreite, Kommentarspalte weg, Labels ab 16 px.
- Folie 10 als Takeaway: 28 Prosa-Zellen ohne Kodierung. Vorschlag: Sprossen × die fünf Kriterien des Abstracts (IBCS-Fit, Performance, Kosten, Wartbarkeit, Self-Service mit KI), dreistufig bewertet, These als Überschrift, dort enden; Fabric Apps davor oder in den Appendix.
- Zwei Zähler je Folie (oben rechts und unten rechts). Beide Oranges (Marke vs Kitchen) vereinheitlichen.

## Power-BI-Experte (gegen Microsoft Learn geprüft, 7.11.2026)

Korrekt: DAX-UDFs GA Juni 2026 · keine Display Folders, keine OLS-Vererbung · Matrix 500-Zeilen-Fenster · 30.000-Zeilen-Fenster, fetchMoreData bis 1.048.576 Zeilen (100 MB nur im Segment-Modus) · unzertifiziert kein PDF/PPT-Export, keine Abos · Lizenzdurchsetzung fehlt in Report Server, Sovereign Cloud, Publish-to-web, App-owns-data (und REST-Export) · Q&A endet 02/2027 · Deneb zertifiziert · Fabric Apps Preview, außerhalb Fabric Git.

Falsch oder zu prüfen: „UDF ohne IntelliSense" (nur in Visual Calculations, Live-Connect-Measures, SSMS) · SVG im Service leer (anekdotisch, Bug zitieren) · DaxLib-IBCS-Paket benennen · „Legacy Card retires" prüfen · Deneb 2.0 bricht Templates (Release Notes, Migrationspfad) · HTML Content zertifiziert? · Inforiver 33 € / Zebra 170 € auf Herstellerseiten · „Vega kommt näher an Power BI" ohne Quelle streichen.

Wichtig: Org-Store-Visuals verlieren ebenfalls PPT-Export und Abos, solange sie nicht zertifiziert aus AppSource kommen. „Paid nicht im Report Server" ist zu hart: Hersteller mit eigenen Lizenzschlüsseln laufen dort. Fabric Apps zeigen React-Ports der Visuals, nicht die .pbiviz. Immer „Microsoft-zertifiziert" von „IBCS-zertifiziert" trennen.

Leiter: Fabric Apps ist ein Host, kein Visual-Stack. Sprosse 4 trennt besser „Deneb (Vega)" von HTML Content. Fehlend: Paginated Reports, Visual Calculations, Report-Level-Measures. Sprosse 3 heißt besser „SVG-Measures + UDF-Bibliothek".

Demo (14 min): Core 1 min, dann SVG/UDF, Deneb, Custom open vs paid je 3 min. Eine schriftliche Definition of Done (PL-Umriss, FC-Schraffur, ΔPL-Panel, Vorzeichen-Trio, YTD/FY) und je Stack abhaken. Performance Analyzer: DAX-Zeit von Render-Zeit trennen, kalt und warm. Je Stack eine Live-Änderung (Kostenzeile hinzufügen) für Wartbarkeit. Einen Service-Export zu PDF zeigen. Aufzeichnung als Backup.

## Controller

- Kosten je Leser: beantwortet, bester Teil. Wartung: fair. Audit: nur Fußnote, gehört in die Überschrift.
- Vorbei geredet: Monatsabschluss. Was passiert, wenn am dritten Tag eine Zahl falsch ist, wer korrigiert wo, zeigen alle Stacks danach dieselbe Zahl, „data as of"-Stempel, Sign-off. Was ein Fachanwender ohne IT in Deneb oder im Paid Visual ändern kann, wird nicht gesagt.
- Folie 3: „Where do we land?" nennt keine Zahl.
- Fehlend, obwohl der Abstract es verspricht: Lokal- vs Konzernwährung, Ist- vs Budgetkurs. Dazu Konsolidierung, Forecast-Versionen, PY-Restatement, Abschlussregel.
- Folie 9 nicht budgetreif: eigener Stundensatz, Power-BI-Lizenzen und Capacity einrechnen, Herstellerangebote statt Listenpreise, Sensitivität auf die eigenen Zahlen. „Independent audit" ohne Namen.
- Überzeugt verlassen: Buchung live korrigieren und alle Stacks zeigen das neue EBITDA mit Stempel · eine Gesellschaft von HUF auf EUR zu Budget- und Ist-Kurs mit FX-Zeile · Rechner mit den eigenen Parametern live, inklusive Plattformlizenzen, und die eine Annahme, die kippt.

## Im Deck umgesetzt (2026-11-07)

| Punkt | Umsetzung |
|---|---|
| Folie 9 Richtung und Widerspruch | 176-Aussage korrigiert, 1:11 bis 1:22 entfernt, Preset-konsistent |
| Folie 6 falsche Margen | Brauerei-Render durch englische Desktop-Seite des Demo-Reports ersetzt (niedrige Auflösung, Live-Demo zeigt es groß) |
| Folien 4 und 5 Skalierung | Ersetzt durch Plan-gap-Kacheln aus Desktop in 3×: ChartKitchen 1.53 zeichnet Δ auf Basisskala, englisch, Mobility FR als Miss sichtbar |
| IBCS-Karten, Trademark, CC, Offenlegung | SAY und STRUCTURE umformuliert, Legende korrigiert, Fußzeilen ergänzt |
| Power-BI-Fakten | IntelliSense gestrichen, Org-Store-Hinweis, Report Server mit Herstellerschlüssel, React-Ports, Vega-Satz gestrichen, zertifiziert getrennt |
| Leiter | Sprosse 3 „SVG measures + UDF", Sprosse 4 „Deneb (Vega) · HTML", Visual Calculations in Sprosse 1 |
| Folie 10 | These als Überschrift, Zeilen 5a/5b/6 korrigiert, Fußzeile mit Evidenzhinweis |
| Deneb-Beispiel | Chart aus dem Business Chart Builder (Integrated variance) in A5 |
| Währung | neue Appendix-Folie A9 mit Kurstabelle und DAX-Muster |
| Folie 3 | Gesamtjahr-Zahl im Chart-Titel des letzten Schritts |

Umgesetzt danach: Folie 10 als bewertete Matrix mit sechs Kriterien · Modell-Folie · Renders auf Basisskala. Offen geblieben: Demo-Report je Sprosse plus Paid-Seite · Monatsabschluss-Szene in der Demo · die „verify"-Liste des Power-BI-Experten.


# Sieben Expert-Reviews der v1 und Synthese für v2 (2026-11-09)

Sieben Opus-Agenten haben die 23 Folienbilder (`reviews-v2/s01–s23.png`), `story.html`, BRIEF, die
Reviews vom 7.11., das TMDL des Demo-Modells und die vier neuen Demo-Seiten begutachtet. Rollen und
Dateien: Power BI Developer (`reviews-v2/power-bi-developer.md`), IBCS-Experte (`ibcs-expert.md`),
Data-Viz-Experte (`dataviz-expert.md`), Finanzer (`finance.md`), CFO (`cfo.md`), Konzern-Controller
(`controller.md`), Datenmodell-Experte (`data-model-expert.md`). Ergebnis der Umsetzung: `story-v2.html`
(25 Folien, `reviews-v2/UMSETZUNG-DECK.md`), Modell und Report geändert wie unten.

## Was mindestens vier der sieben getroffen hat

1. **Zahlenformat und Einheiten.** de-DE-Trennzeichen, zehnstellige Euro-Beträge, „Σ 2.818M“ vor englischem
   Publikum. Umgesetzt: Signed- und Δ-Measures mit Format `#,0.0,,` (EUR m), Titel „in EUR m“, Deneb-Labels
   in mEUR. Modellkultur en-US nachträglich doch gesetzt (Cache `.pbi/cache.abf` gelöscht, Modell aus TMDL neu aufgebaut);
   die Matrix-Anzeige folgt weiter der Windows-Region (Dezimalkomma), DAX-Textkonvertierung ist en-US.
2. **Folie 3 widerspricht dem Modell** (Jan 262 statt 245, Landung −2,0 % statt +1,3 %). Umgesetzt: Arrays
   aus dem Modell, Titel „landing 3,433 vs PL 3,389, +1.3 %“.
3. **Matrix und Rechner widersprechen sich bei den Kosten**, Hersteller-Bias in den Punkten. Umgesetzt:
   Kostenspalte mit Zahlen aus dem Preset, „IBCS fit (as shown today)“ mit 5a ●●○, Offenlegung in der Lead-Zeile,
   Spalte „Platform risk“ statt „Performance“, K.-o.-Zelle Export bei 5a rot umrandet, Punkte einfarbig.
4. **Plattformkosten, Stundensatz, Zeitraum fehlen auf der Rechner-Folie.** Umgesetzt: Zeile unter dem Chart
   (125 EUR/h, Pro/PPU/Capacity ausgeschlossen, Listenpreise), ~92 EUR Verhandlungsgrenze nach vorn,
   Chart in Graustufen (Rot/Grün war als Bewertung lesbar).
5. **Das Ende verpufft** (Fabric Apps als letzte Folie). Umgesetzt: Fabric Apps in A8 zusammengeführt, neue
   Folie „Your decision in four numbers“ und Schlussfolie mit These, QR und Dank.
6. **Datenstand und Forecast fehlen auf den Demo-Seiten.** Umgesetzt: Measure `Data as of` als Karte auf den
   Sprossen-Seiten, Deneb-Seite zeigt Jan..Dec AC&FC vs PL mit gestrichelten FC-Säulen (Builder-Vorlage).
7. **Zeitlogik hängt am Seitenfilter Monate 1–10.** Umgesetzt: Seitenfilter auf allen acht Seiten durch
   `Period Status = Actual` ersetzt; `ΔPL`, `ΔPY`, `Revenue AC&FC`, `FC flag`, Sparkline und SVG rechnen über
   den Periodenstatus bzw. `PeriodeSort`, damit sie ohne Filter und ohne Jahres-Slicer richtig bleiben.
8. **Vorzeichen-Regel 3 widerspricht den Daten** (alle 51 Kostenzeilen `VarianceInvert = true`). Umgesetzt:
   Regel 3 neu formuliert („−1 · shown positive · less is favourable“), Δ-Konvention auf Folie 7 genannt.
9. **A9 verspricht Budgetkurs, den das Modell nicht hat.** Umgesetzt: ehrliche Fußzeile („target pattern, not
   in the demo“), Yen-Beispiel durch Automation CH ersetzt. Nicht gebaut: `Kurs Budget`, `AC @BUD`, FX-Zeile.
10. **Günstige Farbe uneinheitlich** (teal vs grün). Umgesetzt: `#2E8B7A` in `ΔPL status`, `ΔPL SVG`,
    Datenbalken und beiden Deneb-Specs.

## Je Rolle das Wesentliche (Kurzfassung, Details in den Dateien)

- **Power BI Developer:** Deneb-Gesellschaften rechneten 10 Ist- gegen 12 Planmonate (gefixt über Period
  Status); A6 zeigte eine falsche Marge der Brauerei-GuV (Bild ersetzt); „+ UDF“ ohne UDF im Modell
  (Kompatibilitätslevel 1606, offen); Fakten korrigiert: nur Q&A endet 02/2027, HTML Content (lite) ist
  zertifiziert, Deneb 2.0 ist ein eigenes Visual, Copilot braucht F2+/P1+, Zebra ohne Free-Plan (~65–70 EUR),
  Fabric-Apps-Leser brauchen Build-Recht. Demo-Ablauf in Minuten und Live-Risiken (Deneb aus AppSource).
- **IBCS-Experte:** GuV ist eine Rechnung, kein Struktur-Sonderfall (Folie 6 umbenannt); SUCCESS in
  NOTATION/COMPOSITION gruppiert, CC-BY-SA-Fußzeile; Skalenband statt „marked factor“; Doppellinie als
  PL-Referenz im SVG; „four companies below plan“; Tabelle Sprosse × Notationskriterium mit Aufwand je Seite.
- **Data-Viz-Experte:** Renders auf Folie 4 zu klein (geteilt in 4a/4b), Matrix von hinten unlesbar und doppelt
  kodiert (einfarbige 18-px-Punkte), doppelte Zähler (HUD aus), Stack-Klammern über der Leiter, Datenbalken
  überdecken Zahlen (eigene Spalte), Folie für Folie benotet.
- **Finanzer:** Folie 3 falsch, Budgetkurs nicht im Modell, Vorzeichen dreifach widersprüchlich, +12,8 %
  enthält den Zukauf (organisch +8,7 %), FC-Definition (10+2), IFRS 18 ab 2027, Konsolidierung ohne
  Eliminierung benennen; Plausibilitätstabelle: Modellzahlen glaubwürdig, nur die Brüche zwischen Folie und
  Modell greifbar.
- **CFO:** Die eine Frage (Standardisierung, 3-Jahres-Kosten, Wechselkosten) nur halb beantwortet;
  Umkehrbarkeit ausdrücklich sagen; Entscheidungsfolie mit vier Eingaben; „Time to first report“ fehlt (offen).
- **Controller:** Monatsabschluss-Szene (offen, Sprechtext vorbereitet), Stempel auf jeder Seite (gebaut),
  Landung zeigen (Deneb AC&FC), Sprossen 1–3 ohne Zwischensummen („Total“ → „Net income“, Grenze benennen),
  Export-K.-o. bei 5a laut sagen, Tauglichkeitstabelle je Seite.
- **Datenmodell-Experte:** Modell-Folie korrigiert (Beziehungen, L1…L6, Snowflake), Signed-Measures auf GuV
  begrenzt und über `VALUES(SignConvention)` statt `SUMX(fact)`, Überlaufschutz in Text- und SVG-Balken,
  Beschreibungen gerückt, Anti-Patterns zum Selbst-Benennen (40 % Nullzeilen, Präsentationslogik im Modell,
  Szenarien als Spalten, hart kodierte L1-Namen, keine Calculation Groups trotz Folientext).

## Umgesetzt (2026-11-09)

| Bereich | Umsetzung |
|---|---|
| Deck | `story-v2.html`: alle Punkte der Synthese, siehe `reviews-v2/UMSETZUNG-DECK.md` (Folie 4 geteilt, Fabric Apps → A8, neue Folien 13/14, Matrix neu, Rechner-Zeile, Modell-Folie, A2–A11 Texte, HUD aus) |
| Modell | 19 Measures im Ordner „Budapest demo“ neu geschrieben (`demo-report/scripts/budapest_measures.py`): EUR-m-Formate, Period-Status-Logik, GuV-Filter, Teal, Doppellinie, Überlaufschutz, `ΔPL (bar)`, `Data as of`; Filterinfo englisch; dim-gesellschaft-Beschreibung |
| Report | Seitenfilter `Period Status = Actual` auf 8 Seiten; Matrizen: Spaltenfolge PY · PL · AC · Δ, „Net income“, Titel wer/was/wann, Schrift 10, Consolas für Textbalken; Datenbalken in eigener Spalte; Datenstand-Karten; Deneb-Seite auf Business-Chart-Builder-Vorlagen (Integrated variance, Structural variance analysis) mit AC&FC, FC gestrichelt, Teal |

## Offen geblieben

ChartKitchen-Renders auf Folie 4/5 mit deutschem Zahlenformat · Zebra-P&L-Seite · Performance-Messung auf großem Modell ·
40 oder 60 Minuten · Seite „Card and slicer“: ob die UDF-Bilder in neuer Karte und Button-Slicer rendern, ist nicht bestätigt.

Erledigt am 10.11.: UDF (PowerofBI.IBCS 0.11.0, Level 1702) auf Sprosse 3, Modellkultur en-US, Deneb-Feldnamen ·
Budgetkurs im Modell (`fact-kurse[Kurs Budget]`, `AC signed @BUD`, `FX effect`, `ΔPL @BUD`; Net revenue 2,817.6 /
2,803.3 / +14.3) · Monatsabschluss-Szene (`fact-nachbuchung` + Schalter `close-status`, Net income 151.6 → 155.6) ·
Zwischensummen in den Core-Matrizen (`pnl-lines` + `AC/PL/PY/ΔPL line`). Deck nachgezogen: Folien 8, 9, 10, 12, 13,
A2, A3, A9, A10, A11 (Kontrollbilder `reviews-v2/v3-s*.png`).
