from dataclasses import dataclass

from app.shared.domain.models.base_entity import BaseEntity

@dataclass
class OptimalRoute(BaseEntity):
    """
    Represents an optimal route in the route optimization context.

    Attributes:
        origin_port_id (str): The id of the origin port.
        origin_port_name (str): The name of the origin port.
        destination_port_id (str): The id of the destination port.
        destination_port_name (str): The name of the destination port.
        route_mode (str): The mode of the route (e.g., maritime or aerial).
        total_cost (float): The cost of the route.
        total_distance (float): The distance of the route.
        total_time (float): The time of the route.
        visited_ports (list[str]): The list of visited ports.
    """
    origin_port_id: str
    origin_port_name: str
    destination_port_id: str
    destination_port_name: str
    route_mode: str
    total_cost: float
    total_distance: float
    total_time: float
    visited_ports: list[str]