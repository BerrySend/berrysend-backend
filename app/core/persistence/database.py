import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.base_config import config
from app.core.persistence.base import base
from app.core.persistence.engine import engine, async_sesion_local

"""
    This module is responsible for creating the database and tables.
"""
async def create_database():
    url_without_db = str(config.DATABASE_URL).rsplit("/", 1)[0]
    engine_tmp = create_async_engine(url_without_db, echo = True)

    async with engine_tmp.begin() as conn:
        await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config.DATABASE_NAME}"))

    await engine_tmp.dispose()

"""
    This module is responsible for initializing the tables.
"""
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

"""
    This module is responsible for creating the database and tables.
"""
async def main():
    await create_database()
    await init_tables()

"""
    This module is responsible for getting the database session.
"""
async def get_db():
    async with async_sesion_local() as session:
        yield session

"""
    This module is responsible for initializing the database.
"""
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

# Main function
if __name__ == "__main__":
    asyncio.run(main())