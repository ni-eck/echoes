"""Application settings."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    openai_api_key: str
    openai_model: str = "gpt-4o"
    project_name: str = "Echoes"

# Singleton settings instance
settings = Settings()

# Export commonly used settings
OPENAI_API_KEY = settings.openai_api_key
MODEL = settings.openai_model
PROJECT_NAME = settings.project_name