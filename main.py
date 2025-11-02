from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional
import os
import shutil
from pydub import AudioSegment

from database import engine, get_db, Base
from models import User, Track, Delivery, Analytics, Transaction, StoreType, DeliveryStatus, Artwork
from schemas import *
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from audio_processor import AudioProcessor
from ai_profiler import AIProfiler
from store_integrations import StoreIntegration
from metadata_processor import MetadataProcessor
from bulk_upload import BulkUploadProcessor

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Audio Distribution Portal", version="1.0.0")

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
BULK_DIR = "bulk_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(BULK_DIR, exist_ok=True)

@app.post("/register", response_model=UserProfile)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        profile_data={}
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tracks", response_model=TrackResponse)
async def upload_track(
    title: str = Form(...),
    artist: str = Form(...),
    album: Optional[str] = Form(None),
    genre: Optional[str] = Form(None),
    isrc: Optional[str] = Form(None),
    file: UploadFile = File(...),
    artwork: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_hash = MetadataProcessor.calculate_file_hash(file_path)
    
    existing = MetadataProcessor.check_duplicate_track(db, file_hash, isrc)
    if existing:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Duplicate track found (ID: {existing.id})")
    
    artwork_id = None
    if artwork:
        artwork_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{artwork.filename}")
        with open(artwork_path, "wb") as buffer:
            shutil.copyfileobj(artwork.file, buffer)
        
        artwork_obj = MetadataProcessor.process_artwork(artwork_path, db)
        artwork_id = artwork_obj.id
    
    audio_meta = MetadataProcessor.extract_audio_metadata(file_path)
    
    track = Track(
        title=title,
        artist=artist,
        album=album,
        genre=genre,
        isrc=isrc,
        duration=audio_meta['duration'],
        file_path=file_path,
        file_hash=file_hash,
        original_format=file.filename.split(".")[-1],
        artwork_id=artwork_id,
        metadata=audio_meta,
        owner_id=current_user.id
    )
    db.add(track)
    db.commit()
    db.refresh(track)
    return track

@app.get("/tracks", response_model=List[TrackResponse])
def get_tracks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Track).filter(Track.owner_id == current_user.id).all()

@app.post("/tracks/bulk-upload")
async def bulk_upload(
    csv_file: UploadFile = File(...),
    audio_files: List[UploadFile] = File(...),
    artwork_files: Optional[List[UploadFile]] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_bulk_dir = os.path.join(BULK_DIR, str(current_user.id))
    os.makedirs(user_bulk_dir, exist_ok=True)
    
    csv_path = os.path.join(user_bulk_dir, csv_file.filename)
    with open(csv_path, "wb") as buffer:
        shutil.copyfileobj(csv_file.file, buffer)
    
    for audio in audio_files:
        audio_path = os.path.join(user_bulk_dir, audio.filename)
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
    
    if artwork_files:
        for artwork in artwork_files:
            artwork_path = os.path.join(user_bulk_dir, artwork.filename)
            with open(artwork_path, "wb") as buffer:
                shutil.copyfileobj(artwork.file, buffer)
    
    results = BulkUploadProcessor.process_csv(csv_path, user_bulk_dir, current_user, db)
    
    return {
        "total_processed": len(results["success"]) + len(results["skipped"]) + len(results["errors"]),
        "successful": len(results["success"]),
        "skipped": len(results["skipped"]),
        "errors": len(results["errors"]),
        "details": results
    }

@app.get("/tracks/bulk-template")
def download_bulk_template():
    template_path = os.path.join(BULK_DIR, "template.csv")
    BulkUploadProcessor.generate_csv_template(template_path)
    return FileResponse(template_path, filename="bulk_upload_template.csv")

@app.post("/deliveries", response_model=DeliveryResponse)
async def create_delivery(
    delivery: DeliveryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    track = db.query(Track).filter(Track.id == delivery.track_id, Track.owner_id == current_user.id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    output_filename = f"{track.id}_{delivery.store.value}.{AudioProcessor.STORE_SPECS[delivery.store]['format']}"
    output_path = os.path.join(PROCESSED_DIR, output_filename)
    
    metadata = AudioProcessor.process_audio(track.file_path, output_path, delivery.store)
    
    db_delivery = Delivery(
        track_id=track.id,
        store=delivery.store,
        status=DeliveryStatus.PROCESSING,
        processed_file_path=output_path,
        delivery_metadata=metadata
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    
    try:
        result = await StoreIntegration.deliver_to_store(
            delivery.store,
            {"title": track.title, "artist": track.artist, "duration": metadata["duration"]},
            output_path
        )
        
        if result.get("success"):
            db_delivery.status = DeliveryStatus.DELIVERED
            db_delivery.delivered_at = datetime.utcnow()
        else:
            db_delivery.status = DeliveryStatus.FAILED
        
        db.commit()
        db.refresh(db_delivery)
    except Exception as e:
        db_delivery.status = DeliveryStatus.FAILED
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))
    
    return db_delivery

@app.get("/deliveries", response_model=List[DeliveryResponse])
def get_deliveries(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Delivery).join(Track).filter(Track.owner_id == current_user.id).all()

@app.get("/analytics/tracks/{track_id}")
def get_track_analytics(track_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id, Track.owner_id == current_user.id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    analytics = db.query(Analytics).filter(Analytics.track_id == track_id).all()
    
    total_plays = sum(a.plays for a in analytics)
    total_downloads = sum(a.downloads for a in analytics)
    total_revenue = sum(a.revenue for a in analytics)
    
    return {
        "track_id": track_id,
        "total_plays": total_plays,
        "total_downloads": total_downloads,
        "total_revenue": total_revenue,
        "by_store": [{"store": a.store.value, "plays": a.plays, "downloads": a.downloads, "revenue": a.revenue} for a in analytics]
    }

@app.get("/analytics/dashboard")
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tracks = db.query(Track).filter(Track.owner_id == current_user.id).all()
    track_ids = [t.id for t in tracks]
    
    analytics = db.query(Analytics).filter(Analytics.track_id.in_(track_ids)).all()
    deliveries = db.query(Delivery).join(Track).filter(Track.owner_id == current_user.id).all()
    
    total_revenue = sum(a.revenue for a in analytics)
    total_plays = sum(a.plays for a in analytics)
    
    delivery_stats = {
        "total": len(deliveries),
        "delivered": len([d for d in deliveries if d.status == DeliveryStatus.DELIVERED]),
        "pending": len([d for d in deliveries if d.status == DeliveryStatus.PENDING]),
        "failed": len([d for d in deliveries if d.status == DeliveryStatus.FAILED])
    }
    
    return {
        "total_tracks": len(tracks),
        "total_revenue": total_revenue,
        "total_plays": total_plays,
        "delivery_stats": delivery_stats
    }

@app.get("/profile/ai-insights")
def get_ai_insights(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tracks = db.query(Track).filter(Track.owner_id == current_user.id).all()
    deliveries = db.query(Delivery).join(Track).filter(Track.owner_id == current_user.id).all()
    analytics = db.query(Analytics).join(Track).filter(Track.owner_id == current_user.id).all()
    
    user_data = {
        "total_uploads": len(tracks),
        "total_deliveries": len(deliveries),
        "avg_track_duration": sum(t.duration for t in tracks) / len(tracks) if tracks else 0,
        "total_revenue": sum(a.revenue for a in analytics),
        "engagement_score": sum(a.plays + a.downloads for a in analytics) / len(analytics) if analytics else 0
    }
    
    profile = AIProfiler.analyze_user_behavior(user_data)
    
    revenue_history = [a.revenue for a in analytics[-10:]]
    predicted_revenue = AIProfiler.predict_revenue(revenue_history)
    
    return {
        "profile": profile,
        "predicted_next_month_revenue": predicted_revenue
    }

@app.get("/accounting/transactions", response_model=List[TransactionResponse])
def get_transactions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    transactions = db.query(Transaction).join(Delivery).join(Track).filter(Track.owner_id == current_user.id).all()
    return transactions

@app.get("/accounting/summary")
def get_accounting_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    transactions = db.query(Transaction).join(Delivery).join(Track).filter(Track.owner_id == current_user.id).all()
    
    total_earnings = sum(t.amount for t in transactions)
    this_month = datetime.utcnow().replace(day=1)
    monthly_earnings = sum(t.amount for t in transactions if t.transaction_date >= this_month)
    
    return {
        "total_earnings": total_earnings,
        "monthly_earnings": monthly_earnings,
        "transaction_count": len(transactions),
        "currency": "ZAR"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
