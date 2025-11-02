import hashlib
from PIL import Image
from pydub import AudioSegment
from sqlalchemy.orm import Session
from models import Track, Artwork
from typing import Optional, Dict

class MetadataProcessor:
    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    @staticmethod
    def check_duplicate_track(db: Session, file_hash: str, isrc: Optional[str] = None) -> Optional[Track]:
        """Check if track already exists by hash or ISRC"""
        if file_hash:
            existing = db.query(Track).filter(Track.file_hash == file_hash).first()
            if existing:
                return existing
        
        if isrc:
            existing = db.query(Track).filter(Track.isrc == isrc).first()
            if existing:
                return existing
        
        return None
    
    @staticmethod
    def check_duplicate_artwork(db: Session, file_hash: str) -> Optional[Artwork]:
        """Check if artwork already exists"""
        return db.query(Artwork).filter(Artwork.file_hash == file_hash).first()
    
    @staticmethod
    def process_artwork(file_path: str, db: Session) -> Artwork:
        """Process and deduplicate artwork"""
        file_hash = MetadataProcessor.calculate_file_hash(file_path)
        
        existing = MetadataProcessor.check_duplicate_artwork(db, file_hash)
        if existing:
            return existing
        
        with Image.open(file_path) as img:
            width, height = img.size
            format = img.format.lower()
        
        artwork = Artwork(
            file_path=file_path,
            file_hash=file_hash,
            width=width,
            height=height,
            format=format,
            file_size=0
        )
        db.add(artwork)
        db.commit()
        db.refresh(artwork)
        return artwork
    
    @staticmethod
    def extract_audio_metadata(file_path: str) -> Dict:
        """Extract audio file metadata"""
        audio = AudioSegment.from_file(file_path)
        return {
            "duration": len(audio) / 1000.0,
            "channels": audio.channels,
            "sample_rate": audio.frame_rate,
            "bit_depth": audio.sample_width * 8
        }
