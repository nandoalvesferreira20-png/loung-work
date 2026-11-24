from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine():
    database_url = get_settings().database_url
    if database_url is None:
        raise RuntimeError("Configure DATABASE_URL.")
    return create_engine(database_url.get_secret_value(), pool_pre_ping=True)
