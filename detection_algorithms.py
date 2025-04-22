#!/usr/bin/env python3
# detection_algorithms.py - Verbesserte Erkennungsalgorithmen für IRI® Legal Agent

import re
import json
import logging
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("detection.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("detection_algorithms")

# Stelle sicher, dass die benötigten NLTK-Daten heruntergeladen sind
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class HyaluronPenDetector:
    """Klasse zur Erkennung von Hyaluron Pen Angeboten in Texten und Profilen"""
    
    def __init__(self):
        """Initialisiert den HyaluronPenDetector"""
        # Lade deutsche Stopwörter
        self.stopwords = set(stopwords.words('german'))
        
        # Schlüsselwörter für Hyaluron Pen Angebote
        self.hyaluron_keywords = [
            "hyaluron pen", "hyaluronpen", "hyaluron-pen", "hyaluronstift", "hyaluron stift",
            "hyaluronpistole", "hyaluron pistole", "needlefreefiller", "needle free filler",
            "lippenaufspritzen", "lippen aufspritzen", "lippenunterspritzung", "lippen unterspritzung",
            "faltenaufspritzen", "falten aufspritzen", "lippenvergrößerung", "lippen vergrößerung",
            "lippenaufbau", "lippen aufbau", "lippenkorrektur", "lippen korrektur",
            "hyaluronsäurepen", "hyaluronsäure pen", "hyaluronsäure-pen"
        ]
        
        # Preismuster für Preiserkennung
        self.price_patterns = [
            r'(\d+)[.,]?(\d{2})?\s*€',  # 79€, 79.00€, 79,00€
            r'(\d+)[.,]?(\d{2})?\s*Euro',  # 79 Euro, 79.00 Euro
            r'€\s*(\d+)[.,]?(\d{2})?',  # € 79, € 79.00
            r'Euro\s*(\d+)[.,]?(\d{2})?',  # Euro 79
            r'ab\s*(\d+)[.,]?(\d{2})?\s*€',  # ab 79€
            r'ab\s*(\d+)[.,]?(\d{2})?\s*Euro',  # ab 79 Euro
            r'nur\s*(\d+)[.,]?(\d{2})?\s*€',  # nur 79€
            r'nur\s*(\d+)[.,]?(\d{2})?\s*Euro',  # nur 79 Euro
            r'(\d+)[.,]?(\d{2})?\s*EUR',  # 79 EUR
        ]
        
        # Muster für E-Mail-Adressen
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Muster für Telefonnummern
        self.phone_patterns = [
            r'(\+49|0)[- ]?(\d{3,5})[- ]?(\d{5,8})',  # +49 123 45678, 0123 45678
            r'(\+49|0)[- ]?(\d{2})[- ]?(\d{2})[- ]?(\d{2})[- ]?(\d{2})',  # +49 12 34 56 78
            r'(\+49|0)[- ]?(\d{4})[- ]?(\d{6})',  # +49 1234 567890
        ]
        
        # Muster für Orte in Deutschland
        self.location_keywords = [
            "Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart", "Düsseldorf",
            "Leipzig", "Dresden", "Hannover", "Nürnberg", "Dortmund", "Essen", "Bremen",
            "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster", "Karlsruhe",
            "Mannheim", "Augsburg", "Wiesbaden", "Gelsenkirchen", "Mönchengladbach", "Braunschweig",
            "Kiel", "Chemnitz", "Aachen", "Halle", "Magdeburg", "Freiburg", "Krefeld", "Lübeck",
            "Oberhausen", "Erfurt", "Mainz", "Rostock", "Kassel", "Hagen", "Hamm", "Saarbrücken",
            "Mülheim", "Potsdam", "Ludwigshafen", "Oldenburg", "Leverkusen", "Osnabrück", "Solingen"
        ]
        
        # Wörter, die auf kommerzielle Angebote hindeuten
        self.commercial_indicators = [
            "angebot", "preis", "kosten", "termin", "vereinbaren", "buchen", "buchung",
            "behandlung", "behandlungen", "studio", "salon", "kosmetik", "kosmetikstudio",
            "beauty", "beautysalon", "schönheit", "schönheitssalon", "rabatt", "sparen",
            "aktion", "sonderangebot", "gutschein", "geschenkgutschein", "jetzt", "neu",
            "vorher", "nachher", "ergebnis", "ergebnisse", "vorher-nachher", "beratung"
        ]
    
    def detect_hyaluron_pen_content(self, text):
        """
        Erkennt, ob ein Text Hinweise auf Hyaluron Pen Angebote enthält
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            Boolean: True, wenn Hyaluron Pen Angebote erkannt wurden, sonst False
        """
        if not text:
            return False
        
        # Konvertiere Text zu Kleinbuchstaben
        text_lower = text.lower()
        
        # Prüfe auf Hyaluron-Keywords
        for keyword in self.hyaluron_keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    def extract_prices(self, text):
        """
        Extrahiert Preise aus einem Text
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            Liste von gefundenen Preisen
        """
        if not text:
            return []
        
        prices = []
        
        for pattern in self.price_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # Extrahiere den Preis aus dem Match
                price_str = match.group(0)
                # Extrahiere nur die Zahlen und konvertiere zu Float
                price_value = re.search(r'(\d+)[.,]?(\d{2})?', price_str)
                if price_value:
                    euros = price_value.group(1)
                    cents = price_value.group(2) or "00"
                    price = float(f"{euros}.{cents}")
                    prices.append(price)
        
        return prices
    
    def extract_emails(self, text):
        """
        Extrahiert E-Mail-Adressen aus einem Text
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            Liste von gefundenen E-Mail-Adressen
        """
        if not text:
            return []
        
        emails = re.findall(self.email_pattern, text)
        return emails
    
    def extract_phones(self, text):
        """
        Extrahiert Telefonnummern aus einem Text
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            Liste von gefundenen Telefonnummern
        """
        if not text:
            return []
        
        phones = []
        
        for pattern in self.phone_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                phone = match.group(0)
                phones.append(phone)
        
        return phones
    
    def extract_locations(self, text):
        """
        Extrahiert Orte aus einem Text
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            Liste von gefundenen Orten
        """
        if not text:
            return []
        
        locations = []
        
        # Tokenisiere den Text
        words = word_tokenize(text)
        
        # Suche nach Orten
        for word in words:
            for location in self.location_keywords:
                if location.lower() == word.lower():
                    locations.append(location)
        
        return locations
    
    def calculate_commercial_score(self, text):
        """
        Berechnet einen Score für die Wahrscheinlichkeit, dass es sich um ein kommerzielles Angebot handelt
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            Float: Score zwischen 0 und 1
        """
        if not text:
            return 0.0
        
        # Konvertiere Text zu Kleinbuchstaben
        text_lower = text.lower()
        
        # Tokenisiere den Text
        words = word_tokenize(text_lower)
        
        # Entferne Stopwörter
        words = [word for word in words if word not in self.stopwords]
        
        # Zähle kommerzielle Indikatoren
        commercial_count = 0
        for word in words:
            for indicator in self.commercial_indicators:
                if indicator == word:
                    commercial_count += 1
        
        # Berechne Score
        if len(words) > 0:
            score = commercial_count / len(words)
            # Normalisiere Score auf 0-1
            score = min(score * 3, 1.0)  # Multipliziere mit 3, um den Score zu verstärken, aber maximal 1.0
            return score
        
        return 0.0
    
    def analyze_profile(self, profile_data):
        """
        Analysiert ein Profil auf Hinweise auf Hyaluron Pen Angebote
        
        Args:
            profile_data: Dictionary mit Profildaten
            
        Returns:
            Dictionary mit Analyseergebnissen
        """
        # Kombiniere relevante Textfelder
        text_fields = []
        if "description" in profile_data and profile_data["description"]:
            text_fields.append(profile_data["description"])
        if "post_text" in profile_data and profile_data["post_text"]:
            text_fields.append(profile_data["post_text"])
        
        combined_text = " ".join(text_fields)
        
        # Analysiere den Text
        contains_hyaluron = self.detect_hyaluron_pen_content(combined_text)
        prices = self.extract_prices(combined_text)
        emails = self.extract_emails(combined_text)
        phones = self.extract_phones(combined_text)
        locations = self.extract_locations(combined_text)
        commercial_score = self.calculate_commercial_score(combined_text)
        
        # Berechne Risiko-Score
        risk_score = 0.0
        
        if contains_hyaluron:
            risk_score += 0.5  # Grundwert für Hyaluron Pen Erwähnung
        
        if prices:
            risk_score += 0.2  # Preisangaben erhöhen das Risiko
        
        if emails or phones:
            risk_score += 0.1  # Kontaktdaten erhöhen das Risiko
        
        # Kommerzieller Score fließt direkt ein
        risk_score += commercial_score * 0.2
        
        # Normalisiere auf 0-100
        risk_score = min(risk_score * 100, 100.0)
        
        # Erstelle Analyseergebnis
        result = {
            "contains_hyaluron_pen": contains_hyaluron,
            "prices": prices,
            "emails": emails,
            "phones": phones,
            "locations": locations,
            "commercial_score": commercial_score,
            "risk_score": risk_score,
            "analysis_date": datetime.now().isoformat()
        }
        
        return result
    
    def analyze_post(self, post_data):
        """
        Analysiert einen Post auf Hinweise auf Hyaluron Pen Angebote
        
        Args:
            post_data: Dictionary mit Postdaten
            
        Returns:
            Dictionary mit Analyseergebnissen
        """
        # Extrahiere Text
        text = post_data.get("post_text", "")
        
        # Analysiere den Text
        contains_hyaluron = self.detect_hyaluron_pen_content(text)
        prices = self.extract_prices(text)
        commercial_score = self.calculate_commercial_score(text)
        
        # Berechne Risiko-Score
        risk_score = 0.0
        
        if contains_hyaluron:
            risk_score += 0.6  # Grundwert für Hyaluron Pen Erwähnung
        
        if prices:
            risk_score += 0.2  # Preisangaben erhöhen das Risiko
        
        # Kommerzieller Score fließt direkt ein
        risk_score += commercial_score * 0.2
        
        # Normalisiere auf 0-100
        risk_score = min(risk_score * 100, 100.0)
        
        # Erstelle Analyseergebnis
        result = {
            "contains_hyaluron_pen": contains_hyaluron,
            "prices": prices,
            "price_mentioned": ", ".join([f"{price}€" for price in prices]) if prices else None,
            "commercial_score": commercial_score,
            "risk_score": risk_score,
            "analysis_date": datetime.now().isoformat()
        }
        
        return result


class ImageAnalyzer:
    """Klasse zur Analyse von Bildern auf Hinweise auf Hyaluron Pen Behandlungen"""
    
    def __init__(self):
        """Initialisiert den ImageAnalyzer"""
        # In einer realen Implementierung würden wir hier ein Bilderkennungsmodell laden
        # Für Entwicklungszwecke simulieren wir die Bilderkennung
        pass
    
    def analyze_image(self, image_path):
        """
        Analysiert ein Bild auf Hinweise auf Hyaluron Pen Behandlungen
        
        Args:
            image_path: Pfad zum Bild
            
        Returns:
            Dictionary mit Analyseergebnissen
        """
        # In einer realen Implementierung würden wir hier das Bild analysieren
        # Für Entwicklungszwecke simulieren wir die Analyse
        
        # Simuliere Ergebnisse basierend auf dem Dateinamen
        contains_hyaluron = "hyaluron" in image_path.lower() or "lippen" in image_path.lower()
        contains_before_after = "vorher" in image_path.lower() or "nachher" in image_path.lower() or "before" in image_path.lower() or "after" in image_path.lower()
        
        # Berechne Risiko-Score
        risk_score = 0.0
        
        if contains_hyaluron:
            risk_score += 0.5  # Grundwert für Hyaluron Pen Erwähnung im Dateinamen
        
        if contains_before_after:
            risk_score += 0.3  # Vorher-Nachher-Bilder erhöhen das Risiko
        
        # Normalisiere auf 0-100
        risk_score = min(risk_score * 100, 100.0)
        
        # Erstelle Analyseergebnis
        result = {
            "contains_hyaluron_pen": contains_hyaluron,
            "contains_before_after": contains_before_after,
            "risk_score": risk_score,
            "analysis_date": datetime.now().isoformat()
        }
        
        return result


class DetectionManager:
    """Klasse zur Koordination der Erkennungsalgorithmen"""
    
    def __init__(self, db_manager=None):
        """
        Initialisiert den DetectionManager
        
        Args:
            db_manager: Optional, ein DatabaseManager-Objekt für die Datenbankintegration
        """
        self.db_manager = db_manager
        self.hyaluron_detector = HyaluronPenDetector()
        self.image_analyzer = ImageAnalyzer()
    
    def analyze_scraping_results(self, results):
        """
        Analysiert Scraping-Ergebnisse und identifiziert verdächtige Profile
        
        Args:
            results: Dictionary mit Scraping-Ergebnissen pro Plattform
            
        Returns:
            Liste von verdächtigen Profilen mit Analyseergebnissen
        """
        suspicious_profiles = []
        
        # Analysiere Ergebnisse für jede Plattform
        for platform, platform_results in results.items():
            logger.info(f"Analysiere {len(platform_results)} Ergebnisse für {platform}")
            
            for profile_data in platform_results:
                # Analysiere das Profil
                analysis = self.hyaluron_detector.analyze_profile(profile_data)
                
                # Füge Analyseergebnisse zum Profil hinzu
                profile_data["analysis"] = analysis
                
                # Prüfe, ob das Profil verdächtig ist
                if analysis["risk_score"] >= 50.0:  # Schwellenwert für verdächtige Profile
                    suspicious_profiles.append(profile_data)
                    logger.info(f"Verdächtiges Profil gefunden: {profile_data.get('profile_name')} auf {platform} (Risiko-Score: {analysis['risk_score']:.2f})")
                    
                    # Speichere das Profil in der Datenbank mit aktualisiertem Risiko-Score
                    if self.db_manager:
                        # Aktualisiere das Profil mit dem Risiko-Score
                        profile_data["risk_score"] = analysis["risk_score"]
                        
                        # Speichere das Profil in der Datenbank
                        profile = self.db_manager.add_profile(platform, profile_data)
                        
                        # Wenn ein Post vorhanden ist, analysiere und speichere ihn
                        if profile and "post_text" in profile_data:
                            post_data = {
                                "post_link": profile_data.get("post_link"),
                                "post_text": profile_data.get("post_text")
                            }
                            
                            # Analysiere den Post
                            post_analysis = self.hyaluron_detector.analyze_post(post_data)
                            
                            # Aktualisiere Post-Daten mit Analyseergebnissen
                            post_data.update({
                                "contains_hyaluron_pen": post_analysis["contains_hyaluron_pen"],
                                "contains_price": len(post_analysis["prices"]) > 0,
                                "price_mentioned": post_analysis["price_mentioned"]
                            })
                            
                            # Speichere den Post in der Datenbank
                            self.db_manager.add_post(profile.id, post_data)
        
        logger.info(f"Analyse abgeschlossen: {len(suspicious_profiles)} verdächtige Profile gefunden")
        return suspicious_profiles
    
    def analyze_image_file(self, image_path, profile_id=None, post_id=None):
        """
        Analysiert ein Bild und speichert die Ergebnisse
        
        Args:
            image_path: Pfad zum Bild
            profile_id: Optional, ID des zugehörigen Profils
            post_id: Optional, ID des zugehörigen Posts
            
        Returns:
            Dictionary mit Analyseergebnissen
        """
        # Analysiere das Bild
        analysis = self.image_analyzer.analyze_image(image_path)
        
        # Speichere die Ergebnisse in der Datenbank
        if self.db_manager and (profile_id or post_id):
            screenshot_data = {
                "profile_id": profile_id,
                "post_id": post_id,
                "file_path": image_path,
                "url_captured": "",  # In einer realen Implementierung würde hier die URL stehen
                "is_evidence": analysis["risk_score"] >= 50.0,
                "metadata": json.dumps(analysis)
            }
            
            self.db_manager.add_screenshot(screenshot_data)
        
        return analysis


if __name__ == "__main__":
    # Teste die Erkennungsalgorithmen
    detector = HyaluronPenDetector()
    
    # Teste die Hyaluron Pen Erkennung
    test_texts = [
        "Wir bieten Hyaluron Pen Behandlungen an. Lippen aufspritzen ohne Nadel ab 79€!",
        "Schöne Lippen ohne OP! Jetzt Termin vereinbaren.",
        "Kosmetikstudio in Berlin mit Hyaluronsäure-Behandlungen.",
        "Hyaluron Pen Schulung - Lerne die neueste Technik!",
        "Vorher-Nachher Bilder unserer Hyaluron Pen Behandlungen. Jetzt buchen unter info@beauty-studio.de"
    ]
    
    print("Hyaluron Pen Erkennung:")
    for text in test_texts:
        result = detector.detect_hyaluron_pen_content(text)
        print(f"- '{text}': {result}")
    
    # Teste die Preiserkennung
    price_texts = [
        "Hyaluron Pen Behandlung ab 79€",
        "Lippen aufspritzen für nur 99,00 Euro",
        "Preis: € 129.90",
        "Hyaluron Pen Behandlung - 149 EUR"
    ]
    
    print("\nPreiserkennung:")
    for text in price_texts:
        prices = detector.extract_prices(text)
        print(f"- '{text}': {prices}")
    
    # Teste die Profilanalyse
    test_profile = {
        "profile_name": "beauty_studio_berlin",
        "profile_link": "https://instagram.com/beauty_studio_berlin",
        "description": "Beauty Studio in Berlin mit Hyaluron Pen Behandlungen. Lippen aufspritzen ohne Nadel ab 79€!",
        "post_text": "Heute wieder tolle Ergebnisse mit unserem Hyaluron Pen! Vorher-Nachher Bilder. #hyaluronpen #lippenaufspritzen",
        "email": "info@beauty-studio-berlin.de",
        "location": "Berlin"
    }
    
    print("\nProfilanalyse:")
    analysis = detector.analyze_profile(test_profile)
    print(json.dumps(analysis, indent=2))
