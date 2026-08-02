"""
app.py

Serves a card-based catalog of ML projects, read from data/projects.json.
Add a new project by editing the JSON file — no template changes needed.
"""
import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "projects.json"

app = FastAPI(title="ML Projects Catalog")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def load_projects() -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)["projects"]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def catalog(request: Request):
    projects = load_projects()
    live_count = sum(1 for p in projects if p["status"] == "live")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "projects": projects,
            "live_count": live_count,
            "total_count": len(projects),
        },
    )
