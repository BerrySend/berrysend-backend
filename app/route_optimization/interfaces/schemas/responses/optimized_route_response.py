from pydantic import BaseModel, Field


class OptimizedRouteResponse(BaseModel):
    """
    Represents the response for an optimized route.

    This class provides details about the optimized route, including the ports
    visited, distance traveled, time taken, and overall cost associated with the
    route. It is primarily used to summarize and return the results of an
    optimization or planning process for a given route.

    :ivar id: The unique identifier for the optimized route.
    :type id: str
    :ivar visited_ports: The list of ports visited in the order they were
        traveled.
    :type visited_ports: list[str]
    :ivar total_distance: The total distance of the optimized route.
    :type total_distance: float
    :ivar total_time: The total time required to travel the optimized route.
    :type total_time: float
    :ivar total_cost: The total cost of traveling the optimized route.
    :type total_cost: float
    """
    id: str = Field(title="The unique identifier for the optimized route.")
    visited_ports: list[str] = Field(title="The list of visited ports.")
    total_distance: float = Field(title="The total distance of the route.")
    total_time: float = Field(title="The total time required to travel the route.")
    total_cost: float = Field(title="The total cost of the route.")