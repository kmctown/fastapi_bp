import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.config import settings
from app.database.core import Base
from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="session", autouse=True)
def test_db() -> Generator:
    # Change the database URL to use the test database
    test_db_url = settings.DATABASE_URL

    # Replace 'postgresql+asyncpg' with 'postgresql' to use the
    # synchronous psycopg dialect
    sync_test_db_url = test_db_url.replace("postgresql+asyncpg", "postgresql")

    sync_engine = create_engine(sync_test_db_url)

    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)

    # Run migrations on test database
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", sync_test_db_url)
    upgrade(alembic_cfg, "head")

    yield

    # Drop the test database after tests are completed
    drop_database(sync_engine.url)


@pytest_asyncio.fixture(autouse=True)
async def clear_tables(test_db: AsyncGenerator) -> AsyncGenerator:
    """Clear tables between each test"""
    async_engine = create_async_engine(settings.DATABASE_URL)

    async with async_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())

    yield
