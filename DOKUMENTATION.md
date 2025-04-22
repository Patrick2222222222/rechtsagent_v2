# IRI® Legal Agent - Dokumentation

## Übersicht

Der IRI® Legal Agent ist ein System zur Erkennung und Dokumentation von nicht-lizenzierten kosmetischen Behandlungen in Deutschland, insbesondere Hyaluron-Pen-Angeboten. Diese Dokumentation beschreibt die verbesserte Version des Systems mit erweiterter Scraping-Funktionalität, Datenbankintegration und einer benutzerfreundlichen Weboberfläche.

## Inhaltsverzeichnis

1. [Systemarchitektur](#systemarchitektur)
2. [Komponenten](#komponenten)
3. [Datenbankschema](#datenbankschema)
4. [Scraping-Funktionalität](#scraping-funktionalität)
5. [Erkennungsalgorithmen](#erkennungsalgorithmen)
6. [Screenshot-Dienst](#screenshot-dienst)
7. [Weboberfläche](#weboberfläche)
8. [API-Endpunkte](#api-endpunkte)
9. [Installation und Konfiguration](#installation-und-konfiguration)
10. [Deployment-Anleitung](#deployment-anleitung)
11. [Fehlerbehebung](#fehlerbehebung)

## Systemarchitektur

Das System basiert auf einer modularen Architektur mit folgenden Hauptkomponenten:

- **Datenbankschicht**: PostgreSQL-Datenbank zur Speicherung von Profilen, Posts, Screenshots und Suchergebnissen
- **Scraping-Schicht**: Spezialisierte Scraper für verschiedene Plattformen (Instagram, Facebook, TikTok, Google, Websites)
- **Erkennungsschicht**: Algorithmen zur Identifizierung verdächtiger Inhalte
- **Screenshot-Schicht**: Dienst zur Erstellung und Verwaltung von Screenshots als Beweismaterial
- **Anwendungsschicht**: Flask-Webanwendung mit Benutzeroberfläche und API-Endpunkten
- **Deployment-Schicht**: Konfiguration für das Deployment auf render.com

Die Komponenten kommunizieren über definierte Schnittstellen miteinander und können unabhängig voneinander aktualisiert oder ersetzt werden.

## Komponenten

### Hauptkomponenten

- **database_schema.py**: Definiert das Datenbankschema mit SQLAlchemy ORM
- **database_manager.py**: Verwaltet die Datenbankverbindung und -operationen
- **expanded_search_terms.py**: Enthält erweiterte Listen von Suchbegriffen
- **platform_scraper.py**: Implementiert spezialisierte Scraper für verschiedene Plattformen
- **detection_algorithms.py**: Enthält Algorithmen zur Erkennung verdächtiger Inhalte
- **screenshot_service.py**: Dienst zur Erstellung und Verwaltung von Screenshots
- **integrated_scraper.py**: Integriert alle Komponenten für koordinierte Scraping-Operationen
- **improved_app.py**: Flask-Webanwendung mit Benutzeroberfläche und API-Endpunkten
- **test_scraper.py**: Test-Skript zur Überprüfung der Funktionalität
- **wsgi.py**: WSGI-Einstiegspunkt für Produktionsserver
- **gunicorn_config.py**: Konfiguration für den Gunicorn-Server
- **render.yaml**: Konfiguration für das Deployment auf render.com

### Unterstützende Dateien

- **requirements.txt**: Liste der erforderlichen Python-Pakete
- **templates/**: HTML-Templates für die Weboberfläche
- **static/**: Statische Dateien (CSS, JavaScript, Bilder)
- **.env**: Umgebungsvariablen (nicht im Repository enthalten)

## Datenbankschema

Das Datenbankschema umfasst folgende Haupttabellen:

- **Platforms**: Speichert Informationen zu den verschiedenen Plattformen
- **Profiles**: Erfasst gefundene Profile/Accounts mit Verdacht auf nicht-lizenzierte Hyaluron-Pen-Angebote
- **Posts**: Speichert einzelne Beiträge mit relevanten Inhalten
- **Screenshots**: Verwaltet die erstellten Screenshots als Beweismaterial
- **SearchTerms**: Enthält eine erweiterte Liste von Suchbegriffen
- **SearchLogs**: Protokolliert alle Suchvorgänge für Analysen
- **HealthAuthorities**: Speichert Informationen zu Gesundheitsämtern
- **Reports**: Verfolgt Meldungen an Behörden

Beziehungen zwischen den Tabellen:
- Ein Profil gehört zu einer Plattform (1:n)
- Ein Profil kann mehrere Posts haben (1:n)
- Ein Profil oder Post kann mehrere Screenshots haben (1:n)
- Eine Suche verwendet mehrere Suchbegriffe (n:m)
- Ein Profil kann an mehrere Behörden gemeldet werden (n:m)

## Scraping-Funktionalität

Die Scraping-Funktionalität wurde erheblich verbessert und umfasst nun:

### Unterstützte Plattformen

- **Instagram**: Suche nach Profilen, Hashtags und Beiträgen
- **Facebook**: Suche nach Seiten, Gruppen und Beiträgen
- **TikTok**: Suche nach Profilen, Hashtags und Videos
- **Google**: Suche nach relevanten Websites und Einträgen
- **Websites**: Direktes Scraping von bekannten Websites

### Suchmodi

- **Vollständige Suche**: Durchsucht alle Plattformen mit allen Suchbegriffen
- **Gezielte Suche**: Durchsucht ausgewählte Plattformen mit bestimmten Suchbegriffen
- **Profil-Suche**: Durchsucht bestimmte Profile auf verdächtige Inhalte

### Erweiterte Suchbegriffe

Die Suchbegriffe wurden in verschiedene Kategorien unterteilt:
- **Hashtags**: z.B. #hyaluronpen, #lippenaufspritzen
- **Keywords**: z.B. "Hyaluron Pen", "Lippen aufspritzen ohne Nadel"
- **Standorte**: z.B. "Berlin", "München", "Hamburg"
- **Accounts**: Bekannte Instagram-, Facebook- und TikTok-Accounts

## Erkennungsalgorithmen

Die Erkennungsalgorithmen wurden verbessert, um die Genauigkeit der Identifizierung verdächtiger Inhalte zu erhöhen:

### Textanalyse

- **Keyword-Erkennung**: Identifiziert relevante Schlüsselwörter und Phrasen
- **Preiserkennung**: Erkennt Preisangaben für Behandlungen
- **Kontaktdatenerkennung**: Identifiziert E-Mail-Adressen und Telefonnummern
- **Standorterkennung**: Erkennt Standortangaben

### Bildanalyse

- **Bildklassifizierung**: Erkennt Bilder von Hyaluron-Pen-Behandlungen
- **Texterkennung in Bildern**: Extrahiert Text aus Bildern für weitere Analyse

### Risikobewertung

- **Kommerzieller Score**: Bewertet die kommerzielle Natur des Angebots
- **Risiko-Score**: Bewertet das Gesamtrisiko basierend auf verschiedenen Faktoren
- **Vertrauenswürdigkeit**: Bewertet die Vertrauenswürdigkeit der Quelle

## Screenshot-Dienst

Der Screenshot-Dienst wurde optimiert, um zuverlässigere und umfassendere Beweise zu sammeln:

### Funktionen

- **Standard-Screenshots**: Erstellt Screenshots von Profilen und Beiträgen
- **Selenium-Screenshots**: Verwendet Selenium für dynamische Inhalte
- **Mobile-Screenshots**: Erstellt Screenshots in mobiler Ansicht
- **Mehrfach-Screenshots**: Erstellt mehrere Screenshots mit verschiedenen Einstellungen

### Integration

- **Datenbankintegration**: Speichert Screenshots in der Datenbank mit Metadaten
- **Analyse-Integration**: Analysiert Screenshots auf verdächtige Inhalte
- **API-Integration**: Verwendet externe Screenshot-APIs für bessere Qualität

## Weboberfläche

Die Weboberfläche bietet eine benutzerfreundliche Schnittstelle zur Verwaltung des Systems:

### Hauptfunktionen

- **Dashboard**: Übersicht über Statistiken und neueste verdächtige Profile
- **Suche**: Schnittstelle zum Starten verschiedener Suchvorgänge
- **Profile**: Anzeige und Verwaltung gefundener Profile
- **Screenshots**: Anzeige und Verwaltung erstellter Screenshots
- **Jobs**: Überwachung laufender und abgeschlossener Scraping-Jobs
- **Upload**: Hochladen von URLs oder Dateien für die Analyse

### Benutzeroberfläche

- **Responsive Design**: Optimiert für Desktop- und Mobile-Geräte
- **Bootstrap-Framework**: Moderne und benutzerfreundliche Oberfläche
- **Interaktive Elemente**: Dynamische Formulare und Visualisierungen

## API-Endpunkte

Die Anwendung bietet verschiedene API-Endpunkte für die Integration mit anderen Systemen:

### Hauptendpunkte

- **/api/run_scraping**: Startet einen Scraping-Job
- **/api/job_status/<job_id>**: Ruft den Status eines Scraping-Jobs ab
- **/api/search_terms**: Ruft verfügbare Suchbegriffe ab
- **/api/statistics**: Ruft Statistiken aus der Datenbank ab
- **/api/profiles**: Ruft Profile aus der Datenbank ab
- **/api/analyze_url**: Analysiert eine URL auf verdächtige Inhalte
- **/api/report_profile**: Meldet ein Profil als verdächtig

### Verwendung

Alle API-Endpunkte verwenden JSON für Anfragen und Antworten. Beispiel:

```json
// Anfrage an /api/run_scraping
{
  "mode": "targeted",
  "platforms": ["Instagram", "Facebook"],
  "terms": ["hyaluron pen", "lippen aufspritzen"]
}

// Antwort
{
  "success": true,
  "job_id": "job_1650123456",
  "message": "Scraping-Job gestartet (ID: job_1650123456)"
}
```

## Installation und Konfiguration

### Voraussetzungen

- Python 3.8 oder höher
- PostgreSQL-Datenbank
- Pip (Python-Paketmanager)
- Git (für den Zugriff auf das Repository)

### Installation

1. Repository klonen:
   ```
   git clone https://github.com/username/iri-legal-agent.git
   cd iri-legal-agent
   ```

2. Virtuelle Umgebung erstellen und aktivieren:
   ```
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   ```

3. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```

4. Umgebungsvariablen konfigurieren:
   ```
   cp .env.example .env
   # Bearbeiten Sie die .env-Datei mit Ihren Einstellungen
   ```

5. Datenbank initialisieren:
   ```
   python -c "from database_manager import DatabaseManager; DatabaseManager().init_default_data()"
   ```

### Konfiguration

Die Anwendung kann über Umgebungsvariablen konfiguriert werden:

- **DATABASE_URL**: URL für die Datenbankverbindung
- **SCREENSHOT_API_KEY**: API-Schlüssel für den Screenshot-Dienst
- **SECRET_KEY**: Geheimer Schlüssel für die Flask-Anwendung
- **DEBUG**: Debug-Modus aktivieren (True/False)
- **PORT**: Port für den Webserver

## Deployment-Anleitung

### Lokales Deployment

1. Starten Sie die Anwendung:
   ```
   python improved_app.py
   ```

2. Öffnen Sie die Anwendung im Browser:
   ```
   http://localhost:5000
   ```

### Deployment auf render.com

1. Erstellen Sie ein neues Web Service auf render.com.

2. Verbinden Sie Ihr GitHub-Repository.

3. Konfigurieren Sie den Dienst:
   - **Name**: iri-legal-agent
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -c gunicorn_config.py wsgi:app`

4. Konfigurieren Sie Umgebungsvariablen:
   - **DATABASE_URL**: URL für die Datenbankverbindung
   - **SCREENSHOT_API_KEY**: API-Schlüssel für den Screenshot-Dienst
   - **SECRET_KEY**: Geheimer Schlüssel für die Flask-Anwendung

5. Klicken Sie auf "Create Web Service".

6. Warten Sie, bis das Deployment abgeschlossen ist.

7. Öffnen Sie die bereitgestellte URL.

## Fehlerbehebung

### Häufige Probleme

#### Datenbankverbindungsfehler

**Problem**: Die Anwendung kann keine Verbindung zur Datenbank herstellen.

**Lösung**:
1. Überprüfen Sie die DATABASE_URL-Umgebungsvariable.
2. Stellen Sie sicher, dass die Datenbank läuft und erreichbar ist.
3. Überprüfen Sie Firewall-Einstellungen.

#### Screenshot-Fehler

**Problem**: Screenshots können nicht erstellt werden.

**Lösung**:
1. Überprüfen Sie den SCREENSHOT_API_KEY.
2. Stellen Sie sicher, dass das Screenshot-Verzeichnis beschreibbar ist.
3. Prüfen Sie die Logs auf spezifische Fehlermeldungen.

#### Scraping-Fehler

**Problem**: Scraping-Jobs schlagen fehl oder liefern keine Ergebnisse.

**Lösung**:
1. Überprüfen Sie die Internetverbindung.
2. Prüfen Sie, ob die Zielplattformen erreichbar sind.
3. Überprüfen Sie die Logs auf spezifische Fehlermeldungen.
4. Stellen Sie sicher, dass die Suchbegriffe korrekt sind.

#### Deployment-Fehler

**Problem**: Die Anwendung kann nicht auf render.com bereitgestellt werden.

**Lösung**:
1. Überprüfen Sie die Build-Logs auf Fehler.
2. Stellen Sie sicher, dass alle erforderlichen Dateien im Repository vorhanden sind.
3. Überprüfen Sie die Umgebungsvariablen.
4. Stellen Sie sicher, dass die Start-Befehle korrekt sind.

### Support

Bei weiteren Problemen wenden Sie sich bitte an den Support unter support@example.com oder erstellen Sie ein Issue im GitHub-Repository.
