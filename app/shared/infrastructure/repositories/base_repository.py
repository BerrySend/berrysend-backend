"""
Base repository implementation for generic CRUD operations.
"""
from datetime import datetime
from typing import Optional, TypeVar, Generic, Type, cast

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from app.shared.domain.models.base_entity import BaseEntity
from app.shared.infrastructure.models.base_model import BaseModelORM

# Used to represent the type of the entity.
TEntity = TypeVar("TEntity", bound=BaseEntity)

# Used to represent the type of the model to be mapped in the database.
TModel = TypeVar("TModel", bound=BaseModelORM)

class BaseRepository(Generic[TEntity, TModel]):
    """
    Base repository class for generic CRUD operations.

    """
    def __init__(self, db: AsyncSession, model: Type[TModel]):
        """
        Method to initialize the repository.

        :param db: The database session.
        :param model: The model class which is a BaseEntity.
        """
        self._db = db
        self._model: Type[TModel] = model

    def to_entity(self, model: TModel) -> TEntity:
        """
        Converts a model ORM to an entity. This needs to be implemented by the inheriting class.

        :param model: The model ORM.
        :return: The entity.
        """
        raise NotImplementedError

    def to_model(self, entity: TEntity) -> TModel:
        """
        Converts an entity to a model ORM. This needs to be implemented by the inheriting class.

        :param entity: The entity.
        :return: The model ORM.
        """
        raise NotImplementedError

    async def create(self, entity: TEntity) -> TEntity:
        """
        Method to create a new entity in the database.

        :param entity: The entity to be created.
        :return: The created entity.
        """
        model = self.to_model(entity)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        return self.to_entity(model)

    async def update(self, entity: TEntity) -> TEntity:
        """
        Method to update an existing entity in the database.

        :param entity: The entity to be updated.
        :return: The updated entity.
        """
        entity.updated_date = datetime.now
        model = self.to_model(entity)
        merged = await self._db.merge(model)
        await self._db.commit()
        await self._db.refresh(merged)
        return self.to_entity(merged)

    async def get_by_id(self, identifier: str) -> Optional[TEntity]:
        """
        Method to get an entity by its id.

        :param identifier: The id of the entity.
        :return: The entity with the given id, if found, otherwise None.
        """
        result: Result = await self._db.execute(
            select(self._model).where(self._model.id == identifier)
        )
        model = result.scalar_one_or_none()
        return self.to_entity(model) if model else None

    async def get_all(self) -> list[TEntity]:
        """
        Method to get all entities.

        :return: The list of entities.
        """
        result: Result = await self._db.execute(select(self._model))
        models = result.scalars().all()
        return [self.to_entity(m) for m in models]

    async def delete(self, identifier: str) -> None:
        """
        Method to delete an entity.

        :param identifier: The id of the entity to be deleted.
        """
        result: Result = await self._db.execute(
            select(self._model).where(self._model.id == identifier)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._db.delete(model)
            await self._db.commit()