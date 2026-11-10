# Review Datenmodell-Experte

Grundlage: TMDL-Stand vom 09.11.2026, 02:44 (fact-abschluss.tmdl mit `Revenue AC&FC` per `SUMX(VALUES(MonatNr))` und den zwei mEUR-Measures), alle sieben CSVs mit Python nachgerechnet, Report-Seiten 1–4 (Filter und gebundene Felder) gelesen, Folien s07, s17, s21–s23 und story.html geprüft. `te` wurde nicht verwendet. Kein DAX wurde gegen die Engine ausgeführt: die Aussagen über Measure-Ergebnisse sind aus den CSVs nachgerechnet.

## Drei Dinge, die vor dem Vortrag gefixt sein müssen

1. **Das Budgetkurs-Versprechen ist nicht im Modell.** Der Abstract verspricht „current rate vs budget rate“. A9 zeigt `AC @BUD`, `FX effect`, einen „rate view“-Slicer und schreibt „Facts stay in local currency; a rate table … holds one rate per period, currency and type“. Das Modell rechnet dagegen schon im Generator um (so steht es auch auf A10). `fact-kurse` hat nur `Kurs Durchschnitt` und `Kurs Stichtag`, einen Budgetkurs gibt es nicht, und kein Measure rechnet zum Budgetkurs. Ein Zuhörer, der das GitHub-Modell öffnet, findet das in zwei Minuten. Fix: entweder umsetzen (Befund 1, etwa eine Stunde Arbeit) oder A9 als „pattern, not in the demo model“ kennzeichnen und den Satz „Facts stay in local currency“ streichen.
2. **Die Modell-Folie (s07) behauptet Dinge, die das Modell nicht hält.** „Rate table without a relationship“: `fact-kurse` hängt an `dim-datum` und `dim-waehrung`. Rule 3 („cost row … variance not inverted“) widerspricht den Daten, denn alle 51 Kostenzeilen tragen `VarianceInvert = true`. Weitere Fehler: „L1…L4“ (es sind L1…L6), „Unit“ (diese Spalte gibt es nicht), „Star schema“ (Region ist ein Schneeflocken-Ast, und `dim-waehrung` fehlt im Bild) und „AC empty for open months, never 0“ (675 Strukturzeilen tragen im November 2026 AC = 0). Folientexte siehe Befunde 2 und 3.
3. **Die Zeitlogik der neuen Measures hängt am Seitenfilter und an `MonatNr`.** `ΔPL` vergleicht ohne den Seitenfilter „Monate 1–10“ zehn Ist-Monate mit zwölf Plan-Monaten. Für das Gesamtjahr 2026 kommt bei Net revenue ΔPL = −572 M heraus, und jede Gesellschaft liegt dann 13 bis 25 % unter Plan. `Revenue AC&FC`, `Revenue sparkline (text)` und `Revenue AC vs PL SVG` iterieren über `VALUES('dim-datum'[MonatNr])`: Ist der Jahres-Slicer leer, verschmelzen 2025 und 2026. Im Zusammenspiel heißt das: Für Nov und Dez ist das AC 2025 nicht leer, also kommt AC 2025 statt FC 2026 heraus. Die Folie sagt selbst „Trap every rung inherits … The page filter prevents it“. Das Modell sollte die Falle selbst schließen (Befund 4).

## Befunde (priorisiert, max. 12)

**1 · fact-kurse / A9 · Budgetkurs fehlt.** Weder Spalte noch Measure für Ist- vs. Budgetkurs, obwohl Abstract und A9 es versprechen.
Fix (Generator: Spalte `Kurs Budget` je Währung und Jahr in `fact-kurse.csv`, im M-Typschritt `{"Kurs Budget", type number}` ergänzen):
```dax
measure 'AC @BUD' =
    SUMX (
        SUMMARIZE ( 'fact-abschluss', 'dim-gesellschaft'[Währung], 'dim-datum'[Jahr] ),
        VAR _Cur = 'dim-gesellschaft'[Währung]
        VAR _Yr  = 'dim-datum'[Jahr]
        VAR _Rate =
            CALCULATE (
                MAX ( 'fact-kurse'[Kurs Budget] ),
                REMOVEFILTERS ( 'dim-datum' ),
                'fact-kurse'[Währung] = _Cur,
                'fact-kurse'[Jahr] = _Yr
            )
        RETURN DIVIDE ( CALCULATE ( SUM ( 'fact-abschluss'[AC LW Wert] ) ), _Rate )
    )
measure 'FX effect' = [AC] - [AC @BUD]
```
Gilt nur für Erfolgsposten. Auf der Folie sagen: Bilanzposten bräuchten den Budget-Stichtagskurs. Wer das nicht bauen will, ändert auf A9 die Kopfzeile auf „Pattern · not in the demo model“.

**2 · Folie s07 · Fakten zum Modell falsch.** Fünf Aussagen stimmen nicht mit dem TMDL überein.
Folientext-Fix:
- Untertitel: „… a date table, a rate table **not related to the facts** …“
- DimAccount: „L1…L6“ statt „L1…L4“, „Comment DE/EN“ ohne „· Unit“.
- Überschrift: „Star schema“ → „Star schema, one snowflake branch (region)“. Im Diagramm `DimRegion` (3) an `DimEntity` hängen und `DimCurrency` (7) an `FactRates` ergänzen. Dann stimmt auch A10 („five dimensions, two fact tables“).
- Measure-Box: „Measures: AC · PY · PL · FC · FY · LW + signed/Δ for core visuals“. Es sind 44 Measures, davon 17 im Ordner „Budapest demo“.

**3 · Folie s07 Rule 3 / dim-konten · Vorzeichen-Trio widersprüchlich erklärt.** Die Daten sagen: Kostenzeile = `SignConvention −1 · DisplayInvert true · VarianceInvert true` (51 Zeilen). Erlösschmälerungen und sonstige Aufwände = `−1 · false · true` (27). Vorräte und Schulden = `+1 · false · true` (32). `VarianceInvert` heißt also „weniger Rohwert ist besser“, unabhängig vom Vorzeichen. So steht es auch auf s06 und in der Spaltenbeschreibung („Weniger ist besser“).
Folientext-Fix Rule 3: „Cost row: −1 · shown positive · less is favourable. Three flags, three jobs: compute, display, judge. Get one wrong and an overrun turns green.“ Dazu einen Satz für die Brücke zu den Core-Stacks: „The signed measures bake SignConvention in, so for them ‚positive = good‘ needs no VarianceInvert. That holds for the P&L only.“

**4 · ΔPL, Revenue AC&FC, Sparkline, AC-vs-PL-SVG · Zeitlogik nicht robust.** Die Measures setzen auf Seitenfilter MonatNr 1–10 und Jahres-Slicer = 2026 und brechen ohne beide still.
Fix (TMDL, `dim-datum[Periodenstatus]` hat genau die Werte „Ist“/„Forecast“):
```dax
measure ΔPL =
    VAR _Ac = [AC signed]
    VAR _Pl = CALCULATE ( [PL signed], KEEPFILTERS ( 'dim-datum'[Periodenstatus] = "Ist" ) )
    RETURN IF ( NOT ISBLANK ( _Ac ), _Ac - _Pl )

measure 'Revenue AC&FC' =
    CALCULATE ( [Revenue AC], KEEPFILTERS ( 'dim-datum'[Periodenstatus] = "Ist" ) )
        + CALCULATE ( [Revenue FC], KEEPFILTERS ( 'dim-datum'[Periodenstatus] = "Forecast" ) )
```
`ΔPY` bekommt dieselbe Absicherung. In Sparkline und SVG `VALUES('dim-datum'[MonatNr])` durch `VALUES('dim-datum'[PeriodeSort])` ersetzen; die Sortierung im CONCATENATEX dann ebenfalls nach `PeriodeSort`. Im Report den Seitenfilter `MonatNr in 1..10` durch `Periodenstatus = "Ist"` ersetzen: der überlebt den Novemberabschluss ohne Handarbeit.

**5 · fact-abschluss (Daten) · „empty not zero“ gilt nur für Buchungszeilen.** 118 der 296 Kontenzeilen (Knoten, Formeln, KPIs, Trenner) stehen mit 0 in allen 24 Monaten in der Faktentabelle. Das sind 25.488 von 63.936 Zeilen (40 %). Im November 2026 liefert das schlichte `[AC]` deshalb 0 statt BLANK. Auffällig: Für Digital JP vor 2026-04 schreibt der Generator die Strukturzeilen korrekt leer, für Nov und Dez 2026 nicht.
Fix im Generator: Strukturzeilen bekommen in Szenario-Spalten ohne Daten (AC Nov–Dez 2026, PY für Digital JP ab 2026-04) Leerwerte statt 0. Die Zeile bleibt im Visual sichtbar, weil PL und FC dort weiter 0 tragen. Auf der Folie ehrlich sagen: „Structure rows sit in the fact table as zeros so the statement visual can see them; that is a visual-driven compromise.“

**6 · ΔPL bar (text), ΔPL SVG · Überlauf bei |Total| > größte Zeile.** `_Max` kommt aus den L1-Zeilen. Die Summenzeile kann größer sein, dann wird `REPT(" ", 10 − _N)` negativ (Fehler in der Zelle) und der SVG-Balken läuft über das Label. In den Demo-Daten tritt das nicht auf, bei Live-Filtern auf ein Segment kann es passieren. Außerdem: Ist `_Max` 0 oder BLANK, erzeugt `FORMAT(BLANK(),"0.0")` ein leeres `width=''`.
Fix:
```dax
VAR _N   = MIN ( 10, ROUND ( DIVIDE ( ABS ( _D ), _Max ) * 10, 0 ) )        -- Text
VAR _Len = MIN ( 1, DIVIDE ( ABS ( _D ), _Max, 0 ) ) * ( _Mid - 44 )       -- SVG
```
Alternativ in beiden Matrizen die Gesamtsumme der Spalte ausblenden.

**7 · fact-abschluss.tmdl · Beschreibungen verrutscht oder falsch.** Die `///`-Zeilen 562–564 (SVG-Text) hängen an `Revenue AC&FC`, `ΔPL SVG` hat keine Beschreibung. Die Tabellenbeschreibung sagt „in mEUR“, die Werte sind EUR-Basiseinheiten (A10 sagt richtig „base units“). `FC` sagt „Ist für die geschlossenen Monate“, aber FC = AC gilt nur in rund 50 % der Ist-Zeilen. `Revenue AC vs PL SVG` sagt „12 Zeichen Breite“ (es sind 160 px). `dim-gesellschaft` sagt „Sieben Gesellschaften“ (es sind 9). `dim-waehrung` verweist auf einen Kommentar in relationships.tmdl, der dort fehlt.
Fix: Zeilen 562–564 unmittelbar vor `measure 'ΔPL SVG'` verschieben und die vier Texte korrigieren. FC entweder im Generator auf „AC für geschlossene Monate“ ziehen (das ist die übliche Definition, und dann ist `Revenue AC&FC` = `Revenue FC`) oder die Beschreibung ändern auf „eigenständige Forecast-Version, auch für Ist-Monate“.

**8 · Revenue AC/PY/PL/FC, EBITDA × 4 · L1-Namen als String-Literale.** `KEEPFILTERS('dim-konten'[L1 EN] IN {"Net revenue", …})` bricht beim ersten Umbenennen der Zeile und widerspricht „rules in the dimension“. Acht Measures kopieren denselben Ausdruck.
Fix: Spalte `KPI Block` (Text: Revenue/EBITDA/…) im Generator in `dim-konten`. Dann gilt: `Revenue AC = CALCULATE([AC signed], KEEPFILTERS('dim-konten'[KPI Block] = "Revenue"))`, und `EBITDA AC` analog, mit IN über die Blöcke. Damit gibt es eine einzige Vorzeichenlogik (in `AC signed`) statt neun Kopien.

**9 · Signed-Measures · nur für die GuV gültig, aber nicht abgesichert.** `RowType = "account"` lässt auch 40 Cashflow-Zeilen durch. Dort ist „positiv = gut“ falsch (z. B. Capex). Die Matrizen schützt nur ein Visual-Filter `Statement = Income statement`.
Fix: in allen vier Signed-Measures `KEEPFILTERS ( 'dim-konten'[Statement] = "Income statement" )` ergänzen und die Beschreibung mit „GuV only“ beginnen lassen.

**10 · Core-Matrix · Zwischensummen fehlen.** `AC signed` blendet Formelzeilen aus, also verschwinden Gross profit, EBITDA, EBIT und EBT aus der Matrix. Für ein Finanzpublikum ist das die erste Frage. Weil alle GuV-Formeln laufende Summen über die Blöcke sind, reicht ein Measure:
```dax
measure 'AC signed + subtotals' =
    VAR _Sort = MAX ( 'dim-konten'[L1 Sort] )
    RETURN
        IF (
            SELECTEDVALUE ( 'dim-konten'[RowType] ) = "formula",
            CALCULATE ( [AC signed],
                REMOVEFILTERS ( 'dim-konten'[L1 EN], 'dim-konten'[L1 Sort] ),
                'dim-konten'[L1 Sort] < _Sort ),
            [AC signed]
        )
```
Für PL und ΔPL analog. Wenn keine Zeit mehr ist: die fehlenden Zwischensummen auf s08/A2 als bekannte Grenze von Sprosse 1 nennen.

**11 · fact-abschluss, dim-datum · Datentypen und Sichtbarkeit.** Die Wertspalten sind `double`, der Titel von A10 sagt aber „reconciled to the cent“. `FC_FY`, `PL_FY` und die LW-Varianten haben `summarizeBy: sum`, obwohl die Beschreibung „nie mit SUM“ sagt. In der Faktentabelle sind `AccountID`, `EntityID` und `Datum` sichtbar. Flags (`IstAbgeschlossen`, `DisplayInvert`, `VarianceInvert`) liegen als Text „true“/„false“ vor.
Fix: Wertspalten `dataType: decimal` (Fixed Decimal), `summarizeBy: none` auf die vier FY-Spalten, `isHidden` auf `fact-abschluss[AccountID]`, `[EntityID]` und `[Datum]` (`Monat` bleibt sichtbar, es ist die Period-Rolle), Flags als `boolean` typisieren.

**12 · Filterinfo · zeigt „Konzern“, obwohl gefiltert ist.** `ISFILTERED('dim-gesellschaft'[Gesellschaft])` erkennt die Slicer auf `Short name` und `Country` nicht. Bei genau einer Gesellschaft steht deren Landeswährung in der Fußzeile, obwohl die Zahlen in EUR sind. Die Texte sind deutsch („Konzern“, „bis“).
Fix:
```dax
VAR _Ges =
    IF ( ISCROSSFILTERED ( 'dim-gesellschaft' ),
         CONCATENATEX ( VALUES ( 'dim-gesellschaft'[Short name] ), 'dim-gesellschaft'[Short name], ", " ),
         "Group" )
VAR _Wae = "EUR"   -- LW nur in einer eigenen Filterinfo LW
```
und „ to “ statt „ bis “.

## Modell-Inventar (Tabelle: Tabelle · Zeilen · Rolle · Auffälligkeit)

| Tabelle | Zeilen | Rolle | Auffälligkeit |
|---|---:|---|---|
| fact-abschluss | 63.936 (296 Konten × 9 Ges. × 24 Monate) | Fakt, Monatsgrain, Szenarien als Spalten (AC/PY/PL/FC × EUR/LW + 4 FY-Skalare), 44 Measures | 40 % Nullzeilen für Strukturzeilen; `double`; FY-Spalten `summarizeBy: sum`; Schlüssel sichtbar; alle Measures in der Faktentabelle, keine Measure-Tabelle; PY gespeichert (= AC um 12 Monate verschoben, zum damaligen Kurs) |
| dim-konten | 296 (GuV 128 · Bilanz 102 · CF 66) | Konten- und Regeldimension: L1–L6 DE/EN, RowType, SortOrder, FormulaDef, Vorzeichen-Trio | `L1 Sort` korrekt (berechnet über L1 DE, 1:1 zu L1 EN, keine Kollision); Knotenzeilen haben L1 leer; Flags als Text; kein `KPI Block` |
| dim-datum | 730 (tagesgenau 2025–2026) | Datumstabelle, markiert (`dataCategory: Time`, `Datum isKey`), Auto-Datum aus | Fakten nur auf Monatsletzten; 36 Spalten, alle sichtbar; `Periodenstatus` vorhanden, aber nicht genutzt |
| dim-gesellschaft | 9 | Gesellschaft, Segment, Land, Währung | Beschreibung sagt „Sieben“; `Region`/`Region EN` doppelt zu dim-region; `Erstkonsolidierung` als Text |
| dim-region | 3 | Schneeflocken-Ast über dim-gesellschaft | zweites Feld „Region“ in der Feldliste; Slicer nutzen diese Tabelle, Filterinfo prüft sie getrennt |
| dim-waehrung | 7 | Währungsstamm, filtert nur fact-kurse | nicht mit dim-gesellschaft verbunden, der Währungs-Slicer läuft über `dim-gesellschaft[Währung]` |
| fact-kurse | 168 (7 × 24) | Durchschnitts- und Stichtagskurs, Nachvollzug der Umrechnung | kein Budgetkurs; dupliziert Monat/Jahr/Periode aus dim-datum; mit Datum und Währung verbunden (Folie sagt „no relationship“) |
| Beziehungen | 6 | alle 1:*, einfach gefiltert, aktiv | sauber, keine bidirektionalen, keine mehrdeutigen Pfade |

## Was gut ist und bleiben soll

**Drei Modell-Entscheidungen, die als „so baut man das“ auf die Bühne gehören:**
1. **Die Kontendimension ist die Regel-Engine.** Vorzeichen, Anzeige, Bewertung, Zeitaggregation, Sortierung und Formeln stehen als Daten in `dim-konten`. Jeder Stack liest dieselben Spalten: das P&L-Visual direkt, Core/SVG/Deneb über `AC signed`. Daraus folgt: Die Matrix-Summe der Signed-Measures ist genau der Jahresüberschuss, ohne eine einzige Formel in DAX.
2. **Monatsgrain mit Szenarien als Spalten und „leer statt 0“.** Jede Visual-Rolle bekommt ein dünnes `SUM`-Measure. PY wird gespeichert statt per Time Intelligence gerechnet, damit es zum damaligen Kurs steht und sich restaten lässt. Das FY-Skalar mit MAX je Konto × Gesellschaft × Jahr ist ein gutes Lehrstück (A11 Box 3).
3. **Umrechnen vor dem Modell, EUR und LW nebeneinander, LW mit `HASONEVALUE` geschützt.** Die Umrechnung nach IAS 21 bleibt nachvollziehbar (`fact-kurse`, `reconciliation.txt`), und das Modell rechnet keine Kurse zur Laufzeit. Das ist schnell, prüfbar und stack-neutral.

**Anti-Patterns, die der Sprecher selbst benennen sollte, bevor es ein Zuhörer tut:**
- 40 % der Faktzeilen sind Nullen für Strukturzeilen: ein Zugeständnis an das Statement-Visual, kein Modellideal.
- Präsentationslogik im semantischen Modell (SVG, Unicode-Balken, Farbcodes, mEUR-Kopien): bewusst für die Demo. In Produktion gehört sie in eine UDF-Bibliothek oder in Report-Measures.
- Szenarien als Spalten statt Szenario-Dimension: Jede neue Forecast-Version heißt neue Spalten und neue Measures. Für AC/PY/PL/FC ist das richtig, für zwölf FC-Versionen nicht.
- Hart kodierte L1-Namen in Revenue und EBITDA (Befund 8) und deutsche Objektnamen (`fact-abschluss`, `AC Wert`, `Stichtag`) in einer englischen Session: kurz erklären („generated for a German controller, translations not shipped“).
- „Calculation groups“ stehen auf s08/A2 als Plus von Sprosse 1, das Modell hat aber keine. Entweder streichen oder als „would“ formulieren.
- „Real data volumes“ (Abstract): 64 Tsd. Zeilen beweisen keine Performance. Ehrlich sagen und die Größenordnung nennen. `SUMX(fact, x * RELATED(sign))` ist eine einfache Multiplikation, die VertiPaq in die Storage Engine schiebt; das skaliert. Die eigentlichen Kosten liegen in den SVG-Measures je Zelle (`ALLSELECTED` + `MAXX` je Zeile).

**Weiter gut und so lassen:** Keine bidirektionalen Beziehungen und keine Auto-Datumstabellen; die Datumstabelle ist markiert; Wertspalten ausgeblendet, Zugriff nur über Measures; `ALLSELECTED` mit beiden Spalten (`L1 EN`, `L1 Sort`) zum Skalieren, korrekt und auf der Folie erklärbar; SVG-Koordinaten mit `FORMAT(…, "en-US")`; `ΔPL %` mit `ABS` im Nenner, damit das Vorzeichen bei Kosten stimmt; Beschreibungen (`///`) an fast jedem Objekt; ein Parameter `DemoPfad` als einziger Pfad; Display-Ordner trennen die Stacks sauber.
