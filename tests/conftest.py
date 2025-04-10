import asyncio

from dotenv import load_dotenv

load_dotenv(".env.test")

import logging

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import Settings
from main import app
from src.db.connection import get_db
from src.db.models import Base

logging.getLogger("httpx").setLevel(logging.WARNING)

engine = create_async_engine(Settings.TEST_DATABASE_URL, echo=False)
AsyncSessionFactory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def override_get_db():
    async def _get_db():
        async with AsyncSessionFactory() as session:
            try:
                yield session
            finally:
                await session.commit()

    app.dependency_overrides[get_db] = _get_db
    yield

    del app.dependency_overrides[get_db]
