#!/usr/bin/env python3
# iri_legal_agent.py - Einstiegspunkt für IRI® Legal Agent mit vereinfachter Benutzeroberfläche

import os
import sys
import argparse
from datetime import datetime

# Prüfe, ob die erforderlichen Module vorhanden sind
try:
    from dotenv import load_dotenv
    import requests
except ImportError:
    print("Erforderliche Module nicht gefunden. Installiere Module...")
    os.system("pip3 install python-dotenv requests beautifulsoup4")
    from dotenv import load_dotenv
    import requests

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

def check_environment():
    """Überprüft, ob die Umgebung korrekt eingerichtet ist"""
    # Prüfe, ob die erforderlichen Skripte vorhanden sind
    required_files = [
        "main.py",
        "social_media_monitor.py",
        "screenshot_service.py",
        "monday_integration.py",
        "email_notification.py",
        ".env"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Fehler: Folgende Dateien fehlen: {', '.join(missing_files)}")
        return False
    
    # Prüfe, ob die API-Schlüssel konfiguriert sind
    screenshot_api_key = os.getenv("SCREENSHOT_API_KEY")
    monday_api_key = os.getenv("MONDAY_API_KEY")
    
    if not screenshot_api_key or screenshot_api_key == "DEIN_SCREENSHOTAPI_KEY":
        print("Warnung: ScreenshotAPI-Schlüssel nicht konfiguriert")
    
    if not monday_api_key or monday_api_key == "DEIN_MONDAY_KEY":
        print("Warnung: Monday.com-API-Schlüssel nicht konfiguriert")
    
    return True

def display_menu():
    """Zeigt das Hauptmenü an"""
    print("\nIRI® Legal Agent - Hauptmenü")
    print("============================")
    print("1. Vollständigen Workflow ausführen")
    print("2. Nur Social Media Monitoring ausführen")
    print("3. Nur Screenshots und Beweissicherung ausführen")
    print("4. Nur Monday.com-Integration ausführen")
    print("5. Nur E-Mail-Benachrichtigungen ausführen")
    print("6. API-Schlüssel konfigurieren")
    print("7. Hilfe anzeigen")
    print("0. Beenden")
    
    choice = input("\nBitte wählen Sie eine Option (0-7): ")
    return choice

def configure_api_keys():
    """Konfiguriert die API-Schlüssel in der .env-Datei"""
    print("\nAPI-Schlüssel konfigurieren")
    print("=========================")
    
    # Aktuelle Werte auslesen
    current_screenshot_key = os.getenv("SCREENSHOT_API_KEY", "")
    current_monday_key = os.getenv("MONDAY_API_KEY", "")
    current_sendgrid_key = os.getenv("SENDGRID_API_KEY", "")
    
    # Neue Werte abfragen
    print(f"\nAktueller ScreenshotAPI-Schlüssel: {current_screenshot_key if current_screenshot_key and current_screenshot_key != 'DEIN_SCREENSHOTAPI_KEY' else 'Nicht konfiguriert'}")
    screenshot_key = input("Neuer ScreenshotAPI-Schlüssel (leer lassen für unverändert): ")
    
    print(f"\nAktueller Monday.com-API-Schlüssel: {current_monday_key if current_monday_key and current_monday_key != 'DEIN_MONDAY_KEY' else 'Nicht konfiguriert'}")
    monday_key = input("Neuer Monday.com-API-Schlüssel (leer lassen für unverändert): ")
    
    print(f"\nAktueller SendGrid-API-Schlüssel: {current_sendgrid_key if current_sendgrid_key and current_sendgrid_key != 'DEIN_SENDGRID_KEY' else 'Nicht konfiguriert'}")
    sendgrid_key = input("Neuer SendGrid-API-Schlüssel (leer lassen für unverändert): ")
    
    # Werte aktualisieren, wenn neue eingegeben wurden
    if screenshot_key:
        current_screenshot_key = screenshot_key
    
    if monday_key:
        current_monday_key = monday_key
    
    if sendgrid_key:
        current_sendgrid_key = sendgrid_key
    
    # .env-Datei aktualisieren
    with open(".env", "w") as f:
        f.write(f"# API-Schlüssel für IRI® Legal Agent\n")
        f.write(f"# Zuletzt aktualisiert: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        f.write(f"# ScreenshotAPI.net API-Schlüssel\n")
        f.write(f"SCREENSHOT_API_KEY=\"{current_screenshot_key}\"\n\n")
        f.write(f"# Monday.com API-Schlüssel\n")
        f.write(f"MONDAY_API_KEY=\"{current_monday_key}\"\n\n")
        f.write(f"# SendGrid API-Schlüssel (optional)\n")
        f.write(f"SENDGRID_API_KEY=\"{current_sendgrid_key}\"\n")
    
    print("\nAPI-Schlüssel wurden aktualisiert.")
    
    # Umgebungsvariablen neu laden
    load_dotenv(override=True)

def display_help():
    """Zeigt Hilfe-Informationen an"""
    print("\nIRI® Legal Agent - Hilfe")
    print("=======================")
    print("Dieses Tool überwacht soziale Medien nach nicht-lizenzierten kosmetischen Behandlungen")
    print("mit Hyaluron Pens, erstellt Screenshots als Beweismaterial, dokumentiert Fälle in")
    print("Monday.com und kann optional Berechtigungsanfragen per E-Mail versenden.")
    print("\nErforderliche API-Schlüssel:")
    print("- ScreenshotAPI.net: Für die Erstellung von Screenshots")
    print("- Monday.com: Für die Dokumentation von Fällen")
    print("- SendGrid (optional): Für den Versand von E-Mail-Benachrichtigungen")
    print("\nWeitere Informationen finden Sie in der README.md-Datei.")

def main():
    """Hauptfunktion"""
    parser = argparse.ArgumentParser(description="IRI® Legal Agent zur Erkennung illegal arbeitender Kosmetikerinnen")
    parser.add_argument("--cli", action="store_true", help="Startet das Tool im Kommandozeilenmodus")
    
    args = parser.parse_args()
    
    # Prüfe, ob die Umgebung korrekt eingerichtet ist
    if not check_environment():
        print("Fehler: Die Umgebung ist nicht korrekt eingerichtet.")
        sys.exit(1)
    
    if args.cli:
        # Kommandozeilenmodus
        os.system("python3 main.py")
    else:
        # Interaktiver Modus
        while True:
            choice = display_menu()
            
            if choice == "0":
                print("Auf Wiedersehen!")
                break
            elif choice == "1":
                print("\nFühre vollständigen Workflow aus...")
                os.system("python3 main.py")
            elif choice == "2":
                print("\nFühre nur Social Media Monitoring aus...")
                os.system("python3 social_media_monitor.py")
            elif choice == "3":
                print("\nFühre nur Screenshots und Beweissicherung aus...")
                os.system("python3 screenshot_service.py")
            elif choice == "4":
                print("\nFühre nur Monday.com-Integration aus...")
                os.system("python3 monday_integration.py")
            elif choice == "5":
                print("\nFühre nur E-Mail-Benachrichtigungen aus...")
                os.system("python3 email_notification.py")
            elif choice == "6":
                configure_api_keys()
            elif choice == "7":
                display_help()
            else:
                print("Ungültige Eingabe. Bitte wählen Sie eine Option zwischen 0 und 7.")
            
            input("\nDrücken Sie Enter, um fortzufahren...")

if __name__ == "__main__":
    main()
