from __future__ import annotations

from functools import lru_cache

from fastapi import Depends
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.config import get_settings
from app.core.constants import LOOKUP_COLLECTION, USER_COLLECTION


@lru_cache
def get_client() -> MongoClient:
    settings = get_settings()
    return MongoClient(settings.mongo_uri)


def close_client() -> None:
    try:
        get_client().close()
    finally:
        get_client.cache_clear()


def get_db() -> Database:
    settings = get_settings()
    return get_client()[settings.mongo_db_name]


def init_db(db: Database | None = None) -> None:
    database = db or get_db()
    database[USER_COLLECTION].create_index("email", unique=True)
    database[USER_COLLECTION].create_index("created_at")
    database[LOOKUP_COLLECTION].create_index([("user_id", 1), ("requested_at", -1)])
    database[LOOKUP_COLLECTION].create_index([("ip_address", 1), ("requested_at", -1)])


def get_users_collection(db: Database = Depends(get_db)) -> Collection:
    return db[USER_COLLECTION]


def get_lookups_collection(db: Database = Depends(get_db)) -> Collection:
    return db[LOOKUP_COLLECTION]
