import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Configurações gerais
    APP_NAME: str = "Gym Workout Management"
    DEBUG: bool = False
    ENV: str = os.getenv("ENV", "development")

    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_default_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configurações de banco de dados
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    DATABASE_CONNECT_DICT: dict = {}

    # Configurações de email (exemplo)
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT: int = os.getenv("SMTP_PORT", 587)
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "user@example.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "your_password")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@example.com")
    EMAIL_TO: str = os.getenv("EMAIL_TO", "admin@example.com")

    # Configurações adicionais
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    class Config:
        case_sensitive = True
        env_file = ".env"

# Instanciação das configurações
settings = Settings()
