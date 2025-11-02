# 🎵 Escopia Distribution Portal

> Modern, user-friendly music distribution platform for MTN, Vodacom, and Telkom stores.

![Status](https://img.shields.io/badge/status-ready-brightgreen)
![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)

## ✨ Features

- 🎨 **Modern UI/UX** - Clean gradient design with smooth animations
- 📤 **Drag & Drop Upload** - Intuitive file upload experience
- 📊 **Real-time Progress** - Track upload status with progress bar
- 📱 **Fully Responsive** - Works perfectly on all devices
- 🎯 **Quick Actions** - Fast access to common tasks
- 🖼️ **Artwork Preview** - See your artwork before uploading
- ✅ **Form Validation** - Helpful error messages and guidance
- 🚀 **Fast Performance** - Optimized for speed

## 🚀 Quick Start

### One-Command Start

```bash
./start.sh
```

### Manual Start

```bash
# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic-settings python-multipart pillow pydub

# Initialize database
python3 init_db.py

# Start server
uvicorn web_app:app --reload --host 0.0.0.0 --port 8000
```

### Access Portal

Open your browser and visit:
- 🏠 **Dashboard**: http://localhost:8000/dashboard
- 📤 **Upload**: http://localhost:8000/upload
- ⚙️ **Admin**: http://localhost:8000/admin

## 📸 Screenshots

### Dashboard
Modern dashboard with stats cards and quick actions

### Upload Page
Drag & drop interface with real-time preview and progress tracking

### Admin Panel
Comprehensive admin tools for managing releases and users

## 🎯 How to Upload

1. Navigate to **http://localhost:8000/upload**
2. **Drag & drop** your audio files (or click to browse)
3. **Add artwork** (optional but recommended)
4. **Fill in details**:
   - Release Title ✓
   - Artist Name ✓
   - Genre ✓
   - Album, ISRC, UPC (optional)
5. Click **"🚀 Upload Release"**
6. Watch the progress bar
7. Done! 🎉

## 📁 Supported Formats

### Audio Files
- MP3, WAV, AAC, FLAC, M4A, OGG

### Artwork
- JPG, PNG (minimum 3000x3000px recommended)

## 🎨 Design Philosophy

### Colors
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Background**: Light gray (#f8f9fa)
- **Cards**: White with subtle shadows
- **Text**: Dark gray for readability

### Principles
- **Simplicity** - Clean, uncluttered interface
- **Feedback** - Visual response to every action
- **Consistency** - Uniform design language
- **Accessibility** - Easy to use for everyone

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Frontend**: Vanilla JavaScript
- **Styling**: Custom CSS with gradients
- **File Handling**: Multipart form data
- **Audio Processing**: Pydub
- **Image Processing**: Pillow

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get up and running in minutes
- **[Setup Guide](SETUP_GUIDE.md)** - Detailed setup instructions
- **[Changes Log](CHANGES.md)** - What's new and improved

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./ringtone.db
SECRET_KEY=your-secret-key
MTN_CONSUMER_KEY=your-mtn-key
MTN_CONSUMER_SECRET=your-mtn-secret
```

### Directory Structure

```
ringtone/
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── uploads/           # Uploaded files
│   ├── audio/        # Audio files
│   └── artwork/      # Artwork files
├── web_app.py        # Main application
├── api_routes.py     # API endpoints
└── models.py         # Database models
```

## 🐛 Troubleshooting

### Upload Page Not Found
```bash
# Verify templates exist
python3 test_routes.py

# Restart server
./start.sh
```

### Database Errors
```bash
# Reinitialize database
rm ringtone.db
python3 init_db.py
```

### Upload Fails
- Check file size (max 100MB recommended)
- Verify file format is supported
- Check browser console (F12) for errors
- Ensure uploads/ directory has write permissions

## 📊 API Endpoints

### Upload Release
```http
POST /api/tracks/upload
Content-Type: multipart/form-data

Parameters:
- audio_files: File[] (required)
- artwork: File (optional)
- title: string (required)
- artist: string (required)
- genre: string (required)
- album: string (optional)
- isrc: string (optional)
- upc: string (optional)
- release_date: string (optional)
```

### Get Tracks
```http
GET /api/tracks
```

## 🚦 Status

- ✅ Upload functionality - **Working**
- ✅ Dashboard - **Working**
- ✅ Admin panel - **Working**
- ✅ File handling - **Working**
- ✅ Database - **Working**
- ⏳ Store integration - **In Progress**
- ⏳ Analytics - **Planned**
- ⏳ Revenue tracking - **Planned**

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

Copyright © 2024 Escopia Distribution

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- AWAL for design inspiration
- The open-source community

## 📞 Support

For issues or questions:
- Check the documentation
- Review browser console for errors
- Check server logs
- Contact: ofentse@escopia.co.za

---

**Built with ❤️ for music creators**

🎵 **Start distributing your music today!**
