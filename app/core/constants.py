from __future__ import annotations

from dataclasses import dataclass


APP_NAME = "IP Geolocation API"
API_PREFIX = ""
DEFAULT_ROLE = "user"
USER_COLLECTION = "users"
LOOKUP_COLLECTION = "ip_lookups"


@dataclass(frozen=True)
class LookupFields:
    country: str = "country"
    region: str = "region"
    city: str = "city"
    latitude: str = "latitude"
    longitude: str = "longitude"
    timezone: str = "timezone"
    isp: str = "isp"
    org: str = "org"
    query: str = "query"
