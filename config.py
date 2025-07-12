import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "sqlite:///./smart_force.db"
    
    # Security
    secret_key: str = "your-secret-key-here-make-it-long-and-random"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application Settings
    debug: bool = False
    environment: str = "development"
    log_level: str = "INFO"
    
    # CORS Settings
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Cache Settings
    redis_url: Optional[str] = None
    
    # Email Settings
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Google OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings() 