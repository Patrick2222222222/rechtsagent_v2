# API-Konfigurationsanleitung für IRI® Legal Agent

Diese Anleitung erklärt, wie Sie die notwendigen API-Konfigurationen für den IRI® Legal Agent einrichten.

## Übersicht der benötigten API-Schlüssel

Der IRI® Legal Agent benötigt folgende API-Schlüssel für die volle Funktionalität:

1. **ScreenshotAPI**: Für die Erstellung von Screenshots als Beweismaterial
2. **Monday.com API**: Für die Integration mit Monday.com (optional)
3. **SendGrid API**: Für E-Mail-Benachrichtigungen (optional)

## Schritt 1: Umgebungsvariablen einrichten

1. Kopieren Sie die Datei `.env.example` zu `.env`:
   ```
   cp .env.example .env
   ```

2. Öffnen Sie die `.env` Datei und tragen Sie Ihre API-Schlüssel ein:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/iri_legal_agent
   SCREENSHOT_API_KEY=your_screenshot_api_key_here
   MONDAY_API_KEY=your_monday_api_key_here
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

## Schritt 2: API-Konfigurationsdatei anpassen

1. Öffnen Sie die Datei `api_config.py`
2. Ersetzen Sie die Platzhalter mit Ihren tatsächlichen API-Schlüsseln und Konfigurationen:
   ```python
   # ScreenshotAPI Konfiguration
   SCREENSHOT_API = {
       "api_key": "YOUR_SCREENSHOT_API_KEY",  # Ersetzen Sie dies
       ...
   }

   # Monday.com API Konfiguration
   MONDAY_API = {
       "api_key": "YOUR_MONDAY_API_KEY",  # Ersetzen Sie dies
       "board_id": "YOUR_BOARD_ID",  # Ersetzen Sie dies
       ...
   }

   # SendGrid E-Mail API Konfiguration
   SENDGRID_API = {
       "api_key": "YOUR_SENDGRID_API_KEY",  # Ersetzen Sie dies
       ...
   }
   ```

## Schritt 3: API-Schlüssel beschaffen

### ScreenshotAPI

1. Besuchen Sie [ScreenshotAPI.net](https://screenshotapi.net/)
2. Erstellen Sie ein Konto und wählen Sie einen Plan
3. Kopieren Sie Ihren API-Schlüssel aus dem Dashboard

### Monday.com API (optional)

1. Melden Sie sich bei [Monday.com](https://monday.com/) an
2. Gehen Sie zu "Entwicklereinstellungen" > "API"
3. Generieren Sie einen API-Schlüssel
4. Notieren Sie sich die Board-ID und andere erforderliche IDs

### SendGrid API (optional)

1. Erstellen Sie ein Konto bei [SendGrid](https://sendgrid.com/)
2. Gehen Sie zu "Settings" > "API Keys"
3. Erstellen Sie einen neuen API-Schlüssel mit den erforderlichen Berechtigungen

## Schritt 4: Konfiguration testen

1. Starten Sie die Anwendung:
   ```
   python improved_app.py
   ```

2. Überprüfen Sie die Logs auf Fehler im Zusammenhang mit API-Konfigurationen

3. Testen Sie die Screenshot-Funktion, um zu überprüfen, ob die ScreenshotAPI korrekt konfiguriert ist

## Fehlerbehebung

### ScreenshotAPI-Fehler

Wenn Screenshots nicht erstellt werden können:
- Überprüfen Sie, ob der API-Schlüssel korrekt ist
- Stellen Sie sicher, dass Ihr Plan ausreichend API-Aufrufe erlaubt
- Überprüfen Sie die Netzwerkverbindung

### Monday.com-Integrationsfehler

Wenn die Monday.com-Integration nicht funktioniert:
- Überprüfen Sie, ob der API-Schlüssel korrekt ist
- Stellen Sie sicher, dass die Board-ID und andere IDs korrekt sind
- Überprüfen Sie, ob Sie die erforderlichen Berechtigungen haben

### SendGrid-Fehler

Wenn E-Mails nicht gesendet werden können:
- Überprüfen Sie, ob der API-Schlüssel korrekt ist
- Stellen Sie sicher, dass die Absender-E-Mail verifiziert ist
- Überprüfen Sie die SendGrid-Logs auf spezifische Fehlermeldungen

## Wichtige Hinweise

- Bewahren Sie Ihre API-Schlüssel sicher auf und teilen Sie sie nicht
- Die `.env` Datei sollte nicht in das Git-Repository aufgenommen werden (sie ist bereits in .gitignore)
- Für die Produktion sollten Sie sichere Umgebungsvariablen in render.com konfigurieren, anstatt die Schlüssel direkt im Code zu speichern
