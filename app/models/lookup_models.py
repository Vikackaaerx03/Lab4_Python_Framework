from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class GeoLocation(BaseModel):
    country: str | None = None
    region: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    isp: str | None = None
    org: str | None = None
    query: str | None = None


class IpLookupCreate(BaseModel):
    ip_address: str


class IpLookupRecord(BaseModel):
    id: str
    user_id: str
    user_email: str
    ip_address: str
    requested_at: datetime
    location: GeoLocation


class LookupResponse(BaseModel):
    message: str
    record: IpLookupRecord


class HistoryResponse(BaseModel):
    items: list[IpLookupRecord]
