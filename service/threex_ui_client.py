"""3x-UI Panel API client."""

import json
import uuid
from functools import wraps
from typing import Callable, TypeVar, Any, List, Optional
import httpx
from loguru import logger
from config import settings
from schemas.clients import CreateClient, CreateClientSettings
from schemas.inbounds import InboundModel
from schemas.vless import VlessURL

F = TypeVar('F', bound=Callable[..., Any])


def ensure_auth(func: F) -> F:
    """Decorator to ensure authentication before API calls."""
    @wraps(func)
    async def wrapper(self: 'ThreeXUIClient', *args: Any, **kwargs: Any) -> Any:
        if not self.cookies:
            logger.info("Session missing, attempting to login...")
            success = await self.login()
            if not success:
                logger.error("Operation aborted: Auth failed")
                return None
        return await func(self, *args, **kwargs)
    return wrapper  # type: ignore


class ThreeXUIClient:
    
    def __init__(
        self,
        host: str = settings.THREEX_HOST,
        port: int = settings.THREEX_PORT,
        username: str = settings.THREEX_USERNAME,
        password: str = settings.THREEX_PASSWORD,
        hash_panel: str = settings.THREEX_HASH_PANEL,
        spx: str = settings.THREEX_SPX,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.spx = spx
        base_path = f"/{hash_panel}" if hash_panel else ""
        self.panel_url = f"http://{self.host}:{self.port}{base_path}"
        self.cookies: Optional[httpx.Cookies] = None

    async def login(self) -> bool:
        auth_data = {"username": self.username, "password": self.password}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.panel_url}/login", data=auth_data)
                if response.status_code == 200 and response.json().get("success"):
                    self.cookies = response.cookies
                    logger.success("Authorized in 3x-ui")
                    return True
                logger.error(f"Login failed: {response.text}")
            except Exception as e:
                logger.error(f"Connection error: {e}")
            return False

    @ensure_auth
    async def get_all_inbounds(self) -> Optional[List[InboundModel]]:
        async with httpx.AsyncClient(cookies=self.cookies) as client:
            try:
                response = await client.get(f"{self.panel_url}/panel/api/inbounds/list")
                if response.status_code == 200:
                    data = response.json()
                    return [InboundModel(**item) for item in data.get("obj", [])]
            except Exception as e:
                logger.exception(f"get inbounds error: {e}")
            return None

    @ensure_auth
    async def get_inbound(self, inbound_id: int) -> Optional[InboundModel]:
        async with httpx.AsyncClient(cookies=self.cookies) as client:
            try:
                response = await client.get(f"{self.panel_url}/panel/api/inbounds/get/{inbound_id}")
                if response.status_code == 200:
                    data = response.json()
                    inbound = InboundModel(**data.get("obj"))
                    logger.debug(f"inbound: {inbound}")
                    return inbound
            except Exception as e:
                logger.error(f"get inbound error: {e}")
            return None

    async def client_list_by_inbound(self, inbound_id: int) -> Optional[List[str]]:
        inbound = await self.get_inbound(inbound_id)
        if not inbound:
            return None
        clients_email_list = [client.email for client in inbound.settings.clients]
        logger.debug(f"clients email_list: {clients_email_list}")
        return clients_email_list

    async def get_client_by_username(self, username: str) -> Any:
        inbounds = await self.get_all_inbounds()
        if not inbounds:
            return None
        for ib in inbounds:
            logger.debug(f"inbound: {ib}")
            for cl in ib.settings.clients:
                if cl.email == username:
                    return cl
        return None

    async def get_vless_url_by_username(self, username: str) -> List[str]:
        vless_urls = []
        inbounds = await self.get_all_inbounds()
        if not inbounds:
            return vless_urls
        
        for ib in inbounds:
            for cl in ib.settings.clients:
                if cl.email == username:
                    reality = ib.stream_settings.realitySettings
                    config = VlessURL(
                        protocol=ib.protocol,
                        email=cl.email,
                        port=ib.port,
                        user_id=cl.id,
                        type=ib.stream_settings.network,
                        fp=reality.settings.fingerprint,
                        security=ib.stream_settings.security,
                        sni=reality.serverNames[0] if reality.serverNames else "",
                        pbk=reality.settings.publicKey,
                        sid=reality.shortIds[0] if reality.shortIds else ""
                    )
                    vless_urls.append(self._build_vless_url(config))
        return vless_urls

    @ensure_auth
    async def add_client(self, username: str, inbound_id: int, tg_id: str = '') -> bool:
        async with httpx.AsyncClient(cookies=self.cookies) as client:
            try:
                client_data = {
                    "id": str(uuid.uuid4()),
                    "flow": "",
                    "email": username,
                    "limitIp": 0,
                    "totalGB": 0,
                    "expiryTime": 0,
                    "enable": True,
                    "tgId": str(tg_id),
                    "comment": "",
                    "reset": 0
                }
                payload = {
                    "id": str(inbound_id),
                    "settings": json.dumps({"clients": [client_data]})
                }
                response = await client.post(
                    f"{self.panel_url}/panel/api/inbounds/addClient",
                    data=payload
                )
                if response.status_code == 200:
                    res = response.json()
                    if res.get("success"):
                        logger.success(f"Client {username} created. ID: {client_data['id']}")
                        return True
                logger.error(f"Error from panel: {response.text}")
                return False
            except Exception as e:
                logger.error(f"Request failed: {e}")
                return False

    async def reload_xray(self) -> bool:
        async with httpx.AsyncClient(cookies=self.cookies) as client:
            try:
                response = await client.post(f"{self.panel_url}/panel/api/inbounds/reload")
                if response.status_code == 200:
                    logger.info("Inbound reloaded successfully")
                    return True
                else:
                    logger.error(f"Failed to reload inbound: {response.status_code} {response.text}")
            except Exception as e:
                logger.error(f"Exception while reloading inbound: {e}")
            return False

    @ensure_auth
    async def get_online(self) -> Optional[List[Any]]:
        async with httpx.AsyncClient(cookies=self.cookies) as client:
            try:
                response = await client.post(f"{self.panel_url}/panel/api/inbounds/onlines")
                if response.status_code == 200:
                    data = response.json()
                    logger.debug(f"onlines: {data.get('obj')}")
                    return data.get("obj", [])
            except Exception as e:
                logger.error(f"Get online error: {e}")
            return None

    def _build_vless_url(self, client_config: VlessURL) -> str:
        params = (
            f"type={client_config.type}"
            f"&security={client_config.security}"
            f"&pbk={client_config.pbk}"
            f"&fp={client_config.fp}"
            f"&sni={client_config.sni}"
            f"&sid={client_config.sid}"
            f"&spx=%{self.spx}"
        )

        return (
            f"{client_config.protocol}://{client_config.user_id}@{self.host}:{client_config.port}"
            f"?{params}#{client_config.email}"
        )


three_x_ui_client = ThreeXUIClient()
