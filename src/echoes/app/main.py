"""Main FastAPI application for Echoes."""

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers.story import router as story_router
from .routers.chat import router as chat_router
from .settings import PROJECT_NAME
from .. import __version__

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

app = FastAPI(
    title=PROJECT_NAME,
    description="AI-powered historical interactive learning platform",
    version=__version__
)

# Mount static files
static_dir = PROJECT_ROOT / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Templates
templates_dir = PROJECT_ROOT / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

app.include_router(story_router, prefix="/api", tags=["Story Generation"])
app.include_router(chat_router, prefix="/api", tags=["Interactive Chat"])

@app.get("/", tags=["Web Interface"])
def homepage(request: Request):
    """
    Serve the web interface homepage.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health", tags=["Health"])
def health():
    """
    Health check endpoint.
    
    Returns basic application information and status.
    """
    return {
        "name": PROJECT_NAME,
        "version": __version__,
        "status": "ok",
        "description": "AI-powered historical interactive learning platform"
    }