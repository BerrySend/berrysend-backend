from dataclasses import dataclass

from app.shared.domain.models.base_entity import BaseEntity

@dataclass
class Port(BaseEntity):
    """
    Represents a port in the route planning context.

    Attributes:
        name (str): The name of the port.
        country (str): The country where the port is located.
        latitude (float): The latitude coordinate of the port.
        longitude (float): The longitude coordinate of the port.
        type (str): The type of the port (e.g., initial, intermediate, destination).
        capacity (float): The capacity of the port, in tons.
    """
    name: str
    country: str
    latitude: float
    longitude: float
    type: str
    capacity: float