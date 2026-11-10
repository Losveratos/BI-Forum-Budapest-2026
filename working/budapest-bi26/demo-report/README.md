# Demo report: one model, one page per rung

Report: `PnL Demo\Budapest BI Forum.Report` (PBIR, byPath → `PnL ChartkitchenDemoKit.SemanticModel`).
Built 2026-11-08 with `pbir` (pages, visuals, filters, conditional formatting) and direct TMDL edits
(`te` preview expired). Each rung page is a copy of "Plan gap": same slicers, same page filter
(months 1–10), same title and footer boxes, only the two tiles differ.

| Page | Rung | Tiles |
|---|---|---|
| 1 Pure Power BI | Core visuals | Matrix (L1 EN × AC/PY/PL/ΔPL/ΔPL %, data bars, red/green rule) · column chart revenue by month AC vs PY · bar chart revenue by company AC vs PL |
| 2 DAX only | Text measures | Matrix with `ΔPL bar (text)` (unicode blocks) and font colour from `ΔPL status` · company table with `Revenue sparkline (text)` |
| 3 SVG measures | SVG from DAX | Matrix with `ΔPL SVG` (variance bar, zero line) · company table with `Revenue AC vs PL SVG` (AC columns, PL outline) |
| 4 Deneb | Vega-Lite | Two Deneb visuals (`r4months`, `r4companies`): AC columns, PL outline, ΔPL below the zero line on the same y scale; spec in `deneb/integrated-variance.vl.json`, full visual.json in `deneb/r4months.visual.json`. Deneb GUID registered in `report.json` `publicCustomVisuals`; Desktop pulls it from AppSource on load |
| Plan gap, Group P&L, … | Custom visual open | existing ChartKitchen / P&L Statement pages |

## Model additions (`fact-abschluss.tmdl`, display folder "Budapest demo")

- `AC signed`, `PY signed`, `PL signed`, `FC signed`: `SUMX(fact × RELATED(SignConvention))` restricted to `RowType = "account"`, so core visuals get revenue positive and costs negative without knowing the sign convention.
- `ΔPL`, `ΔPL %`, `ΔPY`, `ΔPY %`: variances where positive is always good (format `+#,##0;-#,##0;-`).
- `ΔPL bar (text)`, `Revenue sparkline (text)`, `ΔPL status`: rung 2.
- `ΔPL SVG`, `Revenue AC vs PL SVG`: rung 3, `dataCategory: ImageUrl`, data-URI SVG with `%23` for `#`.
- `dim-konten[L1 Sort]`: calculated column (min SortOrder per German `L1`, which maps 1:1 to `L1 EN`) and `sortByColumn: 'L1 Sort'` on `L1 EN`, so the matrix shows the statement in statement order. Computing it over `L1 EN` itself is a circular dependency; Desktop refuses to load.
- Because `L1 EN` now carries a sort column, every matrix row filters `L1 EN` and `L1 Sort`. Scaling measures therefore use `ALLSELECTED('dim-konten'[L1 EN], 'dim-konten'[L1 Sort])`; with the single column every bar was full length.
- SVG coordinates use `FORMAT(x, "0.0", "en-US")`: under de-DE the decimal comma makes the `<rect>` invalid and only integers (zero line) render.

## Known limits to say out loud in the demo

- Rung 1: no plan outline, no variance panel on base scale, labels unformatted unless each measure carries a format string.
- Rung 2: unicode bars need a monospace font and break on proportional fonts; no scale band.
- Rung 3: SVG size is fixed per cell, no tooltips, PDF export rasterises; a UDF library would shorten the two measures.
- Rung 4: Deneb is Microsoft-certified, spec is code in the repo, but not everyone reads Vega. Vega-Lite gotchas met here: a `rule` layer inherits a shared `x` encoding and turns into per-category ticks, so put `x` on the bar/text layers only; a true base scale needs one layer with one y scale (variance bars hang from a computed `dBase = -0.3 * max(AC)`), `vconcat` panels get their own scale.

## Status 2026-11-08

Pages 1–3 render in Desktop (checked via `pbir desktop screenshot`); captures cropped to the page are in `working/budapest-bi26/assets/demo-rung{1,2,3}-*.png` and sit on deck slide 8 and appendix A2–A4. Captured with Desktop application language set to English (File > Options > Regional settings); number formatting still follows the de-DE model culture (decimal comma, dot as thousands separator). Page 4 (Deneb) renders both visuals after a report-only `pbir desktop refresh`; no Desktop restart needed for a new AppSource visual. `pbir validate --qa` passes (10 pages, 87 visuals).

## v2 after the seven reviews (2026-11-09)

- Page filters: `dim-datum[Period Status] = Actual` on all eight filtered pages instead of `MonatNr 1..10`; the Deneb page has no page filter and shows Jan..Dec with FC.
- Measures (`scripts/budapest_measures.py` rewrites the whole "Budapest demo" folder): signed measures in EUR m, restricted to the income statement, summed over `VALUES(SignConvention)` with `CALCULATE(SUM())`; `ΔPL`/`ΔPY` compare against plan/PY of actual months only; `Revenue AC&FC` and `FC flag` read `Period Status`; sparkline and SVG iterate `PeriodeSort`; favourable colour `#2E8B7A` (teal, as ChartKitchen); SVG variance bar with a double zero line (PL reference); `ΔPL (bar)` for a separate data-bar column; `Data as of` stamp; `Revenue AC/PY/PL/AC&FC mEUR` for charts, tables and Deneb.
- Pages 1–3: titles who/what/when, column order PY · PL · AC · ΔPL, subtotal label "Net income", font 10, Consolas for the text bars, stamp card under the title.
- Deneb page: Business Chart Builder templates "Integrated variance" (months, AC&FC vs PL, FC dashed) and "Structural variance analysis" (companies); field names without parentheses because Deneb cannot read `datum["… (mEUR)"]` in expressions.
- Model culture is now `en-US`: Desktop refuses the change on an existing model, so the local cache (`.pbi/cache.abf`, backed up under `_backup_20261107_budapest/cache_20261109/`) was deleted and the model rebuilt from TMDL. Display formatting in Desktop still follows the Windows region (decimal comma in the matrix); DAX text conversion is en-US, which the SVG library needs. Format-string scaling (`#,0.0,,`) was unreliable; the measures divide by 1,000,000 instead.
- UDF (rung 3): `PowerofBI.IBCS` 0.11.0 from daxlib.org installed as `definition/functions.tmdl`, compatibility level 1702. Measures `ΔPL UDF` (BarChart.AbsoluteVariance) and `ΔPL % UDF` (BarChart.RelativeVariance) sit next to the hand-written `ΔPL SVG` in the rung-3 matrix; convention `main = |PL| + ΔPL, base = |PL|` so the function draws exactly ΔPL. `Revenue months UDF` (ColumnChart.WithAbsoluteVariance) was tested in a month-column matrix and removed again: labels did not match the mEUR inputs. Guide: `udf-ibcs-anleitung.md` (matrix, new card, button slicer).
- Deneb: the two Business Chart Builder templates now bind `Revenue ACFC mEUR` / `Revenue PL mEUR` (no `&`, no parentheses) in field entries **and** in the `datum["…"]` expressions; the earlier `+0.0` variances came from expressions still pointing at the old names.
- Still open: budget rate (`Kurs Budget`, `AC @BUD`, FX row), subtotals in the core matrices, month-end scene, button-slicer/new-card demo page.

## v3 model additions (2026-11-10)

Model only (TMDL edited by hand, `te` expired); no report files touched. Backup of `definition/` and all demokit CSVs/scripts before the change: `PnL Demo/_backup_20261107_budapest/v3_before/`. **Do not run `scripts/budapest_measures.py` any more**: it rewrites the "Budapest demo" folder and would delete the UDF and all v3 measures.

All expected values below: income statement, Jan..Oct 2026 (`Period Status = Actual`), EUR m, signed (positive is favourable). They were computed in Python from the CSVs and then confirmed with DAX queries against the loaded model in Desktop (ADOMD on the local msmdsrv port).

### 1. Budget rate and FX effect ("current rate vs budget rate")

- Data: new column `Kurs Budget` in `fact-kurse.csv` (`demoData/demokit`), units of local currency per 1 EUR like the other rates, one fixed rate per currency and year: mean of the Oct–Dec average rates of the prior year; 2025 (no prior year in the rate table) uses the January 2025 average rate; EUR = 1. Added to the generator (`generate_demokit.py`, `budget_rate()`); a full generator run in a scratch copy reproduced every other CSV byte for byte, so the facts are unchanged.
- Model: column `'fact-kurse'[Kurs Budget]` (double, summarize none), type added to the partition's M step.
- Conversion direction from `engine.py`: EUR = LW / rate. Measures (display folder `Budapest demo\FX`, all in table `fact-abschluss`):
  - `AC signed @BUD`: actuals in local currency (`AC LW Wert`) / `Kurs Budget`, iterated over company currency × year (SUMMARIZE over `'dim-gesellschaft'[Währung]`, `'dim-datum'[Jahr]`), so it works with several currencies and years in the filter.
  - `PL signed @BUD`: plan in local currency (`PL LW Wert`) / `Kurs Budget`.
  - `FX effect` = `AC signed` − `AC signed @BUD`.
  - `ΔPL @BUD` = `AC signed @BUD` − `PL signed @BUD` (plan of actual months only, like `ΔPL`): the operating variance without currency.
  - `Revenue AC @BUD mEUR`, `Revenue FX effect mEUR` (Net revenue only).
- Decision: in this demo the EUR plan (`PL Wert`) was converted at the actual average rate, not a budget rate. So `ΔPL` (AC vs stored plan) already contains almost no currency effect, and `ΔPL @BUD` is computed against a plan *re-translated* from plan local currency at the budget rate. `ΔPL` ≠ `FX effect` + `ΔPL @BUD` exactly; the gap is the plan's own translation difference (PL − PL @BUD, e.g. +14.2 on Net revenue). Say it honestly: "FX effect = what the rate moves did to our actuals".

| Jan..Oct 2026 | AC | AC @BUD | FX effect | PL | PL @BUD | ΔPL | ΔPL @BUD |
|---|---:|---:|---:|---:|---:|---:|---:|
| Net revenue, group | 2,817.6 | 2,803.3 | +14.3 | 2,782.1 | 2,767.9 | +35.5 | +35.4 |
| Net income, group | 151.6 | 150.8 | +0.8 | 176.3 | 175.3 | −24.7 | −24.5 |

Net revenue by company (EUR m): Automation DE 661.9 / 661.9 / 0.0 · Energy DE 550.6 / 550.6 / 0.0 · Mobility FR 371.0 / 371.0 / 0.0 · Automation CH 203.2 / 198.8 / +4.4 · Energy PL 166.2 / 163.2 / +3.0 · Automation CZ 141.4 / 138.6 / +2.7 · Industries US 481.9 / 477.7 / +4.2 · Mobility AU 149.5 / 148.6 / +0.9 · Digital JP 92.0 / 92.8 / −0.8 (AC / AC @BUD / FX effect). EUR companies have FX effect 0 (shown as "-" by the format string).

### 2. Subtotals for the core matrices

- Calculated table `'pnl-lines'` (`tables/pnl-lines.tmdl`, `ref table` in `model.tmdl`, no relationship), built by DAX from `dim-konten` (Statement = Income statement, RowType `account` or `formula`), 14 rows. Columns: `Line` (text, sorted by `Line Sort`), `Line Sort` (= `L1 Sort`, hidden), `Line Type` (`line` | `subtotal`), `Upto Sort` (hidden; a subtotal sums all L1 positions with `L1 Sort` < `Upto Sort`).
- Order: Net revenue 40 · Cost of sales 250 · **Gross profit** 460 · Selling expenses 510 · Administrative expenses 630 · Research & development 810 · Other operating result 890 · **EBITDA** 970 · Depreciation & amortisation 1020 · **EBIT** 1080 · Financial result 1120 · **EBT** 1190 · Income taxes 1220 · **Net income** 1270. The subtotal names are the `L1 EN` labels of the formula rows in `dim-konten` (so "EBT", not "Profit before tax").
- Measures (folder `Budapest demo\Statement`): `AC line`, `PL line`, `PY line`, `ΔPL line`, `ΔPL % line`, `ΔPL line status` (`#2E8B7A` / `#C0392B`). `line` rows = signed measure with `'dim-konten'[L1 EN]` = Line (TREATAS); `subtotal` rows = running sum by `L1 Sort`. `PL line` and `PY line` are restricted to actual months (like `ΔPL`), so AC/PL/ΔPL are comparable even without a page filter. Without a single line in context (matrix total) they return BLANK; switch the matrix total off, Net income is its own row.
- Expected AC / PL / ΔPL: Gross profit 942.8 / 957.0 / −14.2 · EBITDA 400.5 / 424.2 / −23.7 · EBIT 256.3 / 280.9 / −24.5 · EBT 206.5 / 239.2 / −32.6 · Net income 151.6 / 176.3 / −24.7 (matches `reconciliation.txt`).

### 3. Month-end close scene (one adjustment, one switch)

- Data: `demoData/demokit/fact-nachbuchung.csv` (columns `AccountID;EntityID;Datum;Monat;AC Wert;AC LW Wert;Text`), exactly one row: `G-oth_rst_aufloesung` (release of provisions, Other operating result, SignConvention +1), EntityID `1300` (Mobility FR, EUR), 2026-10-31, +4,000,000 EUR in both value columns. Also written by `generate_demokit.py` (`write_fact_nachbuchung()`).
- Model: table `fact-nachbuchung` (`tables/fact-nachbuchung.tmdl`, M partition like the other CSVs; columns `AccountID`, `EntityID`, `Datum`, `Monat`, `AC Wert` and `AC LW Wert` hidden, `Text`), relationships to `dim-konten[AccountID]`, `dim-gesellschaft[EntityID]`, `dim-datum[Datum]`.
- Switch: calculated table `'close-status'`, column `Close status` ("Closed WD3", "Incl. day-3 adjustment", sorted by hidden `Close status Sort` 1/2), no relationship. Measure `Adjustment on` (folder `Budapest demo\Close`) = SELECTEDVALUE = "Incl. day-3 adjustment".
- `AC` = SUM(AC Wert) + hidden `AC adjustment`; `AC LW` likewise with `AC LW adjustment`. The adjustment measures pass the `fact-abschluss[Monat]` filter (period role of the P&L visual) to the adjustment table via TREATAS. `AC signed`, `EBITDA AC` and `AC signed @BUD` go through these, so `ΔPL`, `ΔPL %`, SVG/UDF measures, line measures and the custom visuals follow automatically. `Revenue AC` is unaffected (the booking is not revenue). `Data as of` now contains " · close status: closed WD3" or " · incl. day-3 adjustment".
- Without a selection (default) or with "Closed WD3" every number is exactly as before (checked: Net income 151.6, Net revenue 2,817.6).
- With "Incl. day-3 adjustment": Net income 151.6 → **155.6**, Other operating result 1.5 → 5.5, EBITDA 400.5 → 404.5, EBIT 260.3, EBT 210.5, group ΔPL −24.7 → −20.7, EBITDA ΔPL −23.7 → −19.7. Mobility FR: net income −5.5 → −1.5, ΔPL −9.2 → −5.2, EBITDA 26.0 → 30.0 (ΔPL −12.8 → −8.8). Only October 2026 moves.

### Known limits

- The adjustment is applied by measure, not by data: visuals or measures that sum `fact-abschluss[AC Wert]` directly (`Revenue AC`, `AC Stichtag`, balance sheet/cash flow) do not see it; for this one P&L booking that is correct, but there is no balance-sheet counter entry (provision release would reduce provisions).
- A single-select slicer on `'close-status'[Close status]` is needed; with both values selected `Adjustment on` is FALSE.
- Line measures need `'pnl-lines'[Line]` on rows; combined with `dim-konten` on rows they are meaningless.
- Desktop: with the screen locked, the "Refresh now" load dialog stayed on "Evaluating..." although the engine had finished (partitions Ready), and Desktop then blocked the pbir bridge ("Another operation is already in progress"). Workaround used: restart Desktop and run a TMSL full refresh directly against the local msmdsrv port (ADOMD from the Desktop `bin` folder). Desktop does not know about that refresh, so its yellow banner "Some of the tables have incomplete or no data" may still show and the file is marked unsaved: click Refresh once (or save) before presenting so `.pbi/cache.abf` holds the new tables. Checked after the refresh: page "1 Pure Power BI" unchanged (Net revenue AC 2,817.6, PL 2,782.1, Net income 151.6), "Group P&L" renders.

## v3 report additions (2026-11-10)

Report `Budapest BI Forum.Report` (PBIR, edited with `pbir`; a few properties without a pbir command were patched in visual.json: stale selectors, sync group, slicer image, textbox paragraphs). Screenshots are in `assets/` (names below).

### Subtotals in the core matrices (pages 1 to 3)
- `r1matrix`, `r2matrix`, `r3matrix`: rows `pnl-lines.Line` (sorted ascending), row grand total off, Statement filter removed (the line table has no relationship to `dim-konten`). Values: r1 `PY line, PL line, AC line, ΔPL line, ΔPL % line`; r2 `PL line, AC line, ΔPL line, ΔPL % line`; r3 `PL line, AC line, ΔPL line`. Font colour of `ΔPL line` and `ΔPL % line` is measure CF from `ΔPL line status` (r1, r2) and of `ΔPL line` (r3).
- Dropped because they do not work in the line context: `ΔPL (bar)` (data bars), `ΔPL bar (text)`, `ΔPL SVG`, `ΔPL UDF`, `ΔPL % UDF`, `ΔPL %` (they depend on `dim-konten[L1 EN]` in scope). Tested for r3: every row showed the same -24.7 bar and -14.0 label, so they were removed. Consequence: the left matrix on "3 SVG measures" no longer shows SVG/UDF images; the SVG story there is carried by `r3spark` (company columns). To bring it back, add line-based measures to the model (for example `ΔPL SVG line`, `ΔPL UDF line`) built on `PL line` / `ΔPL line` and `'pnl-lines'[Line]`, then bind them to `r3matrix`.
- Subtotal rows (Gross profit, EBITDA, EBIT, EBT, Net income) cannot be made bold per row in a matrix; they are plain rows. Seen in the screenshots (Jan..Oct 2026, AC / PL / ΔPL): Gross profit 942,8 / 957,0 / -14,2; EBITDA 400,5 / 424,2 / -23,7; Net income 151,6 / 176,3 / -24,7.

### Close switch
- Slicer `closeslicer` (dropdown, single select, no "select all", x 27, y 603, 246 x 78, copy of the Company slicer style) on `close-status.Close status` on pages Group P&L, Plan gap, 1, 2, 3, 4, FX and close, Card and slicer. All carry the same `syncGroup` `dwg-close-status` (filter and field changes), so one selection applies to all pages. If Desktop does not show them synced: View › Sync slicers, group `dwg-close-status`.
- Check (`demo-close-adjusted.png`): page 1 with page filter `Close status = Incl. day-3 adjustment`: Net income 155,6, EBITDA 404,5 (temporary filter removed again).

### New page "FX and close" (after "4 Deneb")
- Title box "FX and close / Model rules", stamp card, slicer column as on the rungs, page filter `Period Status = Actual`.
- `fxmatrix`: rows `dim-gesellschaft.Short name`, values `Revenue AC mEUR, Revenue AC @BUD mEUR, Revenue FX effect mEUR, Revenue PL mEUR`, total labelled "Total". Seen: total 2.817,6 / 2.803,3 / +14,3 / 2.782,1; Automation CH +4,4, Energy PL +3,0, Automation CZ +2,7, Industries US +4,2, Mobility AU +0,9, Digital JP -0,8, DE/FR companies "-".
- `fxpnl`: rows `dim-konten.L1 EN` (sorted ascending, Statement = Income statement), values `AC signed, AC signed @BUD, FX effect, ΔPL, ΔPL @BUD`, total label "Net income". Seen: Net income 151,6 / 150,8 / +0,8 / -24,7 / -24,5; Net revenue 2.817,6 / 2.803,3 / +14,3 / +35,5 / +35,4.
- Screenshot: `demo-fx-close.png`.

### New page "Card and slicer" (after "FX and close") – image binding does NOT render
- Built: `cs_slicer` (`advancedSlicerVisual`, Values `dim-gesellschaft.Short name`, 3 columns) and `cs_card` (`cardVisual`, Data `Revenue AC mEUR` and `Revenue PL mEUR`, Rows `dim-gesellschaft.Short name`, two columns). Both without images. Screenshot: `demo-card-slicer.png` (callouts, e.g. Automation DE 661,9 / 632,1).
- Not working: the IBCS image per button and card. Tried: (1) report extension measure `Company bars UDF` via `pbir dax measures add --data-category ImageUrl` (the report is byPath/thick; no image appeared; measure removed again), (2) `image.imageUrl` on the card via `pbir visuals cf` plus `imageType = imageUrl`, `show`, `imageAreaSize`, (3) `image.image` (Measure expression) and `sourceType = imageUrl` on the slicer, (4) with the existing model measures `ΔPL UDF` and `Revenue AC vs PL SVG` (the latter works in the matrix; added to the card Data it showed the `data:image/svg+xml` text, so the measure is fine), also with the measure added to Tooltips/Data. In every variant the card and the buttons showed no image. So the property format for the image field in PBIR is not right yet (or Desktop ignores it); `pbir visuals cf` refuses `image.image` on the slicer ("semantic field slot").
- To finish: set up one image once in Desktop (Format › Image › Image type = Image URL › fx › field value) on a copy of the card and slicer, save, and read the resulting `image` object from visual.json; then reuse it. The needed model measure (the model must not be changed by this run): `Company bars UDF = PowerofBI.IBCS.BarChart.WithAbsoluteVariance ( [Revenue AC mEUR], [Revenue PL mEUR], 'dim-gesellschaft'[Short name], 0, 1 )` in `fact-abschluss`, data category ImageUrl. The page text already says "with a model measure ... each button and card carries its own chart".

### Assets written (`assets/`)
`demo-rung1-pure.png`, `demo-rung2-dax.png`, `demo-rung3-svg.png`, `demo-rung4-deneb.png`, `demo-rung2-dax-tile.png`, `demo-rung3-svg-tile.png`, `demo-rung4-deneb-tile.png`, `demo-close-adjusted.png`, `demo-fx-close.png`, `demo-card-slicer.png`. The close-status slicer is visible in all of them. The stamp card ("Data as of") renders empty in the screenshots, as before.

## v3b: line variants for rungs 2 and 3

Moving the matrices to the line table `'pnl-lines'` had dropped the text bar (page 2) and the SVG/UDF columns (page 3), because those measures scale over `'dim-konten'[L1 EN]` and return the same value on every line. Four line variants in `fact-abschluss` (folder `Budapest demo\Statement`) fix this; all scale with `MAXX ( ALLSELECTED ( 'pnl-lines'[Line], 'pnl-lines'[Line Sort] ), ABS ( [ΔPL line] ) )` (both columns, because `Line` is sorted by `Line Sort`):

- `ΔPL line bar (text)`: Unicode block bar around a `│` separator, negative left, positive right. Padding uses `UNICHAR ( 160 )` instead of normal spaces, because the matrix strips leading spaces and the separator would otherwise drift per row.
- `ΔPL line SVG` (ImageUrl): hand-written SVG variance bar, label bold on subtotal lines (`Line Type = "subtotal"`).
- `ΔPL line UDF`, `ΔPL % line UDF` (ImageUrl): `PowerofBI.IBCS.BarChart.AbsoluteVariance` / `RelativeVariance` on `[PL line]`/`[ΔPL line]`, subtotal flag = `Line Type = "subtotal"`. Note: the library draws no bar or pin for rows flagged as total, only the bold value, so Gross profit, EBITDA, EBIT, EBT and Net income show the bold number in the UDF columns.

Page 2 (`r2matrix`): PL, AC, ΔPL, ΔPL %, `ΔPL line bar (text)` (Consolas, colour from `ΔPL line status`, column width 200). Page 3 (`r3matrix`): PL, AC, ΔPL, `ΔPL line SVG` (170), `ΔPL line UDF` (250), `ΔPL % line UDF` (170), new title "… hand-written SVG next to PowerofBI.IBCS UDF, subtotals from a line table". Check values Jan..Oct 2026: Gross profit AC 942.8 / ΔPL −14.2, EBITDA 400.5, Net income 151.6 (155.6 with the day-3 adjustment).

Stamp card (`Data as of`, `r1stamp`…`r4stamp` and the stamps on "FX and close" and "Card and slicer"): the measure was fine; the card was empty because the theme wildcard switches title and subtitle on for every visual, and in a 24 px card the (empty) title and subtitle took all the height, pushing the value out. Fix: title and subtitle off, word wrap off, container padding 0, position y 88, height 34. The stamp now reads as one line under the page title in all assets.

Assets rewritten: all page images, the three tiles and `demo-close-adjusted.png`. After restarting Desktop the tables were empty; the data was loaded with a TMSL full refresh sent to the local engine (TOM from DAX Studio, port from the `msmdsrv` process).
