from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models import Track, User
from auth import get_current_user
import os
import shutil

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/tracks")
async def create_track(
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(None),
    genre: str = Form(None),
    isrc: str = Form(None),
    file: UploadFile = File(...),
    artwork: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        os.makedirs("uploads", exist_ok=True)
        
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        track = Track(
            title=title,
            artist=artist,
            album=album,
            genre=genre,
            isrc=isrc,
            file_path=file_path,
            file_hash="temp_hash",
            original_format=file.filename.split(".")[-1],
            duration=0.0,
            owner_id=1
        )
        
        db.add(track)
        db.commit()
        db.refresh(track)
        
        return {"message": "Track uploaded successfully", "track_id": track.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tracks")
def get_tracks(db: Session = Depends(get_db)):
    return db.query(Track).all()
