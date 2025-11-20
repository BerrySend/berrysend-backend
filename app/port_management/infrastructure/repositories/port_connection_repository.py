from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.port_management.infrastructure.models.port_connection_model import PortConnectionModel
from app.shared.infrastructure.repositories.base_repository import BaseRepository, TModel, TEntity
from app.port_management.domain.models.port_connection import PortConnection

class PortConnectionRepository(BaseRepository[PortConnection, PortConnectionModel]):
    def __init__(self, db: AsyncSession):
        """
        Initializes a new instance of PortConnectionRepository.

        :param db: The database session
        """
        super().__init__(db, PortConnectionModel)

    def to_model(self, entity: PortConnection) -> "PortConnectionModel":
        """
        Transform a port connection entity into a port connection model.

        :param entity: The port connection entity to transform.

        :return: The corresponding port connection model.
        """
        return PortConnectionModel(
            id=entity.id,
            port_a_id=entity.port_a_id,
            port_a_name=entity.port_a_name,
            port_b_id=entity.port_b_id,
            port_b_name=entity.port_b_name,
            distance_km=entity.distance_km,
            time_hours=entity.time_hours,
            cost_usd=entity.cost_usd,
            route_type=entity.route_type,
            is_restricted=entity.is_restricted
        )

    def to_entity(self, model: PortConnectionModel) -> "PortConnection":
        """
        Transform a port connection model into a port connection entity.

        :param model: The port connection model to transform.

        :return: The corresponding port connection entity.
        """
        return PortConnection(
            id=model.id,
            port_a_id=model.port_a_id,
            port_a_name=model.port_a_name,
            port_b_id=model.port_b_id,
            port_b_name=model.port_b_name,
            distance_km=model.distance_km,
            time_hours=model.time_hours,
            cost_usd=model.cost_usd,
            route_type=model.route_type,
            is_restricted=model.is_restricted
        )

    async def get_connections_by_port_id(self, port_id: str) -> list["PortConnection"]:
        """
        Retrieve all port connections for a given port id.

        :param port_id: The id of the port.

        :return: A list of port connections associated with the given port id.
        """
        result: Result = await self._db.execute(
            select(self._model).where(self._model.port_a_id == port_id)
        )
        model = result.scalars().all()
        return [self.to_entity(m) for m in model]