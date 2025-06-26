import uvicorn
from app.utils.logging import configure_logging

logger = configure_logging()

if __name__ == "__main__":
    logger.info("Starting TriprTrek API server")
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        log_level="info"
    )
