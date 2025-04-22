# Deployment-Anleitung für IRI® Legal Agent

Diese Anleitung beschreibt den Prozess zum Deployment des IRI® Legal Agent auf render.com.

## Voraussetzungen

- Ein Konto bei [render.com](https://render.com)
- Ein GitHub-Repository mit dem IRI® Legal Agent Code
- API-Schlüssel für ScreenshotAPI, Monday.com und SendGrid (falls verwendet)

## Schritt 1: Vorbereitung des Codes

Stellen Sie sicher, dass Ihr Code die folgenden Dateien enthält:

- `wsgi.py`: WSGI-Einstiegspunkt für den Webserver
- `gunicorn_config.py`: Konfiguration für den Gunicorn-Server
- `requirements.txt`: Liste aller benötigten Abhängigkeiten
- `render.yaml`: Konfigurationsdatei für render.com (optional)

Die `requirements.txt` Datei sollte alle notwendigen Abhängigkeiten enthalten:

```
Flask==2.2.3
gunicorn==20.1.0
gevent==22.10.2
psycopg2-binary==2.9.5
SQLAlchemy==2.0.5
python-dotenv==1.0.0
requests==2.28.2
beautifulsoup4==4.11.2
lxml==4.9.2
Pillow==9.4.0
```

## Schritt 2: Erstellen eines neuen Web Service auf render.com

1. Melden Sie sich bei [render.com](https://render.com) an
2. Klicken Sie auf "New" und wählen Sie "Web Service"
3. Verbinden Sie Ihr GitHub-Repository oder wählen Sie "Deploy from existing repository"
4. Konfigurieren Sie den Web Service:
   - **Name**: `iri-legal-agent` (oder ein Name Ihrer Wahl)
   - **Environment**: `Python 3`
   - **Region**: Wählen Sie eine Region in der Nähe Ihrer Nutzer (z.B. `Frankfurt` für Deutschland)
   - **Branch**: `main` (oder der Branch, den Sie deployen möchten)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -c gunicorn_config.py wsgi:app`

## Schritt 3: Konfiguration der Umgebungsvariablen

Konfigurieren Sie die notwendigen Umgebungsvariablen unter "Environment":

- `DATABASE_URL`: URL für die Datenbankverbindung (wird automatisch konfiguriert, wenn Sie eine Render PostgreSQL-Datenbank verwenden)
- `SCREENSHOT_API_KEY`: Ihr API-Schlüssel für ScreenshotAPI
- `MONDAY_API_KEY`: Ihr API-Schlüssel für Monday.com (falls verwendet)
- `SENDGRID_API_KEY`: Ihr API-Schlüssel für SendGrid (falls verwendet)
- `SECRET_KEY`: Ein sicherer zufälliger String für die Flask-Anwendung
- `FLASK_ENV`: `production` für die Produktionsumgebung

## Schritt 4: Einrichtung einer Datenbank

1. Klicken Sie auf "New" und wählen Sie "PostgreSQL"
2. Konfigurieren Sie die Datenbank:
   - **Name**: `iri-legal-agent-db` (oder ein Name Ihrer Wahl)
   - **Region**: Wählen Sie dieselbe Region wie für Ihren Web Service
   - **PostgreSQL Version**: `14` (oder die neueste verfügbare Version)
3. Klicken Sie auf "Create Database"
4. Sobald die Datenbank erstellt wurde, gehen Sie zurück zu Ihrem Web Service
5. Unter "Environment" > "Environment Variables" sollten Sie die `DATABASE_URL` Variable sehen, die automatisch mit Ihrer neuen Datenbank verknüpft wurde

## Schritt 5: Deployment starten

1. Klicken Sie auf "Create Web Service"
2. Render wird nun Ihren Code bauen und deployen
3. Dieser Prozess kann einige Minuten dauern
4. Sie können den Fortschritt in den Logs verfolgen

## Schritt 6: Überprüfung des Deployments

1. Sobald das Deployment abgeschlossen ist, klicken Sie auf die URL Ihres Web Service
2. Die IRI® Legal Agent Anwendung sollte nun im Browser erscheinen
3. Überprüfen Sie, ob alle Funktionen korrekt arbeiten:
   - Dashboard wird angezeigt
   - Datenbankverbindung funktioniert
   - Scraping-Funktionen können gestartet werden
   - Screenshots können erstellt werden

## Schritt 7: Einrichtung einer benutzerdefinierten Domain (optional)

1. Gehen Sie zu Ihrem Web Service und klicken Sie auf "Settings"
2. Scrollen Sie nach unten zu "Custom Domain"
3. Klicken Sie auf "Add Custom Domain"
4. Geben Sie Ihre Domain ein (z.B. `iri-legal-agent.example.com`)
5. Folgen Sie den Anweisungen, um Ihre DNS-Einstellungen zu konfigurieren

## Fehlerbehebung

### 502 Bad Gateway Fehler

Wenn Sie einen 502 Bad Gateway Fehler erhalten, überprüfen Sie:

1. Die Logs Ihres Web Service auf Fehler
2. Ob alle erforderlichen Abhängigkeiten in `requirements.txt` enthalten sind
3. Ob der Start-Befehl korrekt ist
4. Ob die Umgebungsvariablen korrekt konfiguriert sind

### Datenbank-Verbindungsprobleme

Wenn die Anwendung keine Verbindung zur Datenbank herstellen kann:

1. Überprüfen Sie, ob die `DATABASE_URL` Umgebungsvariable korrekt ist
2. Stellen Sie sicher, dass Ihre Datenbank läuft und erreichbar ist
3. Überprüfen Sie, ob die Datenbank-Anmeldedaten korrekt sind

### Scraping-Probleme

Wenn das Scraping nicht funktioniert:

1. Überprüfen Sie, ob die API-Schlüssel korrekt konfiguriert sind
2. Stellen Sie sicher, dass die Anwendung Zugriff auf das Internet hat
3. Überprüfen Sie die Logs auf spezifische Fehlermeldungen

## Automatische Updates

Render unterstützt automatische Updates, wenn Sie Änderungen an Ihrem GitHub-Repository vornehmen:

1. Gehen Sie zu Ihrem Web Service und klicken Sie auf "Settings"
2. Scrollen Sie nach unten zu "Auto-Deploy"
3. Stellen Sie sicher, dass "Auto-Deploy" aktiviert ist

## Skalierung (für höhere Anforderungen)

Wenn Ihre Anwendung mehr Ressourcen benötigt:

1. Gehen Sie zu Ihrem Web Service und klicken Sie auf "Settings"
2. Scrollen Sie nach unten zu "Instance Type"
3. Wählen Sie einen größeren Instance-Typ aus dem Dropdown-Menü
4. Klicken Sie auf "Save Changes"

## Support

Bei Problemen mit dem Deployment wenden Sie sich bitte an:

- Render Support: [support.render.com](https://support.render.com)
- IRI® Legal Agent Support: support@example.com
