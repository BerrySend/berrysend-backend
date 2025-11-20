from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """
    Manages geographical coordinates.

    This class is used to represent and store geographical coordinates, including
    latitude and longitude. It ensures structured storage and retrieval of
    coordinate values, commonly used in geographical data handling.

    :ivar latitude: The latitude coordinate of the port.
    :type latitude: float
    :ivar longitude: The longitude coordinate of the port.
    :type longitude: float
    """
    latitude: float = Field(title="The latitude coordinate of the port")
    longitude: float = Field(title="The longitude coordinate of the port")