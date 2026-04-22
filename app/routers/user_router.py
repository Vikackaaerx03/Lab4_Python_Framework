from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.db.database import get_users_collection
from app.models.auth_models import UserPublic
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserProfileService

router = APIRouter(tags=["User"])


def get_profile_service(users_collection=Depends(get_users_collection)) -> UserProfileService:
    return UserProfileService(UserRepository(users_collection))


@router.get("/auth/me", response_model=UserPublic)
def me(current_user: dict = Depends(get_current_user), service: UserProfileService = Depends(get_profile_service)):
    return service.get_profile(current_user)
