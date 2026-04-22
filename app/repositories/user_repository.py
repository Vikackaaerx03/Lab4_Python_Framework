from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pymongo.collection import Collection

from app.core.constants import DEFAULT_ROLE
from app.core.exceptions import DatabaseAppError
from app.core.security import hash_password


class UserRepository:
    def __init__(self, users_collection: Collection):
        self.users = users_collection

    def find_by_email(self, email: str) -> dict[str, Any] | None:
        return self.users.find_one({"email": email.lower().strip()})

    def find_by_id(self, user_id: str) -> dict[str, Any] | None:
        return self.users.find_one({"id": user_id})

    def create_user(self, *, name: str, email: str, password: str, role: str = DEFAULT_ROLE) -> dict[str, Any]:
        document = {
            "id": uuid4().hex,
            "name": " ".join(name.split()),
            "email": email.lower().strip(),
            "password_hash": hash_password(password),
            "role": role,
            "created_at": datetime.now(timezone.utc),
        }

        try:
            self.users.insert_one(document)
        except Exception as exc:
            raise DatabaseAppError("Failed to create user") from exc

        return document
