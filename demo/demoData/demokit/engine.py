# -*- coding: utf-8 -*-
"""Finanzmodell des PnL ChartkitchenDemoKit.

Erzeugt je Gesellschaft und Monat einen vollstaendigen Abschluss:
GuV, Bilanz und Kapitalflussrechnung. Die drei Rechenwerke haengen
rechnerisch zusammen -- das ist der Punkt:

  * Die GuV wird aus Treibern gerechnet (Umsatz, Margen, Kostenquoten).
  * Die Bilanz rollt fort: Anlagevermoegen = Anfangsbestand + Zugaenge
    - Abschreibungen, Eigenkapital = Anfangsbestand + Jahresueberschuss
    - Dividende, Working Capital aus DIO/DSO/DPO.
  * Aktiva = Passiva gilt per Konstruktion: die langfristigen
    Finanzverbindlichkeiten sind die Ausgleichsposition (und wenn kein
    Kredit noetig ist, laeuft der Ueberschuss in die liquiden Mittel).
  * Die Kapitalflussrechnung wird aus den Bilanzbewegungen abgeleitet.
    Jede Bilanzbewegung erscheint genau einmal im Cashflow -- direkt
    oder ueber den Jahresueberschuss. Deshalb ergibt
    CFO + CFI + CFF + Waehrungseffekte + Konsolidierungskreis exakt
    die Veraenderung des Finanzmittelfonds.

Szenarien: 'AC' (Ist, mit Rauschen und Storys), 'PL' (Plan, glatt, zu
Jahresbeginn verabschiedet), 'FC' (Ist fuer geschlossene Monate,
Forecast fuer offene). Das Vorjahr PY ist der um 12 Monate verschobene
AC-Pfad -- deshalb laeuft der AC-Pfad schon ab 2024.
"""

import hashlib

from dims import (ENTITIES, SEGMENT_PROFILE, build_fx_rates, fx_base_rate,
                  month_sequence)

SEED = "demokit-20261030"

LAST_ACTUAL = (2026, 10)        # letzter Monat mit Ist-Werten
FIRST_OUT = (2025, 1)           # erster ausgelieferter Monat
LAST_OUT = (2026, 12)           # letzter ausgelieferter Monat
FIRST_CALC = (2023, 12)         # Vorlauf: Vorjahr 2024 + Bilanz-Anfangsbestand

NCI_SHARE = 0.022               # Anteil nicht beherrschender Gesellschafter

# Jaehrliches Umsatzwachstum des Ist-Pfades IN LANDESWAEHRUNG.
GROWTH = {
    "1100": {2024: 0.055, 2025: 0.060, 2026: 0.075},
    "1200": {2024: 0.072, 2025: 0.090, 2026: 0.120},
    "1300": {2024: 0.031, 2025: 0.020, 2026: 0.010},
    "1400": {2024: 0.042, 2025: 0.048, 2026: 0.055},
    "1500": {2024: 0.088, 2025: 0.105, 2026: 0.125},
    "1600": {2024: 0.071, 2025: 0.082, 2026: 0.096},
    "2100": {2024: 0.061, 2025: 0.070, 2026: 0.090},
    "3100": {2024: 0.055, 2025: 0.062, 2026: 0.074},
    "3200": {2024: 0.000, 2025: 0.000, 2026: 0.000},
}

# Plan / Ist je Jahr. <1 heisst "Ist ueber Plan", >1 "Ist unter Plan".
PLAN_FACTOR = {
    "1100": {2024: 0.995, 2025: 0.990, 2026: 0.975},
    "1200": {2024: 0.985, 2025: 0.970, 2026: 0.945},
    "1300": {2024: 1.005, 2025: 1.020, 2026: 1.075},
    "1400": {2024: 1.000, 2025: 1.005, 2026: 1.015},
    "1500": {2024: 0.980, 2025: 0.965, 2026: 0.950},
    "1600": {2024: 0.995, 2025: 0.985, 2026: 0.975},
    "2100": {2024: 1.000, 2025: 1.000, 2026: 0.985},
    "3100": {2024: 1.000, 2025: 1.010, 2026: 1.030},
    "3200": {2024: 1.000, 2025: 1.000, 2026: 1.030},
}

TAX_RATE = {"DE": 0.300, "FR": 0.258, "CH": 0.148, "PL": 0.190,
            "CZ": 0.210, "US": 0.243, "AU": 0.300, "JP": 0.308}

# ---------------------------------------------------------------------------
# Struktur der GuV-Treiber
# ---------------------------------------------------------------------------
REV_SHARES = {
    "IA": {"rev_inland_neu": 0.20, "rev_inland_retrofit": 0.07,
           "rev_export": 0.26, "rev_projekt": 0.12, "rev_anlagenbau": 0.06,
           "rev_wartung": 0.08, "rev_ersatzteile": 0.09,
           "rev_schulung": 0.03, "rev_support": 0.02,
           "rev_lizenz": 0.03, "rev_subskription": 0.03, "rev_cloud": 0.01},
    "ES": {"rev_inland_neu": 0.14, "rev_inland_retrofit": 0.09,
           "rev_export": 0.22, "rev_projekt": 0.24, "rev_anlagenbau": 0.13,
           "rev_wartung": 0.07, "rev_ersatzteile": 0.05,
           "rev_schulung": 0.02, "rev_support": 0.01,
           "rev_lizenz": 0.01, "rev_subskription": 0.01, "rev_cloud": 0.01},
    "MS": {"rev_inland_neu": 0.22, "rev_inland_retrofit": 0.05,
           "rev_export": 0.34, "rev_projekt": 0.14, "rev_anlagenbau": 0.04,
           "rev_wartung": 0.06, "rev_ersatzteile": 0.08,
           "rev_schulung": 0.02, "rev_support": 0.01,
           "rev_lizenz": 0.02, "rev_subskription": 0.01, "rev_cloud": 0.01},
    "DS": {"rev_inland_neu": 0.02, "rev_inland_retrofit": 0.01,
           "rev_export": 0.04, "rev_projekt": 0.10, "rev_anlagenbau": 0.00,
           "rev_wartung": 0.05, "rev_ersatzteile": 0.00,
           "rev_schulung": 0.08, "rev_support": 0.09,
           "rev_lizenz": 0.18, "rev_subskription": 0.31, "rev_cloud": 0.12},
}

DEDUCTIONS = {
    "IA": {"rev_boni": 0.028, "rev_gutschriften": 0.008, "rev_skonti": 0.004},
    "ES": {"rev_boni": 0.022, "rev_gutschriften": 0.006, "rev_skonti": 0.003},
    "MS": {"rev_boni": 0.036, "rev_gutschriften": 0.011, "rev_skonti": 0.004},
    "DS": {"rev_boni": 0.012, "rev_gutschriften": 0.003, "rev_skonti": 0.002},
}

COGS_SHARES = {
    "IA": {"cogs_mat_metall": 0.17, "cogs_mat_elektronik": 0.21,
           "cogs_mat_kunststoff": 0.07, "cogs_handelswaren": 0.06,
           "cogs_bezogene_leistungen": 0.09, "cogs_energie": 0.04,
           "cogs_fertigungsloehne": 0.14, "cogs_gemeinkosten": 0.09,
           "cogs_instandhaltung": 0.03, "cogs_ausschuss": 0.015,
           "cogs_seefracht": 0.018, "cogs_luftfracht": 0.009,
           "cogs_landverkehr": 0.015, "cogs_lager": 0.012,
           "cogs_verpackung": 0.008, "cogs_garantie": 0.016,
           "cogs_gewaehrl_rst": 0.004},
    "ES": {"cogs_mat_metall": 0.26, "cogs_mat_elektronik": 0.11,
           "cogs_mat_kunststoff": 0.05, "cogs_handelswaren": 0.04,
           "cogs_bezogene_leistungen": 0.15, "cogs_energie": 0.06,
           "cogs_fertigungsloehne": 0.12, "cogs_gemeinkosten": 0.08,
           "cogs_instandhaltung": 0.035, "cogs_ausschuss": 0.012,
           "cogs_seefracht": 0.024, "cogs_luftfracht": 0.006,
           "cogs_landverkehr": 0.018, "cogs_lager": 0.013,
           "cogs_verpackung": 0.007, "cogs_garantie": 0.019,
           "cogs_gewaehrl_rst": 0.005},
    "MS": {"cogs_mat_metall": 0.21, "cogs_mat_elektronik": 0.18,
           "cogs_mat_kunststoff": 0.11, "cogs_handelswaren": 0.05,
           "cogs_bezogene_leistungen": 0.08, "cogs_energie": 0.04,
           "cogs_fertigungsloehne": 0.13, "cogs_gemeinkosten": 0.085,
           "cogs_instandhaltung": 0.028, "cogs_ausschuss": 0.021,
           "cogs_seefracht": 0.026, "cogs_luftfracht": 0.011,
           "cogs_landverkehr": 0.017, "cogs_lager": 0.011,
           "cogs_verpackung": 0.009, "cogs_garantie": 0.024,
           "cogs_gewaehrl_rst": 0.006},
    "DS": {"cogs_mat_metall": 0.00, "cogs_mat_elektronik": 0.05,
           "cogs_mat_kunststoff": 0.00, "cogs_handelswaren": 0.06,
           "cogs_bezogene_leistungen": 0.30, "cogs_energie": 0.04,
           "cogs_fertigungsloehne": 0.40, "cogs_gemeinkosten": 0.10,
           "cogs_instandhaltung": 0.01, "cogs_ausschuss": 0.00,
           "cogs_seefracht": 0.00, "cogs_luftfracht": 0.00,
           "cogs_landverkehr": 0.01, "cogs_lager": 0.01,
           "cogs_verpackung": 0.00, "cogs_gewaehrl_rst": 0.00,
           "cogs_garantie": 0.02},
}

SELL_SHARES = {
    "sell_gehaelter": 0.42, "sell_provisionen": 0.16,
    "sell_reisekosten": 0.08, "sell_messen": 0.09,
    "sell_digital": 0.08, "sell_werbemittel": 0.04,
    "sell_bueros": 0.08, "sell_flotte": 0.05,
}
ADMIN_SHARES = {
    "admin_gehaelter": 0.34, "admin_altersversorgung": 0.07,
    "admin_weiterbildung": 0.03, "admin_it_betrieb": 0.10,
    "admin_public_cloud": 0.09, "admin_lizenzen_std": 0.07,
    "admin_telekom": 0.03, "admin_beratung": 0.09,
    "admin_pruefung": 0.03, "admin_versicherungen": 0.04,
    "admin_mieten": 0.08, "admin_nebenkosten": 0.03,
}
RND_SHARES = {
    "rnd_gehaelter": 0.62, "rnd_extern": 0.21,
    "rnd_prototypen": 0.12, "rnd_patente": 0.05,
}

# Konten, die bei einzelnen Gesellschaften nie belegt sind
# (-> Testfall "Nullzeilen ausblenden").
ALL_IDS = {"1100", "1200", "1300", "1400", "1500", "1600",
           "2100", "3100", "3200"}
DORMANT = {
    "oth_mietertraege": {"1300", "1400", "1500", "1600", "2100",
                         "3100", "3200"},
    "da_impair_sachanlagen": ALL_IDS,
    "fin_assoziierte": {"1200", "1300", "1400", "1500", "1600",
                        "3100", "3200"},
    "cogs_luftfracht": {"3200"},
    "rev_anlagenbau": {"3200"},
    "rev_ersatzteile": {"3200"},
    "cogs_mat_metall": {"3200"},
    "cogs_mat_kunststoff": {"3200"},
    "cogs_seefracht": {"3200"},
    "cogs_verpackung": {"3200"},
    "cogs_ausschuss": {"3200"},
    "tax_gewst": {"1300", "1400", "1500", "1600", "2100", "3100", "3200"},
    "tax_kst": {"1300", "1400", "1500", "1600", "2100", "3100", "3200"},
    "tax_auslaendisch": {"1100", "1200"},
    # Cashflow-Zeilen ohne Bewegung im Demozeitraum
    "cf_verkauf_gesellschaften": ALL_IDS,
    "cf_kapitalerhoehung": ALL_IDS,
    "cf_eigene_anteile": ALL_IDS,
    "cf_abgang_finanzanlagen": ALL_IDS,
    "cf_unternehmenserwerbe": ALL_IDS,
    # Bilanzzeilen
    "sachanlagen_anlagen_im_bau": {"3200"},
}

# Aufteilung der Bilanz-Sammelpositionen auf die Kontenplanzeilen.
# Die Anteile summieren je Sammelposition auf 1 -- sonst wuerde die
# Bilanzgleichung nicht mehr aufgehen.
BS_SPLIT = {
    "intang_other": {"ia_software_lizenzen": 0.58, "ia_kundenbeziehungen": 0.42},
    "fininv": {"fa_assoziierte": 0.45, "fa_beteiligungen": 0.35, "fa_sonstige": 0.20},
    "rou": {"rou_immobilien": 0.72, "rou_fahrzeuge_maschinen": 0.28},
    "inv_raw": {"vorraete_rhb": 0.92, "vorraete_anzahlungen": 0.08},
    "other_assets": {"sonstige_finanzielle_va": 0.42,
                     "steuererstattungsansprueche": 0.21, "aktive_rap": 0.37},
    "cash": {"zahlungsmittel_bank": 0.84, "zahlungsmittel_geldanlagen": 0.16},
    "oci": {"ek_waehrungsumrechnung": 0.55, "ek_oci_pensionen": 0.33,
            "ek_oci_hedge": 0.12},
    "prov_other": {"rst_lf_sonstige": 0.35, "rst_kf_garantie": 0.26,
                   "rst_kf_personal": 0.27, "rst_kf_sonstige": 0.12},
    "debt_lt": {"fv_lf_anleihen": 0.46, "fv_lf_banken": 0.34,
                "fv_lf_schuldschein": 0.20},
    "debt_st": {"fv_kf_banken": 0.62, "fv_kf_anteil_lf": 0.38},
    "payables": {"verb_lul_dritte": 0.93, "verb_lul_verbundene": 0.07},
    "contract_liab": {"vertragsverbindlichkeiten_poc": 0.64,
                      "erhaltene_anzahlungen": 0.36},
    "other_liab": {"sonst_verb_lf": 0.22, "sonst_verb_kf_steuern": 0.24,
                   "sonst_verb_kf_soziales": 0.19, "sonst_verb_kf_uebrige": 0.35},
    "ppe": {"sachanlagen_grundstuecke": 0.43, "sachanlagen_maschinen": 0.44,
            "sachanlagen_bga": 0.09, "sachanlagen_anlagen_im_bau": 0.04},
}

# Forderungen: brutto, verbundene Unternehmen, Wertminderung.
# Netto ergibt 1,000 (die Wertminderungszeile hat sign = -1).
RECEIVABLE_SPLIT = {"ford_lul_dritte": 1.060, "ford_lul_verbundene": 0.055,
                    "ford_wertminderung": 0.115}

# Welche Bilanzzeilen sind Aktiva, welche Passiva?
ASSET_ROWS = [
    "goodwill", "ia_entwicklungskosten", "ia_software_lizenzen",
    "ia_kundenbeziehungen", "sachanlagen_grundstuecke", "sachanlagen_maschinen",
    "sachanlagen_bga", "sachanlagen_anlagen_im_bau", "fa_assoziierte",
    "fa_beteiligungen", "fa_sonstige", "rou_immobilien",
    "rou_fahrzeuge_maschinen", "aktive_latente_steuern", "vorraete_rhb",
    "vorraete_unfertig", "vorraete_fertig", "vorraete_anzahlungen",
    "ford_lul_dritte", "ford_lul_verbundene", "ford_wertminderung",
    "vertragsvermoegenswerte_poc", "sonstige_finanzielle_va",
    "steuererstattungsansprueche", "aktive_rap", "zahlungsmittel_bank",
    "zahlungsmittel_geldanlagen",
]
LE_ROWS = [
    "ek_gezeichnetes_kapital", "ek_kapitalruecklage", "ek_gewinnruecklagen",
    "ek_jahresueberschuss", "ek_waehrungsumrechnung", "ek_oci_pensionen",
    "ek_oci_hedge", "ek_minderheiten", "rst_lf_pensionen", "rst_lf_sonstige",
    "fv_lf_anleihen", "fv_lf_banken", "fv_lf_schuldschein", "leasing_lf",
    "passive_latente_steuern", "sonst_verb_lf", "rst_kf_steuern",
    "rst_kf_garantie", "rst_kf_personal", "rst_kf_sonstige", "fv_kf_banken",
    "fv_kf_anteil_lf", "verb_lul_dritte", "verb_lul_verbundene", "leasing_kf",
    "vertragsverbindlichkeiten_poc", "erhaltene_anzahlungen",
    "sonst_verb_kf_steuern", "sonst_verb_kf_soziales", "sonst_verb_kf_uebrige",
]
# Vorzeichen, mit dem die Zeile in die Bilanzsumme eingeht
ROW_SIGN = {"ford_wertminderung": -1}

# Cashflow-Zeilen, die in CFO / CFI / CFF einfliessen, mit ihrem
# Vorzeichen aus dem Kontenplan.
CF_BLOCK_SIGN = {
    "cf_jahresueberschuss": 1, "cf_abschreibungen_sav_ia": 1,
    "cf_abschreibungen_rou": 1, "cf_wertminderungen": 1,
    "cf_ergebnis_anlagenabgaenge": -1, "cf_ergebnis_at_equity": -1,
    "cf_ueberleitung_zinsen": 1, "cf_ueberleitung_steuern": 1,
    "cf_sonstige_zahlungsunwirksam": 1, "cf_delta_vorraete": -1,
    "cf_delta_forderungen": -1, "cf_delta_vertragsvermoegen": -1,
    "cf_delta_verbindlichkeiten": 1, "cf_delta_vertragsverb": 1,
    "cf_delta_sonstige": 1, "cf_delta_pensionsrueckstellungen": 1,
    "cf_delta_sonstige_rueckstellungen": 1, "cf_erhaltene_zinsen": 1,
    "cf_gezahlte_zinsen": -1, "cf_gezahlte_steuern": -1,
    "cf_capex_sachanlagen": -1, "cf_capex_immateriell": -1,
    "cf_capex_entwicklung": -1, "cf_invest_finanzanlagen": -1,
    "cf_unternehmenserwerbe": -1, "cf_verkauf_gesellschaften": 1,
    "cf_abgang_sachanlagen": 1, "cf_abgang_finanzanlagen": 1,
    "cf_erhaltene_dividenden": 1, "cf_aufnahme_kredite": 1,
    "cf_tilgung_kredite": -1, "cf_emission_anleihen": 1,
    "cf_rueckzahlung_anleihen": -1, "cf_leasingzahlungen": -1,
    "cf_kapitalerhoehung": 1, "cf_eigene_anteile": -1,
    "cf_dividende_konzern": -1, "cf_dividende_minderheiten": -1,
}


# ---------------------------------------------------------------------------
# Hilfsmittel
# ---------------------------------------------------------------------------
def norm(d):
    s = float(sum(d.values()))
    return {k: v / s for k, v in d.items()}


REV_SHARES = {k: norm(v) for k, v in REV_SHARES.items()}
COGS_SHARES = {k: norm(v) for k, v in COGS_SHARES.items()}
SELL_SHARES = norm(SELL_SHARES)
ADMIN_SHARES = norm(ADMIN_SHARES)
RND_SHARES = norm(RND_SHARES)


def jitter(*parts):
    """Reproduzierbares Rauschen in [-1, 1], unabhaengig von der
    Iterationsreihenfolge (Hash statt Generator mit Zustand)."""
    key = SEED + "|" + "|".join(str(p) for p in parts)
    h = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") / float(1 << 64) * 2.0 - 1.0


def is_dormant(tag, entity_id):
    return entity_id in DORMANT.get(tag, ())


class Entity:
    """Eine Gesellschaft. Alle Betraege des Motors sind in LANDESWAEHRUNG,
    umgerechnet wird erst am Ende.

    `base_rate` ist der Durchschnittskurs 2026 (Landeswaehrung je 1 EUR).
    Damit werden die in EUR geplanten Umsatzziele und die absoluten
    Eroeffnungswerte in Landeswaehrung gebracht. Weil spaeter mit dem
    TATSAECHLICHEN Monatskurs zurueckgerechnet wird, entsteht ein echter
    Waehrungseffekt: das Wachstum in EUR weicht vom Wachstum in
    Landeswaehrung ab.
    """

    def __init__(self, row, rates):
        (self.id, self.name, self.short, self.region, self.land_de,
         self.land_en, self.iso, self.segment, self.currency, self.legal,
         self.rev2026_eur, self.staff, self.first_cons, self.cons_type) = row
        self.profile = SEGMENT_PROFILE[self.segment]
        self.first_ym = (int(self.first_cons[:4]), int(self.first_cons[5:7]))
        self.rates = rates
        self.base_rate = fx_base_rate(rates, self.currency, 2026)
        # Umsatzziel in Landeswaehrung
        self.rev2026 = self.rev2026_eur * self.base_rate

    def to_local(self, eur_amount):
        """Absoluten EUR-Betrag (Storys, Eroeffnungsbilanz) umrechnen."""
        return eur_amount * self.base_rate

    def rate(self, year, month):
        """(Durchschnittskurs, Stichtagskurs) des Monats."""
        return self.rates[(self.currency, (year, month))]

    def rev_fy(self, year):
        if self.id == "3200":
            return self.rev2026 if year == 2026 else 0.0
        rev = self.rev2026
        for y in (2026, 2025, 2024):
            if year >= y:
                return rev
            rev = rev / (1.0 + GROWTH[self.id][y])
        return rev


FX_RATES = build_fx_rates(FIRST_CALC, LAST_OUT)


def entities():
    return [Entity(r, FX_RATES) for r in ENTITIES]


# ---------------------------------------------------------------------------
# GuV
# ---------------------------------------------------------------------------
def _month_weight(entity, year, month, scenario):
    season = entity.profile["season"][month - 1] / 12.0
    trend = 1.0 + 0.010 * ((month - 6.5) / 5.5)
    noise = 1.0 if scenario == "PL" else \
        1.0 + 0.035 * jitter(scenario, entity.id, year, month, "rev")
    return season * trend * noise


def _gross_revenue(entity, year, month, scenario):
    if entity.id == "3200":
        if (year, month) < entity.first_ym:
            return 0.0
        base = entity.rev2026 / 9.0 * 12.0      # 9 Monate tragen das Zukaufjahr
    else:
        base = entity.rev_fy(year)
    if base <= 0.0:
        return 0.0

    val = base * _month_weight(entity, year, month, scenario)
    if scenario == "PL":
        val *= PLAN_FACTOR[entity.id].get(year, 1.0)
    elif scenario == "FC" and (year, month) > LAST_ACTUAL:
        val *= 1.0 + 0.012 + 0.004 * jitter("FC", entity.id, year, month)

    # Story: Mobility Solutions bricht im zweiten Halbjahr 2026 weiter ein
    if scenario in ("AC", "FC") and entity.id == "1300" and year == 2026 and month >= 7:
        val *= 0.955
    # Story: Lizenz-Einmalerloes 1100 im September 2026
    val += _oneoff_licence(entity, year, month, scenario)
    return val


def _oneoff_licence(entity, year, month, scenario):
    """Einmaliger Lizenzerlös -- Teil des Bruttoumsatzes, wird aber in
    _pnl_month vollstaendig der Zeile 'Lizenzerloese' zugeordnet statt
    ueber alle Umsatzkonten verteilt."""
    if scenario in ("AC", "FC") and entity.id == "1100" \
            and (year, month) == (2026, 9):
        return 14.5
    return 0.0


def _drift(entity, year, month, scenario, kind, amp=0.022):
    if scenario == "PL":
        return 1.0
    return 1.0 + amp * jitter(scenario, entity.id, year, month, kind)


def _pnl_month(entity, y, m, scenario):
    """GuV-Zeilen eines Monats. Kosten als positive Kostenbetraege."""
    prof = entity.profile
    gross = _gross_revenue(entity, y, m, scenario)
    if gross <= 0.0:
        return None
    v = {}

    # Der Einmalerloes wird NICHT ueber die Anteile verteilt, sondern
    # komplett auf die Lizenzzeile gebucht -- sonst weicht die Summe der
    # Umsatzkonten vom Bruttoumsatz ab, mit dem der Motor weiterrechnet.
    oneoff = _oneoff_licence(entity, y, m, scenario)
    base = gross - oneoff
    for tag, share in REV_SHARES[entity.segment].items():
        amount = base * share
        if tag == "rev_lizenz":
            amount += oneoff
        v[tag] = 0.0 if is_dormant(tag, entity.id) else amount

    ded = 0.0
    for tag, rate in DEDUCTIONS[entity.segment].items():
        amount = gross * rate * _drift(entity, y, m, scenario, tag)
        v[tag] = amount
        ded += amount
    net_rev = gross - ded
    v["_gross_revenue"] = gross
    v["_net_revenue"] = net_rev

    gm = prof["gm"]
    if scenario in ("AC", "FC"):
        gm *= 1.0 + 0.012 * jitter(scenario, entity.id, y, m, "gm")
        if entity.id == "1300" and y == 2026:
            gm -= 0.014                      # Story: Margenverlust Mobility
    cogs_total = net_rev * (1.0 - gm)
    for tag, share in COGS_SHARES[entity.segment].items():
        amount = cogs_total * share * _drift(entity, y, m, scenario, tag)
        # Story: Halbleiter-Spotkaeufe Maerz-Mai 2026
        if tag == "cogs_mat_elektronik" and scenario in ("AC", "FC") \
                and y == 2026 and 3 <= m <= 5 and entity.segment in ("IA", "MS"):
            amount *= 1.26
        # Story: Seefracht-Spitze im vierten Quartal 2025
        if tag == "cogs_seefracht" and scenario in ("AC", "FC") \
                and y == 2025 and m >= 10:
            amount *= 1.72
        v[tag] = 0.0 if is_dormant(tag, entity.id) else amount
    v["_cogs_total"] = sum(v[t] for t in COGS_SHARES[entity.segment])

    sell_total = net_rev * prof["sell"] * _drift(entity, y, m, scenario, "sell")
    for tag, share in SELL_SHARES.items():
        v[tag] = sell_total * share * _drift(entity, y, m, scenario, tag)

    admin_total = net_rev * prof["admin"] * _drift(entity, y, m, scenario, "admin")
    for tag, share in ADMIN_SHARES.items():
        amount = admin_total * share * _drift(entity, y, m, scenario, tag)
        # Story: Public-Cloud-Kosten laufen 2026 weg
        if tag == "admin_public_cloud" and scenario in ("AC", "FC"):
            if y == 2026:
                amount *= 1.0 + 0.055 * m
            elif y == 2025:
                amount *= 1.0 + 0.012 * m
        v[tag] = amount

    rnd_total = net_rev * prof["rnd"] * _drift(entity, y, m, scenario, "rnd")
    for tag, share in RND_SHARES.items():
        v[tag] = rnd_total * share * _drift(entity, y, m, scenario, tag)
    v["_rnd_capitalised"] = rnd_total * 0.145
    v["rnd_aktiviert"] = -v["_rnd_capitalised"]   # entlastet den Block

    q4 = 1.9 if m == 12 else 1.0
    v["oth_rst_aufloesung"] = net_rev * 0.0024 * q4 * _drift(entity, y, m, scenario, "rst", 0.40)
    v["oth_kursgewinne"] = net_rev * 0.0031 * _drift(entity, y, m, scenario, "fxg", 0.50)
    v["oth_mietertraege"] = 0.0 if is_dormant("oth_mietertraege", entity.id) \
        else net_rev * 0.0012
    v["oth_anlagenabgang"] = net_rev * 0.0009 * _drift(entity, y, m, scenario, "abg", 0.80)
    v["oth_kursverluste"] = net_rev * 0.0026 * _drift(entity, y, m, scenario, "fxl", 0.50)
    v["oth_wertminderung_ford"] = net_rev * 0.0015 * _drift(entity, y, m, scenario, "wmf", 0.30)
    v["oth_uebrige"] = net_rev * 0.0024 * _drift(entity, y, m, scenario, "ueb", 0.30)
    return v


# ---------------------------------------------------------------------------
# Bilanz-Anfangsbestand
# ---------------------------------------------------------------------------
# Absolute Eroeffnungswerte in mEUR -- werden je Gesellschaft mit dem
# Basiskurs in Landeswaehrung gebracht.
GOODWILL = {"1100": 118.0, "1200": 96.0, "1300": 142.0, "1400": 34.0,
            "1500": 21.0, "1600": 18.0, "2100": 88.0, "3100": 26.0,
            "3200": 76.0}
SHARE_CAPITAL = {"1100": 60.0, "1200": 50.0, "1300": 45.0, "1400": 22.0,
                 "1500": 14.0, "1600": 12.0, "2100": 40.0, "3100": 16.0,
                 "3200": 12.0}


def _opening(entity):
    """Sammelpositionen der Eroeffnungsbilanz."""
    base = entity.rev_fy(2023) if entity.id != "3200" else entity.rev2026
    prof = entity.profile
    return dict(
        goodwill=entity.to_local(GOODWILL[entity.id]),
        intang_other=base * 0.042,
        intang_dev=base * 0.028,
        ppe=base * prof["ppe"],
        fininv=base * 0.021,
        rou=base * 0.076,
        prov_pension=base * (0.085 if entity.iso in ("DE", "CH")
                             else 0.032 if entity.iso in ("FR", "AU")
                             else 0.018),
        prov_tax=base * 0.009,
        debt_st=base * 0.045,
        share_capital=entity.to_local(SHARE_CAPITAL[entity.id]),
        capital_reserve=base * 0.048,
        retained_earnings=base * 0.165,
        oci=base * (-0.011 if entity.iso in ("JP", "AU", "CZ") else 0.004),
        nci=base * 0.014,
    )


# ---------------------------------------------------------------------------
# Vollstaendiger Abschluss
# ---------------------------------------------------------------------------
def build_statements(entity, scenario, agg_by_tag):
    """dict[(year, month)] -> dict[tag] -> Wert.

    None fuer Monate vor der Erstkonsolidierung. Neben den Kontenplan-Tags
    enthaelt jeder Monat Hilfswerte mit '_'-Praefix (Ergebnisstufen,
    Zwischengroessen) fuer die Abstimmung.
    """
    prof = entity.profile
    st = _opening(entity)
    st["debt_lt"] = 0.0
    st["cash"] = 0.0

    prev_rows = None            # Bilanzzeilen des Vormonats
    prev_close = None           # Stichtagskurs des Vormonats
    prev_year_ni = None
    ytd_ni = 0.0
    cur_year = None
    rev_hist, cogs_hist = [], []
    result = {}

    for (y, m) in month_sequence(FIRST_CALC, LAST_OUT):
        p = _pnl_month(entity, y, m, scenario)
        if p is None:
            result[(y, m)] = None
            continue

        net_rev = p["_net_revenue"]
        cogs_total = p["_cogs_total"]
        rev_hist = (rev_hist + [net_rev])[-12:]
        cogs_hist = (cogs_hist + [cogs_total])[-12:]
        ttm_rev = sum(rev_hist) / len(rev_hist) * 12.0
        ttm_cogs = sum(cogs_hist) / len(cogs_hist) * 12.0

        # ---- Abschreibungen aus den Anfangsbestaenden ----
        # Grundstuecke (rund 12 % der Sachanlagen) werden nicht abgeschrieben.
        da_ppe = st["ppe"] * 0.88 / 108.0
        da_int = st["intang_other"] / 84.0 + st["intang_dev"] / 60.0
        da_rou = st["rou"] / 72.0
        imp_goodwill = 0.0
        # Story: Goodwill-Wertminderung Mobility Solutions, Dezember 2025
        if scenario in ("AC", "FC") and entity.id == "1300" and (y, m) == (2025, 12):
            imp_goodwill = entity.to_local(21.0)
        p["da_sachanlagen"] = da_ppe
        p["da_immateriell"] = da_int
        p["da_nutzungsrechte"] = da_rou
        p["da_impair_goodwill"] = imp_goodwill
        p["da_impair_sachanlagen"] = 0.0
        da_total = da_ppe + da_int + da_rou + imp_goodwill

        # ---- Finanzergebnis ----
        debt_open = st["debt_lt"] + st["debt_st"]
        lease_open = st["rou"] * 1.02
        p["fin_zinsertraege"] = max(st["cash"], 0.0) * 0.0215 / 12.0
        p["fin_zinsaufwand"] = debt_open * 0.0415 / 12.0
        p["fin_zins_leasing"] = lease_open * 0.0350 / 12.0
        p["fin_assoziierte"] = 0.0 if is_dormant("fin_assoziierte", entity.id) \
            else net_rev * 0.0021
        fx = net_rev * 0.0008 * jitter(scenario, entity.id, y, m, "finfx")
        # Story: Transaktionsbedingter Waehrungsverlust der US-Gesellschaft,
        # Juni 2026 (nicht zu verwechseln mit dem Umrechnungseffekt)
        if scenario in ("AC", "FC") and entity.id == "2100" and (y, m) == (2026, 6):
            fx -= entity.to_local(6.8)
        p["fin_fx"] = fx
        p["fin_sonstiges"] = -net_rev * 0.0006

        # ---- Ergebnisstufen ----
        gross_profit = net_rev - cogs_total
        sell_total = sum(p[t] for t in SELL_SHARES)
        admin_total = sum(p[t] for t in ADMIN_SHARES)
        rnd_total = sum(p[t] for t in RND_SHARES) + p["rnd_aktiviert"]
        other_result = (p["oth_rst_aufloesung"] + p["oth_kursgewinne"]
                        + p["oth_mietertraege"] + p["oth_anlagenabgang"]
                        - p["oth_kursverluste"] - p["oth_wertminderung_ford"]
                        - p["oth_uebrige"])
        ebitda = gross_profit - sell_total - admin_total - rnd_total + other_result
        ebit = ebitda - da_total
        interest_net = (p["fin_zinsertraege"] - p["fin_zinsaufwand"]
                        - p["fin_zins_leasing"])
        fin_result = (interest_net + p["fin_assoziierte"] + p["fin_fx"]
                      + p["fin_sonstiges"])
        ebt = ebit + fin_result

        rate = TAX_RATE[entity.iso]
        tax_total = ebt * rate
        if entity.iso == "DE":
            p["tax_kst"] = tax_total * 0.62
            p["tax_gewst"] = tax_total * 0.33
            p["tax_auslaendisch"] = 0.0
        else:
            p["tax_kst"] = 0.0
            p["tax_gewst"] = 0.0
            p["tax_auslaendisch"] = tax_total * 0.95
        p["tax_latent"] = tax_total * 0.05 * _drift(entity, y, m, scenario, "dt", 0.60)
        tax_sum = (p["tax_kst"] + p["tax_gewst"] + p["tax_auslaendisch"]
                   + p["tax_latent"])
        net_income = ebt - tax_sum

        p["_gross_profit"] = gross_profit
        p["_ebitda"] = ebitda
        p["_ebit"] = ebit
        p["_ebt"] = ebt
        p["_net_income"] = net_income
        p["_da_total"] = da_total

        # ---- Jahreswechsel: Gewinnverwendung ----
        if cur_year is None:
            cur_year = y
        if y != cur_year:
            prev_year_ni = ytd_ni
            st["retained_earnings"] += ytd_ni * (1.0 - NCI_SHARE)
            ytd_ni = 0.0
            cur_year = y
        ytd_ni += net_income

        dividend = max(prev_year_ni, 0.0) * 0.35 if (m == 5 and prev_year_ni) else 0.0
        nci_payment = st["nci"] * 0.030 if m == 6 else 0.0

        # ---- Investitionen und Abgaenge ----
        capex_ppe = net_rev * prof["capex"] * (1.0 + 0.55 * jitter(scenario, entity.id, y, m, "capex"))
        capex_intang = net_rev * 0.0085 * _drift(entity, y, m, scenario, "capint", 0.40)
        disposal_proceeds = net_rev * 0.0042 * _drift(entity, y, m, scenario, "disp", 0.60)
        disposal_gain = p["oth_anlagenabgang"]
        # Buchwert der Abgaenge = Erloes - Gewinn
        disposal_nbv = max(disposal_proceeds - disposal_gain, 0.0)
        fininv_add = net_rev * 0.0011
        dev_capitalised = p["_rnd_capitalised"]
        rou_add = da_rou * 1.08
        lease_principal = da_rou * 1.02        # vgl. lease_liab = rou * 1.02

        # ---- Sammelpositionen fortschreiben ----
        agg = {}
        agg["goodwill"] = st["goodwill"] - imp_goodwill
        agg["intang_other"] = st["intang_other"] + capex_intang - st["intang_other"] / 84.0
        agg["intang_dev"] = st["intang_dev"] + dev_capitalised - st["intang_dev"] / 60.0
        agg["ppe"] = st["ppe"] + capex_ppe - da_ppe - disposal_nbv
        agg["fininv"] = st["fininv"] + fininv_add
        agg["rou"] = st["rou"] + rou_add - da_rou
        agg["dta"] = ttm_rev * 0.012
        inv_total = prof["dio"] / 365.0 * ttm_cogs
        agg["inv_raw"] = inv_total * 0.38
        agg["inv_wip"] = inv_total * 0.27
        agg["inv_fin"] = inv_total * 0.35
        agg["receivables"] = prof["dso"] / 365.0 * ttm_rev
        agg["contract_assets"] = ttm_rev * {"IA": 0.035, "ES": 0.070,
                                            "MS": 0.028, "DS": 0.022}[entity.segment]
        agg["other_assets"] = ttm_rev * 0.028

        agg["share_capital"] = st["share_capital"]
        agg["capital_reserve"] = st["capital_reserve"]
        agg["retained_earnings"] = st["retained_earnings"] - dividend
        agg["net_income_year"] = ytd_ni * (1.0 - NCI_SHARE)
        agg["oci"] = st["oci"] + net_rev * 0.0004 * jitter(scenario, entity.id, y, m, "oci")
        agg["nci"] = st["nci"] + net_income * NCI_SHARE - nci_payment
        agg["prov_pension"] = st["prov_pension"] * 1.0035
        tax_paid = st["prov_tax"] * 0.80 if m in (3, 6, 9, 12) else 0.0
        agg["prov_tax"] = st["prov_tax"] + max(tax_sum, 0.0) - tax_paid
        agg["prov_other"] = ttm_rev * 0.022
        agg["payables"] = prof["dpo"] / 365.0 * ttm_cogs
        lease_liab = agg["rou"] * 1.02
        agg["lease_lt"] = lease_liab * 0.78
        agg["lease_st"] = lease_liab * 0.22
        agg["contract_liab"] = ttm_rev * {"IA": 0.055, "ES": 0.110,
                                          "MS": 0.042, "DS": 0.140}[entity.segment]
        agg["dtl"] = ttm_rev * 0.009
        agg["other_liab"] = ttm_rev * 0.030
        agg["debt_st"] = st["debt_st"] * 0.955 + ttm_rev * 0.0042

        # ---- Zeilen aus den Sammelpositionen ableiten ----
        rows = {}

        def spread(agg_key, target=None):
            if agg_key in BS_SPLIT:
                for tag, share in BS_SPLIT[agg_key].items():
                    rows[tag] = 0.0 if is_dormant(tag, entity.id) \
                        else agg[agg_key] * share
                # entfaellt eine Zeile, bleibt der Betrag in der ersten
                missing = agg[agg_key] - sum(
                    rows[t] for t in BS_SPLIT[agg_key])
                if abs(missing) > 1e-12:
                    first = next(t for t in BS_SPLIT[agg_key]
                                 if not is_dormant(t, entity.id))
                    rows[first] += missing
            else:
                rows[target] = agg[agg_key]

        spread("goodwill", "goodwill")
        spread("intang_dev", "ia_entwicklungskosten")
        spread("intang_other")
        spread("ppe")
        spread("fininv")
        spread("rou")
        spread("dta", "aktive_latente_steuern")
        spread("inv_raw")
        spread("inv_wip", "vorraete_unfertig")
        spread("inv_fin", "vorraete_fertig")
        for tag, share in RECEIVABLE_SPLIT.items():
            rows[tag] = agg["receivables"] * share
        spread("contract_assets", "vertragsvermoegenswerte_poc")
        spread("other_assets")
        spread("share_capital", "ek_gezeichnetes_kapital")
        spread("capital_reserve", "ek_kapitalruecklage")
        spread("retained_earnings", "ek_gewinnruecklagen")
        spread("net_income_year", "ek_jahresueberschuss")
        spread("oci")
        spread("nci", "ek_minderheiten")
        spread("prov_pension", "rst_lf_pensionen")
        spread("prov_tax", "rst_kf_steuern")
        spread("prov_other")
        spread("payables")
        spread("lease_lt", "leasing_lf")
        spread("lease_st", "leasing_kf")
        spread("contract_liab")
        spread("dtl", "passive_latente_steuern")
        spread("other_liab")
        spread("debt_st")

        # ---- Ausgleichsposition: langfristige Finanzverbindlichkeiten ----
        cash_target = ttm_rev * 0.062 * (1.0 + 0.10 * jitter(scenario, entity.id, y, m, "cash"))
        non_cash_assets = sum(rows[t] * ROW_SIGN.get(t, 1)
                              for t in ASSET_ROWS if t in rows)
        le_known = sum(rows[t] * ROW_SIGN.get(t, 1)
                       for t in LE_ROWS if t in rows)
        need = non_cash_assets + cash_target - le_known
        min_debt_lt = ttm_rev * 0.035
        if need >= min_debt_lt:
            agg["debt_lt"] = need
            agg["cash"] = cash_target
        else:
            agg["debt_lt"] = min_debt_lt
            agg["cash"] = cash_target + (min_debt_lt - need)
        spread("debt_lt")
        spread("cash")

        # ---- Kapitalflussrechnung aus den Bewegungen ----
        if prev_rows is None:
            pr = rows                       # Erstkonsolidierung: keine Bewegung
            cons_inflow = agg["cash"]
            cash_bop = 0.0
        else:
            pr = prev_rows
            cons_inflow = 0.0
            cash_bop = sum(pr[t] for t in BS_SPLIT["cash"])

        def dsum(*tags):
            return sum(rows[t] - pr[t] for t in tags if t in rows and t in pr)

        cf = {}
        cf["cf_jahresueberschuss"] = net_income
        cf["cf_abschreibungen_sav_ia"] = da_ppe + da_int
        cf["cf_abschreibungen_rou"] = da_rou
        cf["cf_wertminderungen"] = imp_goodwill
        cf["cf_ergebnis_anlagenabgaenge"] = disposal_gain
        cf["cf_ergebnis_at_equity"] = p["fin_assoziierte"]
        cf["cf_ueberleitung_zinsen"] = -interest_net
        cf["cf_ueberleitung_steuern"] = tax_sum
        cf["cf_delta_vorraete"] = dsum("vorraete_rhb", "vorraete_unfertig",
                                       "vorraete_fertig", "vorraete_anzahlungen")
        cf["cf_delta_forderungen"] = (dsum("ford_lul_dritte", "ford_lul_verbundene")
                                      - dsum("ford_wertminderung"))
        cf["cf_delta_vertragsvermoegen"] = dsum("vertragsvermoegenswerte_poc")
        cf["cf_delta_verbindlichkeiten"] = dsum("verb_lul_dritte", "verb_lul_verbundene")
        cf["cf_delta_vertragsverb"] = dsum("vertragsverbindlichkeiten_poc",
                                           "erhaltene_anzahlungen")
        cf["cf_delta_sonstige"] = (
            dsum("sonst_verb_lf", "sonst_verb_kf_steuern",
                 "sonst_verb_kf_soziales", "sonst_verb_kf_uebrige")
            - dsum("sonstige_finanzielle_va", "steuererstattungsansprueche",
                   "aktive_rap")
            + dsum("passive_latente_steuern") - dsum("aktive_latente_steuern"))
        cf["cf_delta_pensionsrueckstellungen"] = dsum("rst_lf_pensionen")
        cf["cf_delta_sonstige_rueckstellungen"] = dsum(
            "rst_lf_sonstige", "rst_kf_garantie", "rst_kf_personal",
            "rst_kf_sonstige")
        cf["cf_erhaltene_zinsen"] = p["fin_zinsertraege"]
        cf["cf_gezahlte_zinsen"] = p["fin_zinsaufwand"] + p["fin_zins_leasing"]
        cf["cf_gezahlte_steuern"] = tax_paid
        cf["cf_capex_sachanlagen"] = capex_ppe
        cf["cf_capex_immateriell"] = capex_intang
        cf["cf_capex_entwicklung"] = dev_capitalised
        cf["cf_invest_finanzanlagen"] = fininv_add
        cf["cf_unternehmenserwerbe"] = 0.0
        cf["cf_verkauf_gesellschaften"] = 0.0
        cf["cf_abgang_sachanlagen"] = disposal_proceeds
        cf["cf_abgang_finanzanlagen"] = 0.0
        # Ausschuettung der assoziierten Unternehmen: der Ergebnisbeitrag
        # wird in CFO herausgerechnet und hier als Zahlungseingang gezeigt.
        cf["cf_erhaltene_dividenden"] = p["fin_assoziierte"]

        d_bonds = dsum("fv_lf_anleihen")
        d_loans = dsum("fv_lf_banken", "fv_lf_schuldschein",
                       "fv_kf_banken", "fv_kf_anteil_lf")
        cf["cf_aufnahme_kredite"] = max(d_loans, 0.0)
        cf["cf_tilgung_kredite"] = max(-d_loans, 0.0)
        cf["cf_emission_anleihen"] = max(d_bonds, 0.0)
        cf["cf_rueckzahlung_anleihen"] = max(-d_bonds, 0.0)
        cf["cf_leasingzahlungen"] = lease_principal
        cf["cf_kapitalerhoehung"] = 0.0
        cf["cf_eigene_anteile"] = 0.0
        cf["cf_dividende_konzern"] = dividend
        cf["cf_dividende_minderheiten"] = nci_payment
        cf["cf_waehrungseffekte"] = net_rev * 0.0003 * jitter(scenario, entity.id, y, m, "cffx")
        cf["cf_konsolidierungskreis"] = cons_inflow

        for tag in list(cf):
            if is_dormant(tag, entity.id):
                cf[tag] = 0.0

        # Restposten: CFO + CFI + CFF muss die Fondsveraenderung ohne
        # Waehrungs- und Konsolidierungseffekte ergeben. Darin landen die
        # zahlungsunwirksamen Eigenkapitalbewegungen (OCI) und Rundung.
        cf["cf_sonstige_zahlungsunwirksam"] = 0.0
        explicit = sum(cf[t] * s for t, s in CF_BLOCK_SIGN.items())
        delta_cash = agg["cash"] - cash_bop
        cf["cf_sonstige_zahlungsunwirksam"] = (
            delta_cash - cf["cf_waehrungseffekte"] - cons_inflow - explicit)

        cf["cf_bestand_anfang"] = cash_bop
        cf["cf_bestand_ende"] = agg["cash"]

        p.update(rows)
        p.update(cf)

        # ---- Umrechnung in die Konzernwaehrung (IAS 21) ----
        # Erfolgsposten und Zahlungsstroeme zum Durchschnittskurs,
        # Bilanzposten zum Stichtagskurs, der Anfangsbestand zum
        # Stichtagskurs des Vormonats.
        avg_rate, close_rate = entity.rate(y, m)
        eur = {}
        for tag, val in p.items():
            if tag.startswith("_"):
                continue
            aggr = agg_by_tag.get(tag, "Summe")
            if aggr == "Bestand":
                eur[tag] = val / close_rate
            elif aggr == "Bestand Anfang":
                eur[tag] = val / (prev_close or close_rate)
            else:
                eur[tag] = val / avg_rate
        # Der Zugang aus der Erstkonsolidierung ist ein Bestand, der zugeht
        eur["cf_konsolidierungskreis"] = cf["cf_konsolidierungskreis"] / close_rate
        # Waehrungseffekt auf den Finanzmittelfonds: die Differenz zwischen
        # den zum Durchschnittskurs umgerechneten Zahlungsstroemen und der
        # zum Stichtagskurs umgerechneten Bestandsveraenderung. Genau das
        # weist IAS 7 als eigene Zeile aus -- und genau damit geht die
        # Ueberleitung auch in EUR exakt auf.
        eur["cf_waehrungseffekte"] = 0.0
        explicit_eur = sum(eur[t] * sg for t, sg in CF_BLOCK_SIGN.items())
        eur["cf_waehrungseffekte"] = (
            eur["cf_bestand_ende"] - eur["cf_bestand_anfang"]
            - eur["cf_konsolidierungskreis"] - explicit_eur)

        p["_eur"] = eur
        p["_ttm_rev"] = ttm_rev
        p["_cash"] = agg["cash"]
        p["_delta_cash"] = delta_cash
        p["_kurs_durchschnitt"] = avg_rate
        p["_kurs_stichtag"] = close_rate
        result[(y, m)] = p

        prev_rows = rows
        prev_close = close_rate
        st = dict(agg)

    return result
