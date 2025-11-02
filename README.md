# Audio Distribution Portal

Backend for audio distribution with analytics, delivery tracking, accounting & AI-powered user profiling.

## Features

- **Multi-Store Distribution**: MTN, Vodacom, Telkom support
- **Audio Processing**: Automatic cutting & compression per store specs
- **Artwork Management**: Duplicate detection & metadata extraction
- **Metadata Processing**: ISRC validation & duplicate prevention
- **Bulk Upload**: CSV-based batch processing with validation
- **Analytics Dashboard**: Track plays, downloads, revenue
- **Delivery Tracking**: Real-time status monitoring
- **Accounting**: Transaction management & revenue reporting
- **AI Profiling**: User behavior analysis & revenue prediction
- **API Integration**: RESTful APIs for store delivery

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run with Docker:
```bash
docker-compose up
```

4. Initialize database:
```bash
alembic upgrade head
```

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /token` - Login

### Tracks
- `POST /tracks` - Upload track with artwork (multipart/form-data)
- `GET /tracks` - List user tracks
- `POST /tracks/bulk-upload` - Bulk upload via CSV
- `GET /tracks/bulk-template` - Download CSV template

### Delivery
- `POST /deliveries` - Create delivery to store
- `GET /deliveries` - List deliveries

### Analytics
- `GET /analytics/tracks/{id}` - Track analytics
- `GET /analytics/dashboard` - Dashboard overview

### Accounting
- `GET /accounting/transactions` - List transactions
- `GET /accounting/summary` - Revenue summary

### AI Profile
- `GET /profile/ai-insights` - AI-powered insights

## Bulk Upload CSV Format

Download template: `GET /tracks/bulk-template`

```csv
title,artist,album,genre,isrc,audio_filename,artwork_filename
Example Song,Example Artist,Example Album,Pop,USRC12345678,song.mp3,cover.jpg
```

**Fields:**
- `title` (required): Track title
- `artist` (required): Artist name
- `album` (optional): Album name
- `genre` (optional): Music genre
- `isrc` (optional): International Standard Recording Code
- `audio_filename` (required): Audio file name in upload
- `artwork_filename` (optional): Cover art file name

**Upload Process:**
1. Prepare CSV with metadata
2. Upload CSV + all audio files + artwork files
3. System checks for duplicates (by file hash & ISRC)
4. Skips existing tracks automatically
5. Returns detailed results

## Duplicate Detection

The system prevents duplicate uploads using:
- **File Hash**: SHA256 hash of audio file
- **ISRC**: International Standard Recording Code
- **Artwork Hash**: SHA256 hash of artwork file

Duplicate tracks are automatically skipped during:
- Single track upload
- Bulk CSV upload

## Store Specifications

### MTN
- Format: MP3
- Bitrate: 128k
- Max Duration: 30s

### Vodacom
- Format: AAC
- Bitrate: 96k
- Max Duration: 45s

### Telkom
- Format: MP3
- Bitrate: 192k
- Max Duration: 60s

## Tech Stack

- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Pydub (audio processing)
- Pillow (artwork processing)
- scikit-learn (AI profiling)
- JWT authentication
