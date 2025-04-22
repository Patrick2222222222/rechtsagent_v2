# API-Konfigurationsdatei für IRI® Legal Agent

# ScreenshotAPI Konfiguration
SCREENSHOT_API = {
    "api_key": "YOUR_SCREENSHOT_API_KEY",  # Ersetzen Sie dies mit Ihrem tatsächlichen API-Schlüssel
    "base_url": "https://api.screenshotapi.net/screenshot",
    "output_format": "image",
    "default_width": 1280,
    "default_height": 1024,
    "full_page": True,
    "delay": 2000,  # Verzögerung in Millisekunden
    "fresh": True,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Monday.com API Konfiguration
MONDAY_API = {
    "api_key": "YOUR_MONDAY_API_KEY",  # Ersetzen Sie dies mit Ihrem tatsächlichen API-Schlüssel
    "base_url": "https://api.monday.com/v2",
    "board_id": "YOUR_BOARD_ID",  # ID des Monday.com Boards für Meldungen
    "group_id": "YOUR_GROUP_ID",  # ID der Gruppe innerhalb des Boards
    "status_column_id": "status",  # ID der Statusspalte
    "profile_column_id": "text",  # ID der Profilspalte
    "link_column_id": "link",  # ID der Linkspalte
    "screenshot_column_id": "file",  # ID der Dateispalte für Screenshots
    "date_column_id": "date",  # ID der Datumsspalte
}

# SendGrid E-Mail API Konfiguration
SENDGRID_API = {
    "api_key": "YOUR_SENDGRID_API_KEY",  # Ersetzen Sie dies mit Ihrem tatsächlichen API-Schlüssel
    "from_email": "notifications@example.com",  # Absender-E-Mail
    "from_name": "IRI Legal Agent",  # Absendername
    "template_id": "YOUR_TEMPLATE_ID",  # ID der E-Mail-Vorlage (optional)
}

# Gesundheitsämter Konfiguration
HEALTH_AUTHORITIES = [
    {
        "name": "Gesundheitsamt Berlin Mitte",
        "email": "gesundheitsamt@berlin-mitte.de",
        "phone": "+49 30 12345678",
        "address": "Beispielstraße 1, 10115 Berlin",
        "region": "Berlin"
    },
    {
        "name": "Gesundheitsamt München",
        "email": "gesundheitsamt@muenchen.de",
        "phone": "+49 89 12345678",
        "address": "Beispielstraße 1, 80331 München",
        "region": "München"
    },
    {
        "name": "Gesundheitsamt Hamburg",
        "email": "gesundheitsamt@hamburg.de",
        "phone": "+49 40 12345678",
        "address": "Beispielstraße 1, 20095 Hamburg",
        "region": "Hamburg"
    },
    # Fügen Sie weitere Gesundheitsämter nach Bedarf hinzu
]

# Scraping-Konfiguration
SCRAPING_CONFIG = {
    "max_results_per_platform": 50,  # Maximale Anzahl von Ergebnissen pro Plattform
    "max_posts_per_profile": 10,  # Maximale Anzahl von Posts pro Profil
    "search_delay": 2,  # Verzögerung zwischen Suchanfragen in Sekunden
    "request_timeout": 30,  # Timeout für HTTP-Anfragen in Sekunden
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "use_proxy": False,  # Ob Proxies verwendet werden sollen
    "proxies": [
        # Liste von Proxies im Format "http://user:pass@host:port"
        # "http://user:pass@host:port",
    ]
}

# Erkennungsalgorithmus-Konfiguration
DETECTION_CONFIG = {
    "min_risk_score": 50.0,  # Minimaler Risiko-Score für verdächtige Profile
    "min_commercial_score": 30.0,  # Minimaler kommerzieller Score
    "keyword_weight": 0.4,  # Gewichtung für Schlüsselwörter
    "price_weight": 0.3,  # Gewichtung für Preisangaben
    "contact_weight": 0.2,  # Gewichtung für Kontaktinformationen
    "location_weight": 0.1,  # Gewichtung für Standortangaben
}

# Datenbankverbindung
DATABASE_CONFIG = {
    "url": "postgresql://postgres:postgres@localhost:5432/iri_legal_agent",  # Ersetzen Sie dies mit Ihrer tatsächlichen Datenbankverbindung
    "pool_size": 5,  # Größe des Verbindungspools
    "max_overflow": 10,  # Maximale Anzahl von Verbindungen über den Pool hinaus
    "pool_timeout": 30,  # Timeout für Verbindungen aus dem Pool in Sekunden
    "pool_recycle": 1800,  # Zeit in Sekunden, nach der Verbindungen recycelt werden
}

# Flask-App-Konfiguration
FLASK_CONFIG = {
    "secret_key": "YOUR_SECRET_KEY",  # Ersetzen Sie dies mit einem sicheren Schlüssel
    "debug": True,  # Debug-Modus (für Produktion auf False setzen)
    "host": "0.0.0.0",  # Host für den Webserver
    "port": 5000,  # Port für den Webserver
    "upload_folder": "uploads",  # Verzeichnis für hochgeladene Dateien
    "screenshot_folder": "screenshots",  # Verzeichnis für Screenshots
    "max_content_length": 16 * 1024 * 1024,  # Maximale Upload-Größe (16 MB)
}
