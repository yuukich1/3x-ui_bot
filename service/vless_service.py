"""VLESS service module."""

from typing import Optional
from loguru import logger
from database.crud import UsersRepo
from service.threex_ui_client import three_x_ui_client
from config import settings


class VlessService:
    """Service for managing VLESS clients."""
    
    def __init__(self):
        self.users_repo = UsersRepo()

    async def get_vless_link(self, username: str) -> Optional[str]:
        """Get VLESS link for user."""
        user = await self.users_repo.get_user_by_username(username=username)
        
        if user and user.vless_link:
            return user.vless_link
        
        vless_links = await three_x_ui_client.get_vless_url_by_username(username=username)
        return vless_links[0] if vless_links else None

    async def create_vless_client(self, username: str) -> bool:
        """Create new VLESS client."""
        existing_link = await self.get_vless_link(username)
        if existing_link:
            raise Exception('Client already exists')
        
        try:
            await three_x_ui_client.add_client(
                username=username,
                inbound_id=settings.INBOUND_ID
            )
            client = await three_x_ui_client.get_client_by_username(username=username)
            if not client:
                raise Exception('Failed to get created client')
            
            logger.info(f"Created VLESS client: {client}")
            
            vless_links = await three_x_ui_client.get_vless_url_by_username(username=username)
            if not vless_links:
                raise Exception('Failed to get VLESS URL')
            
            await self.users_repo.update_users_vless_link(
                username=username,
                vless_link=vless_links[0],
                vless_uuid=client.subId
            )
            return True
        except Exception as e:
            logger.error(f"Failed to create VLESS client: {e}")
            raise