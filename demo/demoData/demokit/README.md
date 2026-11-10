# Demodaten „PnL ChartkitchenDemoKit"

Konzernabschluss eines fiktiven Industriekonzerns — **GuV, Bilanz und
Kapitalflussrechnung in einem Modell**, in **Landeswährung und Euro**, mit
eigenen Dimensionen für Datum, Gesellschaft, Region und Währung, damit man
quer filtern kann. Alle Kontenbezeichnungen liegen in Deutsch und Englisch
vor.

Gebaut für das Custom Visual **P&L Statement byDatenWG 1.7.0.0**.

| Datei | Zeilen | Inhalt |
|---|---:|---|
| `dim-konten.csv` | 296 | Kontenplan: GuV 128, Bilanz 102, Cashflow 66 |
| `dim-datum.csv` | 730 | Tagesgenau 1.1.2025 – 31.12.2026, 37 Spalten |
| `dim-gesellschaft.csv` | 9 | Gesellschaften mit Region, Land, Segment, Währung |
| `dim-region.csv` | 3 | EMEA, Americas, APAC |
| `dim-waehrung.csv` | 7 | EUR, CHF, PLN, CZK, USD, AUD, JPY |
| `fact-kurse.csv` | 168 | Monatskurse je Währung, Durchschnitt und Stichtag |
| `fact-abschluss.csv` | 63.936 | Konto × Gesellschaft × Monat, AC/PY/PL/FC je Währung |
| `reconciliation.txt` | — | Abnahmewerte und Ergebnis aller Prüfungen |

> **Einheit:** Die CSV-Dateien liefern **Basiseinheiten** der jeweiligen
> Währung — also Euro, nicht Millionen Euro. Das ist keine Kosmetik: das
> Visual skaliert selbst, seine Einstellung `unit` teilt den Rohwert durch
> 1e3, 1e6 oder 1e9. Lieferte man schon Millionen, zeigte es bei `unit = "m"`
> überall 0,0. Siehe „Fallstricke" unten.

Generator: `python generate_demokit.py` (Seed fest, byte-identisch
reproduzierbar). Modell neu verdrahten: `python build_model_tmdl.py`.

---

## Der Konzern

**DWG Industries SE** mit Sitz in Deutschland, diversifizierter
Industriekonzern, Konzernumsatz 2026 rund 3,4 Mrd. EUR netto. Vier Segmente,
drei Regionen, neun Gesellschaften, **sieben Währungen**:

| ID | Gesellschaft | Region | Land | Währung | Segment | Umsatz 2026 |
|---|---|---|---|---|---|---:|
| 1100 | DWG Automation GmbH | EMEA | Deutschland | EUR | Industrial Automation | 820 |
| 1200 | DWG Energy Systems AG | EMEA | Deutschland | EUR | Energiesysteme | 690 |
| 1300 | DWG Mobility Solutions S.A.S. | EMEA | Frankreich | EUR | Mobilitätslösungen | 480 |
| 1400 | DWG Automation Schweiz AG | EMEA | Schweiz | CHF | Industrial Automation | 260 |
| 1500 | DWG Energy Polska sp. z o.o. | EMEA | Polen | PLN | Energiesysteme | 210 |
| 1600 | DWG Automation Czechia s.r.o. | EMEA | Tschechien | CZK | Industrial Automation | 180 |
| 2100 | DWG Industries North America Inc. | Americas | USA | USD | Industrial Automation | 610 |
| 3100 | DWG Mobility Australia Pty Ltd | APAC | Australien | AUD | Mobilitätslösungen | 190 |
| 3200 | DWG Digital Services KK | APAC | Japan | JPY | Digitale Dienste | 120 |

Umsatzziele in mEUR, brutto vor Erlösschmälerungen. Sechs der neun
Gesellschaften bilanzieren in einer anderen Währung als der Euro.

**Zeitachse:** Ist von Januar 2025 bis Oktober 2026, Forecast für November
und Dezember 2026, Plan über beide Jahre. Das Vorjahr PY ist der um zwölf
Monate verschobene Ist-Pfad — für 2026 ist PY also exakt das Ist aus 2025,
für 2025 ein mitgerechneter 2024er-Pfad. Dadurch stimmt die Vorjahresspalte
monatsgenau und nicht nur ungefähr; in EUR trägt sie zusätzlich den Kurs des
damaligen Monats.

---

## Die drei Rechenwerke hängen rechnerisch zusammen

Das ist der eigentliche Unterschied zu gewürfelten Demodaten:

* Die **GuV** entsteht aus Treibern — Umsatz je Segment, Rohertragsmarge,
  Kostenquoten, DSO/DIO/DPO.
* Die **Bilanz** wird fortgeschrieben: Anlagevermögen = Anfangsbestand
  + Investitionen − Abschreibungen, Eigenkapital = Anfangsbestand
  + Jahresüberschuss − Dividende, Working Capital aus den Umschlagsdauern.
  Aktiva = Passiva gilt per Konstruktion, die langfristigen
  Finanzverbindlichkeiten sind die Ausgleichsposition.
* Die **Kapitalflussrechnung** wird aus den Bilanzbewegungen abgeleitet.
  Jede Bewegung erscheint genau einmal — direkt oder über den
  Jahresüberschuss. Deshalb ergibt CFO + CFI + CFF + Währungseffekte
  + Konsolidierungskreis exakt die Veränderung des Finanzmittelfonds.

Zwei Kontrollzeilen machen das im Bericht sichtbar und müssen in **jeder**
Filterkombination 0 ergeben:

* `Bilanzkontrolle` = Summe Aktiva − Summe Passiva
* `Kontrolle Finanzmittelfonds` = Endbestand − Anfangsbestand
  − Fondsveränderung − Währungs- und Konsolidierungseffekte

Geprüft wird das nicht behauptet, sondern nachgerechnet: `checks.py` baut die
Statement-Logik des Visuals nach (Levels-Pfade, synthetische Zwischensummen,
Vorzeichenkonvention, Bestands- statt Summenbildung, Formelauflösung) und
rechnet **144 Kombinationen** durch — drei Aufstellungen × vier Szenarien ×
drei Zeiträume × Deutsch und Englisch × Euro und Landeswährung. Zusätzlich
die Bilanz je einzelner Gesellschaft und Einzelmonat in beiden Währungen, die
referentielle Integrität aller Schlüssel, eine Stichprobe auf die Umrechnung
(Fluss zum Durchschnitts-, Bestand zum Stichtagskurs) und die Prüfung, dass
kein Wert auf Null rundet. Das Ergebnis steht unten in `reconciliation.txt`.

---

## Aufstellung umschalten

`dim-konten[Abschluss]` enthält `GuV`, `Bilanz` oder `Cashflow`
(englisch: `dim-konten[Statement]`). Jede Aufstellung hat ihre eigene
Hierarchie, ihre eigenen Zwischensummen und ihre eigenen Kennzahlen.

Weil die Formelauflösung des Visuals über **global eindeutige Zeilennamen**
läuft, ist kein Name doppelt belegt — auch nicht über die
Aufstellungsgrenze hinweg. Darum heißt die Cashflow-Zeile
„Jahresüberschuss der Periode" und nicht einfach „Jahresüberschuss".

Der Bericht nutzt beide Wege:

| Seite | Aufstellung kommt von | Slicer |
|---|---|---|
| **GuV** | Seitenfilter `Abschluss = GuV`, in der Leseansicht gesperrt | Region, Land, Währung, Gesellschaft, Jahr, Monat |
| **Bilanz** | Seitenfilter `Abschluss = Bilanz`, gesperrt | dieselben sechs |
| **Cashflow** | Seitenfilter `Abschluss = Cashflow`, gesperrt | dieselben sechs |
| **Abschluss** | Slicer `Abschluss`, auf `GuV` vorbelegt | zusätzlich der Abschluss-Slicer |

Die drei Statement-Seiten tragen je eine eigene Kopfzeile und eine eigene
Kernaussage im Titelblock. Die vierte Seite zeigt, dass eine einzige
Visual-Instanz alle drei Rechenwerke bedienen kann — praktisch zum
Vorführen, weil der Wechsel ohne Seitensprung passiert.

Die Visual-Namen sind je Seite mit einem Kürzel versehen (`pnlGuv`,
`pnlBil`, `pnlCfl`), damit Lesezeichen und Visual-Interaktionen eindeutig
bleiben.

---

## Währungen: Landeswährung und Euro

Jede Gesellschaft bilanziert in ihrer funktionalen Währung. Der Motor rechnet
den **ganzen Abschluss in Landeswährung** und rechnet erst am Ende um — so
wie ein Konzern es auch macht. Das ist wichtig, weil nur dann ein echter
Währungseffekt entsteht: wächst eine Gesellschaft lokal, der Kurs läuft aber
weg, schrumpft ihr Beitrag in Euro trotzdem.

Umgerechnet wird nach **IAS 21**:

| Posten | Kurs |
|---|---|
| Erträge, Aufwendungen, Zahlungsströme | **Durchschnittskurs** des Monats |
| Bilanzposten | **Stichtagskurs** zum Monatsletzten |
| Zahlungsmittelbestand am Anfang der Periode | Stichtagskurs des **Vormonats** |

Die Faktentabelle liefert beides nebeneinander. Spalten **ohne Zusatz** sind
Konzernwährung (EUR), Spalten mit **`_LW`** sind Landeswährung:

```
AC   AC_LW   PY   PY_LW   PL   PL_LW   FC   FC_LW   FC_FY   FC_FY_LW   PL_FY   PL_FY_LW
```

Die Umrechnung ist also bereits vollzogen und braucht kein DAX. `fact-kurse`
macht sie nachvollziehbar: Durchschnitts- und Stichtagskurs je Währung und
Monat, in Einheiten der Landeswährung je 1 EUR. Ein **steigender** Kurs heißt,
die Landeswährung wird schwächer.

Die Measures spiegeln das:

| Anzeigeordner | Measures |
|---|---|
| Szenarien (EUR) | `AC`, `PY`, `PL`, `FC` |
| Szenarien (Landeswährung) | `AC LW`, `PY LW`, `PL LW`, `FC LW` |
| Jahresskalare | `FC FY`, `PL FY`, `FC FY LW`, `PL FY LW` |
| Kurse | `Durchschnittskurs`, `Stichtagskurs` |

**Die LW-Measures liefern BLANK, sobald mehr als eine Währung im Filter
liegt.** Eine Summe über CHF und JPY wäre keine Zahl, die etwas bedeutet, und
eine stumme Fehlsumme ist schlimmer als eine leere Zelle. Erst wenn der
Währungs- oder Gesellschaftsslicer auf eine Währung einschränkt, erscheint
ein Wert.

### Der Währungseffekt als Story

Über den Demozeitraum werten CHF (−3,8 %), PLN (−2,7 %) und CZK (−1,5 %)
gegenüber dem Euro auf, während USD (+3,1 %), AUD (+3,6 %) und besonders
**JPY (+11,1 %)** abwerten. `reconciliation.txt` stellt das Ist in EUR dem Ist
zu den Kursen des Vorjahresmonats gegenüber: der Effekt beträgt +8,4 mEUR oder
0,30 % der Umsatzerlöse. Die japanische Gesellschaft verliert dabei 2,7 mEUR,
die Schweizer gewinnt 5,8 mEUR.

Dazu kommt ein **transaktionsbedingter** Währungsverlust in der GuV der
US-Gesellschaft im Juni 2026 (6,8 mEUR, Fußnote ④) — nicht zu verwechseln
mit dem Umrechnungseffekt, der nirgends in der GuV auftaucht.

### Was in Euro nicht aufgeht, und warum das richtig ist

Die Bilanz geht in **beiden** Währungen exakt auf, weil Aktiva und Passiva mit
demselben Stichtagskurs umgerechnet werden. Die Kapitalflussrechnung geht in
beiden Währungen auf, weil die Zeile **„Währungsbedingte Effekte auf den
Finanzmittelfonds"** genau die Differenz trägt zwischen den zum
Durchschnittskurs umgerechneten Zahlungsströmen und der zum Stichtagskurs
umgerechneten Bestandsveränderung. Genau dafür sieht IAS 7 diese Zeile vor.

Was in Euro **nicht** übereinstimmt: der Jahresüberschuss der GuV
(Durchschnittskurs) und die Eigenkapitalzeile „Jahresüberschuss
(Konzernanteil)" (Stichtagskurs). Das ist der Umrechnungseffekt, den IAS 21
erzeugt und den ein echter Konzernabschluss in der Währungsumrechnungsrücklage
erklärt. In Landeswährung stimmen die drei Rechenwerke auf die Stelle überein
— und genau dort prüft `checks.py` hart.

### Warum die Währung nicht an den Gesellschaften hängt

`dim-waehrung` ist mit `fact-kurse` verbunden, **nicht** mit
`dim-gesellschaft`. Sonst entstünde der Ring

```
dim-datum → fact-kurse → dim-waehrung → dim-gesellschaft → fact-abschluss → dim-datum
```

und Power BI lässt keinen geschlossenen Beziehungsring zu. Nach Währung
filtert man darum über die Spalte `dim-gesellschaft[Währung]` — die filtert
die Gesellschaften und damit die Fakten. Im Bericht steht genau dieser
Slicer.

---

## Bestandsgrößen: eine Bilanz darf man nicht summieren

Version 1.7 des Visuals kann das selbst. Es liest Tokens aus der Spalte
`RowType`:

| RowType | Bedeutung |
|---|---|
| `Account` | Flussgröße, wird über die Perioden summiert |
| `Account stock` | Bestand, Wert der **letzten** Periode der Auswahl |
| `Account opening` | Bestand, Wert der **ersten** Periode der Auswahl |
| `Subtotal stock`, `Formula stock`, `Kpi stock` | dito für Struktur- und Kennzahlenzeilen |

Alle 100 wertführenden Bilanzzeilen tragen `stock` (die beiden Trennzeilen
nicht), im Cashflow trägt der Zahlungsmittelbestand am Ende der Periode
`stock` und der am Anfang `opening` — alles andere ist Fluss. Die Einstellung
`statement.stockMode` steht auf `auto`, damit die Tokens greifen.

Die abgeleitete Spalte `dim-konten[Zeitaggregation]` (`Summe` / `Bestand` /
`Bestand Anfang`) sagt dasselbe in Klartext. Sie wird von den Measures mit
dem Zusatz **Stichtag** ausgewertet — die braucht man nur für Karten und
Matrizen *außerhalb* des P&L-Visuals, wo sonst 24 Bilanzstichtage
aufsummiert würden. Das Visual selbst kommt mit den einfachen
Szenario-Measures aus.

---

## Deutsch und Englisch

Das Visual übersetzt **keine Daten** — nur seine eigene Oberfläche. Für
zweisprachige Kontenpläne muss man die Feldbindung tauschen:

| Rolle im Visual | Deutsch | Englisch |
|---|---|---|
| Account name | `Name` | `Name EN` |
| Levels | `L1` … `L6` | `L1 EN` … `L6 EN` |
| Formula def | `FormulaDef` | `FormulaDef EN` |
| Comment | `Kommentar` | `Comment EN` |

`FormulaDef EN` ist mitübersetzt — die Referenzen in eckigen Klammern zeigen
dort auf die englischen Zeilennamen, sonst würde nach dem Umschalten jede
Formel „unknown reference" melden. Die beiden Spaltensätze liegen in den
Anzeigeordnern *Levels DE* und *Levels EN*.

Auch die Dimensionen sind zweisprachig: `dim-gesellschaft` hat
`Company`/`Country`/`Segment EN`, `dim-region` hat `Region EN`,
`dim-datum` hat `Month Long`/`Month Short`/`Period`/`Period Status`.

---

## Beide Hierarchie-Modi in einer Dimension

* **Levels-Modus** (so ist der Bericht verdrahtet): `L1`…`L6` binden,
  `ParentAccountID` **nicht** binden. Die 80 expliziten Knotenzeilen haben
  leere L-Spalten und werden vom Visual übersprungen; die Zwischensummen
  entstehen aus den Pfaden. Die Äste enden unterschiedlich tief — GuV bis
  Ebene 4, Bilanz und Cashflow bis Ebene 3.
* **Parent-Child-Modus**: `L1`…`L6` entfernen, stattdessen
  `ParentAccountID` in „Parent account ID" ziehen. Jetzt tragen die
  Knotenzeilen die Struktur.

`SortOrder` ist dicht in Zehnerschritten vergeben, Knotenzeilen liegen auf
`−5` vor ihrem ersten Kind. **Die Sortierfalle aus Version 0.3 ist weg:**
seit 1.7 erbt ein synthetischer Zwischensummenknoten das Minimum der
SortOrder seiner Nachfahren und liegt damit zwangsläufig auf derselben Skala
wie die expliziten Zeilen. Die frühere Regel „SortOrder = Periodenanzahl ×
Zeilenposition" gilt nicht mehr, und der Datensatz ist dadurch nicht mehr auf
eine feste Monatszahl kalibriert.

Was weiter gilt: **keine Lücke in der SortOrder-Spalte lassen.** Eine Zeile
ohne Wert fällt auf den DataView-Index zurück und sortiert falsch.

---

## DataView-Budget

Das Visual holt bis zu 30.000 Zeilen (danach Fußnote „Zeilenlimit
erreicht"). Der Bedarf ist Konten × Perioden × Werte der Spaltenkategorie:

| Auswahl | Zeilen |
|---|---:|
| GuV, 24 Monate | 3.072 |
| alle drei Aufstellungen, 24 Monate | 7.104 |
| GuV, 24 Monate, Spaltenkategorie mit 4 Werten | 12.288 |

Reichlich Luft — anders als beim alten 5.000-Zeilen-Stresstest in
`../industrial/`, der exakt am Limit lag. Die zweite Währung kostet keine
DataView-Zeilen, sondern nur Spalten in der Faktentabelle: neun
Gesellschaften × 296 Konten × 24 Monate = 63.936 Zeilen mit je zwölf
Wertspalten, zusammen 7,4 MB.

---

## Eingebaute Storys

Elf Effekte, alle numerisch selbstgeprüft. Sechs tragen eine Fußnote ①–⑥
auf der betroffenen Zeile, vier weitere Fußnoten ⑦–⑩ erklären die beiden
Kontrollzeilen, das `opening`-Token und den Restposten im Cashflow:

1. **Mobility Solutions schwächelt** — 8 % unter Plan YTD 2026, im zweiten
   Halbjahr zusätzlich −4,5 %, dazu 1,4 Punkte Margenverlust.
2. **Energy Systems und Polen überkompensieren** — +6,3 % bzw. +5,0 %
   über Plan; die Automation GmbH liegt +4,7 % über Plan.
3. ① **Halbleiter-Spotkäufe** März bis Mai 2026, +26 % auf die
   Materialgruppe Elektronik bei Automation und Mobility.
4. ② **Seefracht-Spitze** im vierten Quartal 2025, +72 % über Plan.
5. ③ **Public-Cloud-Kosten** wachsen 2026 monatlich um gut 5 %.
6. ④ **Transaktionsbedingter Währungsverlust** der US-Gesellschaft, Juni
   2026, einmalig −6,8 mEUR in der GuV.
7. ⑤ **Lizenz-Einmalerlös** September 2026 bei Automation GmbH, 14,5 mEUR.
8. ⑥ **Goodwill-Wertminderung** Mobility Solutions, Dezember 2025,
   21,0 mEUR — erklärt den Abschreibungssprung im Jahresvergleich.
9. **Währungseffekt über sechs Fremdwährungen** — CHF, PLN und CZK werten
   auf, USD, AUD und besonders JPY (+11,1 %) ab. Konzerneffekt +8,4 mEUR
   auf die Umsatzerlöse; die japanische Gesellschaft wächst lokal und
   verliert in Euro trotzdem.
10. **Zukauf ohne Vorjahr** — DWG Digital Services KK kommt erst 2026-04 in
    den Konsolidierungskreis. Vor April 2026 sind alle Werte leer (Sparkline
    mit Lücke), ein Vorjahr gibt es nie. Der Zugang erscheint im Cashflow als
    „Veränderung des Konsolidierungskreises", 10,0 mEUR.
11. **11 ruhende Konten** ohne Ist-Werte — Testfall „Nullzeilen ausblenden".

---

## Fallstricke, die beim Bau Zeit gekostet haben

**Das Visual skaliert selbst — liefere Basiseinheiten, nicht Millionen.**
Der erste Datenstand lag in mEUR, und das Visual zeigte in *jeder* Zelle
0,0. Grund steht im Code der Zahlenformatierung:

```js
makeFmt(t){ const e=this.ui.unit; let s=1,i="";
  "k"===e?(s=1e3,i="k"): "m"===e?(s=1e6,i="m"): "b"===e?(s=1e9,i="b"):
  "auto"===e&&(t>=5e10?(s=1e9,i="b"):t>=5e7?(s=1e6,i="m"):t>=5e4&&(s=1e3,i="k"));
```

`unit` **teilt den Rohwert**. Bei `unit = "m"` und Daten in Millionen wird aus
60 mEUR Monatsumsatz 60/1e6 = 0,00006 — gerundet 0,0m. Deshalb liefert der
Generator Basiseinheiten (`UNIT = 1_000_000` in `generate_demokit.py`), und
`checks.py` prüft, dass auch das 10-%-Quantil der Werte nicht auf Null rundet.
Nebeneffekt: `unit = "auto"` wählt die Skala jetzt korrekt selbst.

Was dabei **kein** Fehler ist: die 36 % der Faktzeilen mit einer harten Null.
Das sind die Struktur-, Formel- und Trennzeilen. Sie brauchen Faktzeilen,
damit sie im DataView bleiben, und ihre Werte rechnet das Visual aus den
Kindern beziehungsweise der Formel. Im Bericht fallen sie nicht auf, weil die
Rohspalten versteckt sind — nur in der Datenansicht von Desktop sieht man sie.

**Ein Measure darf nicht wie eine Spalte derselben Tabelle heißen.** Sonst
wirft Power BI Desktop beim Laden `PFE_XL_MEASURE_COLUMN_ALREADY_EXIST`.
Darum heißen die Faktspalten `AC Wert`, `PY Wert`, `PL Wert`, `FC Wert`
(mit `sourceColumn` AC/PY/PL/FC) und die Measures `AC`, `PY`, `PL`, `FC`;
für die Landeswährung entsprechend `AC LW Wert` neben `AC LW`. Die
FY-Skalare brauchen das nicht: `FC_FY` und `FC FY` sind für Tabular schon
verschiedene Namen.

**`FC_FY` und `PL_FY` nur mit MAX aggregieren.** Der Jahresskalar steht
identisch auf jeder Monatszeile; SUM wäre zwölffach zu groß. Das Visual
nimmt ohnehin nur den ersten Wert je Konto. Die Measures summieren MAX je
Gesellschaft **und** Jahr — sonst käme bei neun Gesellschaften nur die
größte einzelne heraus statt der Summe. Eindeutig ist die FY-Spalte nur,
wenn ein Geschäftsjahr gefiltert ist.

**Die Rolle „Filter info" braucht eine Text-Measure.** Eine Zahl würde
unformatiert als JS-String in der Fußzeile landen. `Filterinfo` liefert
Gesellschaft, Region und Zeitraum als Text; `titleBlock.filterFooter` muss
dafür an sein.

**Ein gespeicherter Visual-Zustand überlebt den Datenwechsel.** Im
`state.uiState` des Visuals stehen die eingeklappten Knoten als Pfade
(`L:Umsatzerlöse¦Produkterlöse`). Nach einem Umbau der Hierarchie zeigen die
alten Pfade ins Leere — die Liste muss mit. Dasselbe gilt für die
gespeicherte Ansicht.

**Ein geschlossener Beziehungsring ist nicht erlaubt.** Die Währung an
`dim-gesellschaft` *und* `fact-kurse` zu hängen schließt einen Ring über
`dim-datum`; Power BI lehnt das ab. Siehe „Warum die Währung nicht an den
Gesellschaften hängt".

**Vorsicht beim Vergleich von YTD gegen Geschäftsjahr.** Das Ist endet im
Oktober 2026, Plan und Forecast laufen bis Dezember. Wer „2026" filtert,
vergleicht 10 Ist-Monate gegen 12 Plan-Monate und sieht einen Einbruch, der
keiner ist. `reconciliation.txt` zeigt darum beides getrennt: YTD Januar bis
Oktober mit gleicher Monatszahl in allen Spalten, und das Geschäftsjahr über
FC gegen PL.

**`pbir visuals bind` kennt die Rollen eines Custom Visuals nicht.** Es
leitet die erlaubten Rollen aus dem bestehenden `queryState` ab und lehnt
neue ab, auch mit `--rawdog`. Die Rollen `fc` und `filterInfo` mussten
direkt in `visual.json` eingehängt werden.

**Eine explizite `subtotal`-Zeile funktioniert im Levels-Modus nicht.** Sie
hätte dort keine Kinder und bliebe leer, weil die Zwischensummen aus den
Level-Pfaden entstehen. Die Summenzeilen der Bilanz und des Cashflows sind
darum Formelzeilen, die auf die Namen der synthetischen Knoten verweisen
(`[Anlagevermögen] + [Umlaufvermögen]`) — das trägt in beiden
Hierarchie-Modi.

---

## Datenpfad

Alle fünf Partitionen hängen am Power-Query-Parameter **`DemoPfad`** in
`expressions.tmdl`. Ordner verschieben heißt: eine Zeile ändern, nicht fünf
Partitionen.

Nach jedem Eingriff:

```bash
te validate -m "PnL ChartkitchenDemoKit.SemanticModel" --errors-only
```

```bash
pbir validate "PnL ChartkitchenDemoKit.Report" --fields
```
