"""Database base configuration."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings
from loguru import logger


class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""
    pass


class DatabaseManager:
    """Database connection manager."""
    
    def __init__(self, database_url: str = settings.DATABASE_URL):
        self.engine = create_async_engine(database_url, echo=False)
        self.session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    def get_session(self):
        """Get async database session context manager."""
        return self.session_maker()
    
    async def init_db(self) -> None:
        """Initialize database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.success("Database initialized")
    
    async def close(self) -> None:
        """Close database connection."""
        await self.engine.dispose()
        logger.info("Database connection closed")


db_manager = DatabaseManager()
