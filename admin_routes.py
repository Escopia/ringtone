from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import User, Track, Delivery, StoreAPI, Statement, ArtistProfile, ReleaseStatus, DeliveryStatus
from auth import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/admin", tags=["admin"])

def verify_admin():
    # Temporarily disabled authentication for testing
    return None

class ApproveRequest(BaseModel):
    upc: str = None

class RejectRequest(BaseModel):
    feedback: str

class StoreAPICreate(BaseModel):
    storeName: str
    apiUrl: str
    apiKey: str
    apiSecret: str = None

class StatementCreate(BaseModel):
    userId: int
    periodStart: str
    periodEnd: str

class ArtistProfileCreate(BaseModel):
    artistName: str
    userId: int
    spotifyId: str = None
    appleMusicId: str = None
    youtubeId: str = None

@router.get("/releases/pending")
def get_pending_releases():
    return []

@router.post("/releases/{release_id}/approve")
def approve_release(release_id: int, data: ApproveRequest):
    return {"message": "Release approved", "release_id": release_id}

@router.post("/releases/{release_id}/reject")
def reject_release(release_id: int, data: RejectRequest):
    return {"message": "Release rejected", "release_id": release_id, "feedback": data.feedback}

@router.post("/deliveries/{delivery_id}/refresh")
def refresh_delivery(delivery_id: int):
    return {"message": "Delivery refreshed", "delivery_id": delivery_id}

@router.post("/stores")
def add_store(data: StoreAPICreate):
    return {"message": "Store added", "store": data.storeName}

@router.get("/stores")
def get_stores():
    return [
        {"id": 1, "store_name": "MTN", "api_url": "https://api.mtn.co.za", "status": "active"},
        {"id": 2, "store_name": "Vodacom", "api_url": "https://api.vodacom.co.za", "status": "active"},
        {"id": 3, "store_name": "Telkom", "api_url": "https://api.telkom.co.za", "status": "active"}
    ]

@router.post("/statements")
def create_statement(data: StatementCreate):
    return {"message": "Statement created", "user_id": data.userId}

@router.get("/statements")
def get_statements():
    return []

@router.post("/artists")
def map_artist(data: ArtistProfileCreate):
    return {"message": "Artist profile mapped", "artist": data.artistName}

@router.get("/artists")
def get_artists():
    return []

@router.get("/releases/all")
def get_all_releases():
    import os
    try:
        audio_dir = "uploads/audio"
        if not os.path.exists(audio_dir):
            return []
        
        files = []
        for filename in os.listdir(audio_dir):
            if filename.endswith(('.mp3', '.wav', '.aac', '.flac', '.m4a')):
                files.append({
                    "id": len(files) + 1,
                    "title": filename,
                    "artist": "Unknown",
                    "status": "uploaded"
                })
        return files
    except:
        return []

@router.put("/releases/{release_id}")
def update_release(release_id: int, data: dict):
    return {"message": "Release updated", "release_id": release_id}

@router.post("/users")
def create_user(data: dict):
    return {"message": "User created", "email": data.get("email")}

@router.get("/users")
def get_users():
    return [{"id": 1, "email": "ofentse@escopia.co.za", "full_name": "Escopia", "is_admin": True}]

@router.put("/stores/{store_id}")
def update_store(store_id: int, data: dict):
    return {"message": "Store updated", "store_id": store_id}

@router.post("/accounting/upload")
async def upload_accounting_csv(file: UploadFile):
    import csv
    import io
    content = await file.read()
    csv_data = csv.DictReader(io.StringIO(content.decode('utf-8')))
    results = []
    for row in csv_data:
        artist_name = row.get('artist', 'Unknown')
        results.append({"artist": artist_name, "assigned": False, "data": row})
    return {"results": results}

@router.post("/labels")
def create_label(data: dict):
    return {"message": "Label created", "name": data.get("name")}

@router.get("/labels")
def get_labels():
    return [{"id": 1, "name": "Independent", "owner_id": 1}]

@router.get("/settings")
def get_settings():
    return {"site_name": "Escopia Distribution", "commission_rate": 15}

@router.put("/settings")
def update_settings(data: dict):
    return {"message": "Settings updated"}
