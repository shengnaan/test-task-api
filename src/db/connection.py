import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base

engine: AsyncEngine | None = None
async_session: sessionmaker | None = None


def build_engine() -> AsyncEngine:
    from core.config import Settings
    url = Settings.TEST_DATABASE_URL if os.getenv("USE_TEST_DB") == "true" \
        else Settings.DATABASE_URL
    return create_async_engine(url, echo=False, future=True)


async def init_models() -> None:
    global engine, async_session
    engine = build_engine()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models() -> None:
    if engine is not None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


async def dispose_engine() -> None:
    if engine is not None:
        await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if async_session is None:
        init = build_engine()
        session = sessionmaker(init, class_=AsyncSession, expire_on_commit=False)
    else:
        session = async_session

    async with session() as db:
        yield db
