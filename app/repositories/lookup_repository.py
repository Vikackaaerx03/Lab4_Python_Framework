from __future__ import annotations

from typing import Any
from uuid import uuid4

from pymongo.collection import Collection

from app.core.exceptions import DatabaseAppError


class LookupRepository:
    def __init__(self, lookups_collection: Collection):
        self.lookups = lookups_collection

    def create_lookup(self, document: dict[str, Any]) -> dict[str, Any]:
        payload = dict(document)
        payload["id"] = uuid4().hex

        try:
            self.lookups.insert_one(payload)
        except Exception as exc:
            raise DatabaseAppError("Failed to save lookup history") from exc

        return payload

    def list_lookups_for_user(self, user_id: str) -> list[dict[str, Any]]:
        cursor = self.lookups.find({"user_id": user_id}).sort("requested_at", -1)
        return list(cursor)
