from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Mapped

from app.shared.infrastructure.models.base_model import BaseModelORM

class PortModel(BaseModelORM):
    """
    Model class for mapping the port entity fields into the database.

    Attributes:
        name (str): the name of the port
        country (str): the country where the port is located
        latitude (float): the latitude coordinate of the port
        longitude (float): the longitude coordinate of the port
        type (str): the type of the port (e.g., initial, intermediate, destination)
        capacity (float): the capacity of the port, in tons
    """
    __tablename__ = "ports"

    name: Mapped[str] = Column(String(255), unique=True, nullable=False)
    country: Mapped[str] = Column(String(255), nullable=False)
    latitude: Mapped[float] = Column(Float, nullable=False)
    longitude: Mapped[float] = Column(Float, nullable=False)
    type: Mapped[str] = Column(String(255), nullable=False)
    capacity: Mapped[float] = Column(Float, nullable=False)