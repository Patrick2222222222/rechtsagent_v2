#!/usr/bin/env python3
# integrated_scraper.py - Integrierter Scraper mit Datenbankanbindung für IRI® Legal Agent

import os
import json
import time
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Importiere eigene Module
from database_manager import DatabaseManager
from platform_scraper import MultiPlatformScraper
from detection_algorithms import DetectionManager
from screenshot_service import AdvancedScreenshotService
from expanded_search_terms import get_all_search_terms

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("integrated_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("integrated_scraper")

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

class IntegratedScraper:
    """Integrierter Scraper mit Datenbankanbindung für IRI® Legal Agent"""
    
    def __init__(self, db_url=None, screenshot_api_key=None):
        """
        Initialisiert den IntegratedScraper
        
        Args:
            db_url: Optional, URL für die Datenbankverbindung
            screenshot_api_key: Optional, API-Schlüssel für den Screenshot-Dienst
        """
        # Verwende die angegebene URL oder die aus der Umgebungsvariable oder den Standard
        self.db_url = db_url or os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/iri_legal_agent"
        self.screenshot_api_key = screenshot_api_key or os.getenv("SCREENSHOT_API_KEY")
        
        # Initialisiere Datenbankmanager
        logger.info(f"Initialisiere Datenbankverbindung zu {self.db_url}")
        self.db_manager = DatabaseManager(self.db_url)
        
        # Initialisiere Standarddaten in der Datenbank
        self.db_manager.init_default_data()
        
        # Initialisiere DetectionManager
        logger.info("Initialisiere DetectionManager")
        self.detection_manager = DetectionManager(self.db_manager)
        
        # Initialisiere ScreenshotService
        logger.info("Initialisiere ScreenshotService")
        self.screenshot_service = AdvancedScreenshotService(
            self.db_manager,
            api_key=self.screenshot_api_key,
            detection_manager=self.detection_manager
        )
        
        # Initialisiere MultiPlatformScraper
        logger.info("Initialisiere MultiPlatformScraper")
        self.platform_scraper = MultiPlatformScraper(self.db_manager)
    
    def run_full_scraping(self, platforms=None, max_terms_per_platform=10):
        """
        Führt einen vollständigen Scraping-Durchlauf durch
        
        Args:
            platforms: Optional, Liste von Plattformen, die gescrapt werden sollen
            max_terms_per_platform: Optional, maximale Anzahl von Suchbegriffen pro Plattform
            
        Returns:
            Dictionary mit Ergebnissen
        """
        logger.info("Starte vollständigen Scraping-Durchlauf")
        start_time = time.time()
        
        # Verwende alle Plattformen, wenn keine angegeben sind
        if not platforms:
            platforms = ["Instagram", "Facebook", "TikTok", "Google", "Website"]
        
        # Hole alle Suchbegriffe
        all_terms = get_all_search_terms()
        
        # Führe Scraping durch
        logger.info(f"Starte Scraping auf Plattformen: {', '.join(platforms)}")
        results = self.platform_scraper.run_search(platforms=platforms)
        
        # Analysiere die Ergebnisse
        logger.info("Analysiere Scraping-Ergebnisse")
        suspicious_profiles = self.detection_manager.analyze_scraping_results(results)
        
        # Erstelle Screenshots für verdächtige Profile
        if suspicious_profiles:
            logger.info(f"Erstelle Screenshots für {len(suspicious_profiles)} verdächtige Profile")
            screenshots = self.screenshot_service.capture_screenshots_for_suspicious_profiles(suspicious_profiles)
        else:
            logger.info("Keine verdächtigen Profile gefunden")
            screenshots = {}
        
        # Berechne Statistiken
        duration = time.time() - start_time
        stats = self.db_manager.get_statistics()
        
        # Erstelle Ergebnisbericht
        report = {
            "start_time": datetime.fromtimestamp(start_time).isoformat(),
            "end_time": datetime.fromtimestamp(time.time()).isoformat(),
            "duration_seconds": duration,
            "platforms_scraped": platforms,
            "total_profiles_found": sum(len(platform_results) for platform_results in results.values()),
            "suspicious_profiles_found": len(suspicious_profiles),
            "screenshots_created": sum(1 for profile_screenshots in screenshots.values() 
                                     for screenshot_type, screenshot in profile_screenshots.items() 
                                     if screenshot is not None),
            "database_statistics": stats
        }
        
        logger.info(f"Scraping-Durchlauf abgeschlossen in {duration:.2f} Sekunden")
        logger.info(f"Gefundene Profile: {report['total_profiles_found']}")
        logger.info(f"Verdächtige Profile: {report['suspicious_profiles_found']}")
        
        return {
            "results": results,
            "suspicious_profiles": suspicious_profiles,
            "screenshots": screenshots,
            "report": report
        }
    
    def run_targeted_scraping(self, search_terms, platforms=None):
        """
        Führt gezieltes Scraping mit bestimmten Suchbegriffen durch
        
        Args:
            search_terms: Liste von Suchbegriffen
            platforms: Optional, Liste von Plattformen, die gescrapt werden sollen
            
        Returns:
            Dictionary mit Ergebnissen
        """
        logger.info(f"Starte gezieltes Scraping mit {len(search_terms)} Suchbegriffen")
        start_time = time.time()
        
        # Verwende alle Plattformen, wenn keine angegeben sind
        if not platforms:
            platforms = ["Instagram", "Facebook", "TikTok", "Google", "Website"]
        
        # Führe Scraping durch
        logger.info(f"Starte Scraping auf Plattformen: {', '.join(platforms)}")
        results = self.platform_scraper.run_search(search_terms=search_terms, platforms=platforms)
        
        # Analysiere die Ergebnisse
        logger.info("Analysiere Scraping-Ergebnisse")
        suspicious_profiles = self.detection_manager.analyze_scraping_results(results)
        
        # Erstelle Screenshots für verdächtige Profile
        if suspicious_profiles:
            logger.info(f"Erstelle Screenshots für {len(suspicious_profiles)} verdächtige Profile")
            screenshots = self.screenshot_service.capture_screenshots_for_suspicious_profiles(suspicious_profiles)
        else:
            logger.info("Keine verdächtigen Profile gefunden")
            screenshots = {}
        
        # Berechne Statistiken
        duration = time.time() - start_time
        stats = self.db_manager.get_statistics()
        
        # Erstelle Ergebnisbericht
        report = {
            "start_time": datetime.fromtimestamp(start_time).isoformat(),
            "end_time": datetime.fromtimestamp(time.time()).isoformat(),
            "duration_seconds": duration,
            "search_terms_used": search_terms,
            "platforms_scraped": platforms,
            "total_profiles_found": sum(len(platform_results) for platform_results in results.values()),
            "suspicious_profiles_found": len(suspicious_profiles),
            "screenshots_created": sum(1 for profile_screenshots in screenshots.values() 
                                     for screenshot_type, screenshot in profile_screenshots.items() 
                                     if screenshot is not None),
            "database_statistics": stats
        }
        
        logger.info(f"Gezieltes Scraping abgeschlossen in {duration:.2f} Sekunden")
        logger.info(f"Gefundene Profile: {report['total_profiles_found']}")
        logger.info(f"Verdächtige Profile: {report['suspicious_profiles_found']}")
        
        return {
            "results": results,
            "suspicious_profiles": suspicious_profiles,
            "screenshots": screenshots,
            "report": report
        }
    
    def run_profile_scraping(self, profile_links, platforms=None):
        """
        Führt Scraping für bestimmte Profile durch
        
        Args:
            profile_links: Liste von Profil-Links
            platforms: Optional, Liste von Plattformen, die gescrapt werden sollen
            
        Returns:
            Dictionary mit Ergebnissen
        """
        logger.info(f"Starte Profil-Scraping für {len(profile_links)} Profile")
        start_time = time.time()
        
        results = {}
        suspicious_profiles = []
        screenshots = {}
        
        # Verarbeite jedes Profil
        for link in profile_links:
            # Bestimme die Plattform anhand der URL
            platform = "Unknown"
            if "instagram.com" in link:
                platform = "Instagram"
            elif "facebook.com" in link:
                platform = "Facebook"
            elif "tiktok.com" in link:
                platform = "TikTok"
            
            # Überspringe, wenn die Plattform nicht in der Liste ist
            if platforms and platform not in platforms:
                continue
            
            # Extrahiere den Profilnamen aus dem Link
            profile_name = link.split("/")[-1]
            if not profile_name:
                profile_name = link.split("/")[-2]
            
            logger.info(f"Scrape Profil: {profile_name} auf {platform}")
            
            # Führe plattformspezifisches Scraping durch
            profile_data = None
            
            if platform == "Instagram":
                profile_data = self.platform_scraper.instagram_scraper.search_profile(profile_name)
            elif platform == "Facebook":
                profile_data = self.platform_scraper.facebook_scraper.search_page(profile_name)
            elif platform == "TikTok":
                profile_data = self.platform_scraper.tiktok_scraper.search_profile(profile_name)
            else:
                # Für unbekannte Plattformen verwende den Website-Scraper
                profile_data = self.platform_scraper.website_scraper.scrape_website(link)
            
            # Füge das Profil zu den Ergebnissen hinzu
            if profile_data:
                if platform not in results:
                    results[platform] = []
                results[platform].append(profile_data)
                
                # Analysiere das Profil
                analysis = self.detection_manager.hyaluron_detector.analyze_profile(profile_data)
                profile_data["analysis"] = analysis
                
                # Prüfe, ob das Profil verdächtig ist
                if analysis["risk_score"] >= 50.0:
                    suspicious_profiles.append(profile_data)
                    
                    # Erstelle Screenshots
                    profile_screenshots = self.screenshot_service.capture_profile_screenshots(profile_data)
                    screenshots[profile_name] = profile_screenshots
        
        # Berechne Statistiken
        duration = time.time() - start_time
        stats = self.db_manager.get_statistics()
        
        # Erstelle Ergebnisbericht
        report = {
            "start_time": datetime.fromtimestamp(start_time).isoformat(),
            "end_time": datetime.fromtimestamp(time.time()).isoformat(),
            "duration_seconds": duration,
            "profile_links_used": profile_links,
            "platforms_scraped": list(results.keys()),
            "total_profiles_found": sum(len(platform_results) for platform_results in results.values()),
            "suspicious_profiles_found": len(suspicious_profiles),
            "screenshots_created": sum(1 for profile_screenshots in screenshots.values() 
                                     for screenshot_type, screenshot in profile_screenshots.items() 
                                     if screenshot is not None),
            "database_statistics": stats
        }
        
        logger.info(f"Profil-Scraping abgeschlossen in {duration:.2f} Sekunden")
        logger.info(f"Gefundene Profile: {report['total_profiles_found']}")
        logger.info(f"Verdächtige Profile: {report['suspicious_profiles_found']}")
        
        return {
            "results": results,
            "suspicious_profiles": suspicious_profiles,
            "screenshots": screenshots,
            "report": report
        }
    
    def export_results_to_json(self, results, filename="scraping_results.json"):
        """
        Exportiert Scraping-Ergebnisse als JSON-Datei
        
        Args:
            results: Dictionary mit Scraping-Ergebnissen
            filename: Optional, Name der Ausgabedatei
            
        Returns:
            Pfad zur erstellten JSON-Datei
        """
        try:
            # Erstelle ein serialisierbares Dictionary
            serializable_results = {
                "report": results["report"],
                "total_profiles": sum(len(platform_results) for platform_results in results["results"].values()),
                "suspicious_profiles": len(results["suspicious_profiles"]),
                "platforms": list(results["results"].keys()),
                "screenshot_count": sum(1 for profile_screenshots in results["screenshots"].values() 
                                      for screenshot_type, screenshot in profile_screenshots.items() 
                                      if screenshot is not None)
            }
            
            # Füge Details zu verdächtigen Profilen hinzu
            serializable_results["suspicious_profile_details"] = []
            for profile in results["suspicious_profiles"]:
                profile_copy = profile.copy()
                
                # Entferne nicht serialisierbare Objekte
                if "analysis" in profile_copy and isinstance(profile_copy["analysis"], dict):
                    # Konvertiere datetime-Objekte zu Strings
                    if "analysis_date" in profile_copy["analysis"] and not isinstance(profile_copy["analysis"]["analysis_date"], str):
                        profile_copy["analysis"]["analysis_date"] = profile_copy["analysis"]["analysis_date"].isoformat()
                
                serializable_results["suspicious_profile_details"].append(profile_copy)
            
            # Speichere als JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Ergebnisse exportiert nach {filename}")
            return os.path.abspath(filename)
            
        except Exception as e:
            logger.error(f"Fehler beim Exportieren der Ergebnisse: {e}")
            return None
    
    def generate_report(self, results, filename="scraping_report.txt"):
        """
        Generiert einen menschenlesbaren Bericht der Scraping-Ergebnisse
        
        Args:
            results: Dictionary mit Scraping-Ergebnissen
            filename: Optional, Name der Ausgabedatei
            
        Returns:
            Pfad zur erstellten Berichtsdatei
        """
        try:
            report = results["report"]
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== IRI® Legal Agent - Scraping-Bericht ===\n\n")
                
                f.write(f"Startzeit: {report['start_time']}\n")
                f.write(f"Endzeit: {report['end_time']}\n")
                f.write(f"Dauer: {report['duration_seconds']:.2f} Sekunden\n\n")
                
                f.write(f"Gescrapte Plattformen: {', '.join(report['platforms_scraped'])}\n")
                f.write(f"Gefundene Profile: {report['total_profiles_found']}\n")
                f.write(f"Verdächtige Profile: {report['suspicious_profiles_found']}\n")
                f.write(f"Erstellte Screenshots: {report['screenshots_created']}\n\n")
                
                f.write("=== Datenbankstatistiken ===\n\n")
                stats = report['database_statistics']
                f.write(f"Gesamt-Profile: {stats.get('total_profiles', 0)}\n")
                f.write(f"Gesamt-Posts: {stats.get('total_posts', 0)}\n")
                f.write(f"Gesamt-Screenshots: {stats.get('total_screenshots', 0)}\n")
                f.write(f"Gesamt-Suchen: {stats.get('total_searches', 0)}\n")
                f.write(f"Erfolgreiche Suchen: {stats.get('successful_searches', 0)}\n")
                f.write(f"Gemeldete Profile: {stats.get('reported_profiles', 0)}\n\n")
                
                f.write("=== Profile pro Plattform ===\n\n")
                for platform, count in stats.get('platforms', {}).items():
                    f.write(f"{platform}: {count}\n")
                f.write("\n")
                
                f.write("=== Verdächtige Profile ===\n\n")
                for i, profile in enumerate(results["suspicious_profiles"], 1):
                    f.write(f"Profil {i}:\n")
                    f.write(f"  Name: {profile.get('profile_name', 'Unbekannt')}\n")
                    f.write(f"  Plattform: {profile.get('platform', 'Unbekannt')}\n")
                    f.write(f"  Link: {profile.get('profile_link', 'Unbekannt')}\n")
                    f.write(f"  Risiko-Score: {profile.get('analysis', {}).get('risk_score', 0):.2f}\n")
                    
                    if "description" in profile and profile["description"]:
                        f.write(f"  Beschreibung: {profile['description'][:100]}...\n")
                    
                    if "post_text" in profile and profile["post_text"]:
                        f.write(f"  Post-Text: {profile['post_text'][:100]}...\n")
                    
                    f.write("\n")
            
            logger.info(f"Bericht generiert: {filename}")
            return os.path.abspath(filename)
            
        except Exception as e:
            logger.error(f"Fehler beim Generieren des Berichts: {e}")
            return None


def main():
    """Hauptfunktion für die Kommandozeilenausführung"""
    parser = argparse.ArgumentParser(description="IRI® Legal Agent - Integrierter Scraper")
    
    # Definiere Kommandozeilenargumente
    parser.add_argument("--mode", choices=["full", "targeted", "profile"], default="full",
                        help="Scraping-Modus: full (vollständig), targeted (gezielt), profile (Profil)")
    parser.add_argument("--platforms", nargs="+", 
                        help="Zu scrapende Plattformen (Instagram, Facebook, TikTok, Google, Website)")
    parser.add_argument("--terms", nargs="+", 
                        help="Suchbegriffe für gezieltes Scraping")
    parser.add_argument("--profiles", nargs="+", 
                        help="Profil-Links für Profil-Scraping")
    parser.add_argument("--db-url", 
                        help="URL für die Datenbankverbindung")
    parser.add_argument("--output", default="scraping_results",
                        help="Präfix für Ausgabedateien")
    
    args = parser.parse_args()
    
    # Initialisiere IntegratedScraper
    scraper = IntegratedScraper(db_url=args.db_url)
    
    # Führe Scraping entsprechend dem gewählten Modus durch
    if args.mode == "full":
        results = scraper.run_full_scraping(platforms=args.platforms)
    elif args.mode == "targeted":
        if not args.terms:
            logger.error("Für gezieltes Scraping müssen Suchbegriffe angegeben werden")
            return
        results = scraper.run_targeted_scraping(args.terms, platforms=args.platforms)
    elif args.mode == "profile":
        if not args.profiles:
            logger.error("Für Profil-Scraping müssen Profil-Links angegeben werden")
            return
        results = scraper.run_profile_scraping(args.profiles, platforms=args.platforms)
    
    # Exportiere Ergebnisse
    json_file = scraper.export_results_to_json(results, f"{args.output}.json")
    report_file = scraper.generate_report(results, f"{args.output}.txt")
    
    logger.info("Scraping abgeschlossen")
    logger.info(f"JSON-Ergebnisse: {json_file}")
    logger.info(f"Bericht: {report_file}")


if __name__ == "__main__":
    main()
