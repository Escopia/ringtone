# Escopia Distribution Portal - Setup Guide

## 🎵 Modern Audio Distribution Platform

A refined, user-friendly platform for distributing music to MTN, Vodacom, and Telkom stores.

## ✨ What's New

### Modern UI/UX
- **Clean, gradient-based design** with purple theme
- **Drag & drop file uploads** with visual feedback
- **Real-time upload progress** tracking
- **Responsive design** for mobile and desktop
- **Intuitive navigation** with quick actions

### Improved Upload Experience
- Multi-file audio upload support
- Artwork preview before upload
- Form validation with helpful error messages
- Progress bar showing upload status
- Success/error notifications

### Enhanced Dashboard
- Welcome section with personalized greeting
- Stats cards showing key metrics
- Quick action cards for common tasks
- Empty state guidance for new users
- Modern card-based layout

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python3 init_db.py
```

### 3. Start the Server

```bash
uvicorn web_app:app --reload --host 0.0.0.0 --port 8000
```

Or simply:

```bash
python3 web_app.py
```

### 4. Access the Portal

Open your browser and navigate to:
- **Login**: http://localhost:8000
- **Dashboard**: http://localhost:8000/dashboard
- **Upload**: http://localhost:8000/upload
- **Admin**: http://localhost:8000/admin

## 📁 Project Structure

```
ringtone/
├── web_app.py                      # Main FastAPI application
├── api_routes.py                   # API endpoints
├── admin_routes.py                 # Admin endpoints
├── models.py                       # Database models
├── database.py                     # Database configuration
├── init_db.py                      # Database initialization
├── templates/
│   ├── login.html                  # Login page
│   ├── dashboard_modern.html       # Modern dashboard
│   ├── upload_modern.html          # Modern upload page
│   └── admin.html                  # Admin portal
├── static/
│   ├── css/
│   │   └── style.css              # Global styles
│   └── js/
│       └── upload.js              # Upload functionality
└── uploads/                        # Uploaded files storage
    ├── audio/                      # Audio files
    └── artwork/                    # Artwork files
```

## 🎨 Design Features

### Color Palette
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Background**: Light gray (#f8f9fa)
- **Cards**: White with subtle shadows
- **Text**: Dark gray (#1f2937) and medium gray (#6b7280)

### Typography
- **Font**: System fonts (San Francisco, Segoe UI, Roboto)
- **Headings**: Bold, large sizes (42px, 28px, 24px)
- **Body**: 15-16px with good line height

### Components
- **Rounded corners**: 10-20px border radius
- **Shadows**: Subtle elevation with hover effects
- **Transitions**: Smooth 0.3s animations
- **Hover states**: Transform and shadow changes

## 🔧 API Endpoints

### Upload Release
```
POST /api/tracks/upload
Content-Type: multipart/form-data

Fields:
- audio_files: File[] (required)
- artwork: File (optional)
- title: string (required)
- artist: string (required)
- album: string (optional)
- genre: string (required)
- isrc: string (optional)
- upc: string (optional)
- release_date: string (optional)
```

### Get Tracks
```
GET /api/tracks
```

## 🎯 User Flow

1. **Login** → User enters credentials
2. **Dashboard** → View stats and recent activity
3. **Upload** → Drag & drop audio files and artwork
4. **Fill Details** → Enter release metadata
5. **Submit** → Upload with progress tracking
6. **Success** → Redirect to dashboard

## 🛠️ Troubleshooting

### Upload Page Shows "Not Found"
- Ensure `templates/upload_modern.html` exists
- Check that `web_app.py` has the correct route
- Restart the server

### Files Not Uploading
- Check `uploads/audio/` and `uploads/artwork/` directories exist
- Verify file permissions
- Check browser console for errors

### Database Errors
- Run `python3 init_db.py` to recreate tables
- Check `.env` file has correct database URL
- Ensure SQLite database file has write permissions

## 📱 Mobile Support

The portal is fully responsive and works on:
- Desktop (1400px+)
- Tablet (768px - 1400px)
- Mobile (< 768px)

## 🔐 Security Features

- File type validation (audio and image only)
- File size limits
- SQL injection prevention with SQLAlchemy
- CORS middleware for API security

## 🎓 Best Practices

1. **Always test uploads** with small files first
2. **Use high-quality artwork** (min 3000x3000px)
3. **Fill in all metadata** for better distribution
4. **Check file formats** before uploading
5. **Monitor upload progress** to ensure completion

## 📞 Support

For issues or questions:
- Check the logs in `/tmp/app.log`
- Review the browser console for errors
- Verify all dependencies are installed

## 🚀 Next Steps

1. Add user authentication
2. Implement real-time analytics
3. Add store delivery tracking
4. Create revenue reporting
5. Build mobile app

---

**Built with ❤️ for Escopia Distribution**
