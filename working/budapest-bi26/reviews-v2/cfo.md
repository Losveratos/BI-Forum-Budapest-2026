# Review CFO

*Perspektive: CFO, Industriegruppe mit 9 Gesellschaften und mehreren Währungen, entscheidet über Reporting-Tools und Budget. Grundlage: 23 Folienbilder (Stand 09.11.), story.html, BRIEF.md, Demo-Seiten. Was in REVIEWS.md vom 7.11. steht, wiederhole ich nicht.*

## Die eine Frage, die der Vortrag beantworten muss (und ob er es tut)

**„Auf welchen Visual-Stack standardisieren wir das Konzern-Reporting, was kostet das über drei Jahre, und wie teuer wird ein Wechsel, wenn wir falsch liegen?“**

Zur Hälfte beantwortet. Die stärkste Aussage für mich steht schon im Deck, wird aber nicht ausgesprochen: Folie 7 („The model answers the questions. The visuals only draw them.“) zusammen mit „Same model under all six“ heißt, dass **die Wahl des Visuals umkehrbar ist, wenn die Regeln im Modell liegen**. Damit wird aus einer Plattformentscheidung eine Entscheidung, die man in Raten treffen kann. Das ist die beste Antwort auf meine Sorge vor Vendor-Lock-in, aber das Wort „reversible“ fällt nirgends und die Wechselkosten werden nicht beziffert.

Den Rest nimmt mir der Vortrag nicht ab. Die Kostenfolie rechnet über 5 Jahre statt 3, ohne die Power-BI-Plattformlizenz und mit Annahmen, von denen 3 von 58 geprüft sind. Die Matrix (Folie 11) hat 56 Zellen und endet mit „Nothing in this table always wins“. Als Ergebnis eines Vortrags ist das ehrlich. Als Entscheidungsvorlage reicht es nicht.

## Drei Dinge, die vor dem Vortrag gefixt sein müssen

1. **Matrix und Rechner widersprechen sich bei den Kosten (Folie 10 vs. 11).** Laut Rechner liegen Paid und Open gleichauf (144 / 148 €) und Core + SVG ist am teuersten (259 €). In der Matrix stehen Open bei ●●●, Paid bei ●○○ und Pure Power BI bei ●●●. Wer im Publikum eine Budgetfrage hat, sieht hier zuerst Voreingenommenheit. Fix: Die Spalte „Cost per reader“ direkt aus dem Rechner-Preset befüllen (Zahl statt Punkte: „144 €“, „148 €“, „176 €“, „259 €“, Rung 1 mit Fußnote „no IBCS notation, not in preset“) und in den Spaltenkopf schreiben: „at 150 readers, 5 authors“.
2. **Plattformkosten und eigener Stundensatz müssen auf Folie 10 stehen.** Eine Pro-Lizenz kostet je Leser mehr als der gesamte Visual-Unterschied. Fix, Zeile unter dem Chart: „Not included: Power BI Pro/PPU or Fabric capacity (same for every stack, but larger than any difference shown), training beyond Deneb, change management. Hours valued at 125 EUR.“ (66.000 € / 528 h = 125 €/h, das steht bisher nur in A1 und auch dort nur indirekt.)
3. **Die Kernbotschaft „umkehrbar“ ausdrücklich sagen, mit Zahl.** Fix, Satz auf Folie 11 unter dem Titel: „Because the rules sit in the model, switching the visual later is a report rebuild, not a migration: in the demo about X hours per page.“ X einmal in der Demo messen (Seite von Rung 5a auf Rung 4 umbauen) und eintragen.

## Befunde (priorisiert, max. 10)

1. **Folie 10 (Rechner)** · Der Zeitraum ist 5 Jahre, mein Budget- und Abschreibungshorizont 3, und bei 3 Jahren verschiebt sich die Reihenfolge, weil Bauaufwand vorne anfällt und Lizenzen linear laufen. · Fix: Preset auf 3 Jahre stellen oder beide nennen: „5 years: tie at 144 / 148 EUR. 3 years: Paid X, Open Y.“ Im Rechner ist das ein Regler, also live umschalten und sagen, wer dadurch gewinnt.

2. **Folie 11 (Matrix), Spalte „Export & audit“** · Für mich ist „no PDF/PPT export, no subscriptions“ bei 5a ein K.-o.-Kriterium (Board-Pack, Aufsichtsrat, Abo an Geschäftsführer der Gesellschaften), und das steht klein in Zeile 5a, ganz rechts. · Fix: Den Satz in der Moderation tragen und auf Folie 11 eine Zeile ergänzen: „If your board pack is a PDF from the Service, rung 5a is out today.“

3. **Folie 11 und Folie 8: Hersteller-Bias in den Bewertungen** · Der Sprecher stellt die Visuals in 5a selbst her, hat den Rechner mitgeschrieben und die Punkte vergeben. 5a bekommt bei IBCS, Kosten und Self-Service ●●●. Die Offenlegung steht nur in Fußzeilen (Folien 4, 8, A6). · Fix: Einmal laut und auf Folie 11 sichtbar: „I build rung 5a. Discount my ratings there; the calculator link lets you replace every assumption.“ Dazu bei 5a die IBCS-Zelle auf ●●○ setzen („built for it, not certified“ ist workable, nicht strong), weil Paid dort mit Zertifikat gleich bewertet ist.

4. **A6 / Folie 8: Abhängigkeit von Einzelpersonen fehlt im Hauptteil** · „You maintain it“ und „abandonment risk 3 to 13 % a year“ stehen nur im Appendix. Wer ist „you“, wenn der Hersteller ein kleines Team ist? · Fix: In der Matrix eine Zeile im Feld „Avoid when“ von 5a: „nobody in-house can build the .pbiviz from source“. Auf A6 Lizenz (MIT?), Quellcode-Ort und Build-Anleitung nennen. Für Deneb gilt dasselbe: Wer pflegt das JSON, wenn die eine Person geht?

5. **Kein Folienplatz für „Microsoft ändert etwas“** · Die Risiken liegen verstreut (Deneb 2.0, Q&A und Legacy Card 02/2027, SVG leer im Service, Fabric Apps Preview, Org-Store ohne Export). Gesammelt sind sie das, was ich nach Hause trage. · Fix: In der Matrix die Spalte „Performance“ für den Hauptteil streichen (die Demo zeigt sie live) und durch „Platform risk“ ersetzen: 1 „Q&A, legacy card 02/2027“ · 2 „low“ · 3 „Service rendering regressions“ · 4 „Deneb 2.0 format change“ · 5a „certification rules“ · 5b „vendor pricing“ · 6 „preview, no Git“.

6. **Zeit bis zum ersten Bericht kommt nirgends vor** · Für mich ist das die zweitwichtigste Zahl nach den Kosten. Die Bausteine stehen verstreut im Deck: Freigabe 8 / 24 / 60 h, 35 h Einarbeitung, „one template click“, „an hour each“ bei Fabric Apps. · Fix: Auf Folie 11 eine Zeile über der Tabelle: „Time to the first approved P&L page: 1 ≈ x d · 4 ≈ 35 h training + x · 5a ≈ approval 8–60 h + x · 5b ≈ procurement + x“. Die Werte aus dem Demo-Bau nehmen.

7. **Folie 4 und Folie 6: Zahlen und Sprache im de-DE-Format vor englischem Publikum** · „Σ 2.818M“ liest ein Engländer als 2,8 Millionen, gemeint sind 2,8 Mrd. Folie 3 zeigt für „Revenue by month“ andere Werte (Jan 262) als Folie 4 (Jan 245). Im P&L-Visual stehen „Ansicht“, „Einheit“, „günstige Δ“. Ein CFO glaubt keinem Kostenvergleich, wenn sich schon die Umsatzzahlen widersprechen. · Fix: Modellkultur oder Format auf en-US stellen, neu rendern, Folie 3 auf die Werte aus dem Demo-Modell bringen (Untertitel „Demo numbers“ reicht dann nicht mehr als Ausrede) und die Visual-UI auf Englisch schalten.

8. **Folie 12 (Fabric Apps) als letzte Inhaltsfolie** · Der Vortrag endet mit dem eigenen dwg CLI („developed in public“) statt mit der Entscheidung. Als Letztes bleibt also ein Produkt hängen. · Fix: Folie 12 vor die Summary ziehen oder in den Appendix (A8 existiert schon) und mit Folie 11 bzw. der Entscheidungsfolie unten enden. Schlusssatz: „Put the rules in the model this quarter. Pick the visual per audience. Re-decide when the reader count doubles.“

9. **A1: „Parity at about 92 EUR, the negotiation ceiling“** · Das ist die nützlichste Zahl im ganzen Deck für meinen Einkauf, und sie steht im Appendix. · Fix: Auf Folie 10 in „What flips the ranking“ als ersten Punkt: „Negotiate below ~92 EUR per user and year and Paid beats building it yourself at 150 readers.“

10. **Folie 10: „3 of 58 assumptions verified“** · Das ist ehrlich, aber im Saal wirkt es so, als wüsste der Sprecher es selbst nicht. · Fix: Die Zahl beibehalten und um die Robustheitsaussage aus A1 ergänzen, auf einer Zeile: „Robust: order of magnitude and the reader count where licences dominate. Not robust: Paid vs Open. Put in your own hours.“

## Was ich als Entscheidungsvorlage brauche (Folienvorschlag in 5 Zeilen)

**Titel: „Your decision in four numbers: readers per author, licence price, your hourly rate, PDF required?“**
1. Erst das Modell: Regeln (Vorzeichen, FY-Skalar, Währung, FX-Effekt) gehören in das semantische Modell. Das sind einmalig x Tage, und danach lässt sich jeder Stack wieder abwählen.
2. Wenn PDF-Export oder Abos Pflicht sind (Board-Pack): Rung 1, 4 oder 5b. Rung 5a fällt dann heute weg.
3. Über ~35 Leser je Autor, mit IBCS-Pflicht und einem Lizenzpreis unter ~92 €: 5b (Paid). Darunter: 4 (Deneb) oder 5a, wenn jemand im Haus den Quellcode pflegen kann.
4. Nicht enthalten: Pro/PPU/Fabric-Capacity (für alle Stacks gleich, aber größer als jeder gezeigte Unterschied), Schulung, Change Management. Horizont 3 Jahre, Stundensatz 125 €.
5. „Send me your four numbers. You get the calculator link with your preset back.“

## Was gut ist und bleiben soll

- **„The model answers the questions. The visuals only draw them.“ (Folie 7)** ist die richtige Botschaft für jemanden, der Budget verantwortet: Die Investition ins Modell bleibt, das Visual ist austauschbar.
- **„Avoid when“ für jede Sprosse** ist das, was ich in Herstellervorträgen sonst nie bekomme. Bitte auch bei 5a so hart lassen.
- **Ehrlichkeit über die Datenbasis** (A1: was hält, was nicht; „Indication, not a quote“; „prices unverified“): Gerade das macht den Sprecher für mich glaubwürdiger als einen Vertriebler.
- **A9 Währung, besonders das Yen-Problem und der FX-Effekt als eigene Zeile:** Genau das ist meine Welt mit neun Gesellschaften. Wenn die Zeit reicht, 30 Sekunden davon in den Hauptteil.
- **„Rules: in …“ als Etikett je Sprosse** ist die einfachste Form, Audit-Fähigkeit zu erklären, ohne das Wort Audit zu benutzen.
- **Live-Demo mit Performance Analyzer und data-as-of-Stempel:** keine vorbereiteten Bilder. Das macht die Bewertungen prüfbar.
- **Was mich nach dem Vortrag zum Sprecher bringt:** das Angebot, meine vier Zahlen (Leser, Autoren, Stundensatz, Lizenzpreis) in den Rechner einzugeben und einen Link für mein Controlling mitzugeben, und eine gemessene Stundenzahl für den Wechsel von einem Stack auf einen anderen beim selben Modell.
