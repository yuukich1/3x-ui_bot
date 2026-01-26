"""Pydantic models for stream settings."""

from typing import Optional, List
from pydantic import BaseModel


class RealityInner(BaseModel):
    """Reality inner settings model."""
    publicKey: str
    fingerprint: str
    spiderX: str
    serverName: Optional[str] = ""
    mldsa65Verify: Optional[str] = ""


class RealitySettings(BaseModel):
    """Reality settings model."""
    show: bool
    xver: int
    dest: str
    serverNames: List[str]
    privateKey: str
    shortIds: List[str]
    settings: RealityInner
    mldsa65Seed: Optional[str] = ""


class TcpSettings(BaseModel):
    """TCP settings model."""
    acceptProxyProtocol: bool
    header: dict


class StreamSettings(BaseModel):
    """Stream settings model."""
    network: str
    security: str
    realitySettings: Optional[RealitySettings] = None
    tcpSettings: Optional[TcpSettings] = None
    externalProxy: List = []


class SniffingSettings(BaseModel):
    """Sniffing settings model."""
    enabled: bool
    destOverride: List[str]
    metadataOnly: bool
    routeOnly: bool