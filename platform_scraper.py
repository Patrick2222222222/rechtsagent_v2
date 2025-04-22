#!/usr/bin/env python3
# platform_scraper.py - Verbesserte Scraper für verschiedene Plattformen

import os
import json
import time
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
from urllib.parse import quote_plus

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("platform_scraper")

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

class BaseScraper:
    """Basis-Klasse für alle Plattform-Scraper"""
    
    def __init__(self, db_manager=None):
        """
        Initialisiert den Basis-Scraper
        
        Args:
            db_manager: Optional, ein DatabaseManager-Objekt für die Datenbankintegration
        """
        self.db_manager = db_manager
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]
        self.session = requests.Session()
        self.rotate_user_agent()
        
        # Proxy-Konfiguration (falls benötigt)
        self.proxies = self._load_proxies()
        if self.proxies:
            self.rotate_proxy()
    
    def _load_proxies(self):
        """Lädt Proxies aus einer Datei oder Umgebungsvariable"""
        proxy_list = os.getenv("PROXY_LIST")
        if proxy_list:
            return proxy_list.split(",")
        
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        
        return []
    
    def rotate_user_agent(self):
        """Wechselt den User-Agent zufällig"""
        user_agent = random.choice(self.user_agents)
        self.session.headers.update({"User-Agent": user_agent})
        logger.debug(f"User-Agent gewechselt zu: {user_agent}")
    
    def rotate_proxy(self):
        """Wechselt den Proxy zufällig"""
        if not self.proxies:
            return
        
        proxy = random.choice(self.proxies)
        self.session.proxies.update({
            "http": proxy,
            "https": proxy
        })
        logger.debug(f"Proxy gewechselt zu: {proxy}")
    
    def make_request(self, url, method="GET", params=None, data=None, headers=None, retry_count=3, retry_delay=2):
        """
        Führt eine HTTP-Anfrage mit Wiederholungsversuchen und Fehlerbehandlung durch
        
        Args:
            url: Die URL für die Anfrage
            method: HTTP-Methode (GET, POST, etc.)
            params: URL-Parameter
            data: POST-Daten
            headers: Zusätzliche Header
            retry_count: Anzahl der Wiederholungsversuche
            retry_delay: Verzögerung zwischen Wiederholungsversuchen in Sekunden
            
        Returns:
            Response-Objekt oder None bei Fehler
        """
        for attempt in range(retry_count):
            try:
                # Füge zufällige Verzögerung hinzu, um Anti-Scraping-Maßnahmen zu umgehen
                time.sleep(random.uniform(1.0, 3.0))
                
                # Führe die Anfrage durch
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=headers,
                    timeout=10
                )
                
                # Prüfe auf Erfolg
                response.raise_for_status()
                
                # Prüfe auf Anti-Bot-Maßnahmen
                if "captcha" in response.text.lower() or "robot" in response.text.lower():
                    logger.warning(f"Mögliche Anti-Bot-Maßnahme erkannt bei {url}")
                    self.rotate_user_agent()
                    self.rotate_proxy()
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                
                return response
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Fehler bei Anfrage an {url}: {e} (Versuch {attempt+1}/{retry_count})")
                self.rotate_user_agent()
                self.rotate_proxy()
                time.sleep(retry_delay * (attempt + 1))
        
        logger.error(f"Alle Versuche für {url} fehlgeschlagen")
        return None
    
    def log_search(self, platform, search_term, results_count, duration, is_successful=True, error_message=None):
        """Protokolliert einen Suchvorgang in der Datenbank"""
        if self.db_manager:
            self.db_manager.log_search(platform, search_term, results_count, duration, is_successful, error_message)
        else:
            logger.info(f"Suche nach '{search_term}' auf {platform}: {results_count} Ergebnisse in {duration:.2f}s")
    
    def save_profile(self, platform, profile_data):
        """Speichert ein Profil in der Datenbank"""
        if self.db_manager:
            return self.db_manager.add_profile(platform, profile_data)
        else:
            logger.info(f"Profil gefunden: {profile_data.get('profile_name')} auf {platform}")
            return None
    
    def save_post(self, profile_id, post_data):
        """Speichert einen Post in der Datenbank"""
        if self.db_manager and profile_id:
            return self.db_manager.add_post(profile_id, post_data)
        else:
            logger.info(f"Post gefunden: {post_data.get('post_text', '')[:50]}...")
            return None


class InstagramScraper(BaseScraper):
    """Scraper für Instagram"""
    
    def __init__(self, db_manager=None):
        super().__init__(db_manager)
        self.platform_name = "Instagram"
    
    def search_hashtag(self, hashtag):
        """
        Sucht nach einem Hashtag auf Instagram
        
        Args:
            hashtag: Der Hashtag (mit oder ohne #)
            
        Returns:
            Liste von gefundenen Profilen/Posts
        """
        # Entferne # falls vorhanden
        if hashtag.startswith("#"):
            hashtag = hashtag[1:]
        
        logger.info(f"Suche nach Hashtag #{hashtag} auf Instagram")
        start_time = time.time()
        
        url = f"https://www.instagram.com/explore/tags/{hashtag}/"
        response = self.make_request(url)
        
        results = []
        
        if response:
            try:
                # Extrahiere Daten aus der Antwort
                soup = BeautifulSoup(response.text, "html.parser")
                
                # In einer realen Implementierung würden wir hier die HTML-Struktur analysieren
                # und relevante Daten extrahieren. Da Instagram jedoch JavaScript-lastig ist,
                # würde man in der Praxis eher Selenium oder eine API verwenden.
                
                # Simuliere gefundene Ergebnisse für Entwicklungszwecke
                # In einer realen Implementierung würden diese Daten aus der Antwort extrahiert werden
                simulated_results = self._simulate_hashtag_results(hashtag)
                results.extend(simulated_results)
                
                # Speichere die Ergebnisse in der Datenbank
                for result in results:
                    profile = self.save_profile(self.platform_name, result)
                    if profile and "post_text" in result:
                        self.save_post(profile.id, {
                            "post_link": result.get("post_link"),
                            "post_text": result.get("post_text"),
                            "contains_hyaluron_pen": "hyaluron" in result.get("post_text", "").lower()
                        })
                
            except Exception as e:
                logger.error(f"Fehler beim Parsen der Instagram-Hashtag-Ergebnisse: {e}")
        
        duration = time.time() - start_time
        self.log_search(self.platform_name, f"#{hashtag}", len(results), duration)
        
        return results
    
    def search_profile(self, profile_name):
        """
        Sucht nach einem Profil auf Instagram
        
        Args:
            profile_name: Der Profilname (ohne @)
            
        Returns:
            Profildaten oder None
        """
        # Entferne @ falls vorhanden
        if profile_name.startswith("@"):
            profile_name = profile_name[1:]
        
        logger.info(f"Suche nach Profil @{profile_name} auf Instagram")
        start_time = time.time()
        
        url = f"https://www.instagram.com/{profile_name}/"
        response = self.make_request(url)
        
        result = None
        
        if response:
            try:
                # Extrahiere Daten aus der Antwort
                soup = BeautifulSoup(response.text, "html.parser")
                
                # In einer realen Implementierung würden wir hier die HTML-Struktur analysieren
                # und relevante Daten extrahieren. Da Instagram jedoch JavaScript-lastig ist,
                # würde man in der Praxis eher Selenium oder eine API verwenden.
                
                # Simuliere gefundene Ergebnisse für Entwicklungszwecke
                # In einer realen Implementierung würden diese Daten aus der Antwort extrahiert werden
                result = self._simulate_profile_result(profile_name)
                
                # Speichere das Ergebnis in der Datenbank
                if result:
                    self.save_profile(self.platform_name, result)
                
            except Exception as e:
                logger.error(f"Fehler beim Parsen des Instagram-Profils: {e}")
        
        duration = time.time() - start_time
        self.log_search(self.platform_name, f"@{profile_name}", 1 if result else 0, duration)
        
        return result
    
    def _simulate_hashtag_results(self, hashtag):
        """Simuliert Ergebnisse für einen Hashtag (nur für Entwicklungszwecke)"""
        # In einer realen Implementierung würde diese Methode nicht existieren
        # Hier simulieren wir Ergebnisse, um die Funktionalität zu demonstrieren
        
        results = []
        
        # Simuliere 3-5 Ergebnisse
        num_results = random.randint(3, 5)
        
        for i in range(num_results):
            profile_name = f"beauty_studio_{random.choice(['berlin', 'hamburg', 'muenchen', 'koeln'])}{random.randint(1, 999)}"
            
            result = {
                "platform": self.platform_name,
                "profile_name": profile_name,
                "profile_link": f"https://instagram.com/{profile_name}",
                "description": f"Beauty Studio mit Hyaluron Pen Behandlungen. #{hashtag} #beauty #kosmetik",
                "post_text": f"Tolle Ergebnisse mit unserem Hyaluron Pen! #{hashtag} #lippenaufspritzen #beauty",
                "post_link": f"https://instagram.com/p/{profile_name}_{int(time.time())}",
                "email": f"info@{profile_name.replace('_', '')}.de" if random.random() > 0.5 else None,
                "location": random.choice(["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart"])
            }
            
            results.append(result)
        
        return results
    
    def _simulate_profile_result(self, profile_name):
        """Simuliert ein Profilergebnis (nur für Entwicklungszwecke)"""
        # In einer realen Implementierung würde diese Methode nicht existieren
        # Hier simulieren wir ein Ergebnis, um die Funktionalität zu demonstrieren
        
        if "beauty" in profile_name or "kosmetik" in profile_name or "studio" in profile_name:
            return {
                "platform": self.platform_name,
                "profile_name": profile_name,
                "profile_link": f"https://instagram.com/{profile_name}",
                "description": "Beauty Studio mit Hyaluron Pen Behandlungen. #hyaluronpen #beauty #kosmetik",
                "email": f"info@{profile_name.replace('_', '')}.de" if random.random() > 0.5 else None,
                "location": random.choice(["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart"]),
                "follower_count": random.randint(500, 10000)
            }
        
        return None


class FacebookScraper(BaseScraper):
    """Scraper für Facebook"""
    
    def __init__(self, db_manager=None):
        super().__init__(db_manager)
        self.platform_name = "Facebook"
    
    def search_page(self, page_name):
        """
        Sucht nach einer Seite auf Facebook
        
        Args:
            page_name: Der Name der Seite
            
        Returns:
            Seitendaten oder None
        """
        logger.info(f"Suche nach Seite {page_name} auf Facebook")
        start_time = time.time()
        
        url = f"https://www.facebook.com/{page_name}/"
        response = self.make_request(url)
        
        result = None
        
        if response:
            try:
                # Extrahiere Daten aus der Antwort
                soup = BeautifulSoup(response.text, "html.parser")
                
                # In einer realen Implementierung würden wir hier die HTML-Struktur analysieren
                # und relevante Daten extrahieren. Da Facebook jedoch JavaScript-lastig ist,
                # würde man in der Praxis eher Selenium oder eine API verwenden.
                
                # Simuliere gefundene Ergebnisse für Entwicklungszwecke
                # In einer realen Implementierung würden diese Daten aus der Antwort extrahiert werden
                result = self._simulate_page_result(page_name)
                
                # Speichere das Ergebnis in der Datenbank
                if result:
                    self.save_profile(self.platform_name, result)
                
            except Exception as e:
                logger.error(f"Fehler beim Parsen der Facebook-Seite: {e}")
        
        duration = time.time() - start_time
        self.log_search(self.platform_name, page_name, 1 if result else 0, duration)
        
        return result
    
    def search_keyword(self, keyword):
        """
        Sucht nach einem Keyword auf Facebook
        
        Args:
            keyword: Das Suchbegriff
            
        Returns:
            Liste von gefundenen Seiten/Posts
        """
        logger.info(f"Suche nach Keyword '{keyword}' auf Facebook")
        start_time = time.time()
        
        url = f"https://www.facebook.com/search/top/?q={quote_plus(keyword)}"
        response = self.make_request(url)
        
        results = []
        
        if response:
            try:
                # Extrahiere Daten aus der Antwort
                soup = BeautifulSoup(response.text, "html.parser")
                
                # In einer realen Implementierung würden wir hier die HTML-Struktur analysieren
                # und relevante Daten extrahieren. Da Facebook jedoch JavaScript-lastig ist,
                # würde man in der Praxis eher Selenium oder eine API verwenden.
                
                # Simuliere gefundene Ergebnisse für Entwicklungszwecke
                # In einer realen Implementierung würden diese Daten aus der Antwort extrahiert werden
                simulated_results = self._simulate_keyword_results(keyword)
                results.extend(simulated_results)
                
                # Speichere die Ergebnisse in der Datenbank
                for result in results:
                    profile = self.save_profile(self.platform_name, result)
                    if profile and "post_text" in result:
                        self.save_post(profile.id, {
                            "post_link": result.get("post_link"),
                            "post_text": result.get("post_text"),
                            "contains_hyaluron_pen": "hyaluron" in result.get("post_text", "").lower()
                        })
                
            except Exception as e:
                logger.error(f"Fehler beim Parsen der Facebook-Suchergebnisse: {e}")
        
        duration = time.time() - start_time
        self.log_search(self.platform_name, keyword, len(results), duration)
        
        return results
    
    def _simulate_page_result(self, page_name):
        """Simuliert ein Seitenergebnis (nur für Entwicklungszwecke)"""
        # In einer realen Implementierung würde diese Methode nicht existieren
        # Hier simulieren wir ein Ergebnis, um die Funktionalität zu demonstrieren
        
        if "Beauty" in page_name or "Kosmetik" in page_name or "Studio" in page_name:
            return {
                "platform": self.platform_name,
                "profile_name": page_name,
                "profile_link": f"https://facebook.com/{page_name}",
                "description": "Beauty Studio mit Hyaluron Pen Behandlungen. Jetzt Termin vereinbaren!",
                "email": f"info@{page_name.lower().replace(' ', '')}.de" if random.random() > 0.5 else None,
                "location": random.choice(["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart"]),
                "follower_count": random.randint(100, 5000)
            }
        
        return None
    
    def _simulate_keyword_results(self, keyword):
        """Simuliert Ergebnisse für ein Keyword (nur für Entwicklungszwecke)"""
        # In einer realen Implementierung würde diese Methode nicht existieren
        # Hier simulieren wir Ergebnisse, um die Funktionalität zu demonstrieren
        
        results = []
        
        # Simuliere 2-4 Ergebnisse
        num_results = random.randint(2, 4)
        
        for i in range(num_results):
            page_name = f"Beauty Studio {random.choice(['Berlin', 'Hamburg', 'München', 'Köln'])}"
            
            result = {
                "platform": self.platform_name,
                "profile_name": page_name,
                "profile_link": f"https://facebook.com/{page_name.replace(' ', '')}",
                "description": f"Beauty Studio mit {keyword} Behandlungen. Jetzt Termin vereinbaren!",
                "post_text": f"Neue Angebote für {keyword} Behandlungen! Jetzt buchen und 20% sparen.",
                "post_link": f"https://facebook.com/{page_name.replace(' ', '')}/posts/{int(time.time())}",
                "email": f"info@{page_name.lower().replace(' ', '')}.de" if random.random() > 0.5 else None,
                "location": page_name.split()[-1]
            }
            
            results.append(result)
        
        return results


class TikTokScraper(BaseScraper):
    """Scraper für TikTok"""
    
    def __init__(self, db_manager=None):
        super().__init__(db_manager)
        self.platform_name = "TikTok"
    
    def search_hashtag(self, hashtag):
        """
        Sucht nach einem Hashtag auf TikTok
        
        Args:
            hashtag: Der Hashtag (mit oder ohne #)
            
        Returns:
            Liste von gefundenen Profilen/Posts
        """
        # Entferne # falls vorhanden
        if hashtag.startswith("#"):
            hashtag = hashtag[1:]
        
        logger.info(f"Suche nach Hashtag #{hashtag} auf TikTok")
        start_time = time.time()
        
        url = f"https://www.tiktok.com/tag/{hashtag}"
        response = self.make_request(url)
        
        results = []
        
        if response:
            try:
                # Extrahiere Daten aus der Antwort
                soup = BeautifulSoup(response.text, "html.parser")
                
                # In einer realen Implementierung würden wir hier die HTML-Struktur analysieren
                # und relevante Daten extrahieren. Da TikTok jedoch JavaScript-lastig ist,
                # würde man in der Praxis eher Selenium oder eine API verwenden.
                
                # Simuliere gefundene Ergebnisse für Entwicklungszwecke
                # In einer realen Implementierung würden diese Daten aus der Antwort extrahiert werden
                simulated_results = self._simulate_hashtag_results(hashtag)
                results.extend(simulated_results)
                
                # Speichere die Ergebnisse in der Datenbank
                for result in results:
                    profile = self.save_profile(self.platform_name, result)
                    if profile and "post_text" in result:
                        self.save_post(profile.id, {
                            "post_link": result.get("post_link"),
                            "post_text": result.get("post_text"),
                            "contains_hyaluron_pen": "hyaluron" in result.get("post_text", "").lower()
                        })
                
            except Exception as e:
                logger.error(f"Fehler beim Parsen der TikTok-Hashtag-Ergebnisse: {e}")
        
        duration = time.time() - start_time
        self.log_search(self.platform_name, f"#{hashtag}", len(results), duration)
        
        return results
    
    def search_profile(self, profile_name):
        """
        Sucht nach einem Profil auf TikTok
        
        Args:
            profile_name: Der Profilname (mit oder ohne @)
            
        Returns:
            Profildaten oder None
        """
        # Entferne @ falls vorhanden
        if profile_name.startswith("@"):
            profile_name = profile_name[1:]
        
        logger.info(f"Suche nach Profil @{profile_name} auf TikTok")
        start_time = time.time()
        
        url = f"https://www.tiktok.com/@{profile_name}"
        response = self.make_request(url)
        
        result = None
        
        if response:
            try:
                # Extrahiere Daten aus der Antwort
                soup = BeautifulSoup(response.text, "html.parser")
                
                # In einer realen Implementierung würden wir hier die HTML-Struktur analysieren
                # und relevante Daten extrahieren. Da TikTok jedoch JavaScript-lastig ist,
                # würde man in der Praxis eher Selenium oder eine API verwenden.
                
                # Simuliere gefundene Ergebnisse für Entwicklungszwecke
                # In einer realen Implementierung würden diese Daten aus der Antwort extrahiert werden
                result = self._simulate_profile_result(profile_name)
                
                # Speichere das Ergebnis in der Datenbank
                if result:
                    self.save_profile(self.platform_name, result)
                
            except Exception as e:
                logger.error(f"Fehler beim Parsen des TikTok-Profils: {e}")
        
        duration = time.time() - start_time
        self.log_search(self.platform_name, f"@{profile_name}", 1 if result else 0, duration)
        
        return result
    
    def _simulate_hashtag_results(self, hashtag):
        """Simuliert Ergebnisse für einen Hashtag (nur für Entwicklungszwecke)"""
        # In einer realen Implementierung würde diese Methode nicht existieren
        # Hier simulieren wir Ergebnisse, um die Funktionalität zu demonstrieren
        
        results = []
        
        # Simuliere 3-6 Ergebnisse
        num_results = random.randint(3, 6)
        
        for i in range(num_results):
            profile_name = f"beauty_trends_{random.choice(['berlin', 'hamburg', 'muenchen', 'koeln'])}{random.randint(1, 999)}"
            
            result = {
                "platform": self.platform_name,
                "profile_name": profile_name,
                "profile_link": f"https://tiktok.com/@{profile_name}",
                "description": f"Beauty Trends und Hyaluron Pen Behandlungen. #{hashtag} #beauty #kosmetik",
                "post_text": f"Vorher-Nachher mit unserem Hyaluron Pen! #{hashtag} #lippenaufspritzen #beauty",
                "post_link": f"https://tiktok.com/@{profile_name}/video/{int(time.time())}",
                "email": f"info@{profile_name.replace('_', '')}.de" if random.random() > 0.5 else None,
                "location": random.choice(["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart"])
            }
            
            results.append(result)
        
        return results
    
    def _simulate_profile_result(self, profile_name):
        """Simuliert ein Profilergebnis (nur für Entwicklungszwecke)"""
        # In einer realen Implementierung würde diese Methode nicht existieren
        # Hier simulieren wir ein Ergebnis, um die Funktionalität zu demonstrieren
        
        if "beauty" in profile_name or "kosmetik" in profile_name or "trends" in profile_name:
            return {
                "platform": self.platform_name,
                "profile_name": profile_name,
                "profile_link": f"https://tiktok.com/@{profile_name}",
                "description": "Beauty Trends und Hyaluron Pen Behandlungen. #hyaluronpen #beauty #kosmetik",
                "email": f"info@{profile_name.replace('_', '')}.de" if random.random() > 0.5 else None,
                "location": random.choice(["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart"]),
                "follower_count": random.randint(1000, 50000)
            }
        
        return None


class GoogleScraper(BaseScraper):
    """Scraper für Google"""
    
    def __init__(self, db_manager=None):
        super().__init__(db_manager)
        self.platform_name = "Google"
    
    def search_keyword(self, keyword):
        """
        Sucht nach einem Keyword auf Google
        
        Args:
            keyword: Das Suchbegriff
            
        Returns:
            Liste von gefundenen Websites
        """
        logger.info(f"Suche nach Keyword '{keyword}' auf Google")
        start_time = time.time()
        
        url = f"https://www.google.com/search?q={quote_plus(keyword)}"
        response = self.make_request(url)
        
        results = []
        
        if response:
            try:
                # Extrahiere Daten aus der Antwort
                soup = BeautifulSoup(response.text, "html.parser")
                
                # In einer realen Implementierung würden wir hier die HTML-Struktur analysieren
                # und relevante Daten extrahieren.
                
                # Simuliere gefundene Ergebnisse für Entwicklungszwecke
                # In einer realen Implementierung würden diese Daten aus der Antwort extrahiert werden
                simulated_results = self._simulate_search_results(keyword)
                results.extend(simulated_results)
                
                # Speichere die Ergebnisse in der Datenbank
                for result in results:
                    profile = self.save_profile("Website", result)
                    if profile:
                        self.save_post(profile.id, {
                            "post_link": result.get("profile_link"),
                            "post_text": result.get("description"),
                            "contains_hyaluron_pen": "hyaluron" in result.get("description", "").lower()
                        })
                
            except Exception as e:
                logger.error(f"Fehler beim Parsen der Google-Suchergebnisse: {e}")
        
        duration = time.time() - start_time
        self.log_search(self.platform_name, keyword, len(results), duration)
        
        return results
    
    def _simulate_search_results(self, keyword):
        """Simuliert Suchergebnisse (nur für Entwicklungszwecke)"""
        # In einer realen Implementierung würde diese Methode nicht existieren
        # Hier simulieren wir Ergebnisse, um die Funktionalität zu demonstrieren
        
        results = []
        
        # Simuliere 4-8 Ergebnisse
        num_results = random.randint(4, 8)
        
        for i in range(num_results):
            domain = f"kosmetik-{random.choice(['berlin', 'hamburg', 'muenchen', 'koeln'])}{random.randint(1, 99)}.de"
            
            result = {
                "platform": "Website",
                "profile_name": f"Kosmetikstudio {domain.split('.')[0].replace('kosmetik-', '').capitalize()}",
                "profile_link": f"https://{domain}",
                "description": f"{keyword} - Professionelle Behandlungen in unserem Studio. Hyaluron Pen ab 79€. Jetzt Termin vereinbaren!",
                "email": f"info@{domain}",
                "location": domain.split('-')[1].split('.')[0].capitalize() if '-' in domain else None
            }
            
            results.append(result)
        
        return results


class WebsiteScraper(BaseScraper):
    """Scraper für Websites"""
    
    def __init__(self, db_manager=None):
        super().__init__(db_manager)
        self.platform_name = "Website"
    
    def scrape_website(self, url):
        """
        Scrapt eine Website nach Informationen zu Hyaluron Pen Behandlungen
        
        Args:
            url: Die URL der Website
            
        Returns:
            Extrahierte Informationen oder None
        """
        logger.info(f"Scrape Website {url}")
        start_time = time.time()
        
        response = self.make_request(url)
        
        result = None
        
        if response:
            try:
                # Extrahiere Daten aus der Antwort
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Suche nach relevanten Informationen
                title = soup.title.text if soup.title else ""
                
                # Suche nach Kontaktinformationen
                email = None
                location = None
                
                # Suche nach E-Mail-Adressen
                email_links = soup.select("a[href^='mailto:']")
                if email_links:
                    email = email_links[0]['href'].replace('mailto:', '')
                
                # Suche nach Adresse/Ort
                address_elements = soup.find_all(string=lambda text: "straße" in text.lower() or "platz" in text.lower() or "weg" in text.lower())
                if address_elements:
                    location = address_elements[0].strip()
                
                # Suche nach Hyaluron Pen Inhalten
                hyaluron_elements = soup.find_all(string=lambda text: "hyaluron" in text.lower())
                contains_hyaluron = len(hyaluron_elements) > 0
                
                if contains_hyaluron:
                    # Extrahiere relevante Textabschnitte
                    relevant_text = []
                    for element in hyaluron_elements:
                        parent = element.parent
                        if parent:
                            relevant_text.append(parent.get_text().strip())
                    
                    # Erstelle ein Ergebnis
                    result = {
                        "platform": self.platform_name,
                        "profile_name": title,
                        "profile_link": url,
                        "description": "\n".join(relevant_text[:3]),  # Erste 3 relevante Textabschnitte
                        "email": email,
                        "location": location
                    }
                    
                    # Speichere das Ergebnis in der Datenbank
                    profile = self.save_profile(self.platform_name, result)
                    if profile:
                        self.save_post(profile.id, {
                            "post_link": url,
                            "post_text": "\n".join(relevant_text),
                            "contains_hyaluron_pen": True
                        })
                
            except Exception as e:
                logger.error(f"Fehler beim Scrapen der Website {url}: {e}")
        
        duration = time.time() - start_time
        self.log_search(self.platform_name, url, 1 if result else 0, duration)
        
        return result


class MultiPlatformScraper:
    """Klasse zur Koordination von Scraping-Operationen auf mehreren Plattformen"""
    
    def __init__(self, db_manager=None):
        """
        Initialisiert den MultiPlatformScraper
        
        Args:
            db_manager: Optional, ein DatabaseManager-Objekt für die Datenbankintegration
        """
        self.db_manager = db_manager
        
        # Initialisiere Scraper für verschiedene Plattformen
        self.instagram_scraper = InstagramScraper(db_manager)
        self.facebook_scraper = FacebookScraper(db_manager)
        self.tiktok_scraper = TikTokScraper(db_manager)
        self.google_scraper = GoogleScraper(db_manager)
        self.website_scraper = WebsiteScraper(db_manager)
    
    def run_search(self, search_terms=None, platforms=None):
        """
        Führt eine Suche auf allen oder bestimmten Plattformen durch
        
        Args:
            search_terms: Liste von Suchbegriffen oder None für Standardbegriffe
            platforms: Liste von Plattformen oder None für alle Plattformen
            
        Returns:
            Dictionary mit Ergebnissen pro Plattform
        """
        from expanded_search_terms import get_all_search_terms, get_search_terms_for_platform
        
        # Verwende Standardsuchbegriffe, wenn keine angegeben sind
        if not search_terms:
            all_terms = get_all_search_terms()
            search_terms = []
            for category in all_terms.values():
                search_terms.extend(category)
        
        # Verwende alle Plattformen, wenn keine angegeben sind
        if not platforms:
            platforms = ["Instagram", "Facebook", "TikTok", "Google", "Website"]
        
        results = {}
        
        # Führe Suche auf jeder Plattform durch
        for platform in platforms:
            platform_results = []
            
            # Wähle plattformspezifische Suchbegriffe
            platform_terms = get_search_terms_for_platform(platform.lower())
            if not platform_terms:
                platform_terms = search_terms
            
            # Begrenze die Anzahl der Suchbegriffe für Entwicklungszwecke
            # In einer Produktionsumgebung würde man alle Begriffe verwenden
            platform_terms = platform_terms[:5]
            
            logger.info(f"Starte Suche auf {platform} mit {len(platform_terms)} Suchbegriffen")
            
            if platform == "Instagram":
                # Suche nach Hashtags
                for term in [t for t in platform_terms if t.startswith("#")]:
                    results_for_term = self.instagram_scraper.search_hashtag(term)
                    platform_results.extend(results_for_term)
                
                # Suche nach Profilen
                for term in [t for t in platform_terms if not t.startswith("#")]:
                    result = self.instagram_scraper.search_profile(term)
                    if result:
                        platform_results.append(result)
            
            elif platform == "Facebook":
                # Suche nach Seiten
                for term in platform_terms:
                    if " " not in term and not term.startswith("#"):
                        result = self.facebook_scraper.search_page(term)
                        if result:
                            platform_results.append(result)
                
                # Suche nach Keywords
                for term in [t for t in platform_terms if " " in t]:
                    results_for_term = self.facebook_scraper.search_keyword(term)
                    platform_results.extend(results_for_term)
            
            elif platform == "TikTok":
                # Suche nach Hashtags
                for term in [t for t in platform_terms if t.startswith("#")]:
                    results_for_term = self.tiktok_scraper.search_hashtag(term)
                    platform_results.extend(results_for_term)
                
                # Suche nach Profilen
                for term in [t for t in platform_terms if t.startswith("@")]:
                    result = self.tiktok_scraper.search_profile(term)
                    if result:
                        platform_results.append(result)
            
            elif platform == "Google":
                # Suche nach Keywords
                for term in platform_terms:
                    if not term.startswith("#") and not term.startswith("@"):
                        results_for_term = self.google_scraper.search_keyword(term)
                        platform_results.extend(results_for_term)
            
            elif platform == "Website":
                # Scrape Websites
                # In einer realen Implementierung würden wir hier URLs aus den Google-Ergebnissen verwenden
                # Für Entwicklungszwecke verwenden wir einige Beispiel-URLs
                example_urls = [
                    "https://kosmetik-berlin.de",
                    "https://beauty-salon-hamburg.de",
                    "https://hyaluron-pen-muenchen.de"
                ]
                
                for url in example_urls:
                    result = self.website_scraper.scrape_website(url)
                    if result:
                        platform_results.append(result)
            
            results[platform] = platform_results
            logger.info(f"Suche auf {platform} abgeschlossen: {len(platform_results)} Ergebnisse gefunden")
        
        return results


if __name__ == "__main__":
    # Teste den MultiPlatformScraper
    from database_manager import DatabaseManager
    
    # Initialisiere Datenbankmanager
    db_manager = DatabaseManager("sqlite:///iri_legal_agent.db")
    
    # Initialisiere MultiPlatformScraper
    scraper = MultiPlatformScraper(db_manager)
    
    # Führe eine Testsuche durch
    results = scraper.run_search()
    
    # Gib Statistiken aus
    stats = db_manager.get_statistics()
    print("\nStatistiken nach der Suche:")
    print(json.dumps(stats, indent=2))
