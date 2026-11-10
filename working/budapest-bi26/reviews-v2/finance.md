# Review Finance

Rolle: Group Accounting / Financial Reporting (IFRS, Konsolidierung, Monatsabschluss, IAS 21, IAS 7), Publikum Reihe drei.
Grundlage: 23 Folienbilder, `story.html`, BRIEF, REVIEWS vom 7.11., Demo-Seiten, `demokit/*.csv`, `reconciliation.txt`, `engine.py` (nur gelesen, nachgerechnet).

## Drei Dinge, die vor dem Vortrag gefixt sein müssen

1. **Folie 3 erfindet einen eigenen Konzern, und der widerspricht dem Modell in der Richtung.**
   Die SVG-Reihen in `story.html` (Zeile 631 ff.) zeigen Jan 262 … Okt 298 (Summe 2.884). Das Modell liefert 245 … 309 (Summe 2.817,6), und genau diese Zahlen stehen eine Folie später auf Folie 4. Der letzte Aufbauschritt sagt „full year AC&FC 3,440 vs PL 3,510, −2.0 %“. Im Modell liegt der Plan bei 3.389,4, der Forecast also **über** Plan: +1,5 % (FC_FY) bzw. +1,3 % (AC Jan–Okt + FC Nov–Dez = 3.432,6). Der Schlusssatz auf Folie 3 kehrt damit die Aussage um.
   Fix: die Arrays durch die Modellwerte ersetzen (Netto-Umsatz, Mio. EUR, gerundet):
   ```
   const AC=[245,259,295,287,297,308,251,251,316,309,null,null];
   const PY=[223,236,273,252,261,269,218,219,274,273,267,277];
   const PL=[239,251,292,284,294,309,251,249,307,305,300,308];
   const FC=[null,null,null,null,null,null,null,null,null,null,301,314];
   ```
   Titel im letzten Schritt: „**Revenue · landing 3,433 (AC Jan–Oct + FC Nov–Dec) vs PL 3,389, +1.3 %**“. Fußzeile: „Demo model DWG Industries, net revenue, million EUR“. Die Skala (`scale=(base-top)/340`) prüfen, weil Mar/Jun/Sep über 290 liegen.

2. **Die Währungsfolie verspricht etwas, das das Demo-Modell nicht kann.** Der Abstract verspricht „current rate vs budget rate“. A9 zeigt PL zum Budgetkurs, `AC @BUD`, eine FX-Effekt-Zeile und einen „rate view“-Slicer, dazu „Facts stay in local currency … one DAX pattern“. Im Modell sieht es anders aus:
   - `fact-kurse.csv` hat nur `Kurs Durchschnitt` und `Kurs Stichtag`, einen Budgetkurs gibt es nicht.
   - `engine.py` (ab Zeile 849) rechnet **alle** Szenarien, also auch PL und FC, zum Ist-Durchschnittskurs des Monats um, und zwar im Generator. A10 sagt das selbst („Translation happens in the generator, not in DAX“) und widerspricht damit A9.
   - Folge: Wenn sich der Kurs bewegt, ändert sich auch PL in EUR. Der Satz „PL never moves“ stimmt für die Demo nicht. ΔPL ist faktisch ein Vergleich zu konstanten (Ist-)Kursen, was fachlich zulässig ist, aber anders heißt.
   - Der einzige FX-Effekt in `reconciliation.txt` (+8,4 Mio.) misst gegen **Vorjahreskurse**, nicht gegen Budgetkurs.
   Fix, entweder (a) bauen: Spalte `Kurs Budget` je Währung und Planjahr in `fact-kurse`, PL zum Budgetkurs übersetzen, Measures `AC @BUD` und `FX effect` anlegen, im Demo eine Zeile „FX effect vs budget rate“ zeigen. Oder (b) ehrlich beschriften. A9-Fußzeile: „**Target pattern. The demo model translates all scenarios at the actual monthly average rate in the generator; ΔPL is therefore at constant (actual) rates. Budget-rate view: not in the demo.**“ Ohne (a) oder (b) fragt der Head of Reporting genau hier nach, und eine Antwort gibt es dann nicht.

3. **Vorzeichen: Folie, Daten und Stacks sagen dreimal etwas anderes.**
   - Folie 7, Regel 3: „Cost row: −1 · display inverted · variance not inverted. −1 with VarianceInvert rates an overrun as favourable.“ In `dim-konten.csv` haben **alle 51 Kostenkonten** `−1 · true · true`, also VarianceInvert = true. Die Folie beschreibt damit die eigene Datenbasis als Fehlerfall.
   - Für dieselbe Zahl zeigt der P&L-Statement-Screenshot (Folie 6) Cost of sales ΔPL **+49,7** (+2,7 %, Δ des angezeigten Werts, Farbe trägt das Urteil), Rung 1 (Folie 9/A2) dagegen **−49.743.361** (−2,7 %, „positive is always good“). Folie 9 verspricht „same numbers“.
   Fix: Regel 3 auf die Daten umschreiben: „**Cost row: −1 · shown positive · variance inverted. Drop the variance flag and a cost overrun turns green.**“ Für alle Stacks eine Δ-Konvention festlegen und auf Folie 6 nennen: „**Δ = AC − PL of the shown value; colour carries good/bad (IBCS).**“ Dann die Measures `ΔPL`/`ΔPY` in Rung 1–3 umstellen. Wenn die Zeit dafür nicht reicht, im Demo den Satz sagen: „Rung 1–3 sign the variance by favourability, the statement visual by arithmetic. Same 49.7, two conventions. That is exactly the rule that has to live in the model.“

## Befunde (priorisiert, max. 12)

1. **Folie 6 (Headline im Screenshot)** · „Revenue +12.8 % vs prior year“ enthält den Zukauf Japan (Erstkonsolidierung 04/2026, ohne PY, YTD 92,0 Mio.). Organisch und währungsbereinigt sind es nur etwa **+8,7 %**: 3,7 Pp kommen aus der Akquisition, 0,4 Pp aus FX (ohne JP). · Fix: im Vortrag sagen oder als Untertitel ergänzen: „**+12.8 % reported · +8.7 % organic at PY rates (acquisition Digital JP +3.7 pp, FX +0.4 pp)**“. Das ist zugleich die beste Vorlage für die „PY-Restatement / like-for-like“-Frage, die sonst kommt.

2. **Folie 3, 7, A10, A11 (Forecast-Definition)** · FC ist ein eigenes 12-Monats-Szenario, und Jan–Okt FC (2.825,5) ≠ AC (2.817,6). Deshalb ist FC_FY 3.440,4 nicht die Landung AC + Rest (3.432,6). A10 nennt „full-year revenue 3,440 m“ ohne Szenario und Version. · Fix: Version benennen und eine Landungs-Definition festlegen. A10: „reconciliation.txt: **FY 2026 forecast (FC 10+2)** revenue 3,440 m, EBITDA 495 m“. Folie 7 Regel 4 ergänzen: „Landing = AC for closed months + FC for open months; FC_FY must equal it, or the forecast version is stale.“ Im Generator FC Jan–Okt := AC setzen oder FC_FY := AC + FC(rest).

3. **Folie 9 Demo (Abschlussprozess)** · Die Controller-Szene aus dem 7.11. (Buchung am Tag 3 korrigiert, alle Stacks zeigen das neue EBITDA mit Stempel) ist laut REVIEWS weiter offen. „data-as-of“ steht nur als Bullet. · Fix: einen Satz plus 60 Sekunden Demo. Den Stempel auf jede Seite: „**Actuals: Oct 2026 · close status: final, signed off WD5 · plan v2026-1 · forecast 10+2, 04 Nov 2026 · refreshed 09 Nov 07:12**“. Live: einen Wert in `fact-abschluss.csv` ändern, Refresh, alle fünf Seiten zeigen dasselbe neue EBITDA. Wenn das Tooling es nicht trägt, den Satz sagen: „The model is the single closing number; no stack stores its own copy.“

4. **Folie 11 Matrix, Spalte „Cost per reader“** · Die Bewertungen widersprechen dem eigenen Rechner. 5b (Paid) bekommt ●○○, obwohl Paid im gezeigten Preset (150 Leser) mit 144 EUR **am günstigsten** ist. Rung 1 bekommt ●●●, obwohl „Core + SVG“ mit 259 EUR am teuersten ist. · Fix: 5b → „●●○ cheapest at 150 readers, tips at 176“. Rung 1 → „●●● for a plain page; ●○○ once IBCS is required (Core + SVG 1.8×)“. Alternativ eine Fußnote, dass sich die Spalte auf das Preset bezieht.

5. **Folie 10 / A1 (Rechner als TCO)** · Für Finance ist das ein Kostenvergleich, aber noch keine TCO. Es fehlen: der implizite Stundensatz (66.000 EUR / 528 h ≈ **125 EUR/h**, nirgends genannt), interne Vollkosten vs. extern, die Plattformkosten (Pro/PPU/Fabric-CU; sie unterscheiden sich bei SVG-Measures und Fabric Apps sehr wohl), Preissteigerung der Lizenz über 5 Jahre, Mindestabnahmen und Creator- vs. Viewer-Preise, keine Abzinsung. Dazu „3 of 58 assumptions verified“. · Fix: eine Zeile unter das Chart: „**Hours at 125 EUR/h fully loaded · platform licences and capacity excluded (equal except SVG CU and Apps) · list prices, no escalation, no discounting · 3 of 58 assumptions verified: read the P10–P90 band, not the P50.**“ Und „tie“ sprachlich zu „**indistinguishable within the band**“ ändern. Live im Rechner den Stundensatz auf 90 und 150 drehen, denn das ist der Hebel, den jeder CFO zuerst anfasst.

6. **Folie 10 / Matrix „Export & audit“ (Audit-Trail, IKS)** · „Audit“ meint hier „Logik sichtbar“. Für Group Reporting heißt Audit: Ist die Zahl reproduzierbar, versioniert, mit Änderungsnachweis (ITGC/SOX Change Management) und Zugriffskontrolle? Ein Custom Visual mit eigener Rechenlogik ist ein IKS-relevantes Stück Software und braucht Freigabe, Versionierung und Tests. Das sind Kosten, die im Rechner nur als „approval 8–60 h“ auftauchen. · Fix: Spalte umbenennen in „**Export & audit trail**“ und Fußnote: „Audit = number reproducible from the model, versioned in Git, logic reviewable. Visuals that compute subtotals are in scope of IT general controls.“

7. **A2 / Rung 1 (Folie 14, Demo)** · Die Matrix zeigt Euro auf den Euro genau (2.817.623.779), keine Zwischensummen (Gross profit, EBITDA, EBIT fehlen), und die letzte Zeile heißt „Total“. Ein Finanzer liest das nicht als GuV. · Fix: Format „#,0.0,,“ (Mio. EUR, eine Nachkommastelle), „Total“ → „**Net income**“, im Titel „million EUR, Jan–Oct 2026“. Das Fehlen von EBITDA ausdrücklich als Grenze von Rung 1 nennen („no formula rows without DAX“). Sonst sieht es nach einem Versehen aus statt nach einer Grenze.

8. **Folie 6 / 7 (GuV-Format und IFRS 18)** · Umsatzkostenverfahren (funktional) plus eigene Zeile D&A unter EBITDA ist ein Management-Format, keine IAS-1-Primäraufstellung. Ab **1.1.2027 gilt IFRS 18**: Pflichtzwischensumme „Operating profit“, Kategorien operating/investing/financing, EBITDA als Management-defined Performance Measure mit Überleitung im Anhang. Im Saal sitzen Leute mitten in der IFRS-18-Umstellung. · Fix: ein Satz auf Folie 6: „**Management P&L, cost-of-sales format with D&A shown separately. Under IFRS 18 (from 2027) EBITDA becomes a disclosed MPM, and that is one more formula row in the account dimension, not a new report.**“ Damit wird aus einer möglichen Kritik ein Argument für die Sign-Trio-/FormulaDef-Architektur.

9. **A9 Yen-Problem** · „The Japanese company grows in JPY and shrinks in EUR“ lässt sich im Demo nicht zeigen, weil Digital JP ohne Vorjahr ist (Zukauf 04/2026). Gegen Plan gibt es −3,0 % in EUR, die Ursache (Kurs 168,5 → 184,3) bleibt unsichtbar, weil PL ebenfalls zum Ist-Kurs umgerechnet ist. · Fix: Beispiel auf eine Gesellschaft mit PY legen: Automation CH (FX-Effekt +5,8 Mio. vs. PY-Kurs) oder Mobility AU (−1,1 Mio.). Text: „**Automation CH grows 3 % in CHF and 6 % in EUR. The franc did the rest.**“ (Prozentwerte vor Verwendung aus dem Modell ziehen.)

10. **Folie 7 / A11 Kleinigkeiten, die ein Prüfer sieht** · (a) Regel 2 sagt „MAX per company and year“, der Code fasst aber nach **Account × Entity × Year** zusammen. (b) A11: „A plain MAX … returns the largest company, 215 m“: 214,7 Mio. ist ein einzelnes Konto (Export revenue, Automation DE), keine Gesellschaft (die hat ~820 Mio.). (c) Im englischen Deck stehen „LW“, „AC LW“ und „AC Stichtag“, A9 sagt aber „AC LC“. · Fix: (a) „MAX per account, company and year, then summed“. (b) „returns the largest single account-company cell, 215 m instead of 3,440 m“. (c) Durchgängig „LC“ verwenden, „AC at reporting date“.

11. **Konsolidierung (Folie 7, A10)** · „Nine companies, full consolidation“ wird ohne Intercompany-Eliminierung, ohne Konsolidierungsebene (Entity „Elimination“) und ohne Ergebnisaufteilung Eigentümer/NCI gezeigt. Die Bilanz hat NCI-Konten, die GuV nicht (IAS 1.81B). Wer konsolidiert, fragt: „Where are the eliminations?“ · Fix: Satz auf A10: „**Synthetic group: entities are already third-party only, no intercompany, no elimination entity, NCI only in the balance sheet. In a real group the eliminations come as a tenth entity from the consolidation system; the model does not consolidate, it reports.**“ Das sollte auch als Antwort für die Q&A parat sein.

12. **Toter Code Folie 6 (`story.html` Zeile ~275, `display:none`)** · Die versteckte Tabelle enthält weiterhin erfundene Zahlen (Revenue 2.884, EBITDA 415) und die falsche Vorzeichenangabe „−1 · show+ · –“. Das ist harmlos, solange sie verborgen bleibt, aber das Deck liegt öffentlich auf GitHub. · Fix: Block löschen.

## Plausibilitätscheck der Demo-Zahlen (Tabelle)

Basis: `reconciliation.txt` und `fact-abschluss.csv`, YTD Jan–Okt 2026, Mio. EUR, eigene Nachrechnung.

| Größe | Wert Demo | Benchmark / Erwartung Industriekonzern | Urteil |
|---|---|---|---|
| Netto-Umsatz YTD | 2.817,6 (PY 2.498,1, PL 2.782,1) | Folie 4/6 konsistent | plausibel |
| Wachstum vs PY | +12,8 % berichtet, **+8,7 % organisch/kk** | Maschinenbau 2026: 3–8 % organisch | hoch, aber vertretbar; Akquisition benennen |
| Erlösschmälerungen | 114,3 = 3,9 % brutto | 2–5 % | plausibel |
| Rohertragsmarge | 33,5 % (PL 34,4 %) | 28–38 % Automation/Anlagen | plausibel |
| Vertrieb / Verwaltung / F&E | 8,9 % / 5,8 % / 4,6 % vom Umsatz | 8–12 % / 4–7 % / 3–6 % | plausibel |
| Verwaltung vs PY | +17,1 % bei Umsatz +12,8 % | Fixkosten wachsen langsamer | auffällig, guter Demo-Kommentar (IT +10,9 % vs PL) |
| EBITDA / Marge | 400,5 / 14,2 % (PL 15,2 %, −5,6 %) | 12–16 % | plausibel |
| D&A / Capex | 144,1 / 152,0 → Capex/D&A 1,05 | 1,0–1,3 | plausibel |
| EBIT-Marge | 9,1 % | 7–11 % | plausibel |
| Finanzergebnis vs Nettofinanzschulden | −49,8 auf 1.198,9 → ~5,0 % p. a. | 3,5–5,5 % | plausibel, eher hoch |
| Steuerquote | 54,9 / 206,5 = **26,6 %** | Mix DE 30 %, CH 14,8 %, PL 19 %, US 24,3 % | plausibel |
| Jahresüberschuss / Nettomarge | 151,6 / 5,4 % | 4–7 % | plausibel; NCI-Anteil fehlt |
| Nettoverschuldung / EBITDA (LTM ≈ 475,9) | ~2,5× | < 3× | plausibel |
| Eigenkapitalquote | 34,9 % | 30–45 % | plausibel |
| OCF / EBITDA | 263,5 / 400,5 = 66 % | 60–85 % | plausibel |
| „Cash Conversion“ 173,8 % | = OCF / Jahresüberschuss | üblich: FCF/NI oder OCF/EBITDA | Definition nennen, falls gezeigt |
| „CapEx-Quote“ 57,7 % | = Capex / OCF | üblich: Capex / Umsatz (5,4 %) | Definition nennen, falls gezeigt |
| FC Nov–Dez | Umsatz 615 (307/Monat), EBITDA 94,3 (47/Monat vs 40 YTD), JÜ 41,7 (21/Monat vs 15 YTD) | Q4-Saisonalität ja, aber +37 % Ergebnis je Monat | **Hockeystick**, Head of Reporting fragt nach |
| PL FY EBITDA vs PY | 518,3 vs 441,0 = +17,5 % | ambitioniert | erklärt den Plan-Miss |
| FC_FY vs AC + FC-Rest | 3.440,4 vs 3.432,6 | identisch | **Inkonsistenz**, siehe Befund 2 |
| Umsatz je Mitarbeiter | 3.440 / 13.040 MA ≈ 264 TEUR | 200–300 TEUR | plausibel |
| FX-Effekt Umsatz vs PY-Kurs | +8,4 = 0,3 % | klein bei EUR-Mehrheit | plausibel |
| Folie 3 (SVG) | 2.884 / PL FY 3.510 / −2,0 % | soll Modell zeigen | **falsch**, siehe Fix 1 |

Fazit: Ein Finanzer erkennt die Struktur als glaubwürdigen Industriekonzern. Angreifbar sind nur die Brüche zwischen Folie und Modell, nicht die Modellzahlen selbst.

## Was gut ist und bleiben soll

- **Abnahme gegen `reconciliation.txt`**: Bilanzkontrolle 0 in jedem Filter, derselbe Jahresüberschuss in GuV, Bilanz und KFR, die IAS-7-FX-Zeile im Finanzmittelfonds. Das ist mehr Abstimmung, als die meisten Demo-Modelle haben. Auf A10 ruhig laut sagen: „reconciled before a single visual was built“.
- **Empty, not zero** (Regel 1) und **FY als Skalar mit MAX je Zelle** (Regel 2): genau die Fehler, die in echten Konzernberichten passieren. Die Begründung „SUM is twelve times too large“ bleibt hängen.
- **Seitenfilter 1–10 gegen den 10-vs-12-Monats-Fehler**: ein echtes Finance-Thema, gut benannt.
- **Lokalwährung nur bei einer Währung im Filter, sonst leer**: korrekt und finance-tauglich („Adding CHF to JPY is not a number“).
- **Headline im P&L-Screenshot** (Folie 6) nennt Abweichung, Treiber und Ausgleich in einem Satz. So schreibt ein Controller einen Kommentar.
- **Sign-Trio im Kontenstamm statt im Visual**: die richtige Architektur, und mit IFRS 18 aktueller denn je (siehe Befund 8).
- **Rechner mit P10–P90 und offen ausgewiesener Evidenzlage** (3 von 58 verifiziert): ehrlich. Finance traut einer Spanne mehr als einer Punktzahl.
- **Umsetzung der 7.11.-Reviews**: Brauerei-Margen weg, 176-Leser-Richtung korrigiert, Währung als A9 ergänzt, Folie 3 mit Gesamtjahr-Zahl (die aber falsch ist, siehe Fix 1). Offen geblieben: Abschluss-Szene, Budgetkurs im Modell, Plattformkosten im Rechner.
