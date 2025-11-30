from dataclasses import dataclass

from app.shared.domain.models.base_entity import BaseEntity

@dataclass
class PortConnection(BaseEntity):
    """
    Represents a bidirectional connection between two ports in the graph.

    Attributes:
        port_a_id (str): The id of the port a.
        port_a_name (str): The name of the port a.
        port_b_id (str): The id of the port b.
        port_b_name (str): The name of the port b.
        distance_km (float): The distance between the two ports in kilometers.
        time_hours (float): The time between two ports in hours.
        cost_usd (float): The cost of transport between two ports in dollars.
        route_type (str): The route type of the ports. It can be maritime or aerial.
        is_restricted (bool): Indicates whether the connection is restricted or not.

    Here we can add more types of restrictions that correspond to the connection of the two ports.
    """
    port_a_id: str
    port_a_name: str
    port_b_id: str
    port_b_name: str
    distance_km: float
    time_hours: float
    cost_usd: float
    route_type: str
    is_restricted: bool