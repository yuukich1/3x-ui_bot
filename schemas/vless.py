"""VLESS URL configuration model."""

from pydantic import BaseModel


class VlessURL(BaseModel):
    """VLESS URL configuration."""
    protocol: str
    email: str
    port: int
    user_id: str
    type: str
    security: str
    pbk: str
    fp: str
    sni: str
    sid: str