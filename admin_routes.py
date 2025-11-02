from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Track, Delivery, StoreAPI, Statement, ArtistProfile, ReleaseStatus, DeliveryStatus
from auth import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/admin", tags=["admin"])

def verify_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

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
def get_pending_releases(admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    releases = db.query(Track).filter(Track.status == ReleaseStatus.PENDING).all()
    return releases

@router.post("/releases/{release_id}/approve")
def approve_release(release_id: int, data: ApproveRequest, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == release_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Release not found")
    
    track.status = ReleaseStatus.APPROVED
    if data.upc:
        track.upc = data.upc
    db.commit()
    return {"message": "Release approved"}

@router.post("/releases/{release_id}/reject")
def reject_release(release_id: int, data: RejectRequest, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == release_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Release not found")
    
    track.status = ReleaseStatus.DRAFT
    track.rejection_feedback = data.feedback
    db.commit()
    return {"message": "Release rejected and sent to draft"}

@router.post("/deliveries/{delivery_id}/refresh")
def refresh_delivery(delivery_id: int, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    delivery.status = DeliveryStatus.PENDING
    db.commit()
    return {"message": "Delivery refreshed"}

@router.post("/stores")
def add_store(data: StoreAPICreate, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    store = StoreAPI(
        store_name=data.storeName,
        api_url=data.apiUrl,
        api_key=data.apiKey,
        api_secret=data.apiSecret
    )
    db.add(store)
    db.commit()
    return {"message": "Store added"}

@router.get("/stores")
def get_stores(admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    return db.query(StoreAPI).all()

@router.post("/statements")
def create_statement(data: StatementCreate, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    statement = Statement(
        user_id=data.userId,
        period_start=datetime.fromisoformat(data.periodStart),
        period_end=datetime.fromisoformat(data.periodEnd),
        total_revenue=0.0,
        total_plays=0,
        statement_data={}
    )
    db.add(statement)
    db.commit()
    return {"message": "Statement created"}

@router.get("/statements")
def get_statements(admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    return db.query(Statement).all()

@router.post("/artists")
def map_artist(data: ArtistProfileCreate, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    artist = ArtistProfile(
        artist_name=data.artistName,
        user_id=data.userId,
        spotify_id=data.spotifyId,
        apple_music_id=data.appleMusicId,
        youtube_id=data.youtubeId,
        metadata={}
    )
    db.add(artist)
    db.commit()
    return {"message": "Artist profile mapped"}

@router.get("/artists")
def get_artists(admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    return db.query(ArtistProfile).all()

@router.get("/releases/all")
def get_all_releases(admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    return db.query(Track).all()

@router.put("/releases/{release_id}")
def update_release(release_id: int, data: dict, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == release_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Release not found")
    for key, value in data.items():
        setattr(track, key, value)
    db.commit()
    return {"message": "Release updated"}

@router.post("/users")
def create_user(data: dict, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    from auth import get_password_hash
    user = User(
        email=data["email"],
        hashed_password=get_password_hash(data["password"]),
        full_name=data["fullName"],
        is_admin=data.get("isAdmin", 0)
    )
    db.add(user)
    db.commit()
    return {"message": "User created"}

@router.get("/users")
def get_users(admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    return db.query(User).all()

@router.put("/stores/{store_id}")
def update_store(store_id: int, data: dict, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    store = db.query(StoreAPI).filter(StoreAPI.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    for key, value in data.items():
        setattr(store, key, value)
    db.commit()
    return {"message": "Store updated"}

@router.post("/accounting/upload")
async def upload_accounting_csv(file: UploadFile, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    import csv
    import io
    content = await file.read()
    csv_data = csv.DictReader(io.StringIO(content.decode('utf-8')))
    results = []
    for row in csv_data:
        artist_name = row.get('artist')
        artist = db.query(ArtistProfile).filter(ArtistProfile.artist_name == artist_name).first()
        results.append({"artist": artist_name, "assigned": bool(artist), "data": row})
    return {"results": results}

@router.post("/labels")
def create_label(data: dict, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    from models import Label
    label = Label(
        name=data["name"],
        owner_id=data["ownerId"],
        description=data.get("description"),
        logo_url=data.get("logoUrl")
    )
    db.add(label)
    db.commit()
    return {"message": "Label created"}

@router.get("/labels")
def get_labels(admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    from models import Label
    return db.query(Label).all()

@router.get("/settings")
def get_settings(admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    from models import SiteSettings
    settings = db.query(SiteSettings).first()
    if not settings:
        settings = SiteSettings()
        db.add(settings)
        db.commit()
    return settings

@router.put("/settings")
def update_settings(data: dict, admin: User = Depends(verify_admin), db: Session = Depends(get_db)):
    from models import SiteSettings
    settings = db.query(SiteSettings).first()
    if not settings:
        settings = SiteSettings()
        db.add(settings)
    for key, value in data.items():
        setattr(settings, key, value)
    db.commit()
    return {"message": "Settings updated"}
