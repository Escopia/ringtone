import csv
import os
from typing import List, Dict
from sqlalchemy.orm import Session
from models import Track, User
from metadata_processor import MetadataProcessor
from pydub import AudioSegment

class BulkUploadProcessor:
    @staticmethod
    def process_csv(csv_path: str, upload_dir: str, user: User, db: Session) -> Dict:
        """Process bulk upload CSV"""
        results = {"success": [], "skipped": [], "errors": []}
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    audio_path = os.path.join(upload_dir, row['audio_filename'])
                    
                    if not os.path.exists(audio_path):
                        results["errors"].append({
                            "row": row,
                            "error": f"Audio file not found: {row['audio_filename']}"
                        })
                        continue
                    
                    file_hash = MetadataProcessor.calculate_file_hash(audio_path)
                    isrc = row.get('isrc') or None
                    
                    existing = MetadataProcessor.check_duplicate_track(db, file_hash, isrc)
                    if existing:
                        results["skipped"].append({
                            "row": row,
                            "reason": "Duplicate track",
                            "existing_id": existing.id
                        })
                        continue
                    
                    artwork_id = None
                    if row.get('artwork_filename'):
                        artwork_path = os.path.join(upload_dir, row['artwork_filename'])
                        if os.path.exists(artwork_path):
                            artwork = MetadataProcessor.process_artwork(artwork_path, db)
                            artwork_id = artwork.id
                    
                    audio_meta = MetadataProcessor.extract_audio_metadata(audio_path)
                    
                    track = Track(
                        title=row['title'],
                        artist=row['artist'],
                        album=row.get('album'),
                        genre=row.get('genre'),
                        isrc=isrc,
                        duration=audio_meta['duration'],
                        file_path=audio_path,
                        file_hash=file_hash,
                        original_format=row['audio_filename'].split('.')[-1],
                        artwork_id=artwork_id,
                        metadata=audio_meta,
                        owner_id=user.id
                    )
                    
                    db.add(track)
                    db.commit()
                    db.refresh(track)
                    
                    results["success"].append({
                        "row": row,
                        "track_id": track.id
                    })
                    
                except Exception as e:
                    results["errors"].append({
                        "row": row,
                        "error": str(e)
                    })
        
        return results
    
    @staticmethod
    def generate_csv_template(output_path: str):
        """Generate CSV template for bulk upload"""
        headers = ['title', 'artist', 'album', 'genre', 'isrc', 'audio_filename', 'artwork_filename']
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerow({
                'title': 'Example Song',
                'artist': 'Example Artist',
                'album': 'Example Album',
                'genre': 'Pop',
                'isrc': 'USRC12345678',
                'audio_filename': 'song.mp3',
                'artwork_filename': 'cover.jpg'
            })
