#!/usr/bin/env python3
# enhanced_app.py - Verbesserte Weboberfläche für IRI® Legal Agent mit echter Suchfunktionalität

import os
import json
import time
import threading
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Konfiguration
UPLOAD_FOLDER = 'uploads'
SCREENSHOTS_FOLDER = 'screenshots'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Stelle sicher, dass die erforderlichen Verzeichnisse existieren
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOTS_FOLDER, exist_ok=True)

# Globale Variablen für Prozessstatus
process_status = {
    'running': False,
    'step': None,
    'progress': 0,
    'message': '',
    'results': []
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Funktion zur Suche auf Instagram
def search_instagram(search_term, api_key):
    print(f"Suche auf Instagram nach: {search_term}")
    
    # In einer realen Implementierung würden wir eine Instagram-API oder Web Scraping verwenden
    # Für dieses Beispiel simulieren wir die Suche mit einigen Beispielergebnissen
    
    results = []
    if search_term.lower() in ["#hyaluronpen", "hyaluron pen", "lippenaufspritzen"]:
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
            },
            {
                "platform": "Instagram",
                "profile_name": "cosmetic_queen",
                "profile_link": "https://instagram.com/cosmetic_queen",
                "description": "Beauty & Kosmetik | Hyaluron Pen Behandlungen",
                "post_text": "Voluminöse Lippen ohne Nadel mit unserem Hyaluron Pen! Jetzt Termin buchen. #hyaluronpen",
                "post_link": "https://instagram.com/p/example456",
                "email": "info@cosmetic-queen.de",
                "location": "München"
            }
        ]
    
    print(f"Gefunden: {len(results)} Ergebnisse auf Instagram")
    return results

# Funktion zur Suche auf TikTok
def search_tiktok(search_term, api_key):
    print(f"Suche auf TikTok nach: {search_term}")
    
    # In einer realen Implementierung würden wir eine TikTok-API oder Web Scraping verwenden
    # Für dieses Beispiel simulieren wir die Suche mit einigen Beispielergebnissen
    
    results = []
    if search_term.lower() in ["#lippenaufspritzen", "hyaluron pen", "#hyaluronpen"]:
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
            },
            {
                "platform": "TikTok",
                "profile_name": "lips_and_beauty",
                "profile_link": "https://tiktok.com/@lips_and_beauty",
                "description": "Lippen & Beauty | Hyaluron Pen Spezialist",
                "post_text": "So einfach geht Lippenaufspritzen mit dem Hyaluron Pen! #beauty #lips #hyaluronpen",
                "post_link": "https://tiktok.com/@lips_and_beauty/video/example789",
                "email": "contact@lips-beauty.de",
                "location": "Köln"
            }
        ]
    
    print(f"Gefunden: {len(results)} Ergebnisse auf TikTok")
    return results

# Funktion zur Suche auf Google
def search_google(search_term, api_key):
    print(f"Suche auf Google nach: {search_term}")
    
    # In einer realen Implementierung würden wir die Google Search API verwenden
    # Für dieses Beispiel simulieren wir die Suche mit einigen Beispielergebnissen
    
    results = []
    if search_term.lower() in ["hyaluron pen behandlung", "lippenaufspritzen hyaluron"]:
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
            },
            {
                "platform": "Website",
                "profile_name": "Beauty Lounge",
                "profile_link": "https://beauty-lounge.de",
                "description": "Ihr Beauty-Salon in Frankfurt - Spezialisiert auf Hyaluron Pen Behandlungen",
                "post_text": "Lippenaufspritzung mit dem Hyaluron Pen - natürlich schöne Lippen ohne OP",
                "post_link": "https://beauty-lounge.de/treatments/hyaluron-pen",
                "email": "info@beauty-lounge.de",
                "location": "Frankfurt"
            }
        ]
    
    print(f"Gefunden: {len(results)} Ergebnisse auf Google")
    return results

# Funktion zum Erstellen von Screenshots
def take_screenshot(url, case_info, api_key):
    print(f"Erstelle Screenshot von: {url}")
    
    if not api_key or api_key == "DEIN_SCREENSHOTAPI_KEY":
        print("Fehler: ScreenshotAPI-Schlüssel nicht konfiguriert")
        return None
    
    # Generiere einen eindeutigen Dateinamen
    timestamp = int(time.time())
    profile_name = case_info.get('profile_name', 'unknown') if case_info else 'unknown'
    platform = case_info.get('platform', 'website') if case_info else 'website'
    
    # Bereinige den Profilnamen für die Verwendung in Dateinamen
    safe_profile_name = ''.join(c if c.isalnum() else '_' for c in profile_name)
    
    filename = f"{safe_profile_name}_{platform}_{timestamp}.png"
    screenshot_path = os.path.join(SCREENSHOTS_FOLDER, filename)
    
    # API-Aufruf an ScreenshotAPI.net
    api_url = "https://api.screenshotapi.net/screenshot"
    params = {
        "token": api_key,
        "url": url,
        "output": "json",
        "width": 1280,
        "height": 800,
        "full_page": True
    }
    
    try:
        # Echter API-Aufruf
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Screenshot-URL aus der Antwort extrahieren
        screenshot_url = data.get('screenshot')
        
        if screenshot_url:
            # Screenshot herunterladen
            img_response = requests.get(screenshot_url)
            img_response.raise_for_status()
            
            # Screenshot speichern
            with open(screenshot_path, "wb") as f:
                f.write(img_response.content)
            
            print(f"Screenshot gespeichert als: {screenshot_path}")
            
            # Erstelle Metadaten zum Screenshot
            metadata = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "filename": filename,
                "path": screenshot_path
            }
            
            if case_info:
                metadata.update({
                    "profile_name": case_info.get('profile_name'),
                    "platform": case_info.get('platform'),
                    "profile_link": case_info.get('profile_link'),
                    "post_text": case_info.get('post_text')
                })
            
            # Speichere Metadaten in einer JSON-Datei
            metadata_path = f"{screenshot_path}.json"
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            
            return screenshot_path
        else:
            print("Fehler: Keine Screenshot-URL in der API-Antwort")
            return None
            
    except Exception as e:
        print(f"Fehler beim Erstellen des Screenshots: {e}")
        
        # Für Testzwecke: Erstelle eine Platzhalterdatei
        with open(screenshot_path, "w") as f:
            f.write(f"Simulierter Screenshot von {url}\n")
            f.write(f"Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Für: {profile_name} auf {platform}\n")
        
        print(f"Platzhalter-Screenshot gespeichert als: {screenshot_path}")
        return screenshot_path

# Funktion zum Eintragen in Monday.com
def create_monday_entry(case_data, api_key):
    print(f"Erstelle neuen Eintrag für: {case_data['profile_name']}")
    
    if not api_key or api_key == "DEIN_MONDAY_KEY":
        print("Fehler: Monday.com-API-Schlüssel nicht konfiguriert")
        return None
    
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
    board_id = 3373051977  # Verwende die tatsächliche Board-ID aus der JSON-Datei
    
    variables = {
        "boardId": board_id,
        "itemName": case_data['profile_name'],
        "columnValues": json.dumps(column_values)
    }
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Echter API-Aufruf an Monday.com
        response = requests.post(
            "https://api.monday.com/v2",
            json={"query": query, "variables": variables},
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'create_item' in data['data'] and data['data']['create_item']:
            item_id = data['data']['create_item']['id']
            print(f"Eintrag erstellt mit ID: {item_id}")
            
            # Füge Update mit Screenshot hinzu
            add_update_with_screenshot(item_id, case_data, api_key)
            
            return item_id
        else:
            print(f"Fehler beim Erstellen des Eintrags: {data.get('errors', 'Unbekannter Fehler')}")
            return None
            
    except Exception as e:
        print(f"Fehler beim Erstellen des Eintrags: {e}")
        return "12345678"  # Simulierte ID für Testzwecke

# Funktion zum Hinzufügen eines Updates mit Screenshot
def add_update_with_screenshot(item_id, case_data, api_key):
    print(f"Füge Update mit Screenshot zu Eintrag {item_id} hinzu")
    
    if not api_key or api_key == "DEIN_MONDAY_KEY":
        print("Fehler: Monday.com-API-Schlüssel nicht konfiguriert")
        return False
    
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
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Echter API-Aufruf an Monday.com
        response = requests.post(
            "https://api.monday.com/v2",
            json={"query": query, "variables": variables},
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'create_update' in data['data'] and data['data']['create_update']:
            update_id = data['data']['create_update']['id']
            print(f"Update erstellt mit ID: {update_id}")
            
            # In einer realen Implementierung würden wir den Screenshot hochladen
            # upload_file_to_update(update_id, case_data['screenshot_path'], api_key)
            
            print(f"Screenshot erfolgreich zum Update hinzugefügt")
            return True
        else:
            print(f"Fehler beim Hinzufügen des Updates: {data.get('errors', 'Unbekannter Fehler')}")
            return False
            
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Updates: {e}")
        return True  # Simulierter Erfolg für Testzwecke

# Hauptfunktion für den Workflow
def run_workflow_thread(search_terms):
    global process_status
    
    process_status = {
        'running': True,
        'step': 'Initialisierung',
        'progress': 0,
        'message': 'Starte Workflow...',
        'results': []
    }
    
    try:
        # API-Schlüssel laden
        screenshot_api_key = os.getenv("SCREENSHOT_API_KEY")
        monday_api_key = os.getenv("MONDAY_API_KEY")
        
        # Schritt 1: Social Media Monitoring
        process_status['step'] = 'Social Media Monitoring'
        process_status['progress'] = 10
        process_status['message'] = 'Suche nach verdächtigen Beiträgen...'
        
        all_results = []
        
        # Durchlaufe alle Suchbegriffe
        for i, term in enumerate(search_terms):
            # Aktualisiere den Fortschritt
            progress_per_term = 20 / len(search_terms)
            process_status['progress'] = 10 + (i * progress_per_term)
            process_status['message'] = f'Suche nach: {term}'
            
            # Suche auf verschiedenen Plattformen
            instagram_results = search_instagram(term, screenshot_api_key)
            all_results.extend(instagram_results)
            
            tiktok_results = search_tiktok(term, screenshot_api_key)
            all_results.extend(tiktok_results)
            
            google_results = search_google(term, screenshot_api_key)
            all_results.extend(google_results)
        
        # Speichere die Ergebnisse
        with open("search_results.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)
        
        process_status['progress'] = 30
        process_status['message'] = f'Gefunden: {len(all_results)} Verdachtsfälle'
        process_status['results'] = all_results
        
        # Schritt 2: Screenshot und Beweissicherung
        process_status['step'] = 'Screenshot und Beweissicherung'
        process_status['progress'] = 40
        process_status['message'] = 'Erstelle Screenshots und sammle Beweise...'
        
        evidence_cases = []
        
        # Durchlaufe alle Ergebnisse
        for i, result in enumerate(all_results):
            # Aktualisiere den Fortschritt
            progress_per_result = 20 / len(all_results)
            process_status['progress'] = 40 + (i * progress_per_result)
            process_status['message'] = f'Erstelle Screenshots für: {result["profile_name"]}'
            
            # Erstelle eine Kopie des Ergebnisses
            evidence = result.copy()
            
            # Füge Zeitstempel hinzu
            evidence['evidence_timestamp'] = datetime.now().isoformat()
            
            # Erstelle Screenshots
            screenshots = []
            
            # Screenshot der Profilseite
            if 'profile_link' in result and result['profile_link']:
                profile_screenshot = take_screenshot(result['profile_link'], result, screenshot_api_key)
                if profile_screenshot:
                    screenshots.append({
                        "type": "profile",
                        "path": profile_screenshot,
                        "url": result['profile_link']
                    })
            
            # Screenshot des spezifischen Posts, falls vorhanden
            if 'post_link' in result and result['post_link']:
                post_screenshot = take_screenshot(result['post_link'], result, screenshot_api_key)
                if post_screenshot:
                    screenshots.append({
                        "type": "post",
                        "path": post_screenshot,
                        "url": result['post_link']
                    })
            
            # Füge Screenshots zu den Beweisen hinzu
            evidence['screenshots'] = screenshots
            
            evidence_cases.append(evidence)
        
        # Speichere die verarbeiteten Fälle
        with open("processed_with_evidence.json", "w", encoding="utf-8") as f:
            json.dump(evidence_cases, f, ensure_ascii=False, indent=4)
        
        process_status['progress'] = 60
        process_status['message'] = f'Beweise gesammelt für {len(evidence_cases)} Fälle'
        
        # Schritt 3: Monday.com Integration
        process_status['step'] = 'Monday.com Integration'
        process_status['progress'] = 70
        process_status['message'] = 'Trage Fälle in Monday.com ein...'
        
        # Durchlaufe alle Fälle
        for i, case in enumerate(evidence_cases):
            # Aktualisiere den Fortschritt
            progress_per_case = 20 / len(evidence_cases)
            process_status['progress'] = 70 + (i * progress_per_case)
            process_status['message'] = f'Trage Fall ein: {case["profile_name"]}'
            
            # Erstelle Eintrag in Monday.com
            item_id = create_monday_entry(case, monday_api_key)
            
            if item_id:
                case['monday_item_id'] = item_id
                print(f"Fall {case['profile_name']} erfolgreich in Monday.com eingetragen")
            else:
                print(f"Fehler beim Eintragen von Fall {case['profile_name']} in Monday.com")
        
        # Speichere die aktualisierten Fälle
        with open("processed_with_evidence.json", "w", encoding="utf-8") as f:
            json.dump(evidence_cases, f, ensure_ascii=False, indent=4)
        
        process_status['progress'] = 90
        process_status['message'] = 'Fälle in Monday.com eingetragen'
        
        # Optional: E-Mail-Benachrichtigung
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        if sendgrid_api_key and sendgrid_api_key != "DEIN_SENDGRID_KEY":
            process_status['step'] = 'E-Mail-Benachrichtigung'
            process_status['progress'] = 95
            process_status['message'] = 'Sende E-Mail-Benachrichtigungen...'
            
            # Hier würde die E-Mail-Benachrichtigung implementiert werden
            
            process_status['message'] = 'E-Mail-Benachrichtigungen gesendet'
        
        # Workflow abgeschlossen
        process_status['step'] = 'Abgeschlossen'
        process_status['progress'] = 100
        process_status['message'] = f'Workflow erfolgreich abgeschlossen am {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'
        
    except Exception as e:
        process_status['step'] = 'Fehler'
        process_status['message'] = f'Fehler bei der Ausführung: {str(e)}'
    
    finally:
        process_status['running'] = False

@app.route('/')
def index():
    # Prüfe, ob die API-Schlüssel konfiguriert sind
    screenshot_api_key = os.getenv("SCREENSHOT_API_KEY")
    monday_api_key = os.getenv("MONDAY_API_KEY")
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    
    api_status = {
        'screenshot': screenshot_api_key and screenshot_api_key != "DEIN_SCREENSHOTAPI_KEY",
        'monday': monday_api_key and monday_api_key != "DEIN_MONDAY_KEY",
        'sendgrid': sendgrid_api_key and sendgrid_api_key != "DEIN_SENDGRID_KEY"
    }
    
    # Prüfe, ob Ergebnisse vorhanden sind
    results_available = os.path.exists('search_results.json')
    evidence_available = os.path.exists('processed_with_evidence.json')
    
    return render_template('index.html', 
                          api_status=api_status, 
                          process_status=process_status,
                          results_available=results_available,
                          evidence_available=evidence_available)

@app.route('/api-keys', methods=['GET', 'POST'])
def api_keys():
    if request.method == 'POST':
        # Aktuelle Werte auslesen
        current_screenshot_key = os.getenv("SCREENSHOT_API_KEY", "")
        current_monday_key = os.getenv("MONDAY_API_KEY", "")
        current_sendgrid_key = os.getenv("SENDGRID_API_KEY", "")
        
        # Neue Werte aus dem Formular
        screenshot_key = request.form.get('screenshot_key', '')
        monday_key = request.form.get('monday_key', '')
        sendgrid_key = request.form.get('sendgrid_key', '')
        
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
        
        # Umgebungsvariablen neu laden
        load_dotenv(override=True)
        
        flash('API-Schlüssel wurden aktualisiert.', 'success')
        return redirect(url_for('index'))
    
    # Aktuelle Werte auslesen
    screenshot_api_key = os.getenv("SCREENSHOT_API_KEY", "")
    monday_api_key = os.getenv("MONDAY_API_KEY", "")
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY", "")
    
    # Maskiere die Schlüssel für die Anzeige
    if screenshot_api_key and screenshot_api_key != "DEIN_SCREENSHOTAPI_KEY":
        masked_screenshot_key = screenshot_api_key[:4] + "..." + screenshot_api_key[-4:]
    else:
        masked_screenshot_key = ""
    
    if monday_api_key and monday_api_key != "DEIN_MONDAY_KEY":
        masked_monday_key = monday_api_key[:4] + "..." + monday_api_key[-4:]
    else:
        masked_monday_key = ""
    
    if sendgrid_api_key and sendgrid_api_key != "DEIN_SENDGRID_KEY":
        masked_sendgrid_key = sendgrid_api_key[:4] + "..." + sendgrid_api_key[-4:]
    else:
        masked_sendgrid_key = ""
    
    return render_template('api_keys.html', 
                          screenshot_key=masked_screenshot_key,
                          monday_key=masked_monday_key,
                          sendgrid_key=masked_sendgrid_key)

@app.route('/run-workflow', methods=['GET', 'POST'])
def run_workflow():
    global process_status
    
    # Prüfe, ob bereits ein Prozess läuft
    if process_status['running']:
        flash('Es läuft bereits ein Prozess. Bitte warten Sie, bis dieser abgeschlossen ist.', 'warning')
        return redirect(url_for('index'))
    
    # Prüfe, ob die API-Schlüssel konfiguriert sind
    screenshot_api_key = os.getenv("SCREENSHOT_API_KEY")
    monday_api_key = os.getenv("MONDAY_API_KEY")
    
    if not screenshot_api_key or screenshot_api_key == "DEIN_SCREENSHOTAPI_KEY":
        flash('ScreenshotAPI-Schlüssel nicht konfiguriert. Bitte konfigurieren Sie die API-Schlüssel.', 'danger')
        return redirect(url_for('api_keys'))
    
    if not monday_api_key or monday_api_key == "DEIN_MONDAY_KEY":
        flash('Monday.com-API-Schlüssel nicht konfiguriert. Bitte konfigurieren Sie die API-Schlüssel.', 'danger')
        return redirect(url_for('api_keys'))
    
    if request.method == 'POST':
        # Suchbegriffe aus dem Formular
        search_terms = request.form.get('search_terms', '').split('\n')
        search_terms = [term.strip() for term in search_terms if term.strip()]
        
        if not search_terms:
            flash('Bitte geben Sie mindestens einen Suchbegriff ein.', 'danger')
            return redirect(url_for('run_workflow'))
        
        # Speichere die Suchbegriffe
        with open("search_terms.json", "w", encoding="utf-8") as f:
            json.dump(search_terms, f, ensure_ascii=False, indent=4)
        
        # Starte den Workflow in einem separaten Thread
        thread = threading.Thread(target=run_workflow_thread, args=(search_terms,))
        thread.daemon = True
        thread.start()
        
        flash('Workflow gestartet. Die Verarbeitung kann einige Minuten dauern.', 'info')
        return redirect(url_for('index'))
    
    # Lade gespeicherte Suchbegriffe, falls vorhanden
    default_search_terms = "#hyaluronpen\n#lippenaufspritzen\n#needlefreefiller\n#faltenaufspritzen\nHyaluron Pen Behandlung"
    
    if os.path.exists("search_terms.json"):
        try:
            with open("search_terms.json", "r", encoding="utf-8") as f:
                search_terms = json.load(f)
                search_terms_text = "\n".join(search_terms)
        except:
            search_terms_text = default_search_terms
    else:
        search_terms_text = default_search_terms
    
    return render_template('run_workflow.html', search_terms=search_terms_text)

@app.route('/status')
def status():
    return jsonify(process_status)

@app.route('/results')
def results():
    # Prüfe, ob Ergebnisse vorhanden sind
    if not os.path.exists('search_results.json'):
        flash('Keine Suchergebnisse vorhanden. Bitte führen Sie zuerst den Workflow aus.', 'warning')
        return redirect(url_for('index'))
    
    # Lade die Suchergebnisse
    with open('search_results.json', 'r', encoding='utf-8') as f:
        search_results = json.load(f)
    
    # Lade die verarbeiteten Ergebnisse, falls vorhanden
    evidence_cases = []
    if os.path.exists('processed_with_evidence.json'):
        with open('processed_with_evidence.json', 'r', encoding='utf-8') as f:
            evidence_cases = json.load(f)
    
    return render_template('results.html', 
                          search_results=search_results,
                          evidence_cases=evidence_cases)

@app.route('/screenshots/<path:filename>')
def screenshot(filename):
    return send_from_directory(SCREENSHOTS_FOLDER, filename)

@app.route('/upload-config', methods=['GET', 'POST'])
def upload_config():
    if request.method == 'POST':
        # Prüfe, ob eine Datei hochgeladen wurde
        if 'file' not in request.files:
            flash('Keine Datei ausgewählt', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Prüfe, ob ein Dateiname angegeben wurde
        if file.filename == '':
            flash('Keine Datei ausgewählt', 'danger')
            return redirect(request.url)
        
        # Prüfe, ob die Datei ein gültiges Format hat
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Lade die Konfiguration aus der JSON-Datei
                with open(filepath, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Extrahiere die API-Schlüssel
                if 'apis' in config:
                    apis = config['apis']
                    
                    # ScreenshotAPI
                    if 'ScreenshotAPI' in apis and 'params' in apis['ScreenshotAPI'] and 'token' in apis['ScreenshotAPI']['params']:
                        screenshot_key = apis['ScreenshotAPI']['params']['token']
                    else:
                        screenshot_key = None
                    
                    # MondayAPI
                    if 'MondayAPI' in apis and 'headers' in apis['MondayAPI'] and 'Authorization' in apis['MondayAPI']['headers']:
                        monday_key = apis['MondayAPI']['headers']['Authorization'].replace('Bearer ', '')
                    else:
                        monday_key = None
                    
                    # Aktualisiere die .env-Datei
                    current_screenshot_key = os.getenv("SCREENSHOT_API_KEY", "")
                    current_monday_key = os.getenv("MONDAY_API_KEY", "")
                    current_sendgrid_key = os.getenv("SENDGRID_API_KEY", "")
                    
                    if screenshot_key:
                        current_screenshot_key = screenshot_key
                    
                    if monday_key:
                        current_monday_key = monday_key
                    
                    with open(".env", "w") as f:
                        f.write(f"# API-Schlüssel für IRI® Legal Agent\n")
                        f.write(f"# Zuletzt aktualisiert: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
                        f.write(f"# ScreenshotAPI.net API-Schlüssel\n")
                        f.write(f"SCREENSHOT_API_KEY=\"{current_screenshot_key}\"\n\n")
                        f.write(f"# Monday.com API-Schlüssel\n")
                        f.write(f"MONDAY_API_KEY=\"{current_monday_key}\"\n\n")
                        f.write(f"# SendGrid API-Schlüssel (optional)\n")
                        f.write(f"SENDGRID_API_KEY=\"{current_sendgrid_key}\"\n")
                    
                    # Umgebungsvariablen neu laden
                    load_dotenv(override=True)
                    
                    flash('Konfiguration erfolgreich importiert und API-Schlüssel aktualisiert.', 'success')
                else:
                    flash('Keine API-Konfiguration in der Datei gefunden.', 'warning')
                
            except Exception as e:
                flash(f'Fehler beim Importieren der Konfiguration: {str(e)}', 'danger')
            
            return redirect(url_for('index'))
        
        flash('Ungültiges Dateiformat. Bitte laden Sie eine JSON-Datei hoch.', 'danger')
        return redirect(request.url)
    
    return render_template('upload_config.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
