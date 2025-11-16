from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.orm import Mapped

from app.shared.infrastructure.models.base_model import BaseModelORM

class PortConnectionModel(BaseModelORM):
    """
    Model class for mapping the port connection information into the database.

    Attributes:
        port_a_id (str): The id of the port a
        port_b_id (str): The id of the port b
        distance_km (str): The distance km from the port "a" to the port "b"
        time_hours (str): The time hours that the port "a" to the port "b"
        cost_usd (str): The cost of the port "a" to the port "b"
        route_type (str): The route type that the port "a" to the port "b"
        is_restricted (bool): Whether the port "a" to the port "b" is restricted
    """
    __tablename__ = "port_connections"

    port_a_id: Mapped[str] = Column(String(36), nullable=False)
    port_b_id: Mapped[str] = Column(String(36), nullable=False)
    distance_km: Mapped[float] = Column(Float, nullable=False)
    time_hours: Mapped[float] = Column(Float, nullable=False)
    cost_usd: Mapped[float] = Column(Float, nullable=False)
    route_type: Mapped[str] = Column(String(255), nullable=False)
    is_restricted: Mapped[bool] = Column(Boolean, nullable=False)