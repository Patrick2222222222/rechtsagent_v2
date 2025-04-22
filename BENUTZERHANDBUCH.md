# Benutzerhandbuch für IRI® Legal Agent

Dieses Handbuch bietet eine umfassende Anleitung zur Verwendung des IRI® Legal Agent, einem System zur Erkennung und Dokumentation von nicht-lizenzierten kosmetischen Behandlungen in Deutschland.

## Inhaltsverzeichnis

1. [Einführung](#einführung)
2. [Dashboard](#dashboard)
3. [Suche](#suche)
4. [Profile](#profile)
5. [Screenshots](#screenshots)
6. [Jobs](#jobs)
7. [Upload](#upload)
8. [Häufig gestellte Fragen](#häufig-gestellte-fragen)

## Einführung

Der IRI® Legal Agent ist ein spezialisiertes Tool zur Identifizierung und Dokumentation von nicht-lizenzierten kosmetischen Behandlungen, insbesondere Hyaluron-Pen-Angeboten, in sozialen Medien und auf Websites. Das System durchsucht verschiedene Plattformen, erkennt verdächtige Inhalte, erstellt Screenshots als Beweismaterial und verwaltet alle Informationen in einer Datenbank.

### Hauptfunktionen

- Automatisiertes Scraping von Instagram, Facebook, TikTok, Google und Websites
- Erkennung von Hyaluron-Pen-Angeboten durch fortschrittliche Algorithmen
- Erstellung von Screenshots als rechtssicheres Beweismaterial
- Verwaltung von Profilen, Posts und Screenshots in einer Datenbank
- Benutzerfreundliche Weboberfläche zur Steuerung und Überwachung

## Dashboard

Das Dashboard bietet einen Überblick über die wichtigsten Statistiken und neuesten Ergebnisse.

### Elemente des Dashboards

- **Statistik-Karten**: Zeigen die Anzahl der gefundenen Profile, verdächtigen Profile, gemeldeten Profile und Screenshots
- **Laufende Jobs**: Liste der aktuell laufenden Scraping-Jobs mit Status und Fortschritt
- **Neueste verdächtige Profile**: Übersicht über die zuletzt gefundenen verdächtigen Profile
- **Plattform-Statistiken**: Grafische Darstellung der Profile pro Plattform

### Aktionen auf dem Dashboard

- **Neue Suche starten**: Klicken Sie auf "Neue Suche", um zur Suchseite zu gelangen
- **URL hochladen**: Klicken Sie auf "URL hochladen", um zur Upload-Seite zu gelangen
- **Vollständiges Scraping starten**: Klicken Sie auf "Vollständiges Scraping starten", um einen umfassenden Scraping-Durchlauf zu starten
- **Profil melden**: Klicken Sie auf "Melden" bei einem verdächtigen Profil, um es als gemeldet zu markieren

## Suche

Die Suchseite ermöglicht das Starten verschiedener Arten von Scraping-Durchläufen.

### Suchoptionen

- **Vollständige Suche**: Durchsucht alle Plattformen mit allen Suchbegriffen
  - Wählen Sie die zu durchsuchenden Plattformen aus
  - Klicken Sie auf "Vollständige Suche starten"

- **Gezielte Suche**: Durchsucht ausgewählte Plattformen mit bestimmten Suchbegriffen
  - Wählen Sie die zu durchsuchenden Plattformen aus
  - Wählen Sie die zu verwendenden Suchbegriffe aus
  - Klicken Sie auf "Gezielte Suche starten"

- **Profil-Suche**: Durchsucht bestimmte Profile auf verdächtige Inhalte
  - Geben Sie die URLs der zu durchsuchenden Profile ein
  - Klicken Sie auf "Profil-Suche starten"

### Verfügbare Suchbegriffe

Die Suchseite zeigt auch eine Übersicht aller verfügbaren Suchbegriffe:

- **Hashtags**: Relevante Hashtags für soziale Medien
- **Keywords**: Allgemeine Suchbegriffe
- **Standorte**: Standortbezogene Suchbegriffe
- **Accounts**: Bekannte Instagram-, Facebook- und TikTok-Accounts

## Profile

Die Profilseite zeigt alle gefundenen Profile mit verdächtigen Inhalten.

### Funktionen

- **Filterung**: Filtern Sie Profile nach Plattform, Risiko-Score oder Status
- **Sortierung**: Sortieren Sie Profile nach verschiedenen Kriterien
- **Detailansicht**: Klicken Sie auf ein Profil, um detaillierte Informationen anzuzeigen
- **Melden**: Markieren Sie Profile als gemeldet
- **Export**: Exportieren Sie Profildaten als CSV oder JSON

### Profildetails

Die Detailansicht eines Profils zeigt:

- **Allgemeine Informationen**: Name, Plattform, Link, Beschreibung
- **Risikobewertung**: Risiko-Score und Faktoren
- **Posts**: Liste der gefundenen Posts mit verdächtigen Inhalten
- **Screenshots**: Erstellte Screenshots des Profils und der Posts
- **Verlauf**: Zeitlicher Verlauf der Entdeckung und Überprüfung

## Screenshots

Die Screenshot-Seite zeigt alle erstellten Screenshots als Beweismaterial.

### Funktionen

- **Filterung**: Filtern Sie Screenshots nach Profil, Plattform oder Datum
- **Sortierung**: Sortieren Sie Screenshots nach verschiedenen Kriterien
- **Vorschau**: Klicken Sie auf einen Screenshot, um ihn in voller Größe anzuzeigen
- **Download**: Laden Sie Screenshots herunter
- **Export**: Exportieren Sie Screenshot-Metadaten als CSV oder JSON

### Screenshot-Details

Die Detailansicht eines Screenshots zeigt:

- **Bild**: Der Screenshot in voller Größe
- **Metadaten**: URL, Erstellungsdatum, Größe, Format
- **Zugehöriges Profil**: Link zum zugehörigen Profil
- **Zugehöriger Post**: Link zum zugehörigen Post (falls vorhanden)
- **Analyseergebnisse**: Ergebnisse der automatischen Bildanalyse

## Jobs

Die Jobs-Seite zeigt alle laufenden und abgeschlossenen Scraping-Jobs.

### Funktionen

- **Übersicht**: Liste aller Jobs mit Status, Startzeit und Fortschritt
- **Filterung**: Filtern Sie Jobs nach Status, Typ oder Datum
- **Detailansicht**: Klicken Sie auf einen Job, um detaillierte Informationen anzuzeigen
- **Abbrechen**: Brechen Sie laufende Jobs ab
- **Erneut starten**: Starten Sie abgeschlossene Jobs erneut

### Job-Details

Die Detailansicht eines Jobs zeigt:

- **Allgemeine Informationen**: ID, Typ, Status, Start- und Endzeit
- **Parameter**: Verwendete Plattformen, Suchbegriffe oder Profile
- **Ergebnisse**: Anzahl der gefundenen Profile, verdächtigen Profile und Screenshots
- **Logs**: Detaillierte Logs des Jobs
- **Exportierte Dateien**: Links zu exportierten JSON- und Berichtsdateien

## Upload

Die Upload-Seite ermöglicht das Hochladen von URLs oder Dateien für die Analyse.

### Funktionen

- **URL-Upload**: Geben Sie URLs direkt ein
  - Geben Sie eine URL pro Zeile ein
  - Klicken Sie auf "URLs analysieren"

- **Datei-Upload**: Laden Sie Dateien mit URLs hoch
  - Wählen Sie eine Textdatei mit URLs (eine pro Zeile)
  - Klicken Sie auf "Datei hochladen"

- **Batch-Verarbeitung**: Verarbeiten Sie mehrere URLs gleichzeitig
  - Geben Sie mehrere URLs ein oder laden Sie eine Datei mit mehreren URLs hoch
  - Klicken Sie auf "Batch-Verarbeitung starten"

## Häufig gestellte Fragen

### Allgemeine Fragen

**F: Wie oft sollte ich einen Scraping-Durchlauf starten?**

A: Die optimale Häufigkeit hängt von Ihren spezifischen Anforderungen ab. Für eine kontinuierliche Überwachung empfehlen wir tägliche oder wöchentliche Durchläufe. Bei gezielten Untersuchungen können Sie nach Bedarf Durchläufe starten.

**F: Wie lange dauert ein vollständiger Scraping-Durchlauf?**

A: Die Dauer hängt von der Anzahl der Plattformen, Suchbegriffe und der Internetverbindung ab. Ein vollständiger Durchlauf kann zwischen 30 Minuten und mehreren Stunden dauern.

**F: Sind die erstellten Screenshots rechtlich verwertbar?**

A: Ja, die Screenshots werden mit Metadaten wie URL, Datum und Uhrzeit versehen, um ihre Authentizität zu belegen. Sie können als Beweismaterial in rechtlichen Verfahren verwendet werden.

### Technische Fragen

**F: Was tun, wenn ein Scraping-Job fehlschlägt?**

A: Überprüfen Sie die Job-Details und Logs auf spezifische Fehlermeldungen. Häufige Ursachen sind Netzwerkprobleme, Änderungen an den Zielplattformen oder fehlende API-Schlüssel. Sie können den Job mit angepassten Parametern erneut starten.

**F: Kann ich eigene Suchbegriffe hinzufügen?**

A: Ja, Sie können die Datei `expanded_search_terms.py` bearbeiten, um eigene Suchbegriffe hinzuzufügen. Nach dem Neustart der Anwendung werden die neuen Begriffe verfügbar sein.

**F: Wie kann ich die Ergebnisse exportieren?**

A: Auf den Seiten für Profile, Screenshots und Jobs finden Sie Export-Optionen. Sie können Daten als CSV oder JSON exportieren und Berichte als PDF generieren.

### Datenschutz und rechtliche Fragen

**F: Werden die gesammelten Daten DSGVO-konform gespeichert?**

A: Ja, alle gesammelten Daten werden DSGVO-konform gespeichert. Die Anwendung speichert nur öffentlich zugängliche Informationen und verwendet sie ausschließlich zum Zweck der Identifizierung nicht-lizenzierter kosmetischer Behandlungen.

**F: Darf ich die gesammelten Informationen an Behörden weitergeben?**

A: Ja, die gesammelten Informationen dürfen an zuständige Behörden wie Gesundheitsämter oder Gewerbeaufsichtsämter weitergegeben werden, um auf potenzielle Verstöße gegen das Heilpraktikergesetz oder andere relevante Vorschriften hinzuweisen.

**F: Wie lange werden die Daten gespeichert?**

A: Die Daten werden standardmäßig für 12 Monate gespeichert. Sie können die Aufbewahrungsfrist in den Einstellungen anpassen, sollten jedoch sicherstellen, dass relevante Beweise für mögliche rechtliche Verfahren ausreichend lange aufbewahrt werden.
