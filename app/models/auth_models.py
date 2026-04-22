from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

from app.core.constants import DEFAULT_ROLE

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
UserRole = Literal["user", "admin"]


def _clean_email(value: str) -> str:
    cleaned = value.strip().lower()
    if not EMAIL_PATTERN.fullmatch(cleaned):
        raise ValueError("Email must be a valid address")
    return cleaned


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("Name cannot be empty")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return _clean_email(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must contain at least 6 characters")
        return value


class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return _clean_email(value)


class UserPublic(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole = DEFAULT_ROLE
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    token: TokenResponse
    user: UserPublic
