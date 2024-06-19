import asyncio
from typing import AsyncIterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app
from src.settings.database import Base, get_db_session, DatabaseSessionManager

DATABASE_URL = "sqlite+aiosqlite:///./testing.db"

test_session_manager = DatabaseSessionManager(DATABASE_URL, engine_kwargs={"echo": True})


async def init_db():
    async with test_session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def override_get_db_session() -> AsyncIterator[AsyncSession]:
    async with test_session_manager.session() as session:
        yield session

app.dependency_overrides[get_db_session] = override_get_db_session


@pytest.fixture(scope="module")
def client():
    asyncio.run(init_db())

    with TestClient(app) as c:
        yield c

    asyncio.run(test_session_manager.close())


async def cleanup_db():
    async with test_session_manager.session() as session:
        async with session.begin():
            await session.execute(text("DELETE FROM character"))
            await session.commit()


@pytest.fixture(autouse=True)
def cleanup_db_fixture():
    asyncio.run(cleanup_db())

