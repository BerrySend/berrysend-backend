from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.shared.infrastructure.config.base_config import config

# Creates an async engine for the database
engine = create_async_engine(
    config.DATABASE_URL,
    echo = True,
    future = True,
    pool_pre_ping = True
)

# Creates an async session for the database
async_sesion_local = async_sessionmaker(
    class_= AsyncSession,
    autoflush = False,
    autocommit = False,
    expire_on_commit = False,
    bind=engine
)