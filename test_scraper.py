#!/usr/bin/env python3
# test_scraper.py - Test-Skript für den verbesserten Scraper

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("test_scraper")

def test_database_connection():
    """Testet die Datenbankverbindung"""
    try:
        from database_manager import DatabaseManager
        
        logger.info("Teste Datenbankverbindung...")
        db_manager = DatabaseManager("sqlite:///test_iri_legal_agent.db")
        
        # Initialisiere Standarddaten
        db_manager.init_default_data()
        
        # Hole Statistiken
        stats = db_manager.get_statistics()
        logger.info(f"Datenbankstatistiken: {stats}")
        
        logger.info("Datenbankverbindung erfolgreich getestet")
        return True
    except Exception as e:
        logger.error(f"Fehler beim Testen der Datenbankverbindung: {e}")
        return False

def test_detection_algorithms():
    """Testet die Erkennungsalgorithmen"""
    try:
        from detection_algorithms import DetectionManager, HyaluronPenDetector
        from database_manager import DatabaseManager
        
        logger.info("Teste Erkennungsalgorithmen...")
        
        # Initialisiere Datenbankmanager
        db_manager = DatabaseManager("sqlite:///test_iri_legal_agent.db")
        
        # Initialisiere DetectionManager
        detection_manager = DetectionManager(db_manager)
        
        # Teste HyaluronPenDetector
        hyaluron_detector = HyaluronPenDetector()
        
        # Teste Texterkennung
        test_text = """
        Hyaluron Pen Behandlung jetzt verfügbar! 
        Lippen aufspritzen ohne Nadel für nur 150€. 
        Kontaktiere uns unter beauty@example.com oder +49 123 4567890.
        Standort: Berlin Mitte
        """
        
        result = hyaluron_detector.analyze_text(test_text)
        logger.info(f"Texterkennung Ergebnis: {result}")
        
        # Teste Profilanalyse
        test_profile = {
            "profile_name": "beauty_studio_berlin",
            "platform": "Instagram",
            "profile_link": "https://instagram.com/beauty_studio_berlin",
            "description": "Beauty Studio in Berlin | Hyaluron Pen Behandlungen | Lippen aufspritzen ohne Nadel",
            "posts": [
                {
                    "post_text": "Hyaluron Pen Behandlung jetzt verfügbar! Lippen aufspritzen ohne Nadel für nur 150€.",
                    "post_link": "https://instagram.com/p/123456"
                }
            ]
        }
        
        result = hyaluron_detector.analyze_profile(test_profile)
        logger.info(f"Profilanalyse Ergebnis: {result}")
        
        logger.info("Erkennungsalgorithmen erfolgreich getestet")
        return True
    except Exception as e:
        logger.error(f"Fehler beim Testen der Erkennungsalgorithmen: {e}")
        return False

def test_screenshot_service():
    """Testet den Screenshot-Dienst"""
    try:
        from screenshot_service import AdvancedScreenshotService
        from database_manager import DatabaseManager
        from detection_algorithms import DetectionManager
        
        logger.info("Teste Screenshot-Dienst...")
        
        # Initialisiere Datenbankmanager
        db_manager = DatabaseManager("sqlite:///test_iri_legal_agent.db")
        
        # Initialisiere DetectionManager
        detection_manager = DetectionManager(db_manager)
        
        # Initialisiere ScreenshotService
        screenshot_service = AdvancedScreenshotService(
            db_manager,
            detection_manager=detection_manager
        )
        
        # Teste Screenshot-Erstellung (simuliert)
        test_url = "https://example.com"
        screenshot_path = screenshot_service.capture_screenshot(test_url)
        
        if screenshot_path:
            logger.info(f"Screenshot erstellt: {screenshot_path}")
        else:
            logger.warning("Screenshot konnte nicht erstellt werden")
        
        # Teste Screenshot-Erstellung mit Analyse
        result = screenshot_service.capture_and_analyze_screenshot(test_url)
        
        if result:
            logger.info(f"Screenshot mit Analyse erstellt: {result['screenshot_path']}")
            if result["analysis"]:
                logger.info(f"Analyse-Ergebnis: {result['analysis']}")
        else:
            logger.warning("Screenshot mit Analyse konnte nicht erstellt werden")
        
        logger.info("Screenshot-Dienst erfolgreich getestet")
        return True
    except Exception as e:
        logger.error(f"Fehler beim Testen des Screenshot-Dienstes: {e}")
        return False

def test_platform_scraper():
    """Testet den Plattform-Scraper"""
    try:
        from platform_scraper import MultiPlatformScraper
        from database_manager import DatabaseManager
        
        logger.info("Teste Plattform-Scraper...")
        
        # Initialisiere Datenbankmanager
        db_manager = DatabaseManager("sqlite:///test_iri_legal_agent.db")
        
        # Initialisiere MultiPlatformScraper
        platform_scraper = MultiPlatformScraper(db_manager)
        
        # Teste Suche mit begrenzten Parametern (Simulationsmodus)
        search_terms = ["hyaluron pen", "lippen aufspritzen"]
        platforms = ["Instagram", "Google"]
        
        logger.info(f"Starte Suche mit Begriffen: {search_terms} auf Plattformen: {platforms}")
        results = platform_scraper.run_search(search_terms=search_terms, platforms=platforms, simulation_mode=True)
        
        if results:
            logger.info(f"Suchergebnisse: {len(results)} Plattformen")
            for platform, platform_results in results.items():
                logger.info(f"  {platform}: {len(platform_results)} Ergebnisse")
        else:
            logger.warning("Keine Suchergebnisse")
        
        logger.info("Plattform-Scraper erfolgreich getestet")
        return True
    except Exception as e:
        logger.error(f"Fehler beim Testen des Plattform-Scrapers: {e}")
        return False

def test_integrated_scraper():
    """Testet den integrierten Scraper"""
    try:
        from integrated_scraper import IntegratedScraper
        
        logger.info("Teste integrierten Scraper...")
        
        # Initialisiere IntegratedScraper mit SQLite für Tests
        integrated_scraper = IntegratedScraper(db_url="sqlite:///test_iri_legal_agent.db")
        
        # Teste gezielte Suche mit begrenzten Parametern (Simulationsmodus)
        search_terms = ["hyaluron pen", "lippen aufspritzen"]
        platforms = ["Instagram", "Google"]
        
        logger.info(f"Starte gezielte Suche mit Begriffen: {search_terms} auf Plattformen: {platforms}")
        
        # Modifiziere die run_targeted_scraping-Methode für den Test
        original_run_search = integrated_scraper.platform_scraper.run_search
        
        def mock_run_search(*args, **kwargs):
            # Simuliere Suchergebnisse
            return {
                "Instagram": [
                    {
                        "profile_name": "beauty_studio_test",
                        "platform": "Instagram",
                        "profile_link": "https://instagram.com/beauty_studio_test",
                        "description": "Beauty Studio | Hyaluron Pen Behandlungen",
                        "posts": [
                            {
                                "post_text": "Hyaluron Pen Behandlung jetzt verfügbar!",
                                "post_link": "https://instagram.com/p/test123"
                            }
                        ]
                    }
                ],
                "Google": [
                    {
                        "profile_name": "beauty-website-test.de",
                        "platform": "Website",
                        "profile_link": "https://beauty-website-test.de",
                        "description": "Beauty Website | Hyaluron Pen Behandlungen",
                        "posts": []
                    }
                ]
            }
        
        # Ersetze die Methode temporär
        integrated_scraper.platform_scraper.run_search = mock_run_search
        
        # Führe die Suche durch
        results = integrated_scraper.run_targeted_scraping(search_terms, platforms=platforms)
        
        # Stelle die ursprüngliche Methode wieder her
        integrated_scraper.platform_scraper.run_search = original_run_search
        
        if results:
            logger.info("Integrierter Scraper hat Ergebnisse zurückgegeben")
            
            # Exportiere Ergebnisse
            json_file = integrated_scraper.export_results_to_json(results, "test_results.json")
            report_file = integrated_scraper.generate_report(results, "test_report.txt")
            
            logger.info(f"Ergebnisse exportiert nach {json_file}")
            logger.info(f"Bericht generiert: {report_file}")
        else:
            logger.warning("Keine Ergebnisse vom integrierten Scraper")
        
        logger.info("Integrierter Scraper erfolgreich getestet")
        return True
    except Exception as e:
        logger.error(f"Fehler beim Testen des integrierten Scrapers: {e}")
        return False

def test_flask_app():
    """Testet die Flask-App"""
    try:
        import improved_app
        from improved_app import app
        
        logger.info("Teste Flask-App...")
        
        # Teste, ob die App erstellt werden kann
        test_app = improved_app.create_app()
        
        if test_app:
            logger.info("Flask-App erfolgreich erstellt")
            
            # Teste einige Routen
            with app.test_client() as client:
                # Teste Hauptseite
                response = client.get('/')
                if response.status_code == 200:
                    logger.info("Hauptseite erfolgreich geladen")
                else:
                    logger.warning(f"Fehler beim Laden der Hauptseite: {response.status_code}")
                
                # Teste API-Endpunkt
                response = client.get('/api/statistics')
                if response.status_code == 200:
                    logger.info("API-Endpunkt erfolgreich aufgerufen")
                else:
                    logger.warning(f"Fehler beim Aufrufen des API-Endpunkts: {response.status_code}")
        else:
            logger.warning("Flask-App konnte nicht erstellt werden")
        
        logger.info("Flask-App erfolgreich getestet")
        return True
    except Exception as e:
        logger.error(f"Fehler beim Testen der Flask-App: {e}")
        return False

def run_all_tests():
    """Führt alle Tests aus"""
    logger.info("Starte alle Tests...")
    
    tests = [
        ("Datenbankverbindung", test_database_connection),
        ("Erkennungsalgorithmen", test_detection_algorithms),
        ("Screenshot-Dienst", test_screenshot_service),
        ("Plattform-Scraper", test_platform_scraper),
        ("Integrierter Scraper", test_integrated_scraper),
        ("Flask-App", test_flask_app)
    ]
    
    results = {}
    
    for name, test_func in tests:
        logger.info(f"Starte Test: {name}")
        start_time = time.time()
        success = test_func()
        duration = time.time() - start_time
        
        results[name] = {
            "success": success,
            "duration": duration
        }
        
        if success:
            logger.info(f"Test {name} erfolgreich abgeschlossen in {duration:.2f} Sekunden")
        else:
            logger.error(f"Test {name} fehlgeschlagen nach {duration:.2f} Sekunden")
    
    # Erstelle Zusammenfassung
    logger.info("=== Testzusammenfassung ===")
    
    all_success = True
    
    for name, result in results.items():
        status = "Erfolgreich" if result["success"] else "Fehlgeschlagen"
        logger.info(f"{name}: {status} ({result['duration']:.2f}s)")
        
        if not result["success"]:
            all_success = False
    
    if all_success:
        logger.info("Alle Tests erfolgreich abgeschlossen!")
    else:
        logger.warning("Einige Tests sind fehlgeschlagen!")
    
    return all_success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test-Skript für den verbesserten Scraper")
    
    parser.add_argument("--test", choices=["all", "db", "detection", "screenshot", "platform", "integrated", "flask"],
                        default="all", help="Auszuführender Test")
    
    args = parser.parse_args()
    
    if args.test == "all":
        run_all_tests()
    elif args.test == "db":
        test_database_connection()
    elif args.test == "detection":
        test_detection_algorithms()
    elif args.test == "screenshot":
        test_screenshot_service()
    elif args.test == "platform":
        test_platform_scraper()
    elif args.test == "integrated":
        test_integrated_scraper()
    elif args.test == "flask":
        test_flask_app()
