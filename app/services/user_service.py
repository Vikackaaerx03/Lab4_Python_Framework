from __future__ import annotations

from app.core.constants import DEFAULT_ROLE
from app.core.exceptions import UserNotFoundError
from app.models.auth_models import UserPublic
from app.repositories.user_repository import UserRepository


class UserProfileService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_profile(self, current_user: dict[str, str]) -> UserPublic:
        user = self.repository.find_by_id(current_user["sub"])
        if user is None:
            raise UserNotFoundError("User not found")

        return UserPublic(
            id=str(user["id"]),
            name=str(user["name"]),
            email=str(user["email"]),
            role=str(user.get("role", DEFAULT_ROLE)),
            created_at=user["created_at"],
        )
