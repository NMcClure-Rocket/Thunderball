"""
FastAPI main application entrypoint
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.server import router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create single FastAPI app instance
app = FastAPI(
    title="Thunderball API",
    description="Python wrapper API for COBOL modules and Db2 integration",
    version="1.0.0"
)

# ✅ Add CORS middleware FIRST (before routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routes AFTER middleware
app.include_router(router)


# Root endpoints
@app.get("/")
async def root():
    return {"message": "Thunderball API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
