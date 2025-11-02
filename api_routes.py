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

@router.post("/tracks/upload")
async def upload_release(
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(""),
    genre: str = Form(...),
    isrc: str = Form(""),
    upc: str = Form(""),
    release_date: str = Form(""),
    audio_files: list[UploadFile] = File(...),
    artwork: UploadFile = File(None)
):
    try:
        os.makedirs("uploads/audio", exist_ok=True)
        os.makedirs("uploads/artwork", exist_ok=True)
        
        uploaded_tracks = []
        
        for audio_file in audio_files:
            file_path = f"uploads/audio/{audio_file.filename}"
            with open(file_path, "wb") as buffer:
                content = await audio_file.read()
                buffer.write(content)
            uploaded_tracks.append(audio_file.filename)
        
        if artwork:
            artwork_path = f"uploads/artwork/{artwork.filename}"
            with open(artwork_path, "wb") as buffer:
                content = await artwork.read()
                buffer.write(content)
        
        return {
            "message": "Release uploaded successfully",
            "tracks": uploaded_tracks,
            "count": len(uploaded_tracks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tracks")
def get_tracks():
    try:
        audio_dir = "uploads/audio"
        if not os.path.exists(audio_dir):
            return []
        
        files = []
        for filename in os.listdir(audio_dir):
            if filename.endswith(('.mp3', '.wav', '.aac', '.flac', '.m4a')):
                file_path = os.path.join(audio_dir, filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    "filename": filename,
                    "size": file_size,
                    "path": file_path
                })
        return files
    except Exception as e:
        return []
