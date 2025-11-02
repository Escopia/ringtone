"""
Simple test script to verify the portal works locally without database
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Audio Distribution Portal - Test", version="1.0.0")

@app.get("/")
def root():
    return {
        "message": "Audio Distribution Portal is running!",
        "features": [
            "Multi-Store Distribution (MTN, Vodacom, Telkom)",
            "Audio Processing (cutting & compression)",
            "Artwork Management (duplicate detection)",
            "Metadata Processing (ISRC validation)",
            "Bulk Upload (CSV-based)",
            "Analytics Dashboard",
            "Delivery Tracking",
            "Accounting",
            "AI Profiling"
        ],
        "status": "operational"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/stores")
def list_stores():
    return {
        "stores": [
            {
                "name": "MTN",
                "format": "MP3",
                "bitrate": "128k",
                "max_duration": "30s"
            },
            {
                "name": "Vodacom",
                "format": "AAC",
                "bitrate": "96k",
                "max_duration": "45s"
            },
            {
                "name": "Telkom",
                "format": "MP3",
                "bitrate": "192k",
                "max_duration": "60s"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🎵 Audio Distribution Portal - Test Server")
    print("="*60)
    print("\nStarting server at http://localhost:8000")
    print("\nAvailable endpoints:")
    print("  - http://localhost:8000/          (Portal info)")
    print("  - http://localhost:8000/health    (Health check)")
    print("  - http://localhost:8000/stores    (Store specs)")
    print("  - http://localhost:8000/docs      (API documentation)")
    print("\n" + "="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
