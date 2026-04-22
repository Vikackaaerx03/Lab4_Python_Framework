from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = Field(default="mongodb://localhost:27017", alias="MONGO_URI")
    mongo_db_name: str = Field(default="lab4_ip_geo", alias="MONGO_DB_NAME")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    geo_api_url: str = Field(default="http://ip-api.com/json/{ip}", alias="GEO_API_URL")
    geo_timeout_seconds: float = Field(default=7.0, alias="GEO_TIMEOUT_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
