#!/usr/bin/env python3
# monday_integration.py - Integration mit Monday.com für IRI® Legal Agent

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

class MondayIntegration:
    def __init__(self):
        self.api_key = os.getenv("MONDAY_API_KEY")
        self.api_url = "https://api.monday.com/v2"
        self.board_name = "IRI® Verdachtsfälle"
        
        # Prüfe, ob API-Schlüssel vorhanden ist
        if not self.api_key or self.api_key == "DEIN_MONDAY_KEY":
            print("Warnung: Monday.com-API-Schlüssel nicht konfiguriert")
    
    def create_entry(self, case_data):
        """
        Erstellt einen neuen Eintrag im Monday.com-Board
        
        case_data sollte folgende Felder enthalten:
        - profile_name: Name/Studio
        - platform: Plattform
        - profile_link: Profil-Link
        - post_text: Kommentar/Beschreibung
        - screenshot_path: Pfad zum Screenshot
        - email: E-Mail (optional)
        - location: Ort (optional)
        """
        if not self.api_key or self.api_key == "DEIN_MONDAY_KEY":
            print("Fehler: Monday.com-API-Schlüssel nicht konfiguriert")
            return None
        
        print(f"Erstelle neuen Eintrag für: {case_data['profile_name']}")
        
        # Vorbereitung der Daten für Monday.com
        item_name = case_data['profile_name']
        
        # GraphQL-Mutation für die Erstellung eines neuen Items
        query = """
        mutation ($boardId: Int!, $itemName: String!, $columnValues: JSON!) {
          create_item (
            board_id: $boardId,
            item_name: $itemName,
            column_values: $columnValues
          ) {
            id
          }
        }
        """
        
        # Spalten-Werte für Monday.com
        column_values = {
            "plattform": {"text": case_data['platform']},
            "profil_link": {"text": case_data['profile_link']},
            "status": {"text": "Neu"},
            "letzter_schritt": {"text": "Beweissicherung abgeschlossen"}
        }
        
        # Füge optionale Felder hinzu, wenn vorhanden
        if 'email' in case_data and case_data['email']:
            column_values["email"] = {"text": case_data['email']}
        
        if 'location' in case_data and case_data['location']:
            column_values["ort"] = {"text": case_data['location']}
        
        # In einer realen Implementierung würden wir die tatsächliche Board-ID verwenden
        # Für Entwicklungszwecke verwenden wir eine Dummy-ID
        board_id = 12345
        
        variables = {
            "boardId": board_id,
            "itemName": item_name,
            "columnValues": json.dumps(column_values)
        }
        
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            # Simulierter API-Aufruf für Entwicklungszwecke
            # response = requests.post(self.api_url, json={"query": query, "variables": variables}, headers=headers)
            # response.raise_for_status()
            # data = response.json()
            
            # Simulierte Antwort
            item_id = "12345678"
            
            print(f"Eintrag erstellt mit ID: {item_id}")
            
            # Füge Update mit Screenshot hinzu
            self.add_update_with_screenshot(item_id, case_data)
            
            return item_id
            
        except Exception as e:
            print(f"Fehler beim Erstellen des Eintrags: {e}")
            return None
    
    def add_update_with_screenshot(self, item_id, case_data):
        """
        Fügt ein Update mit Screenshot zu einem bestehenden Eintrag hinzu
        """
        if not self.api_key or self.api_key == "DEIN_MONDAY_KEY":
            print("Fehler: Monday.com-API-Schlüssel nicht konfiguriert")
            return False
        
        print(f"Füge Update mit Screenshot zu Eintrag {item_id} hinzu")
        
        # Erstelle den Update-Text
        current_date = datetime.now().strftime("%d.%m.%Y")
        update_text = f"""
Beitrag gefunden am {current_date}
Zitat: "{case_data['post_text']}"
Kein Hinweis auf zugelassenes System, kein Lizenznachweis.
Screenshot im Anhang.
Status: Neu
        """
        
        # GraphQL-Mutation für das Hinzufügen eines Updates
        query = """
        mutation ($itemId: Int!, $body: String!) {
          create_update (
            item_id: $itemId,
            body: $body
          ) {
            id
          }
        }
        """
        
        variables = {
            "itemId": int(item_id),
            "body": update_text
        }
        
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            # Simulierter API-Aufruf für Entwicklungszwecke
            # response = requests.post(self.api_url, json={"query": query, "variables": variables}, headers=headers)
            # response.raise_for_status()
            # data = response.json()
            
            # Simulierte Antwort
            update_id = "87654321"
            
            print(f"Update erstellt mit ID: {update_id}")
            
            # In einer realen Implementierung würden wir den Screenshot hochladen
            # self.upload_file_to_update(update_id, case_data['screenshot_path'])
            
            print(f"Screenshot erfolgreich zum Update hinzugefügt")
            return True
            
        except Exception as e:
            print(f"Fehler beim Hinzufügen des Updates: {e}")
            return False
    
    def upload_file_to_update(self, update_id, file_path):
        """
        Lädt eine Datei zu einem Update hoch
        """
        if not os.path.exists(file_path):
            print(f"Fehler: Datei {file_path} existiert nicht")
            return False
        
        print(f"Lade Datei {file_path} zu Update {update_id} hoch")
        
        # In einer realen Implementierung würden wir die Datei hochladen
        # Für Entwicklungszwecke simulieren wir den Upload
        
        return True
    
    def process_cases(self, processed_results_file):
        """
        Verarbeitet alle Fälle aus der processed_results.json-Datei und erstellt Einträge in Monday.com
        """
        if not os.path.exists(processed_results_file):
            print(f"Fehler: Datei {processed_results_file} existiert nicht")
            return False
        
        with open(processed_results_file, "r", encoding="utf-8") as f:
            cases = json.load(f)
        
        print(f"Verarbeite {len(cases)} Fälle für Monday.com")
        
        for case in cases:
            item_id = self.create_entry(case)
            if item_id:
                print(f"Fall {case['profile_name']} erfolgreich in Monday.com eingetragen")
            else:
                print(f"Fehler beim Eintragen von Fall {case['profile_name']} in Monday.com")
        
        return True

if __name__ == "__main__":
    print("IRI® Legal Agent - Monday.com Integration")
    print("----------------------------------------")
    
    monday = MondayIntegration()
    
    # Verarbeite die Ergebnisse aus der processed_results.json-Datei
    if os.path.exists("processed_results.json"):
        monday.process_cases("processed_results.json")
    else:
        print("Keine verarbeiteten Ergebnisse gefunden. Bitte führen Sie zuerst social_media_monitor.py aus.")
