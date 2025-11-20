from pydantic import BaseModel, Field

class PortConnectionResponse(BaseModel):
    """
    Response schema for the port connection entity.

    Attributes:
        id (str): The unique identifier of the port connection.
        port_a_id (str): The unique identifier of the origin port.
        port_b_id (str): The unique identifier of the destination port.
        distance_km (float): The distance between the two ports in kilometers.
        estimated_travel_time_hours (float): The estimated travel time between the two ports in hours.
        cost_usd (float): The cost of travel from port A to port B.
        route_type (str): The type of route between the two ports (e.g., maritime, aerial).
        is_restricted (bool): Indicates whether the connection is restricted or not.
    """
    id: str = Field(title="The unique identifier of the port connection")
    port_a_id: str = Field(title="The unique identifier of the origin port")
    port_b_id: str = Field(title="The unique identifier of the destination port")
    distance_km: float = Field(title="The distance between the two ports in kilometers")
    estimated_travel_time_hours: float = Field(title="The estimated travel time between the two ports in hours")
    cost_usd: float = Field(title="The cost of travel from port A to port B")
    route_type: str = Field(title="The type of route between the two ports (e.g., maritime, aerial)")
    is_restricted: bool = Field(title="Indicates whether the connection is restricted or not")