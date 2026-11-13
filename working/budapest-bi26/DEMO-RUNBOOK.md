# Budapest BI Forum 2026 · Demo-Ablauf und Spickzettel

**Finance Reporting in Power BI: One Model, Three Visual Stacks Compared**
Dienstag, 17. November 2026 · Danubius Hotel Helia · 40 Minuten · Englisch

Alle Prüfwerte: Gewinn- und Verlustrechnung, Jan..Okt 2026 (`Period Status = Actual`), Mio. EUR,
vorzeichenrichtig (positiv = günstig). Quelle: `demo-report/README.md` (v3, gegen das geladene Modell
per DAX geprüft) und `demo/demoData/demokit/reconciliation.txt`.

---

## 1 · Zeitplan (40 Minuten)

| Minute | Folien | Inhalt | Puffer-Regel |
|---|---|---|---|
| 0:00–2:00 | 1–2 | Cover, Speaker, QR zum Repo | – |
| 2:00–8:00 | 3–7 | AC → PY → PL → FC, Zeit als Säulen, Struktur als Balken, IBCS, P&L als Rechnung | Bei Verzug Folie 6 nur zeigen, nicht erklären |
| 8:00–11:00 | 8–9 | Modell (Sternschema, Rollen-Measures), Leiter 1–6 | – |
| 11:00–24:00 | 10 → **Live-Demo Desktop** | Sprossen 1–5, Day-3-Schalter, FX | Harte Grenze 24:00: dann direkt zum Rechner |
| 24:00–29:00 | 11 → **Live-Rechner** | Finance-Szenario, was die Rangfolge dreht | Bei Verzug nur Ebene 1 zeigen |
| 29:00–34:00 | 12–13 | Bewertete Matrix, Entscheidung in vier Zahlen | – |
| 34:00–40:00 | Q&A | Appendix A1–A11 als Antwortfolien | – |

Kontrollpunkte auf der Uhr: **11:00 Demo beginnt · 18:00 Sprosse 4 erreicht · 24:00 Rechner · 34:00 Fragen.**

---

## 2 · Vorab-Check (Hotelzimmer am Montag und 30 Minuten vor dem Slot)

**Power BI Desktop**

- [ ] `demo/Budapest BI Forum.pbip` öffnen, Parameter `DemoPfad` = lokaler Ordner `demo/demoData/demokit`.
- [ ] **Voll aktualisieren und speichern.** Gelbes Banner „Some of the tables have incomplete or no data“
      darf nicht stehen. Erst dann liegen `fact-nachbuchung` und `close-status` im Cache.
- [ ] **Deneb kommt beim Laden aus AppSource:** einmal *mit Internet* öffnen, Seite „4 Deneb“ ansehen,
      speichern. Ohne Netz im Saal sonst leere Kacheln. ChartKitchen und P&L Statement liegen im
      Projekt (`CustomVisuals/`) und brauchen kein Netz.
- [ ] Close-Slicer auf **„Closed WD3“** oder leer zurücksetzen (synchronisiert über alle Seiten,
      Gruppe `dwg-close-status`).
- [ ] Company-Slicer leer (ganze Gruppe).
- [ ] **Windows-Region auf Englisch** (Dezimalpunkt) stellen, sonst zeigt Desktop „151,6“ statt „151.6“.
      Die Desktop-Formatierung folgt der Windows-Region, nicht der Modellkultur.
- [ ] Bildschirmsperre und Energiesparen aus. Mit gesperrtem Bildschirm blieb der Refresh-Dialog auf
      „Evaluating…“ hängen.
- [ ] Performance Analyzer im Menü „Optimize“ bereitlegen, aber noch nicht starten.
- [ ] Seite **„Card and slicer“ in der Demo überspringen**: Die IBCS-Bilder in Karte und Button-Slicer
      werden noch nicht angezeigt (siehe README v3).
- [ ] Desktop auf Startseite „1 Pure Power BI“ stellen, Vollbild, Zoom passend für 1920×1080.

**Rechner (Browser)**

- [ ] Tab offen mit
      `https://datenwgknowledgekitchen.com/visual-standards-rechner.html?lang=en&preset=finance`
      Ergebnis muss lauten: *„With 5 report authors and 150 viewers, Paid and Open source are level at
      around €144 per viewer per year (P50); Deneb costs 1.2 times as much, Core + SVG costs 1.8 times as
      much. From around 176 viewers …“*
- [ ] Falls `&preset=` noch nicht live ist (Rechner v0.23.1 noch nicht auf `main`): `?lang=en` öffnen,
      **„Straight to the calculator“**, dann Szenario **„Finance with mandatory IBCS · 5 / 150“**.
- [ ] Offline-Rückfall: `calculator-finance-preset-en.pdf` (Ebene 1) und
      `calculator-finance-preset-en-level2.pdf` (Ebene 2) lokal geöffnet.

**Rückfall für alles:** `One-Model-Three-Visual-Stacks.pdf` und die Screenshots in `assets/`
(`demo-rung1-pure.png` … `demo-rung4-deneb.png`, `demo-close-adjusted.png`, `demo-fx-close.png`).

---

## 3 · Live-Demo in Desktop (11:00–24:00)

Leitfrage von Folie 10: *„Same P&L page, same numbers. Who is still right, who is still fast?“*
Auf jeder Seite einmal den Company-Slicer auf **Mobility FR** und zurück: Das ist die Gesellschaft,
die später der Day-3-Schalter trifft.

### 3.1 · „1 Pure Power BI“ (ca. 2 Min.)
- Zeigen: Matrix mit Zwischensummen aus der Zeilentabelle `pnl-lines`, Säulen Umsatz AC vs. PY,
  Balken je Gesellschaft AC vs. PL, Stempel „Data as of“ unter dem Titel.
- Sagen: *„No plan outline, no variance on base scale. The rules live in your head.“*
- **Performance Analyzer starten**, Seite neu zeichnen: DAX-Zeit und Renderzeit getrennt zeigen.

| Zeile | AC | PL | ΔPL |
|---|---:|---:|---:|
| Net revenue | 2,817.6 | 2,782.1 | +35.5 |
| Gross profit | 942.8 | 957.0 | −14.2 |
| EBITDA | 400.5 | 424.2 | −23.7 |
| EBIT | 256.3 | 280.9 | −24.5 |
| EBT | 206.5 | 239.2 | −32.6 |
| **Net income** | **151.6** | **176.3** | **−24.7** |

### 3.2 · „2 DAX only“ (ca. 1,5 Min.)
- Zeigen: dieselbe Matrix plus Unicode-Balken `ΔPL line bar (text)` (Consolas), Sparklines je Gesellschaft.
- Sagen: *„Everything auditable, every change is a measure. Proportional font and it breaks.“*
- Gleiche Zahlen wie 3.1.

### 3.3 · „3 SVG measures“ (ca. 2 Min.)
- Zeigen: handgeschriebenes `ΔPL line SVG` neben `ΔPL line UDF` aus PowerofBI.IBCS (daxlib.org).
- Sagen: *„Far, but handmade. The UDF draws no bar on total rows, only the bold number.“*
- Zwischensummen (Gross profit, EBITDA, EBIT, EBT, Net income) zeigen in den UDF-Spalten nur die fette Zahl.
  Das ist so gewollt und kein Fehler.

### 3.4 · „4 Deneb“ (ca. 2 Min.)
- Zeigen: Business-Chart-Builder-Vorlagen „Integrated variance“ (Monate, AC&FC vs. PL, FC gestrichelt)
  und „Structural variance analysis“ (Gesellschaften).
- Achtung: **kein Seitenfilter**, hier steht Jan..Dez mit Forecast. Die Zahlen sind deshalb nicht dieselben
  wie auf den Sprossen 1–3.
- Sagen: *„The chart is a spec: text, Git, templates. Microsoft announced native Vega-Lite, no date yet.“*

### 3.5 · Sprosse 5: „Group P&L“ und „Plan gap“ (ca. 2 Min.)
- Zeigen: P&L Statement byDatenWG (Group P&L) und ChartKitchen (Plan gap), Δ-Panels auf Basisskala.
- Offenlegen: *„My own visuals, discount my ratings here.“*
- Net income muss auch hier **151.6** zeigen.

### 3.6 · Der Day-3-Schalter (ca. 2 Min.): der Höhepunkt
Szene: *„Day three, 10:40. One booking changes.“* Close-Slicer auf **„Incl. day-3 adjustment“**.
Gebucht: Auflösung einer Rückstellung, Mobility FR, 31.10.2026, +4,0 Mio. EUR (Other operating result).

| Wert | Closed WD3 | Incl. day-3 adjustment |
|---|---:|---:|
| Net income (Gruppe) | 151.6 | **155.6** |
| Other operating result | 1.5 | 5.5 |
| EBITDA | 400.5 | 404.5 |
| EBIT / EBT | 256.3 / 206.5 | 260.3 / 210.5 |
| ΔPL Net income (Gruppe) | −24.7 | −20.7 |
| ΔPL EBITDA | −23.7 | −19.7 |
| Mobility FR Net income / ΔPL | −5.5 / −9.2 | −1.5 / −5.2 |
| Mobility FR EBITDA | 26.0 | 30.0 |
| Net revenue | 2,817.6 | 2,817.6 (unverändert) |

- Durch die Seiten 1 → 2 → 3 → Group P&L klicken: **überall 155.6**. Der Stempel trägt jetzt
  „· incl. day-3 adjustment“.
- Sagen: *„None of the visuals owns a number. The rule sits in the model.“*
- Danach **zurück auf „Closed WD3“**.

### 3.7 · „FX and close“ (ca. 1,5 Min., streichbar)
- Zeigen: Umsatz zum Ist-Kurs vs. Budgetkurs je Gesellschaft, FX-Effekt.

| Gesellschaft | FX effect |
|---|---:|
| Automation CH | +4.4 |
| Industries US | +4.2 |
| Energy PL | +3.0 |
| Automation CZ | +2.7 |
| Mobility AU | +0.9 |
| Digital JP | −0.8 |
| DE- und FR-Gesellschaften (EUR) | – |
| **Total** (AC 2,817.6 · AC @BUD 2,803.3 · PL 2,782.1) | **+14.3** |

- P&L-Matrix: Net income 151.6 / @BUD 150.8 / FX +0.8 / ΔPL −24.7 / ΔPL @BUD −24.5.
- Ehrlich sagen: *„FX effect is what the rate moves did to our actuals.“* ΔPL ist nicht exakt
  FX effect + ΔPL @BUD; die Lücke ist die Umrechnungsdifferenz des Plans selbst.

### Wenn etwas schiefgeht
| Problem | Sofort tun |
|---|---|
| Deneb-Kacheln leer (kein Netz) | Screenshot `demo-rung4-deneb.png` bzw. Folie A5 zeigen |
| Gelbes Banner, leere Tabellen | Nicht im Saal aktualisieren. Auf Deck-Folien A2–A6 wechseln |
| Close-Slicer wirkt nur auf einer Seite | View › Sync slicers, Gruppe `dwg-close-status`; sonst Screenshot `demo-close-adjusted.png` |
| Desktop hängt | Deck-PDF, Folie 10 und Appendix; die Geschichte trägt auch ohne Live-Bild |

---

## 4 · Live-Rechner (24:00–29:00)

1. Tab mit `?lang=en&preset=finance` nach vorn holen. Ebene 1 ist offen, Szenario-Button hervorgehoben.
2. Den Ergebnissatz vorlesen: **Paid ≈ Open source ≈ 144 € je Viewer und Jahr, Deneb ×1.2, Core + SVG ×1.8,
   Kipppunkt ab ~176 Viewern.**
3. Das Band zeigen, nicht den Strich: *„Read the P10–P90 band, not the P50. 3 of 58 assumptions are verified.“*
4. Hebel live drehen (einer reicht, wenn die Zeit knapp ist):
    - **Price anchor** von „Blended price ~€80“ auf „Inforiver ~€33“: *Paid is the cheapest at around €107*,
      Open source ×1.4, Deneb ×1.6, Core + SVG ×2.4.
    - **Price anchor** auf „Zebra level ~€170“: *Open source is the cheapest at around €148*, Deneb ×1.2,
      Paid ×1.4, Core + SVG ×1.7.
    - **Viewers** von 150 auf 400 (Anker €80): *Open source is the cheapest at around €64*, Deneb ×1.2,
      Paid ×1.3, Core + SVG ×1.7. Lizenzen skalieren mit Köpfen, Stunden nicht.
    - Danach Szenario-Button erneut klicken, um auf 5 / 150 zurückzusetzen.
5. Abschluss: *„Send me your four numbers, you get the link with your preset.“* (Folie 13, Punkt 5)
   → Button „Copy link with settings“ zeigen.

Parität mit Open Source bei ca. **92 €** je User und Jahr. Das ist die Verhandlungsobergrenze, nicht der Listenpreis.

---

## 5 · Merksätze für die Fragerunde

- Lizenzkosten Power BI Pro/PPU/Fabric sind **nicht** enthalten: gleich für alle Stacks und größer als
  jede gezeigte Differenz.
- Stundensatz 125 €/h voll belastet, Listenpreise, keine Eskalation, keine Abzinsung.
- PDF-Export oder Abo Pflicht (Board Pack) → Sprossen 1, 4 oder 5b; 5a heute raus.
- Daten sind synthetisch, auf den Cent abgestimmt (`reconciliation.txt`, Appendix A10).
- IBCS® ist eine eingetragene Marke des IBCS Institute; die Inhalte sind nicht von IBCS zertifiziert.
