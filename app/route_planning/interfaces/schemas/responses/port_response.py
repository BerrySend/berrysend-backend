from pydantic import BaseModel, Field


class PortResponse(BaseModel):
    """
    Response schema for the port entity.

    Attributes:
        id (str): The unique identifier of the port.
        name (str): The name of the port.
        country (str): The country where the port is located.
        latitude (float): The latitude coordinate of the port.
        longitude (float): The longitude coordinate of the port.
        type (str): The type of the port (e.g., initial, intermediate, destination).
    """
    id: str = Field(title="The unique identifier of the port")
    name: str = Field(title="The name of the port")
    country: str = Field(title="The country where the port is located")
    latitude: float = Field(title="The latitude coordinate of the port")
    longitude: float = Field(title="The longitude coordinate of the port")
    type: str = Field(title="The type of the port (e.g., initial, intermediate, destination)")