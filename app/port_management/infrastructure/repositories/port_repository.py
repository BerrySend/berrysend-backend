from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.port_management.domain.models.port import Port
from app.port_management.infrastructure.models.port_model import PortModel
from app.shared.infrastructure.repositories.base_repository import BaseRepository

class PortRepository(BaseRepository[Port, PortModel]):
    def __init__(self, db: AsyncSession):
        """
        Initialize the port repository.

        :param db: The database session.
        """
        super().__init__(db, PortModel)

    def to_model(self, entity: Port) -> "PortModel":
        """
        Transform a port entity into a port model.

        :param entity: The port entity to transform.
        :return: The corresponding port model.
        """
        return PortModel(
            id=entity.id,
            name=entity.name,
            latitude=entity.latitude,
            longitude=entity.longitude,
            country=entity.country,
            in_graph_type=entity.in_graph_type,
            capacity=entity.capacity,
            port_type=entity.port_type,
            updated_at=entity.updated_at,
            created_at=entity.created_at
        )

    def to_entity(self, model: PortModel) -> "Port":
        """
        Transform a port model into a port entity.

        :param model: The port model to transform.
        :return: The corresponding port entity.
        """
        return Port(
            id=model.id,
            name=model.name,
            latitude=model.latitude,
            longitude=model.longitude,
            country=model.country,
            in_graph_type=model.in_graph_type,
            capacity=model.capacity,
            port_type=model.port_type,
            updated_at=model.updated_at,
            created_at=model.created_at
        )

    async def get_all_maritime_ports(self):
        """
        Retrieve all maritime ports.

        :return: A list of maritime port entities.
        """
        maritime_result: Result = await self._db.execute(
            select(self._model).where(self._model.port_type == 'maritime')
        )
        both_result: Result = await self._db.execute(
            select(self._model).where(self._model.port_type == 'both')
        )

        both_models = both_result.scalars().all()
        maritime_models = maritime_result.scalars().all()

        result_models = [self.to_entity(model) for model in both_models] + [self.to_entity(model) for model in maritime_models]

        return result_models

    async def get_all_air_ports(self):
        """
        Retrieve all airports.

        :return: A list of airport entities.
        """
        air_result: Result = await self._db.execute(
            select(self._model).where(self._model.port_type == 'air')
        )
        both_result: Result = await self._db.execute(
            select(self._model).where(self._model.port_type == 'both')
        )

        both_models = both_result.scalars().all()
        air_models = air_result.scalars().all()

        result_models = [self.to_entity(model) for model in both_models] + [self.to_entity(model) for model in air_models]

        return result_models

    async def get_port_by_name(self, name: str):
        """
        Retrieve a port by its name. First tries exact match, then partial match.

        :param name: The name of the port to retrieve.
        :return: The port entity if found, otherwise None.
        """

        # Try exact match first
        result: Result = await self._db.execute(
            select(self._model).where(self._model.name == name)
        )
        model = result.scalars().first()
        
        # If no exact match, try partial match (e.g., "Buenos Aires" matches "Buenos Aires (EZE Argentina)")
        if not model:
            result: Result = await self._db.execute(
                select(self._model).where(self._model.name.like(f"{name}%"))
            )
            model = result.scalars().first()
        
        if model:
            return self.to_entity(model)
        return None