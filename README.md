# Finance Reporting in Power BI: One Model, Three Visual Stacks Compared

Speaker: Michael Tenner
Event: Budapest BI Forum 2026, Tuesday 17 November 2026, Danubius Hotel Helia, Budapest (talk in English)

The talk builds one Power BI semantic model for finance reporting (AC, PY, PL, FC; MTD/YTD/FY; local vs. group currency) and shows the same dashboard on several visual stacks, compared on IBCS fit, performance, cost, maintainability and self-service with AI.

## What is in this repository

| Path | Content |
|---|---|
| `working/budapest-bi26/story-v2.html` | Slide deck (current version, 25 slides). Open it locally in a browser. Right arrow, space or click: next step; left arrow: back; `O` or Esc: overview; Home / End: first / last slide. `story.html` is the earlier version. |
| `working/budapest-bi26/One-Model-Three-Visual-Stacks.pdf` | The same deck as PDF, 25 pages. |
| `working/budapest-bi26/calculator-finance-preset-en.pdf` | The Visual Standards Calculator (v0.23) with the scenario "Finance with mandatory IBCS · 5 / 150", level 1 (overview), 7 pages. `…-level2.pdf`: the same with level 2 (volume assumptions, requirements, red flags), 28 pages. Live: [visual-standards-rechner.html?lang=en&preset=finance](https://datenwgknowledgekitchen.com/visual-standards-rechner.html?lang=en&preset=finance). |
| `working/budapest-bi26/DEMO-RUNBOOK.md` / `.pdf` | Speaker runbook for the 40-minute slot (German): timing, pre-flight checklist, live demo page by page with the expected numbers, calculator levers, fallbacks. |
| `working/budapest-bi26/assets/` | Images used by the deck. |
| `working/budapest-bi26/demo-report/` | Documentation of the demo report (one page per rung), Deneb specs, the measure script and a guide for the DAX UDF library. |
| `working/budapest-bi26/BRIEF.md`, `REVIEWS.md`, `reviews-v2/` | Session brief and the expert reviews of the deck (Markdown). The review screenshots are not versioned. |
| `demo/` | Power BI project (PBIP): semantic model (TMDL), report (PBIR, 12 pages), synthetic data as CSV and the generator that wrote it. |
| `material/` | Speaker card. |

## The six rungs

1. Pure Power BI: core visuals only
2. DAX only: text measures (unicode bars, sparklines)
3. SVG measures + UDF: SVG from DAX, plus the PowerofBI.IBCS function library
4. Deneb (Vega-Lite)
5. Custom visual, open and paid
6. Fabric Apps

## Open the demo


1. Open the PBIP in Power BI Desktop.
2. Set the parameter `DemoPfad` to the local folder `demo/demoData/demokit`.
3. Refresh the model.

Deneb is installed from AppSource when the report loads. The UDF library PowerofBI.IBCS comes from daxlib.org (MIT license).

## Notes

- All data is synthetic demo data.
- IBCS(R) is a registered trademark of the IBCS Institute. The content here is not produced or certified by IBCS.
- ChartKitchen and P&L Statement byDatenWG are visuals by the speaker.
- Work in progress: the material changes until the talk.
