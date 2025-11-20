from pydantic import BaseModel, Field

from app.port_management.interfaces.schemas.responses.coordinates_response import Coordinates


class PortResponse(BaseModel):
    """
    Response schema for the port entity.

    Attributes:
        id (str): The unique identifier of the port.
        name (str): The name of the port.
        country (str): The country where the port is located.
        type (str): The type of the port (e.g., initial, intermediate, destination).
        capacity (float): The capacity of the port, in tons.
        connections (int): The number of connections to other ports.
        coordinates (Coordinates): The coordinates of the port.
    """
    id: str = Field(title="The unique identifier of the port")
    name: str = Field(title="The name of the port")
    country: str = Field(title="The country where the port is located")
    type: str = Field(title="The type of the port (e.g., initial, intermediate, destination)")
    capacity: float = Field(title="The capacity of the port, in tons")
    connections: int = Field(title="The number of connections to other ports")
    coordinates: Coordinates = Field(title="The coordinates of the port")
