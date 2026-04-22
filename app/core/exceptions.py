from __future__ import annotations


class AppError(Exception):
    status_code = 400
    default_detail = "Application error"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class ValidationAppError(AppError):
    status_code = 422
    default_detail = "Validation failed"


class RegistrationError(AppError):
    status_code = 409
    default_detail = "User already exists"


class AuthenticationError(AppError):
    status_code = 401
    default_detail = "Invalid email or password"


class AuthorizationError(AppError):
    status_code = 403
    default_detail = "Access denied"


class UserNotFoundError(AppError):
    status_code = 404
    default_detail = "User not found"


class InvalidIPError(AppError):
    status_code = 422
    default_detail = "Invalid IP address"


class GeoLookupError(AppError):
    status_code = 502
    default_detail = "Unable to get geolocation data"


class DatabaseAppError(AppError):
    status_code = 500
    default_detail = "Database error"
