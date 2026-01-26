"""Pydantic models for 3x-UI inbounds."""

from typing import List
from pydantic import BaseModel, Json, Field
from schemas.clients import ClientStat, InboundSettings
from schemas.settings import StreamSettings, SniffingSettings


class InboundModel(BaseModel):
    """3x-UI inbound model."""
    id: int
    up: int
    down: int
    total: int
    allTime: int
    remark: str
    enable: bool
    expiryTime: int
    port: int
    protocol: str
    tag: str
    listen: str = ""

    clientStats: List[ClientStat] | None

    settings: Json[InboundSettings]
    stream_settings: Json[StreamSettings] = Field(alias="streamSettings")
    sniffing: Json[SniffingSettings]

    class Config:
        populate_by_name = True