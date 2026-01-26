import uuid
from typing import Optional, List
from pydantic import BaseModel, Field


class ClientStat(BaseModel):
    id: int
    inboundId: int
    enable: bool
    email: str
    up: int
    down: int
    allTime: int
    expiryTime: int
    total: int
    reset: int


class XUIClient(BaseModel):
    id: str
    email: str
    enable: bool = True
    expiryTime: int
    totalGB: int
    subId: str = ""
    tgId: int | str
    flow: Optional[str] = ""
    limitIp: int = 0
    reset: int = 0
    comment: Optional[str] = ""
    created_at: int
    updated_at: int


class InboundSettings(BaseModel):
    clients: List[XUIClient]
    decryption: str = "none"
    fallbacks: List = []


class CreateClient(BaseModel):
    id: int
    settings: str


class CreateClientSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    flow: str = ""
    email: str
    limitIp: int = 0
    totalGB: int = 0
    expiryTime: int = 0
    enable: bool = True
    tgId: str = ""
    comment: str = ""
    reset: int = 0
