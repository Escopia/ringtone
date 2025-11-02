from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Audio Distribution Portal")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/login.html") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("templates/index.html") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    print("\n🎵 Audio Distribution Portal")
    print("Visit: http://localhost:8000\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
