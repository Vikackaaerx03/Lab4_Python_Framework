from __future__ import annotations

from app.core.constants import DEFAULT_ROLE
from app.core.exceptions import AuthenticationError, RegistrationError
from app.core.security import create_access_token, verify_password
from app.models.auth_models import AuthResponse, TokenResponse, UserCreate, UserLogin, UserPublic
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, payload: UserCreate) -> AuthResponse:
        email = payload.email.lower().strip()
        if self.repository.find_by_email(email) is not None:
            raise RegistrationError("User with this email already exists")

        user = self.repository.create_user(name=payload.name, email=email, password=payload.password, role=DEFAULT_ROLE)
        user_public = UserPublic(
            id=str(user["id"]),
            name=str(user["name"]),
            email=str(user["email"]),
            role=str(user.get("role", DEFAULT_ROLE)),
            created_at=user["created_at"],
        )
        token = create_access_token({"sub": user_public.id, "email": user_public.email, "role": user_public.role})
        return AuthResponse(token=TokenResponse(access_token=token), user=user_public)

    def login(self, payload: UserLogin) -> AuthResponse:
        email = payload.email.lower().strip()
        user = self.repository.find_by_email(email)
        if user is None:
            raise AuthenticationError()

        if not verify_password(payload.password, user.get("password_hash", "")):
            raise AuthenticationError()

        user_public = UserPublic(
            id=str(user["id"]),
            name=str(user["name"]),
            email=str(user["email"]),
            role=str(user.get("role", DEFAULT_ROLE)),
            created_at=user["created_at"],
        )
        token = create_access_token({"sub": user_public.id, "email": user_public.email, "role": user_public.role})
        return AuthResponse(token=TokenResponse(access_token=token), user=user_public)
