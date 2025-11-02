from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from models import StoreType, DeliveryStatus

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserProfile(BaseModel):
    id: int
    email: str
    full_name: str
    profile_data: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ArtworkResponse(BaseModel):
    id: int
    file_path: str
    width: int
    height: int
    format: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TrackCreate(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    genre: Optional[str] = None
    isrc: Optional[str] = None

class TrackResponse(BaseModel):
    id: int
    title: str
    artist: str
    album: Optional[str]
    genre: Optional[str]
    isrc: Optional[str]
    duration: float
    artwork: Optional[ArtworkResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True

class BulkUploadRow(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    genre: Optional[str] = None
    isrc: Optional[str] = None
    audio_filename: str
    artwork_filename: Optional[str] = None

class DeliveryCreate(BaseModel):
    track_id: int
    store: StoreType

class DeliveryResponse(BaseModel):
    id: int
    track_id: int
    store: StoreType
    status: DeliveryStatus
    created_at: datetime
    delivered_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    track_id: int
    store: StoreType
    plays: int
    downloads: int
    revenue: float
    date: datetime
    
    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: int
    delivery_id: int
    amount: float
    currency: str
    transaction_date: datetime
    status: str
    
    class Config:
        from_attributes = True
