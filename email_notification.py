#!/usr/bin/env python3
# email_notification.py - Optionales E-Mail-Benachrichtigungssystem für IRI® Legal Agent

import os
import json
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

class EmailNotificationService:
    def __init__(self):
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        
        # Prüfe, ob API-Schlüssel vorhanden ist
        if not self.sendgrid_api_key or self.sendgrid_api_key == "DEIN_SENDGRID_KEY":
            print("Warnung: SendGrid-API-Schlüssel nicht konfiguriert")
    
    def send_authorization_request(self, case_data):
        """
        Sendet eine Berechtigungsanfrage per E-Mail
        
        Args:
            case_data: Informationen zum Fall, muss 'email' enthalten
            
        Returns:
            True bei Erfolg, False bei Fehler
        """
        if not self.sendgrid_api_key or self.sendgrid_api_key == "DEIN_SENDGRID_KEY":
            print("Fehler: SendGrid-API-Schlüssel nicht konfiguriert")
            return False
        
        if not case_data or 'email' not in case_data or not case_data['email']:
            print("Fehler: Keine E-Mail-Adresse im Fall angegeben")
            return False
        
        recipient_email = case_data['email']
        profile_name = case_data.get('profile_name', 'Unbekannt')
        
        print(f"Sende Berechtigungsanfrage an: {recipient_email} für {profile_name}")
        
        # In einer realen Implementierung würden wir die SendGrid API verwenden
        # Für Entwicklungszwecke simulieren wir den E-Mail-Versand
        
        # Erstelle E-Mail-Inhalt
        subject = "Berechtigungsanfrage: Hyaluron Pen Behandlung"
        
        body = f"""
Sehr geehrte Damen und Herren,

wir haben festgestellt, dass Sie auf Ihrer Plattform Behandlungen mit dem "Hyaluron Pen" anbieten.

Bitte beachten Sie, dass in Deutschland für die Verwendung von Hyaluron Pens eine spezielle Zulassung erforderlich ist. Wir bitten Sie daher, uns innerhalb von 5 Tagen Ihre Berechtigung zur Durchführung dieser Behandlungen nachzuweisen.

Falls wir innerhalb dieser Frist keine Rückmeldung erhalten, sind wir verpflichtet, diesen Fall an das zuständige Gesundheitsamt weiterzuleiten.

Mit freundlichen Grüßen,
IRI® Legal Team
        """
        
        # Simuliere E-Mail-Versand
        print(f"E-Mail-Versand simuliert:")
        print(f"An: {recipient_email}")
        print(f"Betreff: {subject}")
        print(f"Inhalt: {body[:100]}...")
        
        # Aktualisiere den Fall mit Informationen zur Berechtigungsanfrage
        case_data['authorization_request'] = {
            'sent_at': datetime.now().isoformat(),
            'deadline': (datetime.now() + timedelta(days=5)).isoformat(),
            'status': 'sent'
        }
        
        # Speichere den aktualisierten Fall
        case_id = case_data.get('id', str(int(time.time())))
        with open(f"case_{case_id}_with_request.json", "w", encoding="utf-8") as f:
            json.dump(case_data, f, ensure_ascii=False, indent=4)
        
        print(f"Berechtigungsanfrage gesendet und in case_{case_id}_with_request.json gespeichert")
        return True
    
    def check_response_deadline(self, case_data):
        """
        Prüft, ob die Frist für die Berechtigungsanfrage abgelaufen ist
        
        Args:
            case_data: Informationen zum Fall mit 'authorization_request'
            
        Returns:
            True wenn die Frist abgelaufen ist, False sonst
        """
        if not case_data or 'authorization_request' not in case_data:
            print("Fehler: Keine Informationen zur Berechtigungsanfrage im Fall")
            return False
        
        auth_request = case_data['authorization_request']
        if 'deadline' not in auth_request:
            print("Fehler: Keine Frist in der Berechtigungsanfrage angegeben")
            return False
        
        deadline_str = auth_request['deadline']
        try:
            deadline = datetime.fromisoformat(deadline_str)
            now = datetime.now()
            
            if now > deadline:
                print(f"Frist abgelaufen für Fall {case_data.get('profile_name', 'Unbekannt')}")
                return True
            else:
                days_left = (deadline - now).days
                print(f"Frist noch nicht abgelaufen für Fall {case_data.get('profile_name', 'Unbekannt')}. Noch {days_left} Tage übrig.")
                return False
                
        except Exception as e:
            print(f"Fehler beim Prüfen der Frist: {e}")
            return False
    
    def send_health_authority_notification(self, case_data):
        """
        Sendet eine Meldung an das zuständige Gesundheitsamt
        
        Args:
            case_data: Informationen zum Fall
            
        Returns:
            True bei Erfolg, False bei Fehler
        """
        if not self.sendgrid_api_key or self.sendgrid_api_key == "DEIN_SENDGRID_KEY":
            print("Fehler: SendGrid-API-Schlüssel nicht konfiguriert")
            return False
        
        profile_name = case_data.get('profile_name', 'Unbekannt')
        location = case_data.get('location', 'Unbekannt')
        
        # Bestimme das zuständige Gesundheitsamt basierend auf dem Ort
        # In einer realen Implementierung würde hier eine Datenbank oder API verwendet
        health_authority_email = f"gesundheitsamt@{location.lower().replace(' ', '')}.de"
        
        print(f"Sende Meldung an Gesundheitsamt: {health_authority_email} für {profile_name} in {location}")
        
        # In einer realen Implementierung würden wir die SendGrid API verwenden
        # Für Entwicklungszwecke simulieren wir den E-Mail-Versand
        
        # Erstelle E-Mail-Inhalt
        subject = f"Meldung: Nicht-lizenzierte Hyaluron Pen Behandlung in {location}"
        
        body = f"""
Sehr geehrte Damen und Herren,

wir möchten Ihnen hiermit einen Fall von nicht-lizenzierten kosmetischen Behandlungen mit einem "Hyaluron Pen" melden.

Details zum Fall:
- Name/Studio: {profile_name}
- Plattform: {case_data.get('platform', 'Unbekannt')}
- Ort: {location}
- Beschreibung: {case_data.get('post_text', 'Keine Beschreibung verfügbar')}

Wir haben dem Anbieter am {case_data.get('authorization_request', {}).get('sent_at', 'Unbekannt')} eine Berechtigungsanfrage gesendet, haben jedoch keine Rückmeldung erhalten.

Im Anhang finden Sie Screenshots als Beweismaterial.

Mit freundlichen Grüßen,
IRI® Legal Team
        """
        
        # Simuliere E-Mail-Versand
        print(f"E-Mail-Versand an Gesundheitsamt simuliert:")
        print(f"An: {health_authority_email}")
        print(f"Betreff: {subject}")
        print(f"Inhalt: {body[:100]}...")
        
        # Aktualisiere den Fall mit Informationen zur Gesundheitsamtmeldung
        case_data['health_authority_notification'] = {
            'sent_at': datetime.now().isoformat(),
            'authority_email': health_authority_email,
            'status': 'reported'
        }
        
        # Speichere den aktualisierten Fall
        case_id = case_data.get('id', str(int(time.time())))
        with open(f"case_{case_id}_reported.json", "w", encoding="utf-8") as f:
            json.dump(case_data, f, ensure_ascii=False, indent=4)
        
        print(f"Meldung an Gesundheitsamt gesendet und in case_{case_id}_reported.json gespeichert")
        return True
    
    def process_cases_with_email(self, cases_file):
        """
        Verarbeitet alle Fälle aus einer JSON-Datei und sendet Berechtigungsanfragen
        
        Args:
            cases_file: Pfad zur JSON-Datei mit Falldaten
            
        Returns:
            Liste der verarbeiteten Fälle
        """
        if not os.path.exists(cases_file):
            print(f"Fehler: Datei {cases_file} existiert nicht")
            return []
        
        with open(cases_file, "r", encoding="utf-8") as f:
            cases = json.load(f)
        
        print(f"Verarbeite {len(cases)} Fälle für E-Mail-Benachrichtigungen")
        
        processed_cases = []
        
        for case in cases:
            # Prüfe, ob eine E-Mail-Adresse vorhanden ist
            if 'email' in case and case['email']:
                # Sende Berechtigungsanfrage
                success = self.send_authorization_request(case)
                if success:
                    processed_cases.append(case)
                    print(f"Berechtigungsanfrage für Fall {case.get('profile_name', 'Unbekannt')} gesendet")
                else:
                    print(f"Fehler beim Senden der Berechtigungsanfrage für Fall {case.get('profile_name', 'Unbekannt')}")
            else:
                print(f"Keine E-Mail-Adresse für Fall {case.get('profile_name', 'Unbekannt')} vorhanden")
        
        # Speichere die verarbeiteten Fälle
        if processed_cases:
            with open("cases_with_email_requests.json", "w", encoding="utf-8") as f:
                json.dump(processed_cases, f, ensure_ascii=False, indent=4)
            
            print(f"Alle Fälle verarbeitet und in cases_with_email_requests.json gespeichert")
        
        return processed_cases

if __name__ == "__main__":
    print("IRI® Legal Agent - E-Mail-Benachrichtigungssystem")
    print("------------------------------------------------")
    
    email_service = EmailNotificationService()
    
    # Teste den Service mit einem Beispielfall
    test_case = {
        "id": "test123",
        "profile_name": "Test Studio",
        "platform": "Website",
        "profile_link": "https://example.com",
        "post_text": "Lippenaufspritzung mit Hyaluron Pen - 89 €",
        "email": "test@example.com",
        "location": "Berlin"
    }
    
    # Sende Berechtigungsanfrage
    email_service.send_authorization_request(test_case)
    
    # Simuliere abgelaufene Frist
    test_case['authorization_request']['deadline'] = (datetime.now() - timedelta(days=1)).isoformat()
    
    # Prüfe Frist
    if email_service.check_response_deadline(test_case):
        # Sende Meldung an Gesundheitsamt
        email_service.send_health_authority_notification(test_case)
    
    # Verarbeite die Ergebnisse aus der processed_with_evidence.json-Datei, falls vorhanden
    if os.path.exists("processed_with_evidence.json"):
        email_service.process_cases_with_email("processed_with_evidence.json")
    else:
        print("Keine verarbeiteten Fälle mit Beweisen gefunden. Bitte führen Sie zuerst screenshot_service.py aus.")
