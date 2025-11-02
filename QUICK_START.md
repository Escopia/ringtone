# 🚀 Quick Start Guide

## Start the Portal (Easy Way)

```bash
./start.sh
```

That's it! The script will:
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Initialize database
- ✓ Start the server

## Start the Portal (Manual Way)

```bash
# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic-settings python-multipart pillow pydub

# Initialize database
python3 init_db.py

# Start server
uvicorn web_app:app --reload --host 0.0.0.0 --port 8000
```

## Access the Portal

Open your browser:
- **http://localhost:8000** - Login page
- **http://localhost:8000/dashboard** - Dashboard
- **http://localhost:8000/upload** - Upload releases
- **http://localhost:8000/admin** - Admin panel

## Upload a Release

1. Go to **http://localhost:8000/upload**
2. **Drag & drop** audio files (or click to select)
3. **Drag & drop** artwork (optional)
4. **Fill in** release details:
   - Release Title *
   - Artist Name *
   - Genre *
   - Album (optional)
   - ISRC (optional)
   - UPC (optional)
   - Release Date (optional)
5. Click **"🚀 Upload Release"**
6. Watch the progress bar
7. Done! Redirects to dashboard

## Supported File Formats

### Audio
- MP3
- WAV
- AAC
- FLAC
- M4A
- OGG

### Artwork
- JPG
- PNG
- Recommended: 3000x3000px minimum

## Common Issues

### "Not Found" Error on /upload
**Solution**: Make sure you're using the correct URL:
```
http://localhost:8000/upload
```

### Upload Not Working
**Solution**: Check browser console (F12) for errors

### Database Error
**Solution**: Reinitialize database:
```bash
rm ringtone.db
python3 init_db.py
```

## Features

✨ **Modern UI** - Clean, gradient design
📤 **Drag & Drop** - Easy file uploads
📊 **Progress Tracking** - Real-time upload status
📱 **Responsive** - Works on all devices
🎨 **Artwork Preview** - See before you upload
✅ **Validation** - Helpful error messages

## Default Credentials

- **Email**: ofentse@escopia.co.za
- **Name**: Escopia

## Need Help?

1. Check `SETUP_GUIDE.md` for detailed documentation
2. Review browser console (F12) for errors
3. Check server logs in terminal
4. Verify all files exist with `python3 test_routes.py`

---

**Happy Distributing! 🎵**
