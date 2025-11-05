"""
Global session generator for injecting to the repositories
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.persistence.database import Database

# Instance for Database
db_instance = Database()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Gets the database session.

    :return: The async session.
    """
    async with db_instance.SessionLocal() as session:
        yield session