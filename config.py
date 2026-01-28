"""Configuration module for 3x-ui bot."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Telegram Bot
    TELEGRAM_TOKEN: str = ''
    
    # 3x-UI Panel
    THREEX_HOST: str = '127.0.0.1'
    THREEX_PORT: int = 8080
    THREEX_USERNAME: str = 'admin'
    THREEX_PASSWORD: str = 'admin'
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
