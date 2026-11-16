# Finance Reporting in Power BI: One Model, Three Visual Stacks Compared

Talk by Michael Tenner at the Budapest BI Forum 2026, Tuesday 17 November 2026, Danubius Hotel Helia, Budapest (English).
Session page: <https://budapestbi.hu/bi26/sessions/finance-reporting-in-power-bi-one-model-three-visual-stacks-compared/>

**In one line:** one finance semantic model (AC, PY, PL, FC; MTD/YTD/FY; local vs. group currency; current vs. budget rate), the same dashboard built on several visual stacks, compared on IBCS fit, performance, cost, maintainability and self-service with AI.

## Slides

| Format | File |
|---|---|
| HTML deck (25 slides, open in a browser) | [`working/budapest-bi26/story-v2.html`](working/budapest-bi26/story-v2.html) |
| PDF | [`working/budapest-bi26/One-Model-Three-Visual-Stacks.pdf`](working/budapest-bi26/One-Model-Three-Visual-Stacks.pdf) |
| PowerPoint | [`working/budapest-bi26/One-Model-Three-Visual-Stacks.pptx`](working/budapest-bi26/One-Model-Three-Visual-Stacks.pptx) |

HTML deck keys: right arrow, space or click = next step; left arrow = back; `O` or Esc = overview; Home / End = first / last slide.
The PDF and PPTX are rendered from the HTML deck. The PPTX holds each slide as a picture, with the headline as title and the slide text in the notes.

## The demo: one model, one report page per rung

| Rung | Approach | Report page |
|---|---|---|
| 1 | Pure Power BI: core visuals only | `1 Pure Power BI` |
| 2 | DAX only: text measures (Unicode bars, sparklines) | `2 DAX only` |
| 3 | SVG measures, plus the DAX UDF library `PowerofBI.IBCS` by Andrzej Leszkiewicz (MIT, [daxlib.org](https://daxlib.org/package/PowerofBI.IBCS/)) | `3 SVG measures` |
| 4 | Deneb (Vega-Lite) with Business Chart Builder templates | `4 Deneb` |
| 5a | Open custom visuals: ChartKitchen and P&L Statement byDatenWG | `5a Custom visual` (also `Group P&L`, `Plan gap`, `Nine companies, seven currencies`, `Full-year outlook`, `Balance sheet`, `Cash flow`) |
| 5b | Paid custom visual: Zebra BI Tables | `5b Zebra BI` |

The report has 21 pages. Besides the rung pages above it has `FX and close` (budget rate and FX effect, a month-end adjustment switch) and `Card and slicer`, and seven pages at the end: `Scenarios 1 Core`, `Scenarios 2 DAX`, `Scenarios 3 SVG + UDF`, `Scenarios 4 Deneb`, `Scenarios 5a Custom`, `Scenarios 5b Zebra` and `Complications`. The six Scenarios pages show Revenue AC vs PL vs PY by month and by company, once per rung (the Zebra page has not been confirmed to render). `Complications` is a table of nine hidden complexities of a finance report and where each rung solves them. The deck additionally shows Fabric Apps (appendix); they are not part of the demo project.

### Open it

1. Install Power BI Desktop and enable the preview features for Power BI projects (PBIP) and the enhanced report format (PBIR) under Options > Preview features.
2. Open `demo/Budapest BI Forum.pbip`.
3. Set the Power Query parameter `DemoPfad` (Transform data > Manage parameters) to the absolute path of `demo/demoData/demokit`, with a trailing backslash. The shipped value is a placeholder (`C:\path\to\...`).
4. Refresh.

Things to know:

- All measures live in one table, `_Measures` (a Power Query table), with English descriptions. The small table `complications` holds the static text of the `Complications` page.
- The semantic model culture is `en-US` and the compatibility level is 1702. Both are needed for the DAX user-defined functions (UDFs) of `PowerofBI.IBCS` and for the SVG measures (with a decimal comma the SVG breaks). Keep Desktop on a version that supports UDFs.
- The two custom visuals by the speaker, ChartKitchen and P&L Statement byDatenWG, are embedded in the report (`demo/Budapest BI Forum.Report/CustomVisuals/`). Nothing to install.
- Deneb and Zebra BI Tables are AppSource visuals; Desktop loads them from AppSource when the report opens (internet needed). Zebra BI is a commercial product: see the vendor for what works without a licence.
- All data is synthetic: the fictional group DWG Industries, nine companies, seven currencies (EUR, CHF, PLN, CZK, USD, AUD, JPY), 2025 and 2026. Source CSVs and the generator are in `demo/demoData/demokit/` (its README is in German).

## Repository map

| Path | Content |
|---|---|
| `working/budapest-bi26/story-v2.html`, `.pdf`, `.pptx` | The talk (see above). `assets/` holds the images. |
| `working/budapest-bi26/build-exports.py` | Builds the PDF and PPTX from the HTML deck |
| `working/budapest-bi26/demo-report/` | Notes on the demo report, Deneb specs and Business Chart Builder templates, UDF guide |
| `demo/` | Power BI project: semantic model (TMDL), report (PBIR), data (CSV) and generator |
| `material/` | Speaker card |

## Rebuild the PDF and PPTX

```
pip install pymupdf python-pptx
python working/budapest-bi26/build-exports.py
```

Needs Google Chrome or Microsoft Edge (or set `CHROME` to the executable) and internet access for the deck's web font. Use a virtual environment. Details at the top of the script.

## Credits and trademarks

- IBCS(R) is a registered trademark of the IBCS Institute. The presentation and the demo report are inspired by the IBCS standards. They are not produced, reviewed or certified by the IBCS Institute.
- `PowerofBI.IBCS` (DAX UDF library) by Andrzej Leszkiewicz, MIT licence, via [daxlib.org](https://daxlib.org/package/PowerofBI.IBCS/).
- Deneb, Zebra BI and Inforiver are products of their respective owners; names are used for identification only.
- ChartKitchen and P&L Statement byDatenWG are visuals by the speaker (Daten-WG).

## Licence

MIT, see [`LICENSE`](LICENSE). Third-party components keep their own licences.
