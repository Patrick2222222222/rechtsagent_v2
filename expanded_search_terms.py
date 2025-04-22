#!/usr/bin/env python3
# expanded_search_terms.py - Erweiterte Suchbegriffe für IRI® Legal Agent

# Kategorien von Suchbegriffen
HASHTAGS = [
    "#hyaluronpen",
    "#lippenaufspritzen",
    "#needlefreefiller",
    "#faltenaufspritzen",
    "#hyaluronpistole",
    "#hyaluronstift",
    "#lipfiller",
    "#lippenfiller",
    "#lippenunterspritzung",
    "#lippenvergrößerung",
    "#lippenaufbau",
    "#lippenkorrektur",
    "#hyaluronsäurepen",
    "#hyaluronsäure",
    "#hyaluronbehandlung",
    "#lippenohnenadel",
    "#lippenaufspritzungohnenadel",
    "#kosmetikstudio",
    "#beautytreatment",
    "#schönheitskosmetik",
    "#kosmetikerin",
    "#kosmetikbehandlung",
    "#lippenvorher",
    "#lippennachher",
    "#vorhernachher",
    "#lippenaufspritzungvorher",
    "#lippenaufspritzungnachher",
    "#beautytrend",
    "#beautysalon",
    "#kosmetiksalon",
    "#hyaluronpentraining",
    "#hyaluronpenschulung",
    "#hyaluronpenkurs",
    "#hyaluronpenkaufen",
    "#hyaluronpenset"
]

KEYWORDS = [
    "Hyaluron Pen Behandlung",
    "Lippen aufspritzen ohne Nadel",
    "Hyaluron Stift kaufen",
    "Hyaluron Pen Schulung",
    "Hyaluron Pen Erfahrung",
    "Hyaluron Pen Vorher Nachher",
    "Lippen aufspritzen Kosten",
    "Hyaluronsäure Pen",
    "Hyaluron Pistole",
    "Lippenunterspritzung ohne Nadel",
    "Kosmetikstudio Hyaluron",
    "Hyaluron Pen Angebot",
    "Hyaluron Pen Preis",
    "Hyaluron Pen Ergebnisse",
    "Lippen vergrößern ohne OP",
    "Lippen aufspritzen Erfahrungen",
    "Hyaluron Pen Zertifikat",
    "Hyaluron Pen Ausbildung",
    "Hyaluron Pen Starter Set",
    "Hyaluron Pen Ampullen",
    "Hyaluron Pen Gerät",
    "Hyaluron Pen Zubehör",
    "Hyaluron Pen Behandlung Preis",
    "Hyaluron Pen Behandlung buchen",
    "Hyaluron Pen Behandlung Termin",
    "Lippen aufspritzen Hyaluron Pen",
    "Falten aufspritzen ohne Nadel",
    "Hyaluron Pen Anwendung",
    "Hyaluron Pen selber machen",
    "Hyaluron Pen zu Hause",
    "Hyaluron Pen Risiken",
    "Hyaluron Pen Nebenwirkungen",
    "Hyaluron Pen Erfahrungsberichte",
    "Hyaluron Pen Bewertungen",
    "Hyaluron Pen Kosmetikstudio",
    "Hyaluron Pen Beauty Salon",
    "Hyaluron Pen Kosmetikerin",
    "Hyaluron Pen Behandlung in der Nähe",
    "Hyaluron Pen Lippen aufspritzen",
    "Hyaluron Pen Falten behandeln"
]

LOCATION_KEYWORDS = [
    "Hyaluron Pen Berlin",
    "Hyaluron Pen Hamburg",
    "Hyaluron Pen München",
    "Hyaluron Pen Köln",
    "Hyaluron Pen Frankfurt",
    "Hyaluron Pen Stuttgart",
    "Hyaluron Pen Düsseldorf",
    "Hyaluron Pen Leipzig",
    "Hyaluron Pen Dresden",
    "Hyaluron Pen Hannover",
    "Hyaluron Pen Nürnberg",
    "Hyaluron Pen Dortmund",
    "Hyaluron Pen Essen",
    "Hyaluron Pen Bremen",
    "Hyaluron Pen Duisburg",
    "Hyaluron Pen Bochum",
    "Hyaluron Pen Wuppertal",
    "Hyaluron Pen Bielefeld",
    "Hyaluron Pen Bonn",
    "Hyaluron Pen Münster",
    "Hyaluron Pen Karlsruhe",
    "Hyaluron Pen Mannheim",
    "Hyaluron Pen Augsburg",
    "Hyaluron Pen Wiesbaden",
    "Hyaluron Pen Gelsenkirchen",
    "Hyaluron Pen Mönchengladbach",
    "Hyaluron Pen Braunschweig",
    "Hyaluron Pen Kiel",
    "Hyaluron Pen Chemnitz",
    "Hyaluron Pen Aachen",
    "Hyaluron Pen Halle",
    "Hyaluron Pen Magdeburg",
    "Hyaluron Pen Freiburg",
    "Hyaluron Pen Krefeld",
    "Hyaluron Pen Lübeck",
    "Hyaluron Pen Oberhausen",
    "Hyaluron Pen Erfurt",
    "Hyaluron Pen Mainz",
    "Hyaluron Pen Rostock",
    "Hyaluron Pen Kassel",
    "Hyaluron Pen Hagen",
    "Hyaluron Pen Hamm",
    "Hyaluron Pen Saarbrücken",
    "Hyaluron Pen Mülheim",
    "Hyaluron Pen Potsdam",
    "Hyaluron Pen Ludwigshafen",
    "Hyaluron Pen Oldenburg",
    "Hyaluron Pen Leverkusen",
    "Hyaluron Pen Osnabrück",
    "Hyaluron Pen Solingen"
]

INSTAGRAM_ACCOUNTS_TO_CHECK = [
    "beauty_studio_berlin",
    "kosmetik_studio_hamburg",
    "beauty_salon_muenchen",
    "hyaluron_pen_germany",
    "lippenaufspritzen_de",
    "beauty_treatment_koeln",
    "kosmetikstudio_frankfurt",
    "hyaluron_pen_behandlung",
    "beauty_salon_deutschland",
    "kosmetik_studio_berlin",
    "lippen_aufspritzen_hamburg",
    "hyaluron_pen_muenchen",
    "beauty_kosmetik_berlin",
    "kosmetikerin_hamburg",
    "beauty_salon_koeln",
    "hyaluron_behandlung_frankfurt",
    "lippen_aufspritzen_stuttgart",
    "kosmetikstudio_duesseldorf",
    "beauty_treatment_leipzig",
    "hyaluron_pen_dresden"
]

FACEBOOK_PAGES_TO_CHECK = [
    "BeautyStudioBerlin",
    "KosmetikStudioHamburg",
    "BeautySalonMuenchen",
    "HyaluronPenGermany",
    "LippenaufspritzenDE",
    "BeautyTreatmentKoeln",
    "KosmetikstudioFrankfurt",
    "HyaluronPenBehandlung",
    "BeautySalonDeutschland",
    "KosmetikStudioBerlin",
    "LippenaufspritzenHamburg",
    "HyaluronPenMuenchen",
    "BeautyKosmetikBerlin",
    "KosmetikerinHamburg",
    "BeautySalonKoeln",
    "HyaluronBehandlungFrankfurt",
    "LippenaufspritzenStuttgart",
    "KosmetikstudioDuesseldorf",
    "BeautyTreatmentLeipzig",
    "HyaluronPenDresden"
]

TIKTOK_ACCOUNTS_TO_CHECK = [
    "@beauty_studio_berlin",
    "@kosmetik_studio_hamburg",
    "@beauty_salon_muenchen",
    "@hyaluron_pen_germany",
    "@lippenaufspritzen_de",
    "@beauty_treatment_koeln",
    "@kosmetikstudio_frankfurt",
    "@hyaluron_pen_behandlung",
    "@beauty_salon_deutschland",
    "@kosmetik_studio_berlin",
    "@lippen_aufspritzen_hamburg",
    "@hyaluron_pen_muenchen",
    "@beauty_kosmetik_berlin",
    "@kosmetikerin_hamburg",
    "@beauty_salon_koeln",
    "@hyaluron_behandlung_frankfurt",
    "@lippen_aufspritzen_stuttgart",
    "@kosmetikstudio_duesseldorf",
    "@beauty_treatment_leipzig",
    "@hyaluron_pen_dresden"
]

WEBSITE_DOMAINS_TO_CHECK = [
    "kosmetikstudio-berlin.de",
    "beauty-salon-hamburg.de",
    "kosmetik-muenchen.de",
    "hyaluron-pen-behandlung.de",
    "lippenaufspritzen-koeln.de",
    "beauty-studio-frankfurt.de",
    "kosmetikstudio-stuttgart.de",
    "hyaluron-pen-duesseldorf.de",
    "beauty-salon-leipzig.de",
    "kosmetik-dresden.de",
    "lippenaufspritzen-hannover.de",
    "hyaluron-pen-nuernberg.de",
    "beauty-studio-dortmund.de",
    "kosmetikstudio-essen.de",
    "hyaluron-behandlung-bremen.de",
    "beauty-salon-duisburg.de",
    "kosmetik-bochum.de",
    "lippenaufspritzen-wuppertal.de",
    "hyaluron-pen-bielefeld.de",
    "beauty-studio-bonn.de"
]

# Kombinierte Liste aller Suchbegriffe
ALL_SEARCH_TERMS = {
    "hashtags": HASHTAGS,
    "keywords": KEYWORDS,
    "location_keywords": LOCATION_KEYWORDS,
    "instagram_accounts": INSTAGRAM_ACCOUNTS_TO_CHECK,
    "facebook_pages": FACEBOOK_PAGES_TO_CHECK,
    "tiktok_accounts": TIKTOK_ACCOUNTS_TO_CHECK,
    "website_domains": WEBSITE_DOMAINS_TO_CHECK
}

def get_all_search_terms():
    """Gibt alle Suchbegriffe als Dictionary zurück"""
    return ALL_SEARCH_TERMS

def get_search_terms_by_category(category):
    """Gibt Suchbegriffe für eine bestimmte Kategorie zurück"""
    return ALL_SEARCH_TERMS.get(category, [])

def get_search_terms_for_platform(platform):
    """Gibt geeignete Suchbegriffe für eine bestimmte Plattform zurück"""
    if platform.lower() == "instagram":
        return HASHTAGS + INSTAGRAM_ACCOUNTS_TO_CHECK
    elif platform.lower() == "facebook":
        return KEYWORDS + LOCATION_KEYWORDS + FACEBOOK_PAGES_TO_CHECK
    elif platform.lower() == "tiktok":
        return HASHTAGS + TIKTOK_ACCOUNTS_TO_CHECK
    elif platform.lower() == "google":
        return KEYWORDS + LOCATION_KEYWORDS + WEBSITE_DOMAINS_TO_CHECK
    elif platform.lower() == "website":
        return WEBSITE_DOMAINS_TO_CHECK
    else:
        # Für unbekannte Plattformen geben wir alle Suchbegriffe zurück
        return HASHTAGS + KEYWORDS + LOCATION_KEYWORDS

def generate_combined_search_terms(max_terms=50):
    """Generiert kombinierte Suchbegriffe für erweiterte Suche"""
    import random
    import itertools
    
    # Beispiele für Kombinationen
    base_terms = ["Hyaluron Pen", "Lippen aufspritzen", "Hyaluronsäure", "Kosmetikstudio"]
    locations = ["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart", "Düsseldorf"]
    attributes = ["günstig", "Angebot", "Termin", "Erfahrung", "Vorher Nachher", "Preis", "ohne Nadel"]
    
    combined_terms = []
    
    # Kombiniere Basis-Begriffe mit Attributen
    for base, attr in itertools.product(base_terms, attributes):
        combined_terms.append(f"{base} {attr}")
    
    # Kombiniere Basis-Begriffe mit Orten
    for base, loc in itertools.product(base_terms, locations):
        combined_terms.append(f"{base} {loc}")
    
    # Wähle zufällig max_terms Begriffe aus
    if len(combined_terms) > max_terms:
        combined_terms = random.sample(combined_terms, max_terms)
    
    return combined_terms

if __name__ == "__main__":
    # Teste die Funktionen
    print(f"Anzahl der Hashtags: {len(HASHTAGS)}")
    print(f"Anzahl der Keywords: {len(KEYWORDS)}")
    print(f"Anzahl der Location Keywords: {len(LOCATION_KEYWORDS)}")
    print(f"Anzahl der Instagram-Accounts: {len(INSTAGRAM_ACCOUNTS_TO_CHECK)}")
    print(f"Anzahl der Facebook-Seiten: {len(FACEBOOK_PAGES_TO_CHECK)}")
    print(f"Anzahl der TikTok-Accounts: {len(TIKTOK_ACCOUNTS_TO_CHECK)}")
    print(f"Anzahl der Website-Domains: {len(WEBSITE_DOMAINS_TO_CHECK)}")
    
    print("\nBeispiele für kombinierte Suchbegriffe:")
    combined_terms = generate_combined_search_terms(10)
    for term in combined_terms:
        print(f"- {term}")
