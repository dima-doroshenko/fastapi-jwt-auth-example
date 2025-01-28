import sys
import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from fastapi.testclient import TestClient

BASEDIR = Path(__file__).parent.parent
sys.path.append(str(BASEDIR / "src"))

from config import settings, BASEDIR
from main import app
from database import session_dependency, Base


engine = create_async_engine(settings.db.test_url, poolclass=NullPool)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def override_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
        await session.commit()

app.dependency_overrides[session_dependency] = override_session_dependency

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

client = TestClient(app, 'http://testserver/api/v1/')

@pytest.fixture(scope='session')
async def ac():
    async with AsyncClient(transport=ASGITransport(app), base_url=client.base_url) as ac:
        yield ac
        