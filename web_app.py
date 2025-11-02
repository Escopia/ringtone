from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Audio Distribution Portal")

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
