#!/usr/bin/env python3
# database_schema.py - Datenbankschema für IRI® Legal Agent

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Platform(Base):
    """Tabelle für die verschiedenen Plattformen (Instagram, Facebook, TikTok, etc.)"""
    __tablename__ = 'platforms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    api_endpoint = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Beziehungen
    profiles = relationship("Profile", back_populates="platform")
    
    def __repr__(self):
        return f"<Platform(name='{self.name}')>"


class Profile(Base):
    """Tabelle für die gefundenen Profile/Accounts"""
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    profile_name = Column(String(255), nullable=False)
    profile_link = Column(String(512), nullable=False)
    description = Column(Text)
    email = Column(String(255))
    location = Column(String(255))
    follower_count = Column(Integer)
    is_verified = Column(Boolean, default=False)
    first_seen = Column(DateTime, default=datetime.now)
    last_checked = Column(DateTime, default=datetime.now)
    risk_score = Column(Float, default=0.0)  # Bewertung des Risikos (0-100)
    is_reported = Column(Boolean, default=False)
    monday_item_id = Column(String(50))  # ID des Eintrags in Monday.com
    
    # Beziehungen
    platform = relationship("Platform", back_populates="profiles")
    posts = relationship("Post", back_populates="profile")
    screenshots = relationship("Screenshot", back_populates="profile")
    
    def __repr__(self):
        return f"<Profile(name='{self.profile_name}', platform='{self.platform.name}')>"


class Post(Base):
    """Tabelle für die gefundenen Posts/Beiträge"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    post_link = Column(String(512))
    post_text = Column(Text)
    post_date = Column(DateTime)
    contains_hyaluron_pen = Column(Boolean, default=False)
    contains_price = Column(Boolean, default=False)
    price_mentioned = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    
    # Beziehungen
    profile = relationship("Profile", back_populates="posts")
    screenshots = relationship("Screenshot", back_populates="post")
    
    def __repr__(self):
        return f"<Post(id='{self.id}', profile='{self.profile.profile_name}')>"


class Screenshot(Base):
    """Tabelle für die erstellten Screenshots"""
    __tablename__ = 'screenshots'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    file_path = Column(String(512), nullable=False)
    screenshot_date = Column(DateTime, default=datetime.now)
    url_captured = Column(String(512), nullable=False)
    is_evidence = Column(Boolean, default=True)
    metadata = Column(Text)  # JSON-Metadaten
    
    # Beziehungen
    profile = relationship("Profile", back_populates="screenshots")
    post = relationship("Post", back_populates="screenshots")
    
    def __repr__(self):
        return f"<Screenshot(id='{self.id}', file='{self.file_path}')>"


class SearchTerm(Base):
    """Tabelle für die verwendeten Suchbegriffe"""
    __tablename__ = 'search_terms'
    
    id = Column(Integer, primary_key=True)
    term = Column(String(255), nullable=False, unique=True)
    category = Column(String(50))  # z.B. 'hashtag', 'keyword', 'location'
    is_active = Column(Boolean, default=True)
    success_rate = Column(Float, default=0.0)  # Erfolgsrate (0-100%)
    last_used = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<SearchTerm(term='{self.term}')>"


class SearchLog(Base):
    """Tabelle für die Protokollierung der Suchvorgänge"""
    __tablename__ = 'search_logs'
    
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    search_term_id = Column(Integer, ForeignKey('search_terms.id'), nullable=False)
    search_date = Column(DateTime, default=datetime.now)
    results_count = Column(Integer, default=0)
    duration_seconds = Column(Float)
    is_successful = Column(Boolean, default=True)
    error_message = Column(Text)
    
    # Beziehungen
    platform = relationship("Platform")
    search_term = relationship("SearchTerm")
    
    def __repr__(self):
        return f"<SearchLog(id='{self.id}', platform='{self.platform.name}', term='{self.search_term.term}')>"


class HealthAuthority(Base):
    """Tabelle für die Gesundheitsämter"""
    __tablename__ = 'health_authorities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    region = Column(String(255))
    postal_code = Column(String(20))
    contact_person = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<HealthAuthority(name='{self.name}', region='{self.region}')>"


class Report(Base):
    """Tabelle für die erstellten Meldungen an Gesundheitsämter"""
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    health_authority_id = Column(Integer, ForeignKey('health_authorities.id'))
    report_date = Column(DateTime, default=datetime.now)
    report_type = Column(String(50))  # z.B. 'email', 'letter', 'phone'
    status = Column(String(50))  # z.B. 'sent', 'received', 'in_progress', 'closed'
    response_received = Column(Boolean, default=False)
    response_date = Column(DateTime)
    response_details = Column(Text)
    
    # Beziehungen
    profile = relationship("Profile")
    health_authority = relationship("HealthAuthority")
    
    def __repr__(self):
        return f"<Report(id='{self.id}', profile='{self.profile.profile_name}', authority='{self.health_authority.name}')>"


def init_db(db_url="sqlite:///iri_legal_agent.db"):
    """Initialisiert die Datenbank und erstellt alle Tabellen"""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    """Erstellt eine neue Datenbanksitzung"""
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Erstelle die Datenbank
    engine = init_db()
    print("Datenbank wurde erfolgreich initialisiert.")
    
    # Erstelle eine Sitzung
    session = get_session(engine)
    
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
        {"term": "Kosmetikstudio Hyaluron", "category": "keyword"}
    ]
    
    for term_data in search_terms:
        term = SearchTerm(**term_data)
        session.add(term)
    
    # Speichere die Änderungen
    session.commit()
    session.close()
    
    print("Standarddaten wurden erfolgreich hinzugefügt.")
