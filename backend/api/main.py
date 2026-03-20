"""
FastAPI main application entrypoint
"""
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.server import router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create single FastAPI app instance
app = FastAPI(
    title="Thunderball API",
    description="Python wrapper API for COBOL modules and Db2 integration",
    version="1.0.0"
)

# Add CORS middleware FIRST (before routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve spell images from backend/assets/
_assets_dir = Path(__file__).resolve().parent.parent / "assets"
app.mount("/assets", StaticFiles(directory=_assets_dir), name="assets")

# Include routes AFTER middleware
app.include_router(router)

# Root endpoints
@app.get("/")
async def root():
    """Return API status message."""
    return {"message": "Thunderball API is running"}

@app.get("/health")
async def health():
    """Return health check status."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
