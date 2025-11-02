from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Audio Distribution Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    from admin_routes import router as admin_router
    app.include_router(admin_router)
except Exception as e:
    print(f"Admin routes error: {e}")

try:
    from api_routes import router as api_router
    app.include_router(api_router)
except Exception as e:
    print(f"API routes error: {e}")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("templates/login.html") as f:
            return f.read()
    except:
        return "<h1>Login page not found</h1>"

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    try:
        with open("templates/index.html") as f:
            return f.read()
    except:
        return "<h1>Dashboard not found</h1>"

@app.get("/upload", response_class=HTMLResponse)
def upload_wizard():
    try:
        with open("templates/upload_wizard.html") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Upload wizard error: {str(e)}</h1>"

@app.get("/admin", response_class=HTMLResponse)
def admin_portal():
    try:
        with open("templates/admin.html") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Admin portal error: {str(e)}</h1>"

if __name__ == "__main__":
    import uvicorn
    print("\n🎵 Audio Distribution Portal")
    print("Visit: http://localhost:8000\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
