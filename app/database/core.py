"""
The `database` module contains functions and classes related to database
configuration and interaction.

This module provides an `engine` object for connecting to a database, as
well as a `Base` object for defining database models using SQLAlchemy.
"""

from typing import AsyncGenerator
from sqlalchemy.orm import declarative_base  # type: ignore[attr-defined]
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings


def get_database_url() -> str:
    if settings.TESTING:
        return settings.DATABASE_URL.replace("app_db", "test_app_db")
    return settings.DATABASE_URL


engine = create_async_engine(get_database_url(), echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> AsyncGenerator:
    """Get a SQLAlchemy db session to use around the app.

    Usage:

    # In a FastAPI view
    async def my_view(db: AsyncSession = Depends(get_db)) -> ReturnType:
        ...
    """
    async with async_session() as session:
        yield session
