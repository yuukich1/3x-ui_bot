"""Database repository for user operations."""

from typing import Optional
from loguru import logger
from sqlalchemy import select, update, insert
from database.models import Users as UserModels
from database.base import db_manager


class UsersRepo:
    """Repository for user database operations."""
    
    def __init__(self):
        self.db_manager = db_manager

    async def get_user_by_username(self, username: str) -> Optional[UserModels]:
        """Get user by username."""
        async with self.db_manager.get_session() as session:
            stmt = select(UserModels).where(UserModels.username == username)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def add_new_users(self, username: str, tg_id: int) -> Optional[UserModels]:
        """Add new user to database."""
        async with self.db_manager.get_session() as session:
            try:
                stmt = insert(UserModels).values(username=username, tg_id=tg_id).returning(UserModels)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar()
            except Exception as e:
                logger.error(f"DB Error: {e}")
                await session.rollback()
                return None

    async def update_users_vless_link(
        self, username: str, vless_link: str, vless_uuid: str
    ) -> Optional[UserModels]:
        """Update user's VLESS link."""
        async with self.db_manager.get_session() as session:
            try:
                stmt = (
                    update(UserModels)
                    .values(vless_uuid=vless_uuid, vless_link=vless_link)
                    .where(UserModels.username == username)
                    .returning(UserModels)
                )
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar()
            except Exception as e:
                logger.error(f"Update error: {e}")
                await session.rollback()
                return None
