from pydantic import BaseModel, Field


class GenerateRouteRequest(BaseModel):
    """
    Represents a request to generate a route with specific parameters.

    This class is used to encapsulate the necessary information required to
    generate a route from a specified source to a destination using a certain
    mode of transportation and a specified routing algorithm.

    :ivar source: The starting point/location for the route.
    :type source: str
    :ivar destination: The ending point/location for the route.
    :type destination: str
    :ivar mode: The transportation mode to use for the route (e.g., maritime or air)
    :type mode: str
    :ivar algorithm_name: The name of the routing algorithm to plan the route
        (e.g., Dijkstra, A*).
    :type algorithm_name: str
    """
    source: str = Field(title="The starting port for the route.")
    destination: str = Field(title="The ending port for the route.")
    mode: str = Field(title="The transportation mode for the route (e.g., maritime or air).")
    algorithm_name: str = Field(title="The name of the routing algorithm to plan the route (only can be A* or Dijkstra).")