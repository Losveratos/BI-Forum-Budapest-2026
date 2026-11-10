# -*- coding: utf-8 -*-
"""Kontenplan GuV (Gewinn- und Verlustrechnung) fuer das PnL ChartkitchenDemoKit.

Zeilenformat (identisch fuer GuV, Bilanz und Cashflow):

    (l1, l2, l3, l4, rowtype, sign, display_invert, variance_invert, formula, tag)

l1..l4          Hierarchie-Ebenen, deutsche Bezeichnung. Strukturzeilen
                (subtotal / formula / kpi / separator) fuellen nur l1 und
                lassen den Rest leer -- so stehen sie auf oberster Ebene.
rowtype         account | subtotal | formula | kpi | separator
sign            Vorzeichenkonvention; wird VOR Summen und Formeln
                anmultipliziert (Visual-Semantik).
display_invert  Zeile mit umgekehrtem Vorzeichen anzeigen (Kostenzeilen
                erscheinen dadurch positiv).
variance_invert "weniger ist besser" -- Abweichung unter Plan wird gruen.
formula         nur fuer formula/kpi: Referenzen in eckigen Klammern auf
                global eindeutige Zeilennamen, Operatoren + - * / ( ).
                KPI-Zeilen liefern ein Verhaeltnis OHNE *100 -- das Visual
                formatiert rowtype=kpi selbst als Prozent.
tag             eindeutiger ASCII-Slug ueber alle drei Aufstellungen hinweg;
                Schluessel fuer die Wertgenerierung.

Die Ebenen enthalten bewusst KEINE Gesellschaft und KEINE Region mehr --
die stecken jetzt in eigenen Dimensionen, damit man quer filtern kann.
"""

# ---------------------------------------------------------------------------
# GuV
# ---------------------------------------------------------------------------

GUV = [
    # --- Umsatzerloese ----------------------------------------------------
    ("Umsatzerlöse", "Produkterlöse", "Erlöse Inland", "Neuanlagen",
     "account", 1, False, False, "", "rev_inland_neu"),
    ("Umsatzerlöse", "Produkterlöse", "Erlöse Inland", "Modernisierung & Retrofit",
     "account", 1, False, False, "", "rev_inland_retrofit"),
    ("Umsatzerlöse", "Produkterlöse", "Erlöse Export", "",
     "account", 1, False, False, "", "rev_export"),
    ("Umsatzerlöse", "Produkterlöse", "Erlöse Projektgeschäft", "",
     "account", 1, False, False, "", "rev_projekt"),
    ("Umsatzerlöse", "Produkterlöse", "Erlöse Anlagenbau", "",
     "account", 1, False, False, "", "rev_anlagenbau"),

    ("Umsatzerlöse", "Serviceerlöse", "Wartung & Instandhaltung", "",
     "account", 1, False, False, "", "rev_wartung"),
    ("Umsatzerlöse", "Serviceerlöse", "Ersatzteilerlöse", "",
     "account", 1, False, False, "", "rev_ersatzteile"),
    ("Umsatzerlöse", "Serviceerlöse", "Schulung & Inbetriebnahme", "",
     "account", 1, False, False, "", "rev_schulung"),
    ("Umsatzerlöse", "Serviceerlöse", "Technischer Support", "",
     "account", 1, False, False, "", "rev_support"),

    ("Umsatzerlöse", "Software & Lizenzen", "Lizenzerlöse", "",
     "account", 1, False, False, "", "rev_lizenz"),
    ("Umsatzerlöse", "Software & Lizenzen", "Subskriptionserlöse", "",
     "account", 1, False, False, "", "rev_subskription"),
    ("Umsatzerlöse", "Software & Lizenzen", "Cloud- & Hosting-Erlöse", "",
     "account", 1, False, False, "", "rev_cloud"),

    ("Umsatzerlöse", "Erlösschmälerungen", "Boni & Rabatte", "",
     "account", -1, False, True, "", "rev_boni"),
    ("Umsatzerlöse", "Erlösschmälerungen", "Gutschriften & Retouren", "",
     "account", -1, False, True, "", "rev_gutschriften"),
    ("Umsatzerlöse", "Erlösschmälerungen", "Skonti", "",
     "account", -1, False, True, "", "rev_skonti"),

    # --- Umsatzkosten -----------------------------------------------------
    ("Umsatzkosten", "Materialaufwand", "Roh-, Hilfs- & Betriebsstoffe", "Metalle & Stahl",
     "account", -1, True, True, "", "cogs_mat_metall"),
    ("Umsatzkosten", "Materialaufwand", "Roh-, Hilfs- & Betriebsstoffe", "Elektronik & Halbleiter",
     "account", -1, True, True, "", "cogs_mat_elektronik"),
    ("Umsatzkosten", "Materialaufwand", "Roh-, Hilfs- & Betriebsstoffe", "Kunststoffe & Dichtungen",
     "account", -1, True, True, "", "cogs_mat_kunststoff"),
    ("Umsatzkosten", "Materialaufwand", "Bezogene Handelswaren", "",
     "account", -1, True, True, "", "cogs_handelswaren"),
    ("Umsatzkosten", "Materialaufwand", "Bezogene Leistungen", "",
     "account", -1, True, True, "", "cogs_bezogene_leistungen"),
    ("Umsatzkosten", "Materialaufwand", "Energie & Medien", "",
     "account", -1, True, True, "", "cogs_energie"),

    ("Umsatzkosten", "Fertigungskosten", "Fertigungslöhne", "",
     "account", -1, True, True, "", "cogs_fertigungsloehne"),
    ("Umsatzkosten", "Fertigungskosten", "Fertigungsgemeinkosten", "",
     "account", -1, True, True, "", "cogs_gemeinkosten"),
    ("Umsatzkosten", "Fertigungskosten", "Instandhaltung Produktion", "",
     "account", -1, True, True, "", "cogs_instandhaltung"),
    ("Umsatzkosten", "Fertigungskosten", "Ausschuss & Nacharbeit", "",
     "account", -1, True, True, "", "cogs_ausschuss"),

    ("Umsatzkosten", "Logistikkosten", "Frachten & Zölle", "Seefracht",
     "account", -1, True, True, "", "cogs_seefracht"),
    ("Umsatzkosten", "Logistikkosten", "Frachten & Zölle", "Luftfracht",
     "account", -1, True, True, "", "cogs_luftfracht"),
    ("Umsatzkosten", "Logistikkosten", "Frachten & Zölle", "Landverkehr",
     "account", -1, True, True, "", "cogs_landverkehr"),
    ("Umsatzkosten", "Logistikkosten", "Lagerkosten", "",
     "account", -1, True, True, "", "cogs_lager"),
    ("Umsatzkosten", "Logistikkosten", "Verpackung", "",
     "account", -1, True, True, "", "cogs_verpackung"),

    ("Umsatzkosten", "Gewährleistung", "Garantie & Kulanz", "",
     "account", -1, True, True, "", "cogs_garantie"),
    ("Umsatzkosten", "Gewährleistung", "Veränderung Gewährleistungsrückstellung", "",
     "account", -1, True, True, "", "cogs_gewaehrl_rst"),

    # --- Rohertrag --------------------------------------------------------
    ("Rohertrag", "", "", "",
     "formula", 1, False, False, "[Umsatzerlöse] + [Umsatzkosten]", "f_rohertrag"),
    ("Rohertragsmarge %", "", "", "",
     "kpi", 1, False, False, "[Rohertrag] / [Umsatzerlöse]", "k_rohertragsmarge"),
    ("———", "", "", "", "separator", 1, False, False, "", "sep_1"),

    # --- Vertriebskosten --------------------------------------------------
    ("Vertriebskosten", "Personalkosten Vertrieb", "Gehälter Vertrieb", "",
     "account", -1, True, True, "", "sell_gehaelter"),
    ("Vertriebskosten", "Personalkosten Vertrieb", "Provisionen & Prämien", "",
     "account", -1, True, True, "", "sell_provisionen"),
    ("Vertriebskosten", "Personalkosten Vertrieb", "Reisekosten Vertrieb", "",
     "account", -1, True, True, "", "sell_reisekosten"),
    ("Vertriebskosten", "Marketing", "Messen & Events", "",
     "account", -1, True, True, "", "sell_messen"),
    ("Vertriebskosten", "Marketing", "Digitales Marketing", "",
     "account", -1, True, True, "", "sell_digital"),
    ("Vertriebskosten", "Marketing", "Werbemittel & Kataloge", "",
     "account", -1, True, True, "", "sell_werbemittel"),
    ("Vertriebskosten", "Vertriebsstruktur", "Vertriebsbüros", "",
     "account", -1, True, True, "", "sell_bueros"),
    ("Vertriebskosten", "Vertriebsstruktur", "Fahrzeugflotte", "",
     "account", -1, True, True, "", "sell_flotte"),

    # --- Verwaltungskosten ------------------------------------------------
    ("Verwaltungskosten", "Personalkosten Verwaltung", "Gehälter Verwaltung", "",
     "account", -1, True, True, "", "admin_gehaelter"),
    ("Verwaltungskosten", "Personalkosten Verwaltung", "Altersversorgung", "",
     "account", -1, True, True, "", "admin_altersversorgung"),
    ("Verwaltungskosten", "Personalkosten Verwaltung", "Aus- & Weiterbildung", "",
     "account", -1, True, True, "", "admin_weiterbildung"),
    ("Verwaltungskosten", "IT & Infrastruktur", "IT-Betrieb", "",
     "account", -1, True, True, "", "admin_it_betrieb"),
    ("Verwaltungskosten", "IT & Infrastruktur", "Cloud- & Softwarelizenzen", "Public Cloud",
     "account", -1, True, True, "", "admin_public_cloud"),
    ("Verwaltungskosten", "IT & Infrastruktur", "Cloud- & Softwarelizenzen", "Lizenzen Standardsoftware",
     "account", -1, True, True, "", "admin_lizenzen_std"),
    ("Verwaltungskosten", "IT & Infrastruktur", "Telekommunikation", "",
     "account", -1, True, True, "", "admin_telekom"),
    ("Verwaltungskosten", "Externe Dienstleistungen", "Rechts- & Beratungskosten", "",
     "account", -1, True, True, "", "admin_beratung"),
    ("Verwaltungskosten", "Externe Dienstleistungen", "Abschluss- & Prüfungskosten", "",
     "account", -1, True, True, "", "admin_pruefung"),
    ("Verwaltungskosten", "Externe Dienstleistungen", "Versicherungen", "",
     "account", -1, True, True, "", "admin_versicherungen"),
    ("Verwaltungskosten", "Raumkosten", "Mieten & Pachten", "",
     "account", -1, True, True, "", "admin_mieten"),
    ("Verwaltungskosten", "Raumkosten", "Nebenkosten & Gebäudebetrieb", "",
     "account", -1, True, True, "", "admin_nebenkosten"),

    # --- Forschung & Entwicklung -----------------------------------------
    ("Forschung & Entwicklung", "F&E Personal", "Entwicklungsgehälter", "",
     "account", -1, True, True, "", "rnd_gehaelter"),
    ("Forschung & Entwicklung", "F&E Personal", "Externe Entwicklungsleistungen", "",
     "account", -1, True, True, "", "rnd_extern"),
    ("Forschung & Entwicklung", "F&E Sachkosten", "Prototypen & Versuche", "",
     "account", -1, True, True, "", "rnd_prototypen"),
    ("Forschung & Entwicklung", "F&E Sachkosten", "Patente & Schutzrechte", "",
     "account", -1, True, True, "", "rnd_patente"),
    # negativer Kostenbetrag => entlastet den Block (aktivierte Eigenleistung)
    ("Forschung & Entwicklung", "F&E Sachkosten", "Aktivierte Entwicklungskosten", "",
     "account", -1, True, True, "", "rnd_aktiviert"),

    # --- Sonstiges betriebliches Ergebnis ---------------------------------
    ("Sonstiges betriebliches Ergebnis", "Sonstige Erträge", "Erträge aus Auflösung von Rückstellungen", "",
     "account", 1, False, False, "", "oth_rst_aufloesung"),
    ("Sonstiges betriebliches Ergebnis", "Sonstige Erträge", "Kursgewinne operativ", "",
     "account", 1, False, False, "", "oth_kursgewinne"),
    ("Sonstiges betriebliches Ergebnis", "Sonstige Erträge", "Mieterträge", "",
     "account", 1, False, False, "", "oth_mietertraege"),
    ("Sonstiges betriebliches Ergebnis", "Sonstige Erträge", "Erträge aus Anlagenabgängen", "",
     "account", 1, False, False, "", "oth_anlagenabgang"),
    ("Sonstiges betriebliches Ergebnis", "Sonstige Aufwendungen", "Kursverluste operativ", "",
     "account", -1, False, True, "", "oth_kursverluste"),
    ("Sonstiges betriebliches Ergebnis", "Sonstige Aufwendungen", "Wertminderung auf Forderungen", "",
     "account", -1, False, True, "", "oth_wertminderung_ford"),
    ("Sonstiges betriebliches Ergebnis", "Sonstige Aufwendungen", "Übrige betriebliche Aufwendungen", "",
     "account", -1, False, True, "", "oth_uebrige"),

    # --- EBITDA -----------------------------------------------------------
    ("EBITDA", "", "", "",
     "formula", 1, False, False,
     "[Rohertrag] + [Vertriebskosten] + [Verwaltungskosten] + "
     "[Forschung & Entwicklung] + [Sonstiges betriebliches Ergebnis]", "f_ebitda"),
    ("EBITDA-Marge %", "", "", "",
     "kpi", 1, False, False, "[EBITDA] / [Umsatzerlöse]", "k_ebitda_marge"),
    ("———  ", "", "", "", "separator", 1, False, False, "", "sep_2"),

    # --- Abschreibungen ---------------------------------------------------
    ("Abschreibungen", "Planmäßige Abschreibungen", "Abschreibungen Sachanlagen", "",
     "account", -1, True, True, "", "da_sachanlagen"),
    ("Abschreibungen", "Planmäßige Abschreibungen", "Abschreibungen immaterielle Vermögenswerte", "",
     "account", -1, True, True, "", "da_immateriell"),
    ("Abschreibungen", "Planmäßige Abschreibungen", "Abschreibungen Nutzungsrechte", "",
     "account", -1, True, True, "", "da_nutzungsrechte"),
    ("Abschreibungen", "Wertminderungen", "Wertminderung Geschäfts- oder Firmenwert", "",
     "account", -1, True, True, "", "da_impair_goodwill"),
    ("Abschreibungen", "Wertminderungen", "Wertminderung Sachanlagen", "",
     "account", -1, True, True, "", "da_impair_sachanlagen"),

    # --- EBIT -------------------------------------------------------------
    ("EBIT", "", "", "",
     "formula", 1, False, False, "[EBITDA] + [Abschreibungen]", "f_ebit"),
    ("EBIT-Marge %", "", "", "",
     "kpi", 1, False, False, "[EBIT] / [Umsatzerlöse]", "k_ebit_marge"),

    # --- Finanzergebnis ---------------------------------------------------
    ("Finanzergebnis", "Zinsergebnis", "Zinserträge", "",
     "account", 1, False, False, "", "fin_zinsertraege"),
    ("Finanzergebnis", "Zinsergebnis", "Zinsaufwand Finanzverbindlichkeiten", "",
     "account", -1, False, True, "", "fin_zinsaufwand"),
    ("Finanzergebnis", "Zinsergebnis", "Zinsaufwand Leasing", "",
     "account", -1, False, True, "", "fin_zins_leasing"),
    ("Finanzergebnis", "Übriges Finanzergebnis", "Ergebnis aus assoziierten Unternehmen", "",
     "account", 1, False, False, "", "fin_assoziierte"),
    ("Finanzergebnis", "Übriges Finanzergebnis", "Währungsergebnis Finanzierung", "",
     "account", 1, False, False, "", "fin_fx"),
    ("Finanzergebnis", "Übriges Finanzergebnis", "Sonstiges Finanzergebnis", "",
     "account", 1, False, False, "", "fin_sonstiges"),

    # --- EBT --------------------------------------------------------------
    ("EBT", "", "", "",
     "formula", 1, False, False, "[EBIT] + [Finanzergebnis]", "f_ebt"),

    # --- Ertragsteuern ----------------------------------------------------
    ("Ertragsteuern", "Laufende Steuern", "Körperschaftsteuer", "",
     "account", -1, True, True, "", "tax_kst"),
    ("Ertragsteuern", "Laufende Steuern", "Gewerbesteuer", "",
     "account", -1, True, True, "", "tax_gewst"),
    ("Ertragsteuern", "Laufende Steuern", "Ausländische Ertragsteuern", "",
     "account", -1, True, True, "", "tax_auslaendisch"),
    ("Ertragsteuern", "Latente Steuern", "Veränderung latenter Steuern", "",
     "account", -1, True, True, "", "tax_latent"),

    # --- Jahresueberschuss -------------------------------------------------
    ("Jahresüberschuss", "", "", "",
     "formula", 1, False, False, "[EBT] + [Ertragsteuern]", "f_jahresueberschuss"),
    ("Nettomarge %", "", "", "",
     "kpi", 1, False, False, "[Jahresüberschuss] / [Umsatzerlöse]", "k_nettomarge"),
]


# Uebersetzungen aller in GUV vorkommenden Bezeichnungen (Ebenen l1..l4).
TRANSLATIONS_GUV = {
    # L1
    "Umsatzerlöse": "Net revenue",
    "Umsatzkosten": "Cost of sales",
    "Rohertrag": "Gross profit",
    "Rohertragsmarge %": "Gross margin %",
    "Vertriebskosten": "Selling expenses",
    "Verwaltungskosten": "Administrative expenses",
    "Forschung & Entwicklung": "Research & development",
    "Sonstiges betriebliches Ergebnis": "Other operating result",
    "EBITDA": "EBITDA",
    "EBITDA-Marge %": "EBITDA margin %",
    "Abschreibungen": "Depreciation & amortisation",
    "EBIT": "EBIT",
    "EBIT-Marge %": "EBIT margin %",
    "Finanzergebnis": "Financial result",
    "EBT": "EBT",
    "Ertragsteuern": "Income taxes",
    "Jahresüberschuss": "Net income",
    "Nettomarge %": "Net margin %",
    # L2
    "Produkterlöse": "Product revenue",
    "Serviceerlöse": "Service revenue",
    "Software & Lizenzen": "Software & licences",
    "Erlösschmälerungen": "Sales deductions",
    "Materialaufwand": "Cost of materials",
    "Fertigungskosten": "Production costs",
    "Logistikkosten": "Logistics costs",
    "Gewährleistung": "Warranty",
    "Personalkosten Vertrieb": "Sales personnel expenses",
    "Marketing": "Marketing",
    "Vertriebsstruktur": "Sales infrastructure",
    "Personalkosten Verwaltung": "Administrative personnel expenses",
    "IT & Infrastruktur": "IT & infrastructure",
    "Externe Dienstleistungen": "External services",
    "Raumkosten": "Occupancy costs",
    "F&E Personal": "R&D personnel",
    "F&E Sachkosten": "R&D non-personnel costs",
    "Sonstige Erträge": "Other income",
    "Sonstige Aufwendungen": "Other expenses",
    "Planmäßige Abschreibungen": "Scheduled depreciation & amortisation",
    "Wertminderungen": "Impairment losses",
    "Zinsergebnis": "Net interest result",
    "Übriges Finanzergebnis": "Other financial result",
    "Laufende Steuern": "Current taxes",
    "Latente Steuern": "Deferred taxes",
    # L3
    "Erlöse Inland": "Domestic revenue",
    "Erlöse Export": "Export revenue",
    "Erlöse Projektgeschäft": "Project business revenue",
    "Erlöse Anlagenbau": "Plant engineering revenue",
    "Wartung & Instandhaltung": "Maintenance & repair",
    "Ersatzteilerlöse": "Spare parts revenue",
    "Schulung & Inbetriebnahme": "Training & commissioning",
    "Technischer Support": "Technical support",
    "Lizenzerlöse": "Licence revenue",
    "Subskriptionserlöse": "Subscription revenue",
    "Cloud- & Hosting-Erlöse": "Cloud & hosting revenue",
    "Boni & Rabatte": "Rebates & discounts",
    "Gutschriften & Retouren": "Credit notes & returns",
    "Skonti": "Cash discounts",
    "Roh-, Hilfs- & Betriebsstoffe": "Raw materials & supplies",
    "Bezogene Handelswaren": "Purchased merchandise",
    "Bezogene Leistungen": "Purchased services",
    "Energie & Medien": "Energy & utilities",
    "Fertigungslöhne": "Direct production wages",
    "Fertigungsgemeinkosten": "Production overheads",
    "Instandhaltung Produktion": "Production maintenance",
    "Ausschuss & Nacharbeit": "Scrap & rework",
    "Frachten & Zölle": "Freight & customs duties",
    "Lagerkosten": "Warehousing costs",
    "Verpackung": "Packaging",
    "Garantie & Kulanz": "Warranty & goodwill claims",
    "Veränderung Gewährleistungsrückstellung": "Change in warranty provisions",
    "Gehälter Vertrieb": "Sales salaries",
    "Provisionen & Prämien": "Commissions & bonuses",
    "Reisekosten Vertrieb": "Sales travel expenses",
    "Messen & Events": "Trade fairs & events",
    "Digitales Marketing": "Digital marketing",
    "Werbemittel & Kataloge": "Advertising material & catalogues",
    "Vertriebsbüros": "Sales offices",
    "Fahrzeugflotte": "Vehicle fleet",
    "Gehälter Verwaltung": "Administrative salaries",
    "Altersversorgung": "Pension costs",
    "Aus- & Weiterbildung": "Training & development",
    "IT-Betrieb": "IT operations",
    "Cloud- & Softwarelizenzen": "Cloud & software licences",
    "Telekommunikation": "Telecommunications",
    "Rechts- & Beratungskosten": "Legal & consulting fees",
    "Abschluss- & Prüfungskosten": "Audit & financial reporting fees",
    "Versicherungen": "Insurance",
    "Mieten & Pachten": "Rent & leases",
    "Nebenkosten & Gebäudebetrieb": "Utilities & facility management",
    "Entwicklungsgehälter": "Development salaries",
    "Externe Entwicklungsleistungen": "External development services",
    "Prototypen & Versuche": "Prototypes & testing",
    "Patente & Schutzrechte": "Patents & intellectual property",
    "Aktivierte Entwicklungskosten": "Own development work capitalised",
    "Erträge aus Auflösung von Rückstellungen": "Income from the reversal of provisions",
    "Kursgewinne operativ": "Operating foreign exchange gains",
    "Mieterträge": "Rental income",
    "Erträge aus Anlagenabgängen": "Gains on disposal of fixed assets",
    "Kursverluste operativ": "Operating foreign exchange losses",
    "Wertminderung auf Forderungen": "Impairment of receivables",
    "Übrige betriebliche Aufwendungen": "Sundry operating expenses",
    "Abschreibungen Sachanlagen": "Depreciation of property, plant and equipment",
    "Abschreibungen immaterielle Vermögenswerte": "Amortisation of intangible assets",
    "Abschreibungen Nutzungsrechte": "Depreciation of right-of-use assets",
    "Wertminderung Geschäfts- oder Firmenwert": "Impairment of goodwill",
    "Wertminderung Sachanlagen": "Impairment of property, plant and equipment",
    "Zinserträge": "Interest income",
    "Zinsaufwand Finanzverbindlichkeiten": "Interest expense on financial liabilities",
    "Zinsaufwand Leasing": "Interest expense on lease liabilities",
    "Ergebnis aus assoziierten Unternehmen": "Result from associates",
    "Währungsergebnis Finanzierung": "Foreign exchange result on financing",
    "Sonstiges Finanzergebnis": "Other financial result",
    "Körperschaftsteuer": "Corporate income tax",
    "Gewerbesteuer": "Local trade tax",
    "Ausländische Ertragsteuern": "Foreign income taxes",
    "Veränderung latenter Steuern": "Change in deferred taxes",
    # L4
    "Neuanlagen": "New equipment",
    "Modernisierung & Retrofit": "Modernisation & retrofit",
    "Metalle & Stahl": "Metals & steel",
    "Elektronik & Halbleiter": "Electronics & semiconductors",
    "Kunststoffe & Dichtungen": "Plastics & seals",
    "Seefracht": "Ocean freight",
    "Luftfracht": "Air freight",
    "Landverkehr": "Road & rail transport",
    "Public Cloud": "Public cloud",
    "Lizenzen Standardsoftware": "Standard software licences",
    # Separatoren
    "———": "———",
    "———  ": "———  ",
}
