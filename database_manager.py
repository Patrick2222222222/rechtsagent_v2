#!/usr/bin/env python3
# database_manager.py - Datenbankmanager für IRI® Legal Agent

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_schema import Base, Platform, Profile, Post, Screenshot, SearchTerm, SearchLog, HealthAuthority, Report
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

class DatabaseManager:
    """Klasse zur Verwaltung der Datenbankoperationen für den IRI® Legal Agent"""
    
    def __init__(self, db_url=None):
        """
        Initialisiert den DatabaseManager
        
        Args:
            db_url: Die Datenbank-URL. Wenn None, wird die URL aus der Umgebungsvariable oder dem Standard verwendet.
        """
        # Verwende die angegebene URL oder die aus der Umgebungsvariable oder den Standard
        self.db_url = db_url or os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/iri_legal_agent"
        
        # Für SQLite (Entwicklung/Tests)
        if self.db_url.startswith("sqlite"):
            self.engine = create_engine(self.db_url)
        else:
            # Für PostgreSQL (Produktion)
            self.engine = create_engine(self.db_url, pool_size=10, max_overflow=20)
        
        # Erstelle alle Tabellen, falls sie nicht existieren
        Base.metadata.create_all(self.engine)
        
        # Erstelle eine Session-Factory
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Erstellt und gibt eine neue Datenbanksitzung zurück"""
        return self.Session()
    
    def init_default_data(self):
        """Initialisiert die Datenbank mit Standarddaten"""
        session = self.get_session()
        
        try:
            # Prüfe, ob bereits Plattformen existieren
            if session.query(Platform).count() == 0:
                # Füge Standardplattformen hinzu
                platforms = [
                    {"name": "Instagram", "description": "Instagram-Plattform für Bilder und Videos"},
                    {"name": "TikTok", "description": "TikTok-Plattform für Kurzvideos"},
                    {"name": "Facebook", "description": "Facebook-Plattform für soziale Netzwerke"},
                    {"name": "Google", "description": "Google-Suchergebnisse"},
                    {"name": "YouTube", "description": "YouTube-Videoplattform"},
                    {"name": "Pinterest", "description": "Pinterest-Plattform für Bilder und Ideen"},
                    {"name": "Twitter", "description": "Twitter/X-Plattform für Kurznachrichten"},
                    {"name": "Website", "description": "Allgemeine Websites"}
                ]
                
                for platform_data in platforms:
                    platform = Platform(**platform_data)
                    session.add(platform)
                
                print("Standardplattformen wurden hinzugefügt.")
            
            # Prüfe, ob bereits Suchbegriffe existieren
            if session.query(SearchTerm).count() == 0:
                # Füge Standardsuchbegriffe hinzu
                search_terms = [
                    {"term": "#hyaluronpen", "category": "hashtag"},
                    {"term": "#lippenaufspritzen", "category": "hashtag"},
                    {"term": "#needlefreefiller", "category": "hashtag"},
                    {"term": "#faltenaufspritzen", "category": "hashtag"},
                    {"term": "Hyaluron Pen Behandlung", "category": "keyword"},
                    {"term": "Lippen aufspritzen ohne Nadel", "category": "keyword"},
                    {"term": "Hyaluron Stift kaufen", "category": "keyword"},
                    {"term": "Hyaluron Pen Schulung", "category": "keyword"},
                    {"term": "Hyaluron Pen Erfahrung", "category": "keyword"},
                    {"term": "Hyaluron Pen Vorher Nachher", "category": "keyword"},
                    {"term": "Lippen aufspritzen Kosten", "category": "keyword"},
                    {"term": "Hyaluronsäure Pen", "category": "keyword"},
                    {"term": "Hyaluron Pistole", "category": "keyword"},
                    {"term": "Lippenunterspritzung ohne Nadel", "category": "keyword"},
                    {"term": "Kosmetikstudio Hyaluron", "category": "keyword"},
                    {"term": "Hyaluron Pen Berlin", "category": "location_keyword"},
                    {"term": "Hyaluron Pen Hamburg", "category": "location_keyword"},
                    {"term": "Hyaluron Pen München", "category": "location_keyword"},
                    {"term": "Hyaluron Pen Köln", "category": "location_keyword"},
                    {"term": "Hyaluron Pen Frankfurt", "category": "location_keyword"},
                    {"term": "Hyaluron Pen Stuttgart", "category": "location_keyword"},
                    {"term": "Hyaluron Pen Düsseldorf", "category": "location_keyword"},
                    {"term": "Hyaluron Pen Leipzig", "category": "location_keyword"},
                    {"term": "Hyaluron Pen Dresden", "category": "location_keyword"},
                    {"term": "Hyaluron Pen Hannover", "category": "location_keyword"}
                ]
                
                for term_data in search_terms:
                    term = SearchTerm(**term_data)
                    session.add(term)
                
                print("Standardsuchbegriffe wurden hinzugefügt.")
            
            # Commit der Änderungen
            session.commit()
            print("Standarddaten wurden erfolgreich initialisiert.")
            
        except Exception as e:
            session.rollback()
            print(f"Fehler bei der Initialisierung der Standarddaten: {e}")
        finally:
            session.close()
    
    def add_profile(self, platform_name, profile_data):
        """
        Fügt ein neues Profil hinzu oder aktualisiert ein bestehendes
        
        Args:
            platform_name: Name der Plattform (z.B. 'Instagram')
            profile_data: Dictionary mit den Profildaten
            
        Returns:
            Das hinzugefügte oder aktualisierte Profil-Objekt
        """
        session = self.get_session()
        
        try:
            # Finde die Plattform
            platform = session.query(Platform).filter_by(name=platform_name).first()
            if not platform:
                print(f"Plattform '{platform_name}' nicht gefunden. Erstelle neu.")
                platform = Platform(name=platform_name)
                session.add(platform)
                session.flush()
            
            # Prüfe, ob das Profil bereits existiert
            profile = session.query(Profile).filter_by(
                platform_id=platform.id,
                profile_name=profile_data.get('profile_name')
            ).first()
            
            if profile:
                # Aktualisiere das bestehende Profil
                profile.description = profile_data.get('description', profile.description)
                profile.email = profile_data.get('email', profile.email)
                profile.location = profile_data.get('location', profile.location)
                profile.follower_count = profile_data.get('follower_count', profile.follower_count)
                profile.last_checked = datetime.now()
                print(f"Profil '{profile.profile_name}' auf {platform_name} aktualisiert.")
            else:
                # Erstelle ein neues Profil
                profile = Profile(
                    platform_id=platform.id,
                    profile_name=profile_data.get('profile_name'),
                    profile_link=profile_data.get('profile_link'),
                    description=profile_data.get('description'),
                    email=profile_data.get('email'),
                    location=profile_data.get('location'),
                    follower_count=profile_data.get('follower_count'),
                    first_seen=datetime.now(),
                    last_checked=datetime.now()
                )
                session.add(profile)
                print(f"Neues Profil '{profile.profile_name}' auf {platform_name} hinzugefügt.")
            
            # Commit der Änderungen
            session.commit()
            return profile
            
        except Exception as e:
            session.rollback()
            print(f"Fehler beim Hinzufügen/Aktualisieren des Profils: {e}")
            return None
        finally:
            session.close()
    
    def add_post(self, profile_id, post_data):
        """
        Fügt einen neuen Post hinzu
        
        Args:
            profile_id: ID des zugehörigen Profils
            post_data: Dictionary mit den Postdaten
            
        Returns:
            Das hinzugefügte Post-Objekt
        """
        session = self.get_session()
        
        try:
            # Prüfe, ob der Post bereits existiert
            existing_post = None
            if 'post_link' in post_data and post_data['post_link']:
                existing_post = session.query(Post).filter_by(
                    profile_id=profile_id,
                    post_link=post_data.get('post_link')
                ).first()
            
            if existing_post:
                print(f"Post mit Link '{post_data.get('post_link')}' existiert bereits.")
                return existing_post
            
            # Erstelle einen neuen Post
            post = Post(
                profile_id=profile_id,
                post_link=post_data.get('post_link'),
                post_text=post_data.get('post_text'),
                post_date=post_data.get('post_date'),
                contains_hyaluron_pen=post_data.get('contains_hyaluron_pen', False),
                contains_price=post_data.get('contains_price', False),
                price_mentioned=post_data.get('price_mentioned')
            )
            session.add(post)
            
            # Commit der Änderungen
            session.commit()
            print(f"Neuer Post für Profil-ID {profile_id} hinzugefügt.")
            return post
            
        except Exception as e:
            session.rollback()
            print(f"Fehler beim Hinzufügen des Posts: {e}")
            return None
        finally:
            session.close()
    
    def add_screenshot(self, screenshot_data):
        """
        Fügt einen neuen Screenshot hinzu
        
        Args:
            screenshot_data: Dictionary mit den Screenshot-Daten
            
        Returns:
            Das hinzugefügte Screenshot-Objekt
        """
        session = self.get_session()
        
        try:
            # Erstelle einen neuen Screenshot
            screenshot = Screenshot(
                profile_id=screenshot_data.get('profile_id'),
                post_id=screenshot_data.get('post_id'),
                file_path=screenshot_data.get('file_path'),
                url_captured=screenshot_data.get('url_captured'),
                is_evidence=screenshot_data.get('is_evidence', True),
                metadata=screenshot_data.get('metadata')
            )
            session.add(screenshot)
            
            # Commit der Änderungen
            session.commit()
            print(f"Neuer Screenshot für URL '{screenshot_data.get('url_captured')}' hinzugefügt.")
            return screenshot
            
        except Exception as e:
            session.rollback()
            print(f"Fehler beim Hinzufügen des Screenshots: {e}")
            return None
        finally:
            session.close()
    
    def log_search(self, platform_name, search_term, results_count, duration_seconds, is_successful=True, error_message=None):
        """
        Protokolliert einen Suchvorgang
        
        Args:
            platform_name: Name der Plattform
            search_term: Der verwendete Suchbegriff
            results_count: Anzahl der gefundenen Ergebnisse
            duration_seconds: Dauer der Suche in Sekunden
            is_successful: War die Suche erfolgreich?
            error_message: Fehlermeldung, falls vorhanden
            
        Returns:
            Das erstellte SearchLog-Objekt
        """
        session = self.get_session()
        
        try:
            # Finde die Plattform
            platform = session.query(Platform).filter_by(name=platform_name).first()
            if not platform:
                print(f"Plattform '{platform_name}' nicht gefunden. Erstelle neu.")
                platform = Platform(name=platform_name)
                session.add(platform)
                session.flush()
            
            # Finde oder erstelle den Suchbegriff
            search_term_obj = session.query(SearchTerm).filter_by(term=search_term).first()
            if not search_term_obj:
                print(f"Suchbegriff '{search_term}' nicht gefunden. Erstelle neu.")
                search_term_obj = SearchTerm(term=search_term)
                session.add(search_term_obj)
                session.flush()
            
            # Aktualisiere den Suchbegriff
            search_term_obj.last_used = datetime.now()
            
            # Erstelle einen neuen Sucheintrag
            search_log = SearchLog(
                platform_id=platform.id,
                search_term_id=search_term_obj.id,
                search_date=datetime.now(),
                results_count=results_count,
                duration_seconds=duration_seconds,
                is_successful=is_successful,
                error_message=error_message
            )
            session.add(search_log)
            
            # Commit der Änderungen
            session.commit()
            print(f"Suchvorgang für '{search_term}' auf {platform_name} protokolliert.")
            return search_log
            
        except Exception as e:
            session.rollback()
            print(f"Fehler beim Protokollieren des Suchvorgangs: {e}")
            return None
        finally:
            session.close()
    
    def get_active_search_terms(self, category=None, limit=None):
        """
        Gibt aktive Suchbegriffe zurück
        
        Args:
            category: Optional, filtert nach Kategorie
            limit: Optional, begrenzt die Anzahl der zurückgegebenen Begriffe
            
        Returns:
            Liste von SearchTerm-Objekten
        """
        session = self.get_session()
        
        try:
            query = session.query(SearchTerm).filter_by(is_active=True)
            
            if category:
                query = query.filter_by(category=category)
            
            # Sortiere nach Erfolgsrate (absteigend)
            query = query.order_by(SearchTerm.success_rate.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
            
        except Exception as e:
            print(f"Fehler beim Abrufen der aktiven Suchbegriffe: {e}")
            return []
        finally:
            session.close()
    
    def get_platforms(self, active_only=True):
        """
        Gibt alle Plattformen zurück
        
        Args:
            active_only: Nur aktive Plattformen zurückgeben
            
        Returns:
            Liste von Platform-Objekten
        """
        session = self.get_session()
        
        try:
            query = session.query(Platform)
            
            if active_only:
                query = query.filter_by(is_active=True)
            
            return query.all()
            
        except Exception as e:
            print(f"Fehler beim Abrufen der Plattformen: {e}")
            return []
        finally:
            session.close()
    
    def get_profiles_by_platform(self, platform_name, limit=100):
        """
        Gibt Profile für eine bestimmte Plattform zurück
        
        Args:
            platform_name: Name der Plattform
            limit: Maximale Anzahl der zurückgegebenen Profile
            
        Returns:
            Liste von Profile-Objekten
        """
        session = self.get_session()
        
        try:
            platform = session.query(Platform).filter_by(name=platform_name).first()
            
            if not platform:
                print(f"Plattform '{platform_name}' nicht gefunden.")
                return []
            
            profiles = session.query(Profile).filter_by(platform_id=platform.id).limit(limit).all()
            return profiles
            
        except Exception as e:
            print(f"Fehler beim Abrufen der Profile: {e}")
            return []
        finally:
            session.close()
    
    def get_unreported_profiles(self, limit=50):
        """
        Gibt Profile zurück, die noch nicht gemeldet wurden
        
        Args:
            limit: Maximale Anzahl der zurückgegebenen Profile
            
        Returns:
            Liste von Profile-Objekten
        """
        session = self.get_session()
        
        try:
            profiles = session.query(Profile).filter_by(is_reported=False).limit(limit).all()
            return profiles
            
        except Exception as e:
            print(f"Fehler beim Abrufen der nicht gemeldeten Profile: {e}")
            return []
        finally:
            session.close()
    
    def get_statistics(self):
        """
        Gibt Statistiken über die gesammelten Daten zurück
        
        Returns:
            Dictionary mit Statistiken
        """
        session = self.get_session()
        
        try:
            stats = {
                "total_profiles": session.query(func.count(Profile.id)).scalar(),
                "total_posts": session.query(func.count(Post.id)).scalar(),
                "total_screenshots": session.query(func.count(Screenshot.id)).scalar(),
                "total_searches": session.query(func.count(SearchLog.id)).scalar(),
                "successful_searches": session.query(func.count(SearchLog.id)).filter_by(is_successful=True).scalar(),
                "reported_profiles": session.query(func.count(Profile.id)).filter_by(is_reported=True).scalar(),
                "platforms": {}
            }
            
            # Statistiken pro Plattform
            platforms = session.query(Platform).all()
            for platform in platforms:
                profile_count = session.query(func.count(Profile.id)).filter_by(platform_id=platform.id).scalar()
                stats["platforms"][platform.name] = profile_count
            
            return stats
            
        except Exception as e:
            print(f"Fehler beim Abrufen der Statistiken: {e}")
            return {}
        finally:
            session.close()

if __name__ == "__main__":
    # Teste den DatabaseManager
    db_manager = DatabaseManager("sqlite:///iri_legal_agent.db")
    
    # Initialisiere Standarddaten
    db_manager.init_default_data()
    
    # Teste das Hinzufügen eines Profils
    test_profile = {
        "profile_name": "test_studio",
        "profile_link": "https://instagram.com/test_studio",
        "description": "Test-Studio für Hyaluron Pen Behandlungen",
        "email": "test@example.com",
        "location": "Berlin"
    }
    
    profile = db_manager.add_profile("Instagram", test_profile)
    
    if profile:
        # Teste das Hinzufügen eines Posts
        test_post = {
            "post_link": "https://instagram.com/p/test123",
            "post_text": "Heute tolle Ergebnisse mit unserem Hyaluron Pen! #hyaluronpen",
            "contains_hyaluron_pen": True
        }
        
        post = db_manager.add_post(profile.id, test_post)
        
        if post:
            # Teste das Hinzufügen eines Screenshots
            test_screenshot = {
                "profile_id": profile.id,
                "post_id": post.id,
                "file_path": "screenshots/test.png",
                "url_captured": "https://instagram.com/test_studio"
            }
            
            db_manager.add_screenshot(test_screenshot)
    
    # Teste das Protokollieren einer Suche
    db_manager.log_search("Instagram", "#hyaluronpen", 5, 2.5)
    
    # Gib Statistiken aus
    stats = db_manager.get_statistics()
    print("\nStatistiken:")
    print(json.dumps(stats, indent=2))
