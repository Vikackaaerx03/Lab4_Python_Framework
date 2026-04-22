from __future__ import annotations

from fastapi import APIRouter, Depends

from app.db.database import get_users_collection
from app.models.auth_models import AuthResponse, UserCreate, UserLogin
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(users_collection=Depends(get_users_collection)) -> AuthService:
    return AuthService(UserRepository(users_collection))


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(payload: UserCreate, service: AuthService = Depends(get_auth_service)):
    return service.register(payload)


@router.post("/login", response_model=AuthResponse)
def login(payload: UserLogin, service: AuthService = Depends(get_auth_service)):
    return service.login(payload)
