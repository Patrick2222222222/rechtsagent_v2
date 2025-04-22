#!/usr/bin/env python3
# screenshot_service.py - Optimierter Screenshot-Dienst für IRI® Legal Agent

import os
import json
import time
import random
import logging
import requests
from datetime import datetime
from urllib.parse import urlparse, quote_plus
from dotenv import load_dotenv

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("screenshot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("screenshot_service")

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

class ScreenshotService:
    """Klasse zur Erstellung und Verwaltung von Screenshots"""
    
    def __init__(self, db_manager=None, api_key=None):
        """
        Initialisiert den ScreenshotService
        
        Args:
            db_manager: Optional, ein DatabaseManager-Objekt für die Datenbankintegration
            api_key: Optional, API-Schlüssel für den Screenshot-Dienst
        """
        self.db_manager = db_manager
        self.api_key = api_key or os.getenv("SCREENSHOT_API_KEY")
        self.screenshot_dir = os.path.abspath("screenshots")
        
        # Erstelle Screenshot-Verzeichnis, falls es nicht existiert
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        
        # Initialisiere Session für API-Anfragen
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
    
    def capture_screenshot(self, url, profile_id=None, post_id=None, full_page=True, width=1280, height=1024, delay=2):
        """
        Erstellt einen Screenshot einer URL
        
        Args:
            url: Die URL, von der ein Screenshot erstellt werden soll
            profile_id: Optional, ID des zugehörigen Profils
            post_id: Optional, ID des zugehörigen Posts
            full_page: Optional, ob die gesamte Seite erfasst werden soll
            width: Optional, Breite des Screenshots
            height: Optional, Höhe des Screenshots
            delay: Optional, Verzögerung vor dem Screenshot in Sekunden
            
        Returns:
            Pfad zum erstellten Screenshot oder None bei Fehler
        """
        logger.info(f"Erstelle Screenshot von {url}")
        
        try:
            # Generiere einen eindeutigen Dateinamen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
            domain = urlparse(url).netloc.replace(".", "_")
            filename = f"{domain}_{timestamp}_{random_suffix}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Verwende die Screenshot-API
            if self.api_key:
                screenshot_path = self._capture_with_api(url, filepath, full_page, width, height, delay)
            else:
                # Fallback: Simuliere Screenshot für Entwicklungszwecke
                screenshot_path = self._simulate_screenshot(url, filepath)
            
            if screenshot_path:
                logger.info(f"Screenshot erstellt: {screenshot_path}")
                
                # Speichere den Screenshot in der Datenbank
                if self.db_manager:
                    screenshot_data = {
                        "profile_id": profile_id,
                        "post_id": post_id,
                        "file_path": screenshot_path,
                        "url_captured": url,
                        "is_evidence": True,
                        "metadata": json.dumps({
                            "capture_date": datetime.now().isoformat(),
                            "full_page": full_page,
                            "width": width,
                            "height": height
                        })
                    }
                    
                    self.db_manager.add_screenshot(screenshot_data)
                
                return screenshot_path
            
            return None
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen des Screenshots von {url}: {e}")
            return None
    
    def _capture_with_api(self, url, filepath, full_page=True, width=1280, height=1024, delay=2):
        """
        Erstellt einen Screenshot mit der Screenshot-API
        
        Args:
            url: Die URL, von der ein Screenshot erstellt werden soll
            filepath: Pfad, unter dem der Screenshot gespeichert werden soll
            full_page: Optional, ob die gesamte Seite erfasst werden soll
            width: Optional, Breite des Screenshots
            height: Optional, Höhe des Screenshots
            delay: Optional, Verzögerung vor dem Screenshot in Sekunden
            
        Returns:
            Pfad zum erstellten Screenshot oder None bei Fehler
        """
        # Verwende die ScreenshotAPI.net API
        api_url = "https://api.screenshotapi.net/screenshot"
        
        params = {
            "token": self.api_key,
            "url": url,
            "output": "image",
            "width": width,
            "height": height,
            "full_page": "true" if full_page else "false",
            "delay": delay * 1000,  # Umrechnung in Millisekunden
            "fresh": "true",  # Immer einen frischen Screenshot erstellen
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            # Sende Anfrage an die API
            response = self.session.get(api_url, params=params, stream=True)
            response.raise_for_status()
            
            # Speichere den Screenshot
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filepath
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API-Fehler beim Erstellen des Screenshots: {e}")
            return None
    
    def _simulate_screenshot(self, url, filepath):
        """
        Simuliert einen Screenshot für Entwicklungszwecke
        
        Args:
            url: Die URL, von der ein Screenshot erstellt werden soll
            filepath: Pfad, unter dem der Screenshot gespeichert werden soll
            
        Returns:
            Pfad zum erstellten Screenshot oder None bei Fehler
        """
        try:
            # Erstelle eine leere Datei
            with open(filepath, 'w') as f:
                f.write(f"Simulierter Screenshot von {url} erstellt am {datetime.now().isoformat()}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Fehler beim Simulieren des Screenshots: {e}")
            return None
    
    def capture_multiple_screenshots(self, urls, profile_id=None, post_id=None):
        """
        Erstellt Screenshots von mehreren URLs
        
        Args:
            urls: Liste von URLs
            profile_id: Optional, ID des zugehörigen Profils
            post_id: Optional, ID des zugehörigen Posts
            
        Returns:
            Liste von Pfaden zu den erstellten Screenshots
        """
        screenshot_paths = []
        
        for url in urls:
            # Füge zufällige Verzögerung hinzu, um Anti-Scraping-Maßnahmen zu umgehen
            time.sleep(random.uniform(1.0, 3.0))
            
            screenshot_path = self.capture_screenshot(url, profile_id, post_id)
            if screenshot_path:
                screenshot_paths.append(screenshot_path)
        
        return screenshot_paths
    
    def capture_profile_screenshots(self, profile_data):
        """
        Erstellt Screenshots für ein Profil und seine Posts
        
        Args:
            profile_data: Dictionary mit Profildaten
            
        Returns:
            Dictionary mit Pfaden zu den erstellten Screenshots
        """
        screenshots = {
            "profile": None,
            "posts": []
        }
        
        # Speichere das Profil in der Datenbank, falls noch nicht geschehen
        profile = None
        if self.db_manager:
            profile = self.db_manager.add_profile(
                profile_data.get("platform", "Unknown"),
                profile_data
            )
        
        # Erstelle Screenshot des Profils
        if "profile_link" in profile_data and profile_data["profile_link"]:
            profile_screenshot = self.capture_screenshot(
                profile_data["profile_link"],
                profile_id=profile.id if profile else None
            )
            screenshots["profile"] = profile_screenshot
        
        # Erstelle Screenshots der Posts
        if "posts" in profile_data and profile_data["posts"]:
            for post_data in profile_data["posts"]:
                # Speichere den Post in der Datenbank, falls noch nicht geschehen
                post = None
                if self.db_manager and profile:
                    post = self.db_manager.add_post(profile.id, post_data)
                
                # Erstelle Screenshot des Posts
                if "post_link" in post_data and post_data["post_link"]:
                    post_screenshot = self.capture_screenshot(
                        post_data["post_link"],
                        profile_id=profile.id if profile else None,
                        post_id=post.id if post else None
                    )
                    screenshots["posts"].append(post_screenshot)
        
        return screenshots
    
    def capture_search_results(self, search_results):
        """
        Erstellt Screenshots für Suchergebnisse
        
        Args:
            search_results: Dictionary mit Suchergebnissen pro Plattform
            
        Returns:
            Dictionary mit Pfaden zu den erstellten Screenshots pro Plattform
        """
        screenshots = {}
        
        for platform, results in search_results.items():
            platform_screenshots = []
            
            for result in results:
                # Erstelle Screenshots für das Profil und seine Posts
                result_screenshots = self.capture_profile_screenshots(result)
                platform_screenshots.append(result_screenshots)
            
            screenshots[platform] = platform_screenshots
        
        return screenshots


class AdvancedScreenshotService(ScreenshotService):
    """Erweiterte Klasse zur Erstellung und Verwaltung von Screenshots mit zusätzlichen Funktionen"""
    
    def __init__(self, db_manager=None, api_key=None, detection_manager=None):
        """
        Initialisiert den AdvancedScreenshotService
        
        Args:
            db_manager: Optional, ein DatabaseManager-Objekt für die Datenbankintegration
            api_key: Optional, API-Schlüssel für den Screenshot-Dienst
            detection_manager: Optional, ein DetectionManager-Objekt für die Analyse von Screenshots
        """
        super().__init__(db_manager, api_key)
        self.detection_manager = detection_manager
    
    def capture_and_analyze_screenshot(self, url, profile_id=None, post_id=None):
        """
        Erstellt einen Screenshot und analysiert ihn
        
        Args:
            url: Die URL, von der ein Screenshot erstellt werden soll
            profile_id: Optional, ID des zugehörigen Profils
            post_id: Optional, ID des zugehörigen Posts
            
        Returns:
            Dictionary mit Pfad zum Screenshot und Analyseergebnissen
        """
        # Erstelle Screenshot
        screenshot_path = self.capture_screenshot(url, profile_id, post_id)
        
        if not screenshot_path:
            return None
        
        # Analysiere Screenshot, falls ein DetectionManager verfügbar ist
        analysis = None
        if self.detection_manager:
            analysis = self.detection_manager.analyze_image_file(screenshot_path, profile_id, post_id)
        
        return {
            "screenshot_path": screenshot_path,
            "analysis": analysis
        }
    
    def capture_screenshots_for_suspicious_profiles(self, suspicious_profiles):
        """
        Erstellt Screenshots für verdächtige Profile
        
        Args:
            suspicious_profiles: Liste von verdächtigen Profilen
            
        Returns:
            Dictionary mit Pfaden zu den erstellten Screenshots pro Profil
        """
        screenshots = {}
        
        for profile in suspicious_profiles:
            profile_name = profile.get("profile_name", "unknown")
            logger.info(f"Erstelle Screenshots für verdächtiges Profil: {profile_name}")
            
            # Speichere das Profil in der Datenbank, falls noch nicht geschehen
            db_profile = None
            if self.db_manager:
                db_profile = self.db_manager.add_profile(
                    profile.get("platform", "Unknown"),
                    profile
                )
            
            profile_screenshots = {
                "profile": None,
                "posts": []
            }
            
            # Erstelle Screenshot des Profils
            if "profile_link" in profile and profile["profile_link"]:
                profile_screenshot = self.capture_and_analyze_screenshot(
                    profile["profile_link"],
                    profile_id=db_profile.id if db_profile else None
                )
                profile_screenshots["profile"] = profile_screenshot
            
            # Erstelle Screenshots der Posts
            if "post_link" in profile and profile["post_link"]:
                # Speichere den Post in der Datenbank, falls noch nicht geschehen
                post = None
                if self.db_manager and db_profile:
                    post_data = {
                        "post_link": profile["post_link"],
                        "post_text": profile.get("post_text", "")
                    }
                    post = self.db_manager.add_post(db_profile.id, post_data)
                
                # Erstelle Screenshot des Posts
                post_screenshot = self.capture_and_analyze_screenshot(
                    profile["post_link"],
                    profile_id=db_profile.id if db_profile else None,
                    post_id=post.id if post else None
                )
                profile_screenshots["posts"].append(post_screenshot)
            
            screenshots[profile_name] = profile_screenshots
        
        return screenshots
    
    def capture_screenshots_with_selenium(self, url, profile_id=None, post_id=None, scroll=True, wait_time=5):
        """
        Erstellt einen Screenshot mit Selenium für dynamische Webseiten
        
        Args:
            url: Die URL, von der ein Screenshot erstellt werden soll
            profile_id: Optional, ID des zugehörigen Profils
            post_id: Optional, ID des zugehörigen Posts
            scroll: Optional, ob die Seite gescrollt werden soll
            wait_time: Optional, Wartezeit in Sekunden
            
        Returns:
            Pfad zum erstellten Screenshot oder None bei Fehler
        """
        try:
            # In einer realen Implementierung würden wir hier Selenium verwenden
            # Für Entwicklungszwecke simulieren wir den Screenshot
            
            # Generiere einen eindeutigen Dateinamen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
            domain = urlparse(url).netloc.replace(".", "_")
            filename = f"{domain}_selenium_{timestamp}_{random_suffix}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Simuliere Screenshot
            with open(filepath, 'w') as f:
                f.write(f"Simulierter Selenium-Screenshot von {url} erstellt am {datetime.now().isoformat()}")
            
            # Speichere den Screenshot in der Datenbank
            if self.db_manager:
                screenshot_data = {
                    "profile_id": profile_id,
                    "post_id": post_id,
                    "file_path": filepath,
                    "url_captured": url,
                    "is_evidence": True,
                    "metadata": json.dumps({
                        "capture_date": datetime.now().isoformat(),
                        "method": "selenium",
                        "scroll": scroll,
                        "wait_time": wait_time
                    })
                }
                
                self.db_manager.add_screenshot(screenshot_data)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen des Selenium-Screenshots von {url}: {e}")
            return None
    
    def capture_multiple_screenshots_with_variations(self, url, profile_id=None, post_id=None):
        """
        Erstellt mehrere Screenshots mit verschiedenen Einstellungen
        
        Args:
            url: Die URL, von der Screenshots erstellt werden sollen
            profile_id: Optional, ID des zugehörigen Profils
            post_id: Optional, ID des zugehörigen Posts
            
        Returns:
            Liste von Pfaden zu den erstellten Screenshots
        """
        screenshot_paths = []
        
        # Standard-Screenshot
        standard_screenshot = self.capture_screenshot(url, profile_id, post_id)
        if standard_screenshot:
            screenshot_paths.append(standard_screenshot)
        
        # Screenshot mit Selenium (für dynamische Inhalte)
        selenium_screenshot = self.capture_screenshots_with_selenium(url, profile_id, post_id)
        if selenium_screenshot:
            screenshot_paths.append(selenium_screenshot)
        
        # Screenshot mit mobiler Ansicht
        mobile_screenshot = self.capture_screenshot(
            url, profile_id, post_id,
            width=375, height=812  # iPhone X Abmessungen
        )
        if mobile_screenshot:
            screenshot_paths.append(mobile_screenshot)
        
        return screenshot_paths


if __name__ == "__main__":
    # Teste den ScreenshotService
    from database_manager import DatabaseManager
    from detection_algorithms import DetectionManager
    
    # Initialisiere Datenbankmanager
    db_manager = DatabaseManager("sqlite:///iri_legal_agent.db")
    
    # Initialisiere DetectionManager
    detection_manager = DetectionManager(db_manager)
    
    # Initialisiere AdvancedScreenshotService
    screenshot_service = AdvancedScreenshotService(db_manager, detection_manager=detection_manager)
    
    # Teste Screenshot-Erstellung
    test_url = "https://example.com"
    screenshot_path = screenshot_service.capture_screenshot(test_url)
    
    if screenshot_path:
        print(f"Screenshot erstellt: {screenshot_path}")
    
    # Teste Screenshot-Erstellung mit Analyse
    result = screenshot_service.capture_and_analyze_screenshot(test_url)
    
    if result:
        print(f"Screenshot mit Analyse erstellt: {result['screenshot_path']}")
        if result["analysis"]:
            print(f"Analyse-Ergebnis: {result['analysis']}")
    
    # Teste Screenshot-Erstellung mit Variationen
    variation_paths = screenshot_service.capture_multiple_screenshots_with_variations(test_url)
    
    if variation_paths:
        print(f"Screenshots mit Variationen erstellt: {len(variation_paths)} Screenshots")
        for path in variation_paths:
            print(f"- {path}")
