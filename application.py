import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from app.main import app

frontend_build = os.path.join(os.path.dirname(__file__), 'frontend', 'build')

app.mount("/static", StaticFiles(directory=os.path.join(frontend_build, "static")), name="static")

@app.get("/favicon.ico")
async def favicon():
    path = os.path.join(frontend_build, "favicon.ico")
    return FileResponse(path) if os.path.exists(path) else Response(status_code=204)

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    if full_path.startswith("api/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404)
    return FileResponse(os.path.join(frontend_build, "index.html"))
