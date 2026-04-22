from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError, AuthorizationError


auth_scheme = HTTPBearer(auto_error=False)

_PBKDF2_ALG = "pbkdf2_sha256"
_PBKDF2_ITERATIONS = 200_000
_PBKDF2_SALT_BYTES = 16


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(_PBKDF2_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS)
    return f"{_PBKDF2_ALG}${_PBKDF2_ITERATIONS}${_b64encode(salt)}${_b64encode(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        alg, iterations_str, salt_b64, digest_b64 = password_hash.split("$", 3)
        if alg != _PBKDF2_ALG:
            return False
        iterations = int(iterations_str)
        salt = _b64decode(salt_b64)
        expected = _b64decode(digest_b64)
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(candidate, expected)
    except Exception:
        return False


def _sign(value: str) -> str:
    settings = get_settings()
    secret = settings.secret_key.encode("utf-8")
    return hmac.new(secret, value.encode("ascii"), hashlib.sha256).hexdigest()


def create_access_token(payload: dict[str, Any]) -> str:
    settings = get_settings()
    data = dict(payload)
    data["exp"] = int(time.time()) + settings.access_token_expire_minutes * 60
    body = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    encoded = _b64encode(body)
    return f"{encoded}.{_sign(encoded)}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        encoded, signature = token.rsplit(".", 1)
    except ValueError as exc:
        raise AuthenticationError("Malformed access token") from exc

    if not hmac.compare_digest(signature, _sign(encoded)):
        raise AuthenticationError("Invalid access token")

    try:
        payload = json.loads(_b64decode(encoded).decode("utf-8"))
    except Exception as exc:
        raise AuthenticationError("Invalid access token payload") from exc

    if not isinstance(payload, dict):
        raise AuthenticationError("Invalid access token payload")

    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(time.time()):
        raise AuthenticationError("Access token expired")

    return payload


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(auth_scheme)) -> dict[str, Any]:
    if credentials is None:
        raise AuthenticationError("Missing bearer token")
    return decode_access_token(credentials.credentials)


def require_auth_user(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    return current_user


def require_admin(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    if current_user.get("role") != "admin":
        raise AuthorizationError("Admin access required")
    return current_user
