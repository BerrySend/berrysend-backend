from pydantic import BaseModel, Field


class OptimizedRouteResponse(BaseModel):
    """
    Represents a response for an optimized route, providing detailed information about
    the route's properties, such as the origin and destination ports, transportation mode,
    algorithm used, and metrics such as distance, time, and cost. This model is used to
    encapsulate the details of a computed optimized route.

    :ivar id: The unique identifier for the optimized route.
    :type id: str
    :ivar origin_port_name: The name of the origin port.
    :type origin_port_name: str
    :ivar destination_port_name: The name of the destination port.
    :type destination_port_name: str
    :ivar route_mode: The mode of transportation used for the route.
    :type route_mode: str
    :ivar algorithm_used: The name of the routing algorithm used for the route.
    :type algorithm_used: str
    :ivar visited_ports: The list of visited ports.
    :type visited_ports: list[str]
    :ivar total_distance: The total distance of the route.
    :type total_distance: float
    :ivar total_time: The total time required to travel the route.
    :type total_time: float
    :ivar total_cost: The total cost of the route.
    :type total_cost: float
    """
    id: str = Field(title="The unique identifier for the optimized route.")
    origin_port_name: str = Field(title="The name of the origin port.")
    destination_port_name: str = Field(title="The name of the destination port.")
    route_mode: str = Field(title="The mode of transportation used for the route.")
    algorithm_used: str = Field(title="The name of the routing algorithm used for the route.")
    visited_ports: list[str] = Field(title="The list of visited ports.")
    total_distance: float = Field(title="The total distance of the route.")
    total_time: float = Field(title="The total time required to travel the route.")
    total_cost: float = Field(title="The total cost of the route.")