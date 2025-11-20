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
            type=entity.type,
            capacity=entity.capacity,
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
            type=model.type,
            capacity=model.capacity,
            updated_at=model.updated_at,
            created_at=model.created_at
        )