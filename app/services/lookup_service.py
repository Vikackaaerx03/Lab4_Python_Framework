from __future__ import annotations

import ipaddress
from datetime import datetime, timezone
from typing import Any

import requests

from app.core.config import get_settings
from app.core.exceptions import GeoLookupError, InvalidIPError
from app.models.lookup_models import GeoLocation, HistoryResponse, IpLookupCreate, IpLookupRecord, LookupResponse
from app.repositories.lookup_repository import LookupRepository


class LookupService:
    def __init__(self, repository: LookupRepository):
        self.repository = repository

    def lookup_ip(self, payload: IpLookupCreate, current_user: dict[str, Any]) -> LookupResponse:
        normalized_ip = self._validate_ip(payload.ip_address)
        location = self._fetch_geolocation(normalized_ip)
        record = self.repository.create_lookup(
            {
                "user_id": current_user["sub"],
                "user_email": current_user["email"],
                "ip_address": normalized_ip,
                "requested_at": datetime.now(timezone.utc),
                "location": location.model_dump(),
            }
        )
        return LookupResponse(message="Geolocation data received successfully", record=IpLookupRecord(**record))

    def history(self, current_user: dict[str, Any]) -> HistoryResponse:
        items = [IpLookupRecord(**item) for item in self.repository.list_lookups_for_user(current_user["sub"])]
        return HistoryResponse(items=items)

    def _validate_ip(self, value: str) -> str:
        try:
            return str(ipaddress.ip_address(value.strip()))
        except Exception as exc:
            raise InvalidIPError("Invalid IP address format") from exc

    def _fetch_geolocation(self, ip_address: str) -> GeoLocation:
        settings = get_settings()
        url = settings.geo_api_url.format(ip=ip_address)

        try:
            response = requests.get(url, timeout=settings.geo_timeout_seconds)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise GeoLookupError("Failed to contact geolocation service") from exc

        if not isinstance(data, dict):
            raise GeoLookupError("Unexpected response from geolocation service")

        if data.get("status") == "fail":
            raise GeoLookupError(data.get("message") or "Geolocation service returned an error")

        return GeoLocation(
            country=data.get("country"),
            region=data.get("regionName") or data.get("region"),
            city=data.get("city"),
            latitude=data.get("lat"),
            longitude=data.get("lon"),
            timezone=data.get("timezone"),
            isp=data.get("isp"),
            org=data.get("org"),
            query=data.get("query") or ip_address,
        )
