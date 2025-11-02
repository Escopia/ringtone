#!/bin/bash

echo "🎵 Starting Escopia Distribution Portal..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q fastapi uvicorn sqlalchemy pydantic-settings python-multipart pillow pydub

# Create necessary directories
mkdir -p uploads/audio uploads/artwork

# Initialize database if it doesn't exist
if [ ! -f "ringtone.db" ]; then
    echo "Initializing database..."
    python3 init_db.py
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "🚀 Starting server at http://localhost:8000"
echo ""
echo "Available routes:"
echo "  • Login:     http://localhost:8000"
echo "  • Dashboard: http://localhost:8000/dashboard"
echo "  • Upload:    http://localhost:8000/upload"
echo "  • Admin:     http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn web_app:app --reload --host 0.0.0.0 --port 8000
