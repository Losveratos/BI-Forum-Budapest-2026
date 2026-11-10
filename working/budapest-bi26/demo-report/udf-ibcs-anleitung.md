# IBCS-Charts mit DAX-UDFs: PowerofBI.IBCS in Matrix, neuer Karte und Button-Slicer

Stand 09.11.2026 · Paket `PowerofBI.IBCS` 0.11.0 (Andrzej Leszkiewicz, MIT, https://daxlib.org/package/PowerofBI.IBCS/) ·
getestet im Demo-Modell `PnL ChartkitchenDemoKit.SemanticModel` (Sprosse 3 der Budapest-Leiter).

## 1. Was das Paket ist

Zwölf DAX-Funktionen (User-Defined Functions), die SVG-Bilder als `data:image/svg+xml`-URI zurückgeben:
Balken mit absoluter und relativer Abweichung, Säulen je Monat mit Plan-Umriss und Forecast-Schraffur,
vertikaler GuV-Wasserfall, Small Multiples, gestapelte Säulen, ein Titel-Helfer. Die Bilder werden von
Core-Visuals gerendert, die Bilder aus Measures anzeigen können: Matrix, Tabelle, **neue Karte** (`cardVisual`),
**Button-Slicer** (`advancedSlicerVisual`), Listen-Slicer, Bild-Visual. Kein Custom Visual, kein AppSource,
der ganze „Visual“ ist Text im Modell.

Nicht von IBCS® produziert oder zertifiziert; der Autor ist IBCS-zertifizierter Analyst.

## 2. Voraussetzungen

| Punkt | Warum | Im Demo |
|---|---|---|
| Kompatibilitätslevel **1702** (`database.tmdl`) | UDFs gibt es erst ab 1702 (GA Juni 2026) | von 1606 angehoben |
| `definition/functions.tmdl` | enthält die zwölf Funktionen; Datei aus dem `.daxpkg` (ZIP) kopieren: `lib/functions.tmdl` | kopiert, keine Änderung |
| Modellkultur **en-US** (`model.tmdl`: `culture: en-US`) | Die Funktionen setzen Zahlen per `&` in den SVG-Text. Unter de-DE entsteht `y='4,4'`, das SVG verwirft das Rechteck; es bleiben nur Achsen und Labels. | Desktop ändert die Kultur eines bestehenden Modells nicht („Culture … may be changed only before any other object has been created“). Lösung: `.pbi/cache.abf` löschen, Kultur im TMDL setzen, Desktop baut das Modell neu auf und lädt die Daten nach. |
| Measure mit `dataCategory: ImageUrl` | sonst zeigt die Matrix den Data-URI als Text | an allen UDF-Measures gesetzt |
| Bildgröße im Visual | Matrix: Format › Grid › Image height; Spaltenbreite ≈ `imageWidth` der Funktion | Matrix 22 px / 240 px und 170 px |

Installation ohne Tabular Editor: `.daxpkg` ist ein ZIP. `lib/functions.tmdl` nach `definition/` kopieren, Level auf 1702 setzen,
Desktop neu starten. Mit Tabular Editor 3: DAX Lib › Install package.

## 3. Konvention für Vorzeichen und Skalierung (wichtig für GuV)

Die Funktionen rechnen `Varianz = Hauptwert − Basis` und färben über `businessImpact` (1 = positiv ist gut, −1 = Kosten).
Mit vorzeichenrichtigen Measures (`AC signed`, `PL signed`: Kosten negativ, `ΔPL` positiv = günstig) gilt:

```dax
ΔPL UDF =
IF ( ISBLANK ( [ΔPL] ), BLANK (),
    PowerofBI.IBCS.BarChart.AbsoluteVariance (
        'dim-konten'[L1 EN],                 -- Zeilen-Dimension
        ABS ( [PL signed] ) + [ΔPL],         -- Hauptwert: so ist Hauptwert − Basis genau ΔPL
        BLANK (),                            -- kein FC-Anteil
        ABS ( [PL signed] ),                 -- Basis positiv, sonst kippt die Prozentrechnung bei Kosten
        MAXX ( ALLSELECTED ( 'dim-konten'[L1 EN], 'dim-konten'[L1 Sort] ), ABS ( [ΔPL] ) ),  -- Skala über alle Zeilen
        "outlined",                          -- Doppellinie = Plan-Referenz (IBCS)
        NOT ISINSCOPE ( 'dim-konten'[L1 EN] ),  -- Summenzeile fett
        FORMAT ( [ΔPL], "+#,##0.0;-#,##0.0;=", "en-US" ),
        240, 22, 1 ) )
```

Drei Fallen:

1. **Sortierspalte.** Hat die Zeilen-Spalte eine `sortByColumn`, filtert jede Matrixzeile beide Spalten. `ALLSELECTED ( dimensionColumn )`
   in der Funktion hebt nur eine davon auf, die Skala wird je Zeile neu berechnet und alle Balken gleich lang. Deshalb die
   Skala selbst als `scaleValueExpr` übergeben, mit `ALLSELECTED` über beide Spalten.
2. **Formelzeilen.** Die Funktion liefert auch für leere Werte ein Bild (Nulllinie, Label „=“); dadurch tauchen Gross profit,
   EBITDA usw. als Zeilen auf. Daher der `IF ( ISBLANK … )`-Mantel.
3. **Label-Format.** `FORMAT ( x, "+#,##0.0;…", "en-US" )` mit explizitem Kulturparameter; der Rest der Funktion braucht die Modellkultur en-US (Punkt 2).

## 4. Rezepte je Visual

### Matrix (Sprosse 3 im Demo-Report)

Zeilen `dim-konten[L1 EN]`, Werte `PL signed · AC signed · ΔPL · ΔPL UDF · ΔPL % UDF`. Grid › Image height 22,
Spaltenbreiten 240 / 170 (pbir: `columnWidth.field(fact-abschluss.ΔPL UDF).value`). Summenzeile „Net income“ (Subtotals › Row subtotals label).
Monatssäulen: Matrix mit **Spalten** `dim-datum[Month Short]`, Wert `Revenue months UDF` =
`PowerofBI.IBCS.ColumnChart.WithAbsoluteVariance ( [Revenue AC mEUR], [Revenue PY mEUR], [Revenue PL mEUR], [Revenue FC mEUR], 'dim-datum'[Month Short], 1 )`,
Image height 300, Spalten nach `Month Short` sortieren. Jede Zelle ist eine Säule, die Matrix setzt das Chart zusammen.

### Neue Karte (`cardVisual`)

1. Visual „Karte (neu)“, Feld **Data** = ein Measure, das ein Bild liefert, z. B. `ΔPL UDF` oder
   `PowerofBI.IBCS.BarChart.WithAbsoluteVariance ( [Revenue AC mEUR], [Revenue PL mEUR], 'dim-gesellschaft'[Short name], 0, 1 )`.
2. Format › **Image** › Image type = *Image URL*, Image = fx › Feldwert › das Measure; Fit = *Fit*; Image area size ≈ 60 %.
3. Format › Callout value: Measure `Revenue AC mEUR` mit `Revenue PL mEUR` als Referenzlabel; Titel über `PowerofBI.IBCS.Helpers.Title ( "Revenue in mEUR", "by company", "Jan..Oct 2026 AC and PL" )` als Measure in die Titelzeile.
4. Small Multiples: Format › Layout › Rows/Columns; **Rows**-Feld = `Short name`, dann eine Karte je Gesellschaft mit eigenem Bild.

PBIR (pbir CLI): `pbir add visual cardVisual "<Page>" -d "Data:fact-abschluss.Revenue AC mEUR" -d "Rows:dim-gesellschaft.Short name"`, dann
`pbir visuals cf "<Visual>" --measure "image.imageUrl fact-abschluss.<Bild-Measure>"` und `pbir set "<Visual>.image.imageType" --value imageUrl -f`.

### Button-Slicer (`advancedSlicerVisual`)

Der Slicer bleibt ein Slicer (Auswahl filtert die Seite), zeigt aber je Button ein IBCS-Chart.

1. Visual „Slicer (neu)“ / Button-Slicer, Feld **Values** = `dim-gesellschaft[Short name]`.
2. Format › **Image** › Image type = *Image URL* › fx › Feldwert = Measure, z. B.
   `Company bars UDF = PowerofBI.IBCS.BarChart.WithAbsoluteVariance ( [Revenue AC mEUR], [Revenue PL mEUR], 'dim-gesellschaft'[Short name], 0, 1 )`
   oder für drei Ebenen (Säulen, Wasserfall, Pins) `PowerofBI.IBCS.ColumnChart.WithWaterfall` (Parameter siehe `functions.tmdl`, Zeile 1941).
3. Format › Layout: Buttons per row 3, Shape rectangle, Image area size 70–85 %, Label unten (`label.position`).
4. Sortierung: Measure in **Tooltips** legen und danach sortieren (das Paket nutzt diesen Trick bei `SmallMultiple`, Parameter `sortOrderExpr`).
5. Die Funktion skaliert über `ALLSELECTED ( dimensionColumn )`: alle Buttons haben dieselbe Skala, solange kein Button gewählt ist; nach Auswahl skaliert sie neu (IBCS: dann Skalenband erwähnen).

PBIR: `pbir add visual advancedSlicerVisual "<Page>" -d "Values:dim-gesellschaft.Short name"`, dann
`pbir visuals cf "<Visual>" --measure "image.image fact-abschluss.Company bars UDF"` (Property `image.image`, Typ „Field“),
`pbir set "<Visual>.layout.columnCount" --value 3 -f`.

## 5. Grenzen, die man im Vortrag sagen sollte

- Kultur: Pakete von daxlib.org sind auf en-US-Modelle geschrieben; in de-DE-Modellen liefern implizite Zahl→Text-Konvertierungen Dezimalkommas. Prüfen, bevor man ein Paket in ein Bestandsmodell nimmt.
- Export: PDF/PPT-Export aus dem Service rastert die Bilder; „Daten exportieren“ liefert den Data-URI als Text.
- Keine Tooltips, keine Interaktion im Bild; Auswahl nur über den Slicer-Button, nicht über Chart-Elemente.
- Eine Funktion lebt je Modell. Zwanzig Modelle heißt zwanzigmal installieren und updaten (Rechner: Core +209 %).
- Release 0.11.0 hat Parameter gegenüber älteren Versionen geändert; beim Update die Aufrufe prüfen (Release Notes im Manifest).
- UDFs haben keine Display Folders, keine Übersetzungen, keine vererbte OLS (Microsoft Learn, UDF considerations).

## 6. Dateien

- Paket entpackt: `functions.tmdl` im Modell (`PnL ChartkitchenDemoKit.SemanticModel/definition/functions.tmdl`)
- Measures: Ordner „Budapest demo\UDF“ in `fact-abschluss.tmdl` (`ΔPL UDF`, `ΔPL % UDF`, `Revenue months UDF`, `Revenue FC mEUR`)
- Seite „3 SVG measures“: Matrix `r3matrix` (handgeschriebenes SVG neben UDF), `r3cols` (Monatssäulen)
