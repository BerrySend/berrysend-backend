from typing import Generic, TypeVar, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository class for generic CRUD operations."""

    def __init__(self, db: AsyncSession, model: Type[T]):
        self._db = db
        self._model = model

    async def create(self, entity: T) -> T:
        self._db.add(entity)
        await self._db.commit()
        await self._db.refresh(entity)
        return entity

    async def update(self, entity: T) -> T:
        updated_entity = self._db.merge(entity)  # merge no es awaitable
        await self._db.commit()
        await self._db.refresh(updated_entity)
        return updated_entity

    async def get_by_id(self, id: int) -> Optional[T]:
        stmt = select(self._model).where(self._model.id == id)
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[T]:
        stmt = select(self._model)
        result = await self._db.execute(stmt)
        return result.scalars().all()

    async def delete(self, entity: T):
        await self._db.delete(entity)
        await self._db.commit()
