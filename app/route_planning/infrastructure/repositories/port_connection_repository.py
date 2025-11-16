from sqlalchemy.ext.asyncio import AsyncSession

from app.route_planning.infrastructure.models.port_connection_model import PortConnectionModel
from app.shared.infrastructure.repositories.base_repository import BaseRepository
from app.route_planning.domain.models.port_connection import PortConnection

class PortConnectionRepository(BaseRepository[PortConnection, PortConnectionModel]):
    def __init__(self, db: AsyncSession):
        """
        Initializes a new instance of PortConnectionRepository.

        :param db: The database session
        """
        super().__init__(db, PortConnectionModel)

    def to_model(self, entity: PortConnection) -> "PortConnectionModel":
        return PortConnectionModel(
            id=entity.id,

        )