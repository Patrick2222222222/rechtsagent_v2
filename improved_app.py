#!/usr/bin/env python3
# improved_app.py - Verbesserte Hauptanwendung für IRI® Legal Agent

import os
import json
import time
import logging
import argparse
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Importiere eigene Module
from database_manager import DatabaseManager
from integrated_scraper import IntegratedScraper
from detection_algorithms import DetectionManager
from screenshot_service import AdvancedScreenshotService
from expanded_search_terms import get_all_search_terms, get_search_terms_by_category

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("improved_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("improved_app")

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Initialisiere Flask-App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Erstelle Upload-Verzeichnis, falls es nicht existiert
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Erstelle Screenshot-Verzeichnis, falls es nicht existiert
screenshot_dir = os.path.abspath('screenshots')
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Initialisiere Datenbankmanager
db_url = os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/iri_legal_agent"
db_manager = DatabaseManager(db_url)

# Initialisiere IntegratedScraper
integrated_scraper = IntegratedScraper(db_url=db_url)

# Initialisiere DetectionManager
detection_manager = DetectionManager(db_manager)

# Initialisiere ScreenshotService
screenshot_service = AdvancedScreenshotService(
    db_manager,
    api_key=os.getenv("SCREENSHOT_API_KEY"),
    detection_manager=detection_manager
)

# Globale Variable für laufende Scraping-Jobs
running_jobs = {}

@app.route('/')
def index():
    """Hauptseite der Anwendung"""
    # Hole Statistiken aus der Datenbank
    stats = db_manager.get_statistics()
    
    # Hole die letzten 10 verdächtigen Profile
    suspicious_profiles = db_manager.get_unreported_profiles(limit=10)
    
    return render_template(
        'index.html',
        stats=stats,
        suspicious_profiles=suspicious_profiles,
        running_jobs=running_jobs
    )

@app.route('/search')
def search():
    """Suchseite der Anwendung"""
    # Hole alle Suchbegriffe
    all_terms = get_all_search_terms()
    
    # Hole alle Plattformen
    platforms = db_manager.get_platforms()
    
    return render_template(
        'search.html',
        hashtags=all_terms['hashtags'],
        keywords=all_terms['keywords'],
        location_keywords=all_terms['location_keywords'],
        instagram_accounts=all_terms['instagram_accounts'],
        facebook_pages=all_terms['facebook_pages'],
        tiktok_accounts=all_terms['tiktok_accounts'],
        website_domains=all_terms['website_domains'],
        platforms=platforms
    )

@app.route('/profiles')
def profiles():
    """Profilseite der Anwendung"""
    # Hole alle Profile aus der Datenbank
    platform = request.args.get('platform', None)
    limit = int(request.args.get('limit', 100))
    
    if platform:
        profiles_list = db_manager.get_profiles_by_platform(platform, limit=limit)
    else:
        # Hole Profile von allen Plattformen
        profiles_list = []
        platforms = db_manager.get_platforms()
        for platform in platforms:
            platform_profiles = db_manager.get_profiles_by_platform(platform.name, limit=limit // len(platforms))
            profiles_list.extend(platform_profiles)
    
    return render_template(
        'profiles.html',
        profiles=profiles_list,
        platform=platform
    )

@app.route('/screenshots')
def screenshots():
    """Screenshot-Seite der Anwendung"""
    # Hole alle Screenshots aus dem Screenshot-Verzeichnis
    screenshot_files = []
    for filename in os.listdir(screenshot_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            screenshot_files.append(filename)
    
    return render_template(
        'screenshots.html',
        screenshots=screenshot_files
    )

@app.route('/screenshot/<path:filename>')
def serve_screenshot(filename):
    """Liefert einen Screenshot aus"""
    return send_from_directory(screenshot_dir, filename)

@app.route('/api/run_scraping', methods=['POST'])
def api_run_scraping():
    """API-Endpunkt zum Starten eines Scraping-Jobs"""
    data = request.json
    
    mode = data.get('mode', 'full')
    platforms = data.get('platforms', None)
    terms = data.get('terms', None)
    profiles = data.get('profiles', None)
    
    # Generiere eine eindeutige Job-ID
    job_id = f"job_{int(time.time())}"
    
    # Starte den Scraping-Job in einem separaten Thread
    import threading
    
    def run_job():
        try:
            # Aktualisiere Job-Status
            running_jobs[job_id] = {
                'status': 'running',
                'start_time': datetime.now().isoformat(),
                'mode': mode,
                'platforms': platforms,
                'progress': 0
            }
            
            # Führe Scraping entsprechend dem gewählten Modus durch
            if mode == 'full':
                results = integrated_scraper.run_full_scraping(platforms=platforms)
            elif mode == 'targeted':
                results = integrated_scraper.run_targeted_scraping(terms, platforms=platforms)
            elif mode == 'profile':
                results = integrated_scraper.run_profile_scraping(profiles, platforms=platforms)
            else:
                raise ValueError(f"Ungültiger Modus: {mode}")
            
            # Exportiere Ergebnisse
            json_file = integrated_scraper.export_results_to_json(results, f"results_{job_id}.json")
            report_file = integrated_scraper.generate_report(results, f"report_{job_id}.txt")
            
            # Aktualisiere Job-Status
            running_jobs[job_id] = {
                'status': 'completed',
                'start_time': running_jobs[job_id]['start_time'],
                'end_time': datetime.now().isoformat(),
                'mode': mode,
                'platforms': platforms,
                'results': {
                    'total_profiles': results['report']['total_profiles_found'],
                    'suspicious_profiles': results['report']['suspicious_profiles_found'],
                    'screenshots': results['report']['screenshots_created']
                },
                'files': {
                    'json': json_file,
                    'report': report_file
                }
            }
            
            logger.info(f"Job {job_id} abgeschlossen")
            
        except Exception as e:
            logger.error(f"Fehler bei Job {job_id}: {e}")
            
            # Aktualisiere Job-Status bei Fehler
            running_jobs[job_id] = {
                'status': 'error',
                'start_time': running_jobs[job_id]['start_time'],
                'end_time': datetime.now().isoformat(),
                'mode': mode,
                'platforms': platforms,
                'error': str(e)
            }
    
    # Starte den Thread
    thread = threading.Thread(target=run_job)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'message': f"Scraping-Job gestartet (ID: {job_id})"
    })

@app.route('/api/job_status/<job_id>')
def api_job_status(job_id):
    """API-Endpunkt zum Abfragen des Status eines Scraping-Jobs"""
    if job_id in running_jobs:
        return jsonify({
            'success': True,
            'job': running_jobs[job_id]
        })
    else:
        return jsonify({
            'success': False,
            'message': f"Job {job_id} nicht gefunden"
        })

@app.route('/api/search_terms')
def api_search_terms():
    """API-Endpunkt zum Abrufen von Suchbegriffen"""
    category = request.args.get('category', None)
    
    if category:
        terms = get_search_terms_by_category(category)
    else:
        terms = get_all_search_terms()
    
    return jsonify({
        'success': True,
        'terms': terms
    })

@app.route('/api/statistics')
def api_statistics():
    """API-Endpunkt zum Abrufen von Statistiken"""
    stats = db_manager.get_statistics()
    
    return jsonify({
        'success': True,
        'statistics': stats
    })

@app.route('/api/profiles')
def api_profiles():
    """API-Endpunkt zum Abrufen von Profilen"""
    platform = request.args.get('platform', None)
    limit = int(request.args.get('limit', 100))
    
    if platform:
        profiles_list = db_manager.get_profiles_by_platform(platform, limit=limit)
        
        # Konvertiere SQLAlchemy-Objekte in Dictionaries
        profiles_dict = []
        for profile in profiles_list:
            profile_dict = {
                'id': profile.id,
                'platform_id': profile.platform_id,
                'profile_name': profile.profile_name,
                'profile_link': profile.profile_link,
                'description': profile.description,
                'email': profile.email,
                'location': profile.location,
                'follower_count': profile.follower_count,
                'is_verified': profile.is_verified,
                'first_seen': profile.first_seen.isoformat() if profile.first_seen else None,
                'last_checked': profile.last_checked.isoformat() if profile.last_checked else None,
                'risk_score': profile.risk_score,
                'is_reported': profile.is_reported
            }
            profiles_dict.append(profile_dict)
        
        return jsonify({
            'success': True,
            'platform': platform,
            'profiles': profiles_dict
        })
    else:
        return jsonify({
            'success': False,
            'message': "Platform parameter is required"
        })

@app.route('/api/analyze_url', methods=['POST'])
def api_analyze_url():
    """API-Endpunkt zum Analysieren einer URL"""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({
            'success': False,
            'message': "URL parameter is required"
        })
    
    # Erstelle Screenshot und analysiere ihn
    result = screenshot_service.capture_and_analyze_screenshot(url)
    
    if result:
        return jsonify({
            'success': True,
            'screenshot_path': result['screenshot_path'],
            'analysis': result['analysis']
        })
    else:
        return jsonify({
            'success': False,
            'message': "Failed to capture and analyze screenshot"
        })

@app.route('/api/report_profile', methods=['POST'])
def api_report_profile():
    """API-Endpunkt zum Melden eines Profils"""
    data = request.json
    profile_id = data.get('profile_id')
    
    if not profile_id:
        return jsonify({
            'success': False,
            'message': "profile_id parameter is required"
        })
    
    # Hole das Profil aus der Datenbank
    session = db_manager.get_session()
    
    try:
        from database_schema import Profile
        
        profile = session.query(Profile).filter_by(id=profile_id).first()
        
        if not profile:
            return jsonify({
                'success': False,
                'message': f"Profile with ID {profile_id} not found"
            })
        
        # Markiere das Profil als gemeldet
        profile.is_reported = True
        
        # Speichere die Änderungen
        session.commit()
        
        return jsonify({
            'success': True,
            'message': f"Profile {profile.profile_name} marked as reported"
        })
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'success': False,
            'message': f"Error reporting profile: {str(e)}"
        })
    finally:
        session.close()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Seite zum Hochladen von URLs oder Dateien"""
    if request.method == 'POST':
        # Prüfe, ob URLs hochgeladen wurden
        urls = request.form.get('urls', '')
        
        if urls:
            # Verarbeite URLs
            url_list = [url.strip() for url in urls.split('\n') if url.strip()]
            
            if url_list:
                # Starte einen Scraping-Job für die URLs
                job_id = f"job_{int(time.time())}"
                
                # Starte den Scraping-Job in einem separaten Thread
                import threading
                
                def run_job():
                    try:
                        # Aktualisiere Job-Status
                        running_jobs[job_id] = {
                            'status': 'running',
                            'start_time': datetime.now().isoformat(),
                            'mode': 'profile',
                            'profiles': url_list,
                            'progress': 0
                        }
                        
                        # Führe Profil-Scraping durch
                        results = integrated_scraper.run_profile_scraping(url_list)
                        
                        # Exportiere Ergebnisse
                        json_file = integrated_scraper.export_results_to_json(results, f"results_{job_id}.json")
                        report_file = integrated_scraper.generate_report(results, f"report_{job_id}.txt")
                        
                        # Aktualisiere Job-Status
                        running_jobs[job_id] = {
                            'status': 'completed',
                            'start_time': running_jobs[job_id]['start_time'],
                            'end_time': datetime.now().isoformat(),
                            'mode': 'profile',
                            'profiles': url_list,
                            'results': {
                                'total_profiles': results['report']['total_profiles_found'],
                                'suspicious_profiles': results['report']['suspicious_profiles_found'],
                                'screenshots': results['report']['screenshots_created']
                            },
                            'files': {
                                'json': json_file,
                                'report': report_file
                            }
                        }
                        
                        logger.info(f"Job {job_id} abgeschlossen")
                        
                    except Exception as e:
                        logger.error(f"Fehler bei Job {job_id}: {e}")
                        
                        # Aktualisiere Job-Status bei Fehler
                        running_jobs[job_id] = {
                            'status': 'error',
                            'start_time': running_jobs[job_id]['start_time'],
                            'end_time': datetime.now().isoformat(),
                            'mode': 'profile',
                            'profiles': url_list,
                            'error': str(e)
                        }
                
                # Starte den Thread
                thread = threading.Thread(target=run_job)
                thread.daemon = True
                thread.start()
                
                return redirect(url_for('index'))
        
        # Prüfe, ob Dateien hochgeladen wurden
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename:
                # Speichere die Datei
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Verarbeite die Datei je nach Typ
                if filename.endswith('.txt'):
                    # Lese URLs aus der Textdatei
                    with open(filepath, 'r') as f:
                        url_list = [url.strip() for url in f.readlines() if url.strip()]
                    
                    if url_list:
                        # Starte einen Scraping-Job für die URLs
                        job_id = f"job_{int(time.time())}"
                        
                        # Starte den Scraping-Job in einem separaten Thread
                        import threading
                        
                        def run_job():
                            try:
                                # Aktualisiere Job-Status
                                running_jobs[job_id] = {
                                    'status': 'running',
                                    'start_time': datetime.now().isoformat(),
                                    'mode': 'profile',
                                    'profiles': url_list,
                                    'progress': 0
                                }
                                
                                # Führe Profil-Scraping durch
                                results = integrated_scraper.run_profile_scraping(url_list)
                                
                                # Exportiere Ergebnisse
                                json_file = integrated_scraper.export_results_to_json(results, f"results_{job_id}.json")
                                report_file = integrated_scraper.generate_report(results, f"report_{job_id}.txt")
                                
                                # Aktualisiere Job-Status
                                running_jobs[job_id] = {
                                    'status': 'completed',
                                    'start_time': running_jobs[job_id]['start_time'],
                                    'end_time': datetime.now().isoformat(),
                                    'mode': 'profile',
                                    'profiles': url_list,
                                    'results': {
                                        'total_profiles': results['report']['total_profiles_found'],
                                        'suspicious_profiles': results['report']['suspicious_profiles_found'],
                                        'screenshots': results['report']['screenshots_created']
                                    },
                                    'files': {
                                        'json': json_file,
                                        'report': report_file
                                    }
                                }
                                
                                logger.info(f"Job {job_id} abgeschlossen")
                                
                            except Exception as e:
                                logger.error(f"Fehler bei Job {job_id}: {e}")
                                
                                # Aktualisiere Job-Status bei Fehler
                                running_jobs[job_id] = {
                                    'status': 'error',
                                    'start_time': running_jobs[job_id]['start_time'],
                                    'end_time': datetime.now().isoformat(),
                                    'mode': 'profile',
                                    'profiles': url_list,
                                    'error': str(e)
                                }
                        
                        # Starte den Thread
                        thread = threading.Thread(target=run_job)
                        thread.daemon = True
                        thread.start()
                
                return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/jobs')
def jobs():
    """Seite zur Anzeige von Scraping-Jobs"""
    return render_template('jobs.html', jobs=running_jobs)

@app.route('/job/<job_id>')
def job_details(job_id):
    """Seite zur Anzeige von Details zu einem Scraping-Job"""
    if job_id in running_jobs:
        job = running_jobs[job_id]
        
        # Prüfe, ob Ergebnisdateien existieren
        json_file = None
        report_file = None
        
        if job['status'] == 'completed' and 'files' in job:
            json_file = job['files'].get('json')
            report_file = job['files'].get('report')
        
        return render_template(
            'job_details.html',
            job_id=job_id,
            job=job,
            json_file=json_file,
            report_file=report_file
        )
    else:
        return render_template('error.html', message=f"Job {job_id} nicht gefunden")

@app.route('/file/<path:filename>')
def serve_file(filename):
    """Liefert eine Datei aus"""
    return send_from_directory(os.path.dirname(os.path.abspath(filename)), os.path.basename(filename))

@app.errorhandler(404)
def page_not_found(e):
    """Fehlerseite für 404-Fehler"""
    return render_template('error.html', message="Seite nicht gefunden"), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Fehlerseite für 500-Fehler"""
    return render_template('error.html', message="Interner Serverfehler"), 500

def create_app():
    """Erstellt und konfiguriert die Flask-App"""
    return app

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='IRI® Legal Agent - Verbesserte Hauptanwendung')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Run the app
    app.run(host=args.host, port=args.port, debug=args.debug)
