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

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
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
    duration = Column(Float)
    file_path = Column(String)
    file_hash = Column(String, unique=True, index=True)
    original_format = Column(String)
    artwork_id = Column(Integer, ForeignKey("artworks.id"), nullable=True)
    metadata = Column(JSON)
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
    metadata = Column(JSON)
    track = relationship("Track", back_populates="analytics")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.id"))
    amount = Column(Float)
    currency = Column(String, default="ZAR")
    transaction_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    metadata = Column(JSON)
    delivery = relationship("Delivery", back_populates="transactions")
