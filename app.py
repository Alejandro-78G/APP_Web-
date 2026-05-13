from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
import logging
from config import get_settings
from github_client import GitHubClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Portfolio API")
settings = get_settings()
github_client = GitHubClient()

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

def load_projects():
    """Helper to load and parse proyectos.json"""
    file_path = os.path.join(os.path.dirname(__file__), 'proyectos.json')
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading projects: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the index page with projects."""
    data = load_projects()
    projects = data.get("projects", []) if data else []
    return templates.TemplateResponse("index.html", {"request": request, "projects": projects, "settings": settings})

@app.get("/project/{slug}", response_class=HTMLResponse)
async def read_project(request: Request, slug: str):
    """Render the project detail page."""
    data = load_projects()
    projects = data.get("projects", []) if data else []
    project = next((p for p in projects if p.get("slug") == slug or p.get("id") == slug), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("project_detail.html", {"request": request, "project": project, "settings": settings})

@app.get("/api/projects")
async def get_projects():
    """Returns the list of projects from proyectos.json."""
    data = load_projects()
    if data is None:
        raise HTTPException(status_code=500, detail="Error loading projects data. Please check server logs.")
    return data

@app.get("/api/github/{owner}/{repo}")
async def get_github_metrics(owner: str, repo: str):
    """Fetches metrics for a specific GitHub repository."""
    repo_full_name = f"{owner}/{repo}"
    metrics = await github_client.get_repo_metrics(repo_full_name)
    if metrics.get("error"):
        # We still return 200 with the error object so the frontend can handle it gracefully without breaking
        return metrics
    return metrics

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok", "app_title": settings.APP_TITLE}

@app.get("/test")
async def run_link_validator():
    """Runs the link validator and returns the results."""
    from link_validator import validate_links
    if not settings.APP_DEBUG:
        raise HTTPException(status_code=403, detail="Test endpoint is only available in debug mode.")
    results = await validate_links(silent=True)
    return results
