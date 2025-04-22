#!/usr/bin/env python3
# main.py - Hauptskript für IRI® Legal Agent

import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Importiere die einzelnen Komponenten
from social_media_monitor import SocialMediaMonitor
from screenshot_service import ScreenshotService
from monday_integration import MondayIntegration
from email_notification import EmailNotificationService

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

def run_full_workflow(skip_email=False):
    """
    Führt den vollständigen Workflow des IRI® Legal Agent aus
    
    Args:
        skip_email: Wenn True, wird die E-Mail-Benachrichtigung übersprungen
    """
    print("IRI® Legal Agent - Vollständiger Workflow")
    print("=========================================")
    print(f"Gestartet am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print()
    
    # Schritt 1: Social Media Monitoring
    print("Schritt 1: Social Media Monitoring")
    print("---------------------------------")
    monitor = SocialMediaMonitor()
    search_results = monitor.run_search()
    print(f"Gefunden: {len(search_results)} Verdachtsfälle")
    print()
    
    # Schritt 2: Screenshot und Beweissicherung
    print("Schritt 2: Screenshot und Beweissicherung")
    print("----------------------------------------")
    screenshot_service = ScreenshotService()
    evidence_cases = screenshot_service.process_cases("search_results.json")
    print(f"Beweise gesammelt für {len(evidence_cases)} Fälle")
    print()
    
    # Schritt 3: Monday.com Integration
    print("Schritt 3: Monday.com Integration")
    print("--------------------------------")
    monday = MondayIntegration()
    monday.process_cases("processed_with_evidence.json")
    print("Fälle in Monday.com eingetragen")
    print()
    
    # Schritt 4: E-Mail-Benachrichtigung (optional)
    if not skip_email:
        print("Schritt 4: E-Mail-Benachrichtigung")
        print("----------------------------------")
        email_service = EmailNotificationService()
        email_cases = email_service.process_cases_with_email("processed_with_evidence.json")
        print(f"E-Mail-Benachrichtigungen gesendet für {len(email_cases)} Fälle")
        print()
    
    print("Workflow abgeschlossen!")
    print(f"Beendet am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

def check_api_keys():
    """
    Überprüft, ob die benötigten API-Schlüssel konfiguriert sind
    
    Returns:
        True wenn alle erforderlichen Schlüssel konfiguriert sind, False sonst
    """
    screenshot_api_key = os.getenv("SCREENSHOT_API_KEY")
    monday_api_key = os.getenv("MONDAY_API_KEY")
    
    if not screenshot_api_key or screenshot_api_key == "DEIN_SCREENSHOTAPI_KEY":
        print("Warnung: ScreenshotAPI-Schlüssel nicht konfiguriert")
        return False
    
    if not monday_api_key or monday_api_key == "DEIN_MONDAY_KEY":
        print("Warnung: Monday.com-API-Schlüssel nicht konfiguriert")
        return False
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRI® Legal Agent zur Erkennung illegal arbeitender Kosmetikerinnen")
    parser.add_argument("--skip-email", action="store_true", help="Überspringt die E-Mail-Benachrichtigung")
    parser.add_argument("--check-keys", action="store_true", help="Überprüft, ob die API-Schlüssel konfiguriert sind")
    
    args = parser.parse_args()
    
    if args.check_keys:
        if check_api_keys():
            print("Alle erforderlichen API-Schlüssel sind konfiguriert.")
        else:
            print("Nicht alle erforderlichen API-Schlüssel sind konfiguriert. Bitte überprüfen Sie die .env-Datei.")
    else:
        # Führe den vollständigen Workflow aus
        run_full_workflow(skip_email=args.skip_email)
