from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class StoreType(enum.Enum):
    MTN = "mtn"
    VODACOM = "vodacom"
    TELKOM = "telkom"

class DeliveryStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    FAILED = "failed"

class ReleaseStatus(enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_admin = Column(Integer, default=0)
    profile_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    tracks = relationship("Track", back_populates="owner")

class Artwork(Base):
    __tablename__ = "artworks"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, unique=True)
    file_hash = Column(String, unique=True, index=True)
    width = Column(Integer)
    height = Column(Integer)
    format = Column(String)
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    tracks = relationship("Track", back_populates="artwork")

class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)
    album = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    isrc = Column(String, unique=True, nullable=True, index=True)
    upc = Column(String, nullable=True)
    duration = Column(Float)
    file_path = Column(String)
    file_hash = Column(String, unique=True, index=True)
    original_format = Column(String)
    artwork_id = Column(Integer, ForeignKey("artworks.id"), nullable=True)
    track_metadata = Column(JSON)
    status = Column(Enum(ReleaseStatus), default=ReleaseStatus.DRAFT)
    rejection_feedback = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="tracks")
    artwork = relationship("Artwork", back_populates="tracks")
    deliveries = relationship("Delivery", back_populates="track")
    analytics = relationship("Analytics", back_populates="track")

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"))
    store = Column(Enum(StoreType))
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING)
    processed_file_path = Column(String)
    delivery_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    delivered_at = Column(DateTime, nullable=True)
    track = relationship("Track", back_populates="deliveries")
    transactions = relationship("Transaction", back_populates="delivery")

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"))
    store = Column(Enum(StoreType))
    plays = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    date = Column(DateTime, default=datetime.utcnow)
    analytics_metadata = Column(JSON)
    track = relationship("Track", back_populates="analytics")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.id"))
    amount = Column(Float)
    currency = Column(String, default="ZAR")
    transaction_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    transaction_metadata = Column(JSON)
    delivery = relationship("Delivery", back_populates="transactions")

class StoreAPI(Base):
    __tablename__ = "store_apis"
    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, unique=True)
    api_url = Column(String)
    api_key = Column(String)
    api_secret = Column(String, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class ArtistProfile(Base):
    __tablename__ = "artist_profiles"
    id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    spotify_id = Column(String, nullable=True)
    apple_music_id = Column(String, nullable=True)
    youtube_id = Column(String, nullable=True)
    artist_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Statement(Base):
    __tablename__ = "statements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    total_revenue = Column(Float)
    total_plays = Column(Integer)
    status = Column(String, default="draft")
    statement_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class SiteSettings(Base):
    __tablename__ = "site_settings"
    id = Column(Integer, primary_key=True, index=True)
    site_title = Column(String, default="Escopia Distribution")
    site_description = Column(String)
    logo_url = Column(String)
    footer_text = Column(String)
    terms_conditions = Column(String)
    privacy_policy = Column(String)
    support_email = Column(String)
    ticket_system_url = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Label(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String)
    logo_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
