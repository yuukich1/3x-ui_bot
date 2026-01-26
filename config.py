"""Configuration module for 3x-ui bot."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Telegram Bot
    TELEGRAM_TOKEN: str = '6074700070:AAEUZGmYTKzSGEul-tfvecYnSFdnxsDCVuA'
    
    # 3x-UI Panel
    THREEX_HOST: str = '46.226.165.208'
    THREEX_PORT: int = 8080
    THREEX_USERNAME: str = 'Ky0WV7sjpF'
    THREEX_PASSWORD: str = '70gkfXDh0M'
    THREEX_HASH_PANEL: str = '0RhWnlULBur17Smznu'
    THREEX_SPX: str = '2F'
    
    # Database
    DATABASE_URL: str = 'sqlite+aiosqlite:///db.sql'
    
    # Inbound
    INBOUND_ID: int = 1
    
    # Logging
    LOG_LEVEL: str = 'INFO'
    
    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
