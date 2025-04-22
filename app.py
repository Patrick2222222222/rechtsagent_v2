#!/usr/bin/env python3
# app.py - Weboberfläche für IRI® Legal Agent

import os
import json
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Importiere die einzelnen Komponenten
from social_media_monitor import SocialMediaMonitor
from screenshot_service import ScreenshotService
from monday_integration import MondayIntegration
from email_notification import EmailNotificationService

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Konfiguration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Stelle sicher, dass die erforderlichen Verzeichnisse existieren
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('screenshots', exist_ok=True)

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

@app.route('/run-workflow')
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
    
    # Starte den Workflow in einem separaten Thread
    import threading
    thread = threading.Thread(target=run_workflow_thread)
    thread.daemon = True
    thread.start()
    
    flash('Workflow gestartet. Die Verarbeitung kann einige Minuten dauern.', 'info')
    return redirect(url_for('index'))

def run_workflow_thread():
    global process_status
    
    process_status = {
        'running': True,
        'step': 'Initialisierung',
        'progress': 0,
        'message': 'Starte Workflow...',
        'results': []
    }
    
    try:
        # Schritt 1: Social Media Monitoring
        process_status['step'] = 'Social Media Monitoring'
        process_status['progress'] = 10
        process_status['message'] = 'Suche nach verdächtigen Beiträgen...'
        
        monitor = SocialMediaMonitor()
        search_results = monitor.run_search()
        
        process_status['progress'] = 30
        process_status['message'] = f'Gefunden: {len(search_results)} Verdachtsfälle'
        process_status['results'] = search_results
        
        # Schritt 2: Screenshot und Beweissicherung
        process_status['step'] = 'Screenshot und Beweissicherung'
        process_status['progress'] = 40
        process_status['message'] = 'Erstelle Screenshots und sammle Beweise...'
        
        screenshot_service = ScreenshotService()
        evidence_cases = screenshot_service.process_cases("search_results.json")
        
        process_status['progress'] = 60
        process_status['message'] = f'Beweise gesammelt für {len(evidence_cases)} Fälle'
        
        # Schritt 3: Monday.com Integration
        process_status['step'] = 'Monday.com Integration'
        process_status['progress'] = 70
        process_status['message'] = 'Trage Fälle in Monday.com ein...'
        
        monday = MondayIntegration()
        monday.process_cases("processed_with_evidence.json")
        
        process_status['progress'] = 90
        process_status['message'] = 'Fälle in Monday.com eingetragen'
        
        # Optional: E-Mail-Benachrichtigung
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        if sendgrid_api_key and sendgrid_api_key != "DEIN_SENDGRID_KEY":
            process_status['step'] = 'E-Mail-Benachrichtigung'
            process_status['progress'] = 95
            process_status['message'] = 'Sende E-Mail-Benachrichtigungen...'
            
            email_service = EmailNotificationService()
            email_service.process_cases_with_email("processed_with_evidence.json")
            
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
    return send_from_directory('screenshots', filename)

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
