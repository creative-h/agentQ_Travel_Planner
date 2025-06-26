from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    AMADEUS_API_KEY: str = os.getenv("AMADEUS_API_KEY", "")
    AMADEUS_API_SECRET: str = os.getenv("AMADEUS_API_SECRET", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tripy_trek_db")
    
    # Application
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # LLM Model Configuration
    LLM_MODEL: str = "llama3-8b-8192"  # Default Groq LLaMa 3 model
    
    # Trip Constants
    MAX_TRIP_DAYS: int = 30
    MIN_TRIP_DAYS: int = 1
    MAX_TRAVELERS: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
