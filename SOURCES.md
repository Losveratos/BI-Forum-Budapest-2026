# Sources and credits

**Finance Reporting in Power BI: One Model, Three Visual Stacks Compared**
Michael Tenner · Budapest BI Forum 2026 · Tuesday 17 November 2026 · Danubius Hotel Helia

Everything the talk, the slide deck, the demo report and the cost calculator use or cite. Product facts,
prices and feature states were checked at the dates given; Power BI changes monthly, so check again
before you rely on them. All data in the demo is synthetic.

Session page: <https://budapestbi.hu/bi26/sessions/finance-reporting-in-power-bi-one-model-three-visual-stacks-compared/>
Material: <https://github.com/Losveratos/BI-Forum-Budapest-2026>

---

## 1 · Standards and accounting rules

| Source | Used for | Link |
|---|---|---|
| IBCS® Standards 2.0, IBCS Association, CC BY-SA 4.0 | SUCCESS rules (slide "IBCS on one page"), notation: AC/PY/PL/FC, hatching for forecast, outlined plan, variances on the base scale | <https://www.ibcs.com/standards> |
| IBCS Standards 1.2 | Reference cited by the PowerofBI.IBCS function library | <https://www.ibcs.com/ibcs-standards-1-2/> |
| IBCS certified software list | Which paid visuals carry the certificate | <https://www.ibcs.com/software/> |
| IAS 21 *The Effects of Changes in Foreign Exchange Rates* | Income statement and cash flow at average rate, balance sheet at closing rate; translation difference (slide A9, demo kit) | IFRS Foundation, <https://www.ifrs.org/issued-standards/list-of-standards/ias-21-the-effects-of-changes-in-foreign-exchange-rates/> |
| IAS 7 *Statement of Cash Flows* | Separate line for the effect of exchange-rate changes on cash (demo kit cash flow) | IFRS Foundation, <https://www.ifrs.org/issued-standards/list-of-standards/ias-7-statement-of-cash-flows/> |

The SUCCESS cards in the deck are adapted from the IBCS Standards 2.0 under CC BY-SA 4.0. The speaker is
not an IBCS member and the material is not certified: the notation is used as inspiration, taken literally.

## 2 · Microsoft documentation (Microsoft Learn, checked 09–11/2026)

| Topic | Fact used in the talk | Link |
|---|---|---|
| DAX user-defined functions | GA since June 2026, compatibility level 1702, limitations (translations, display folders, OLS); rung 3 | <https://learn.microsoft.com/dax/best-practices/dax-user-defined-functions> |
| Q&A visual | Q&A retires in February 2027 (summary matrix, rung 1) | <https://learn.microsoft.com/power-bi/natural-language/power-bi-tutorial-q-and-a> |
| Card visual | New card; the legacy card stays available ("Card and slicer" page) | <https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-card> |
| Copilot in Power BI | Needs paid capacity F2+/P1+, no trial, no sovereign clouds; builds and edits reports with core visuals | <https://learn.microsoft.com/power-bi/create-reports/copilot-introduction> · <https://learn.microsoft.com/power-bi/create-reports/copilot-create-reports> |
| Organizational visuals | No PowerPoint export, no subscriptions, not in Report Server | <https://learn.microsoft.com/power-bi/developer/visuals/power-bi-custom-visuals-organization> |
| Visuals admin settings | Tenant approval of custom visuals | <https://learn.microsoft.com/fabric/admin/organizational-visuals> · <https://learn.microsoft.com/power-bi/admin/service-admin-portal-power-bi-visuals> |
| Certified Power BI visuals | What "certified" means (export, subscriptions) | <https://learn.microsoft.com/power-bi/developer/visuals/power-bi-custom-visuals-certified> |
| AppSource licence models | Licence enforcement for paid visuals and where it is absent | <https://learn.microsoft.com/power-bi/developer/visuals/custom-visual-licenses> |
| Fabric Apps | Preview, regions; data-app template (Build + Read, execute-queries tenant setting); rung 6 | <https://learn.microsoft.com/fabric/apps/overview> · <https://learn.microsoft.com/fabric/apps/data-apps-template> |
| Fabric Git integration | Supported items (Fabric Apps not listed yet) | <https://learn.microsoft.com/fabric/cicd/git-integration/intro-to-git-integration> |
| PBIR report format | Report definition as files (the demo report is PBIR) | <https://learn.microsoft.com/power-bi/developer/projects/projects-report> |
| Data point limits, fetch more data | Volume limits per visual type | <https://learn.microsoft.com/power-bi/visuals/power-bi-data-points> · <https://learn.microsoft.com/power-bi/developer/visuals/fetch-more-data> |
| Export data from a visual | Export and audit trail column of the summary | <https://learn.microsoft.com/javascript/api/overview/powerbi/export-data> |
| Accessibility | Keyboard focus, high contrast, accessible report design | <https://learn.microsoft.com/power-bi/developer/visuals/supportskeyboardfocus-feature> · <https://learn.microsoft.com/power-bi/developer/visuals/high-contrast-support> · <https://learn.microsoft.com/power-bi/create-reports/desktop-accessibility-creating-reports> |
| Power BI pricing | Pro/PPU list prices in EUR, as of 07/2026 (excluded from the comparison, same for every stack) | <https://powerbi.microsoft.com/de-de/pricing/> · <https://powerbi.microsoft.com/en-us/blog/important-update-to-microsoft-power-bi-pricing/> |

## 3 · Visuals, libraries and themes in the demo report

| Component | Version | Licence / status | Where | Link |
|---|---|---|---|---|
| ChartKitchen byDatenWG | 1.53.0.0 | open source, free; **speaker's own project** | Rung 5a, pages "Plan gap", "Nine companies…", "Full-year outlook" | <https://github.com/Losveratos/PowerBI-Kitchen-/tree/main/ibcsInspiredChartDeck> · docs <https://datenwgknowledgekitchen.com/chartkitchen-doku_en.html> |
| P&L Statement byDatenWG | 1.7.0.0 | open source, free; **speaker's own project** | Rung 5a, pages "Group P&L", "Balance sheet", "Cash flow", "FX and close" | <https://github.com/Losveratos/PowerBI-Kitchen-> · docs <https://datenwgknowledgekitchen.com/pnl-doku_en.html> |
| Deneb (Vega / Vega-Lite for Power BI), Daniel Marsh-Patrick | v1, from AppSource on load | free, Microsoft-certified | Rung 4, page "4 Deneb" | <https://deneb.guide> · <https://deneb.guide/blog/2024-2025-summary> · sponsors/releases <https://github.com/sponsors/deneb-viz> |
| Vega-Lite | schema v5 (Chart Builder templates), v6 (specs) | BSD-3-Clause | `demo-report/deneb/*.json` | <https://vega.github.io/vega-lite/> |
| PowerofBI.IBCS (DAX UDF library), Andrzej Leszkiewicz | 0.11.0 | MIT | Rung 3, `functions.tmdl`, measures `ΔPL line UDF`, `ΔPL % line UDF` | <https://daxlib.org/package/PowerofBI.IBCS/> · <https://www.powerofbi.org/ibcs> · <https://github.com/avatorl/dax-udf-svg-ibcs> |
| DAX Lib (package registry for DAX UDFs) | – | community | Source of the UDF library | <https://daxlib.org> · <https://www.sqlbi.com/blog/marco/2025/12/12/introducing-dax-lib-the-app-store-for-dax-user-defined-functions/> |
| DaxLib.SVG | – | community | Compared, not used | <https://evaluationcontext.github.io/daxlib.svg> |
| HTML Content (lite) | – | certified (lite only) | Mentioned on rung 4 | <https://appsource.microsoft.com/en-us/product/power-bi-visuals/coacervolimited1596856650797.htmlcontent_certified> |
| Base theme Fluent2-CY26SU05 | Power BI Desktop | Microsoft | Report | – |
| Daten-WG report theme | v1595… | own | Report | `demo/…/RegisteredResources/` |

## 4 · Paid custom visuals (vendor pages, list prices 11/2026)

Quotes differ from list prices; the calculator uses three anchors: ~33 EUR (Inforiver level), ~80 EUR
(blended, default) and ~170 EUR (Zebra level) per user and year.

| Vendor | Used for | Link |
|---|---|---|
| Zebra BI for Power BI | Rung 5b, appendix A7 (working capital dashboard screenshot), price anchor | <https://zebrabi.com/pricing/> |
| Inforiver (Lumel) | Price anchor; Lumel EPM IBCS-certified | <https://inforiver.com/pricing> · <https://www.ibcs.com/?p=73528> |
| graphomate | Named on rung 5b | <https://www.graphomate.com/en/licences/> |

## 5 · Community articles and talks

| Source | Used for | Link |
|---|---|---|
| Tabular Editor blog: Fabric Apps explained, visualization as code | Rung 6, Vega-Lite in Fabric Apps | <https://tabulareditor.com/blog/fabric-apps-explained-visualization-as-code-in-a-data-app-dashboard> |
| Tabular Editor blog: FabCon Barcelona 2026 recap | Announcement of native Vega-Lite in Power BI (no date yet) | <https://tabulareditor.com/blog/fabcon-barcelona-2026-recap> |
| Data Goblins: Power BI MacGuyver toolbox | Core + SVG approach ("MacGyver" in the calculator title) | <https://github.com/data-goblin/powerbi-macguyver-toolbox> |
| Daten-WG: Standard, Custom oder Deneb? | Earlier comparison of the three stacks (German) | <https://www.daten-wg.com/post/power-bi-visuals-richtig-ausw%C3%A4hlen> |
| Ben Shneiderman: "Overview first, zoom and filter, then details on demand" (1996) | Structure of the calculator and the report pages | *The Eyes Have It*, IEEE Symposium on Visual Languages, 1996 |

## 6 · Visual Standards Calculator (cost comparison)

Visual Standards Calculator v0.23 (v0.23.1 adds `?preset=`), Michael Tenner & Diana Ackermann, Daten-WG Knowledge Kitchen.
Indication, not a quote: three-point estimates, Monte Carlo simulation, P10–P90 per reader and year.
Of 58 assumptions, 3 are verified, 9 come from search snippets, 3 are rules of thumb, 9 from a simulated
expert panel and 34 are the authors' estimates.

- Live, finance preset: <https://datenwgknowledgekitchen.com/visual-standards-rechner.html?lang=en&preset=finance>
- Model, assumptions and sources (German): <https://github.com/Losveratos/PowerBI-Kitchen-/blob/main/md/visual-standards-rechner.md>
- Assumptions audit 09/2026: `sessions/visual-standards-rechner-audit/` in the PowerBI-Kitchen- repository
- PDF of the finance preset: [`calculator-finance-preset-en.pdf`](working/budapest-bi26/calculator-finance-preset-en.pdf) (level 1), [`…-level2.pdf`](working/budapest-bi26/calculator-finance-preset-en-level2.pdf)

Further sources inside the calculator (beyond those in sections 2 and 4):

| Source | Used for | Link |
|---|---|---|
| freelancermap Freelancer-Kompass 2025 | Hourly rates | <https://www.freelancermap.de/media/press_release/PM-Freelancer-Kompass-2025.pdf> |
| Robert Half salary guide 2026 | Internal hourly cost (125 EUR/h fully loaded) | <https://www.roberthalf.com/de/de> |
| Forrester Total Economic Impact (TEI) methodology | Cost structure | <https://www.forrester.com/policies/tei> |
| McConnell: Cone of Uncertainty | Estimate ranges | Steve McConnell, *Software Estimation*, 2006 |
| blueforte / TU München: "More than just a standard" (2019) | Benefit of reporting standards | <https://www.blueforte.com/> |
| BFSG and BITV 2.0 (German accessibility law) | Accessibility requirement | <https://www.gesetze-im-internet.de/bfsg/> |
| Daten-WG whitepaper: ten days to a marketable product | Build hours with coding agents | <https://datenwgknowledgekitchen.com/whitepaper-ki-entwicklung-roi.html> |

## 7 · Demo data and model

| Item | Content | Where |
|---|---|---|
| DWG Industries (fictitious group) | 9 companies, 7 currencies, 3 regions, 24 months, AC/PY/PL/FC plus full-year scalars; 296 accounts (P&L 128 · BS 102 · CF 66); 63,936 fact rows | [`demo/demoData/demokit/`](demo/demoData/demokit/) |
| Generator | Python, writes the seven CSVs, translates per IAS 21, budget rate, day-3 adjustment | `generate_demokit.py`, `engine.py`, `coa_*.py`, `dims.py` |
| Reconciliation | Group totals checked to the cent | [`reconciliation.txt`](demo/demoData/demokit/reconciliation.txt), `checks.py` |
| Semantic model | TMDL, compatibility level 1702, culture en-US | [`demo/PnL ChartkitchenDemoKit.SemanticModel/`](demo/PnL%20ChartkitchenDemoKit.SemanticModel/) |
| Report | PBIR, 12 pages, one page per rung | [`demo/Budapest BI Forum.Report/`](demo/Budapest%20BI%20Forum.Report/) |
| Documentation | Measures, page by page, known limits, expected values | [`working/budapest-bi26/demo-report/README.md`](working/budapest-bi26/demo-report/README.md) |

Exchange rates, companies and figures are invented. No real company data is used.

## 8 · Tools used to build the material

| Tool | Used for |
|---|---|
| Power BI Desktop (PBIP/PBIR, TMDL) | Model and report; Performance Analyzer in the live demo |
| `pbir` CLI | Pages, visuals, filters, conditional formatting, validation (`pbir validate`), screenshots from Desktop (`pbir desktop screenshot --scale 3`) |
| Tabular Editor (CLI preview) | Model edits until the preview expired; later TMDL edited by hand |
| DAX Studio (TOM/ADOMD) | DAX checks against the local engine, TMSL full refresh |
| Business Chart Builder (Daten-WG) | Deneb templates "Integrated variance" and "Structural variance analysis" — <https://datenwgknowledgekitchen.com/business-chart-builder.html> |
| `dwg` CLI (early preview) | Report and app from one spec, parity check — <https://github.com/Losveratos/dwg-cli> |
| Fabric Apps byDatenWG | ChartKitchen as React port in a Fabric App (rung 6) — <https://github.com/Losveratos/fabric-apps-byDatenWG> |
| Python 3, Pillow | Data generator; cropping of the screenshots |
| Playwright / headless Chromium | Calculator screenshots and PDFs, deck PDF |
| Claude Code (AI coding agent) | Build support for report and model, and the deck reviews (section 9) |

## 9 · Reviews of the deck

The deck was reviewed in two rounds by AI agents (Claude) in expert roles: first four (IBCS expert,
data-viz expert, Power BI expert, group controller), then seven (CFO, controller, data model expert,
data-viz expert, finance, IBCS expert, Power BI developer). These are simulated reviews, not statements by
real people. Findings and how they were applied: [`REVIEWS.md`](working/budapest-bi26/REVIEWS.md),
[`reviews-v2/`](working/budapest-bi26/reviews-v2/), [`UMSETZUNG-DECK.md`](working/budapest-bi26/reviews-v2/UMSETZUNG-DECK.md).

## 10 · Images in the deck (`working/budapest-bi26/assets/`)

| Files | Origin |
|---|---|
| `demo-*.png`, `pbi-*.png`, `pbi3-*.png` | Screenshots of the demo report from Power BI Desktop (`pbir desktop screenshot`) |
| `ck-*.png` | ChartKitchen byDatenWG renders |
| `pnl-*.webp` | P&L Statement byDatenWG documentation |
| `cb-*.png`, `deneb-vega-gantt.png` | Business Chart Builder / Deneb renders, Daten-WG Knowledge Kitchen |
| `calc-*.png` | Visual Standards Calculator, headless renders (`?lang=en`) |
| `fabric-apps-live.jpg` | Sales controlling app (Fabric App with ChartKitchen React port), own |
| `zebra-working-capital.png` | Zebra BI working capital dashboard, Zebra BI for Power BI (third-party product, shown for comparison) |
| `michael-tenner.webp`, `material/bi26_spc_MichaelTenner.png` | Speaker photo and speaker card (Budapest BI Forum) |

Deck typeface: Exo 2 (SIL Open Font License), from the Budapest BI Forum 2026 slide template.

## 11 · Links from the deck

- Daten-WG Knowledge Kitchen: <https://datenwgknowledgekitchen.com>
- IBCS trainer: <https://datenwgknowledgekitchen.com/ibcs-trainer.html>
- Business Chart Builder: <https://datenwgknowledgekitchen.com/business-chart-builder.html>
- Daten-WG community: <https://www.daten-wg.de>
- Speaker on LinkedIn: <https://www.linkedin.com/in/michael-tenner-5b885970/>

## Notes

- IBCS® is a registered trademark of the IBCS Institute. This material is not produced, certified or
  endorsed by IBCS. The same holds for the PowerofBI.IBCS library (see its own notice).
- ChartKitchen byDatenWG and P&L Statement byDatenWG are the speaker's own projects; ratings for rung 5a
  should be discounted accordingly.
- Microsoft, Power BI, Fabric and Copilot are trademarks of Microsoft. Zebra BI, Inforiver and graphomate
  are trademarks of their owners.
