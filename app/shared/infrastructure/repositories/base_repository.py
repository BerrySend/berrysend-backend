from typing import Generic, TypeVar, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# A generic type for the repository. It should represent a class
T = TypeVar("T")

"""
Base repository class for using with other repositories.
"""
class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self._db = db
        self._model = model

    """
    The 'create' method creates a new entity in the database.
    """
    async def create(self, entity: T) -> T:
        self._db.add(entity)
        await self._db.commit()
        await self._db.refresh(entity)
        return entity

    """
    The 'update' method updates an existing entity in the database.
    """
    async def update(self, entity: T) -> T:
        updated_entity = self._db.merge(entity)
        await self._db.commit()
        await self._db.refresh(updated_entity)
        return updated_entity

    """
    The 'get_by_id' method retrieves an entity by its ID.
    """
    async def get_by_id(self, id: int) -> Optional[T]:
        stmt = select(self._model).where(id == self._model.id)
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()

    """
    The 'get_all' method retrieves all entities from the database.
    """
    async def get_all(self) -> list[T]:
        stmt = select(self._model)
        result = await self._db.execute(stmt)
        return list(result.scalars().all())

    """
    The 'delete' method deletes an entity from the database.
    """
    async def delete(self, entity: T):
        await self._db.delete(entity)
        await self._db.commit()