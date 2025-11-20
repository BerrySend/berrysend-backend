"""
Global session generator for injecting to the repositories
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

# Import the db_instance from the main file instead of creating a new one
def get_db_instance():
    """Lazy import to avoid circular dependencies"""
    from app.main import db_instance
    return db_instance

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Gets the database session.

    :return: The async session.
    """
    db = get_db_instance()
    async with db.SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()