# IRI® Legal Agent - Vollständige Dokumentation

## Übersicht

Der IRI® Legal Agent ist ein automatisiertes System zur Erkennung und Dokumentation von nicht-lizenzierten kosmetischen Behandlungen mit "Hyaluron Pens" in Deutschland. Das System durchsucht soziale Medien nach verdächtigen Angeboten, erstellt Screenshots als Beweismaterial und dokumentiert die Fälle in einem Monday.com-Board.

## Inhaltsverzeichnis

1. [Installation und Einrichtung](#installation-und-einrichtung)
2. [API-Schlüssel konfigurieren](#api-schlüssel-konfigurieren)
3. [Funktionsweise](#funktionsweise)
4. [Komponenten](#komponenten)
5. [Verwendung](#verwendung)
6. [Fehlerbehebung](#fehlerbehebung)
7. [Rechtliche Grundlagen](#rechtliche-grundlagen)

## Installation und Einrichtung

### Systemanforderungen

- Python 3.8 oder höher
- Internetverbindung
- API-Schlüssel für ScreenshotAPI.net, Monday.com und optional SendGrid

### Installation

1. Entpacken Sie die ZIP-Datei in ein Verzeichnis Ihrer Wahl
2. Öffnen Sie eine Kommandozeile und navigieren Sie zu diesem Verzeichnis
3. Installieren Sie die erforderlichen Python-Pakete:

```bash
pip install -r requirements.txt
```

## API-Schlüssel konfigurieren

Der IRI® Legal Agent benötigt API-Schlüssel für verschiedene Dienste. Diese können auf zwei Arten konfiguriert werden:

### Methode 1: .env-Datei

Erstellen Sie eine Datei namens `.env` im Hauptverzeichnis mit folgendem Inhalt:

```
SCREENSHOT_API_KEY=Ihr_ScreenshotAPI_Schlüssel
MONDAY_API_KEY=Ihr_Monday_API_Schlüssel
SENDGRID_API_KEY=Ihr_SendGrid_API_Schlüssel
```

### Methode 2: Konfigurationsdatei importieren

1. Erstellen Sie eine JSON-Datei mit folgendem Format:

```json
{
  "screenshot_api_key": "Ihr_ScreenshotAPI_Schlüssel",
  "monday_api_key": "Ihr_Monday_API_Schlüssel",
  "sendgrid_api_key": "Ihr_SendGrid_API_Schlüssel"
}
```

2. Importieren Sie die Datei mit dem Befehl:

```bash
python iri_legal_agent.py --import-config pfad/zur/config.json
```

## Funktionsweise

Der IRI® Legal Agent arbeitet in drei Phasen:

### Phase 1: Erkennung & Dokumentation

- Suche auf Instagram, TikTok und Google nach Posts & Profilen mit Suchbegriffen wie #hyaluronpen, #lippenaufspritzen, etc.
- Für jeden verdächtigen Beitrag wird ein Screenshot erstellt
- Extrahiert werden: Profilname, Beschreibung, Plattform, Link, E-Mail-Adresse, Ort

### Phase 2: Eintrag in Monday

- Die gefundenen Verdachtsfälle werden automatisch im Monday.com-Board "IRI® Verdachtsfälle" dokumentiert
- Für jeden Fall wird ein neuer Eintrag erstellt mit folgenden Spalten:
  - Name / Studio
  - Plattform
  - Profil-Link
  - Kommentar
  - Status
  - Letzter Schritt
  - E-Mail (optional)
  - Ort (optional)
- Der Screenshot wird als Update-Kommentar mit Beweistext und Bild angehängt

### Phase 3: Berechtigungsanfrage & Eskalation (optional)

- Wenn eine E-Mail-Adresse gefunden wurde, kann das System nach 24 Stunden automatisch eine Berechtigungsanfrage per E-Mail versenden
- Es wird eine Frist von 5 Tagen gesetzt
- Wenn keine Rückmeldung erfolgt, ermittelt das System das zuständige Gesundheitsamt und sendet eine Meldung mit Beweismaterial
- Der Status in Monday wird entsprechend aktualisiert

## Komponenten

Der IRI® Legal Agent besteht aus mehreren Komponenten:

### social_media_monitor.py

Diese Komponente ist für die Suche auf sozialen Medien zuständig. Sie verwendet verschiedene Techniken, um verdächtige Beiträge zu identifizieren:

- Instagram: Suche nach Hashtags und Profilen
- TikTok: Suche nach Videos und Profilen
- Google: Suche nach Websites mit relevanten Inhalten

### screenshot_service.py

Diese Komponente erstellt Screenshots von verdächtigen Beiträgen als Beweismaterial. Sie verwendet die ScreenshotAPI.net-API, um hochwertige Screenshots zu erstellen.

### monday_integration.py

Diese Komponente ist für die Integration mit Monday.com zuständig. Sie erstellt neue Einträge im Board "IRI® Verdachtsfälle" und fügt Screenshots als Update-Kommentare hinzu.

### email_notification.py

Diese optionale Komponente versendet E-Mail-Benachrichtigungen an Anbieter und Gesundheitsämter. Sie verwendet die SendGrid-API für den E-Mail-Versand.

### main.py

Dies ist die Hauptkomponente, die alle anderen Komponenten koordiniert und den vollständigen Workflow ausführt.

### iri_legal_agent.py

Dies ist eine benutzerfreundliche Oberfläche für die Kommandozeile, die es ermöglicht, den IRI® Legal Agent zu steuern und zu konfigurieren.

## Verwendung

### Vollständigen Workflow ausführen

Um den vollständigen Workflow auszuführen, verwenden Sie den folgenden Befehl:

```bash
python iri_legal_agent.py --run-workflow
```

### Nur Suche ausführen

Um nur die Suche auf sozialen Medien auszuführen, ohne Screenshots zu erstellen oder Einträge in Monday.com zu erstellen:

```bash
python iri_legal_agent.py --search-only
```

### Nur Screenshots erstellen

Um nur Screenshots von bereits gefundenen Beiträgen zu erstellen:

```bash
python iri_legal_agent.py --screenshot-only
```

### Nur Monday.com-Integration ausführen

Um nur die Integration mit Monday.com auszuführen, ohne neue Suchen durchzuführen:

```bash
python iri_legal_agent.py --monday-only
```

### E-Mail-Benachrichtigungen aktivieren

Um E-Mail-Benachrichtigungen zu aktivieren:

```bash
python iri_legal_agent.py --run-workflow --enable-email
```

### Suchbegriffe anpassen

Um eigene Suchbegriffe zu definieren:

```bash
python iri_legal_agent.py --run-workflow --search-terms "hyaluronpen,lippenaufspritzen,needlefreefiller"
```

### Hilfe anzeigen

Um alle verfügbaren Optionen anzuzeigen:

```bash
python iri_legal_agent.py --help
```

## Fehlerbehebung

### API-Schlüssel-Probleme

Wenn Sie Probleme mit API-Schlüsseln haben, überprüfen Sie Folgendes:

- Sind die API-Schlüssel korrekt in der .env-Datei oder der Konfigurationsdatei eingetragen?
- Haben die API-Schlüssel die erforderlichen Berechtigungen?
- Sind die API-Schlüssel noch gültig?

Sie können die API-Schlüssel mit folgendem Befehl überprüfen:

```bash
python iri_legal_agent.py --check-keys
```

### Netzwerkprobleme

Wenn Sie Netzwerkprobleme haben, überprüfen Sie Folgendes:

- Haben Sie eine aktive Internetverbindung?
- Werden die API-Endpunkte von einer Firewall blockiert?
- Sind die API-Dienste verfügbar?

### Monday.com-Integration

Wenn Sie Probleme mit der Monday.com-Integration haben, überprüfen Sie Folgendes:

- Existiert das Board "IRI® Verdachtsfälle" in Ihrem Monday.com-Workspace?
- Hat der API-Schlüssel die erforderlichen Berechtigungen für dieses Board?
- Sind die Spalten im Board korrekt konfiguriert?

## Rechtliche Grundlagen

Die Verwendung von Hyaluron Pens für kosmetische Behandlungen ist in Deutschland aus mehreren Gründen problematisch:

### Medizinprodukterechtliche Aspekte

Hyaluron Pens fallen unter das Medizinproduktegesetz (MPG) und die EU-Medizinprodukteverordnung (MDR). Die meisten auf dem Markt befindlichen Geräte verfügen nicht über eine gültige CE-Kennzeichnung als Medizinprodukt und dürfen daher nicht für medizinische oder kosmetische Behandlungen eingesetzt werden.

### Heilpraktiker- und Arztvorbehalte

Das Einbringen von Substanzen in die Haut mittels Druck (auch ohne Nadel) kann unter den Heilpraktiker- oder Arztvorbehalt fallen, insbesondere wenn dabei die Hautbarriere überwunden wird. Kosmetikerinnen ohne entsprechende Qualifikation dürfen solche Behandlungen nicht durchführen.

### Hygienevorschriften

Bei der Anwendung von Hyaluron Pens müssen strenge Hygienevorschriften eingehalten werden, um Infektionen zu vermeiden. Viele nicht-lizenzierte Anbieter erfüllen diese Vorschriften nicht.

### Zuständige Behörden

Für die Überwachung und Durchsetzung der rechtlichen Bestimmungen sind folgende Behörden zuständig:

- Gesundheitsämter: Überwachung der hygienischen Anforderungen und der Einhaltung des Heilpraktikergesetzes
- Gewerbeaufsichtsämter: Überwachung der gewerberechtlichen Bestimmungen
- Landesämter für Gesundheit und Soziales: Überwachung der Einhaltung des Medizinproduktegesetzes

Der IRI® Legal Agent unterstützt die zuständigen Behörden bei der Identifizierung von nicht-lizenzierten Anbietern von Hyaluron Pen Behandlungen und liefert Beweismaterial für mögliche Verstöße.
