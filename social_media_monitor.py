#!/usr/bin/env python3
# social_media_monitor.py - Hauptskript für die Überwachung sozialer Medien

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Konfiguration
SEARCH_TERMS = [
    "#hyaluronpen", 
    "#lippenaufspritzen", 
    "#needlefreefiller", 
    "#faltenaufspritzen", 
    "Hyaluron Pen Behandlung"
]

class SocialMediaMonitor:
    def __init__(self):
        self.results = []
        self.screenshot_api_key = os.getenv("SCREENSHOT_API_KEY")
        self.monday_api_key = os.getenv("MONDAY_API_KEY")
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        
        # Prüfe, ob API-Schlüssel vorhanden sind
        if not self.screenshot_api_key or self.screenshot_api_key == "DEIN_SCREENSHOTAPI_KEY":
            print("Warnung: ScreenshotAPI-Schlüssel nicht konfiguriert")
        
        if not self.monday_api_key or self.monday_api_key == "DEIN_MONDAY_KEY":
            print("Warnung: Monday.com-API-Schlüssel nicht konfiguriert")
    
    def search_instagram(self, search_term):
        """
        Sucht auf Instagram nach dem angegebenen Suchbegriff
        """
        print(f"Suche auf Instagram nach: {search_term}")
        # Hier würde die tatsächliche Instagram-API-Integration erfolgen
        # Da Instagram API-Zugriff eingeschränkt ist, verwenden wir einen simulierten Ansatz
        
        # Simulierte Ergebnisse für Entwicklungszwecke
        results = []
        if search_term == "#hyaluronpen":
            results = [
                {
                    "platform": "Instagram",
                    "profile_name": "beauty_studio_berlin",
                    "profile_link": "https://instagram.com/beauty_studio_berlin",
                    "description": "Spezialist für Lippenaufspritzung mit Hyaluron Pen - Schmerzfrei und effektiv!",
                    "post_text": "Heute wieder tolle Ergebnisse mit unserem Hyaluron Pen! #hyaluronpen #lippenaufspritzen",
                    "post_link": "https://instagram.com/p/example123",
                    "email": "beauty@example.com",
                    "location": "Berlin"
                }
            ]
        
        print(f"Gefunden: {len(results)} Ergebnisse auf Instagram")
        return results
    
    def search_tiktok(self, search_term):
        """
        Sucht auf TikTok nach dem angegebenen Suchbegriff
        """
        print(f"Suche auf TikTok nach: {search_term}")
        # Hier würde die tatsächliche TikTok-API-Integration erfolgen
        # Da TikTok API-Zugriff eingeschränkt ist, verwenden wir einen simulierten Ansatz
        
        # Simulierte Ergebnisse für Entwicklungszwecke
        results = []
        if search_term == "#lippenaufspritzen":
            results = [
                {
                    "platform": "TikTok",
                    "profile_name": "beauty_trends_hamburg",
                    "profile_link": "https://tiktok.com/@beauty_trends_hamburg",
                    "description": "Beauty-Salon in Hamburg - Hyaluron Pen Behandlungen ab 79€",
                    "post_text": "Vorher-Nachher Ergebnis unserer Hyaluron Pen Behandlung #lippenaufspritzen #hyaluronpen",
                    "post_link": "https://tiktok.com/@beauty_trends_hamburg/video/example456",
                    "email": "info@beauty-trends.de",
                    "location": "Hamburg"
                }
            ]
        
        print(f"Gefunden: {len(results)} Ergebnisse auf TikTok")
        return results
    
    def search_google(self, search_term):
        """
        Sucht auf Google nach dem angegebenen Suchbegriff
        """
        print(f"Suche auf Google nach: {search_term}")
        # Hier würde die tatsächliche Google-Suche erfolgen
        # Für Entwicklungszwecke verwenden wir simulierte Ergebnisse
        
        # Simulierte Ergebnisse für Entwicklungszwecke
        results = []
        if search_term == "Hyaluron Pen Behandlung":
            results = [
                {
                    "platform": "Website",
                    "profile_name": "Kosmetikstudio Schönheit",
                    "profile_link": "https://kosmetik-schoenheit.de",
                    "description": "Kosmetikstudio in München - Hyaluron Pen Behandlungen ohne Nadel",
                    "post_text": "Wir bieten Lippenaufspritzung mit dem Hyaluron Pen an. Ohne Nadel, ohne Schmerzen!",
                    "post_link": "https://kosmetik-schoenheit.de/hyaluron-pen",
                    "email": "kontakt@kosmetik-schoenheit.de",
                    "location": "München"
                }
            ]
        
        print(f"Gefunden: {len(results)} Ergebnisse auf Google")
        return results
    
    def take_screenshot(self, url):
        """
        Erstellt einen Screenshot der angegebenen URL mit ScreenshotAPI.net
        """
        if not self.screenshot_api_key or self.screenshot_api_key == "DEIN_SCREENSHOTAPI_KEY":
            print("Fehler: ScreenshotAPI-Schlüssel nicht konfiguriert")
            return None
        
        print(f"Erstelle Screenshot von: {url}")
        
        # API-Aufruf an ScreenshotAPI.net
        api_url = "https://api.screenshotapi.net/screenshot"
        params = {
            "token": self.screenshot_api_key,
            "url": url,
            "output": "json",
            "width": 1280,
            "height": 800,
            "full_page": True
        }
        
        try:
            # Simulierter API-Aufruf für Entwicklungszwecke
            # response = requests.get(api_url, params=params)
            # response.raise_for_status()
            # data = response.json()
            
            # Simulierte Antwort
            timestamp = int(time.time())
            screenshot_filename = f"screenshots/screenshot_{timestamp}.png"
            
            # In einer realen Implementierung würden wir das Bild herunterladen
            # with open(screenshot_filename, "wb") as f:
            #     image_data = requests.get(data["screenshot"]).content
            #     f.write(image_data)
            
            print(f"Screenshot gespeichert als: {screenshot_filename}")
            return screenshot_filename
            
        except Exception as e:
            print(f"Fehler beim Erstellen des Screenshots: {e}")
            return None
    
    def run_search(self):
        """
        Führt die Suche auf allen Plattformen mit allen Suchbegriffen durch
        """
        all_results = []
        
        for term in SEARCH_TERMS:
            # Instagram-Suche
            instagram_results = self.search_instagram(term)
            all_results.extend(instagram_results)
            
            # TikTok-Suche
            tiktok_results = self.search_tiktok(term)
            all_results.extend(tiktok_results)
            
            # Google-Suche
            google_results = self.search_google(term)
            all_results.extend(google_results)
        
        # Speichere die Ergebnisse
        self.results = all_results
        
        # Speichere die Ergebnisse in einer JSON-Datei
        with open("search_results.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)
        
        print(f"Insgesamt {len(all_results)} Ergebnisse gefunden und in search_results.json gespeichert")
        return all_results
    
    def process_results(self):
        """
        Verarbeitet die gefundenen Ergebnisse (Screenshots erstellen)
        """
        if not self.results:
            print("Keine Ergebnisse zum Verarbeiten")
            return
        
        processed_results = []
        
        for result in self.results:
            print(f"Verarbeite Ergebnis: {result['profile_name']} auf {result['platform']}")
            
            # Erstelle Screenshot der Profilseite
            screenshot_path = self.take_screenshot(result['profile_link'])
            
            # Füge Screenshot-Pfad zum Ergebnis hinzu
            result['screenshot_path'] = screenshot_path
            result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            processed_results.append(result)
        
        # Speichere die verarbeiteten Ergebnisse
        with open("processed_results.json", "w", encoding="utf-8") as f:
            json.dump(processed_results, f, ensure_ascii=False, indent=4)
        
        print(f"Verarbeitung abgeschlossen. {len(processed_results)} Ergebnisse mit Screenshots gespeichert.")
        return processed_results

if __name__ == "__main__":
    print("IRI® Legal Agent - Social Media Monitor")
    print("---------------------------------------")
    
    monitor = SocialMediaMonitor()
    results = monitor.run_search()
    processed = monitor.process_results()
    
    print("Monitoring abgeschlossen.")
