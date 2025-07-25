from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.config.settings import settings

app = FastAPI(
    title="TriprTrek API",
    description="API for AI-powered travel planning",
    version="1.0.0",
)

# Configure CORS - make it as permissive as possible for development
app.add_middleware(
    CORSMiddleware,
    # Allow all origins for development
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include API routes
app.include_router(api_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
