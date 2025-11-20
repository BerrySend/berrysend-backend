"""
Service class for managing optimal routes in the route optimization context.
"""
from app.route_optimization.domain.models.optimal_route import OptimalRoute


class OptimalRouteService:
    def __init__(self):
        pass

    @staticmethod
    def register_optimal_route(
            origin_port_id: str,
            origin_port_name: str,
            destination_port_id: str,
            destination_port_name: str,
            route_mode: str,
            total_cost: float,
            total_distance: float,
            total_time: float,
            visited_ports: list[str]
    ) -> "OptimalRoute":
        """
        Registers an optimal route based on the provided parameters. Ensures all inputs are valid
        and non-empty. Converts relevant numeric inputs to float types and validates their values
        to be greater than zero. Raises an exception if any input is invalid or if an error occurs
        during the registration process.

        :param origin_port_id: ID of the origin port
        :type origin_port_id: str
        :param origin_port_name: Name of the origin port
        :type origin_port_name: str
        :param destination_port_id: ID of the destination port
        :type destination_port_id: str
        :param destination_port_name: Name of the destination port
        :type destination_port_name: str
        :param route_mode: Mode of the route (e.g., sea, road, air)
        :type route_mode: str
        :param total_cost: Total cost associated with the route
        :type total_cost: float
        :param total_distance: Total distance of the route
        :type total_distance: float
        :param total_time: Total time required for the route
        :type total_time: float
        :param visited_ports: List of ports visited during the route
        :type visited_ports: list[str]
        :return: Returns an instance of the OptimalRoute class
        :rtype: OptimalRoute
        :raises Exception: If any input validation fails or an error occurs during processing
        """
        try:
            total_cost = float(total_cost)
            total_distance = float(total_distance)
            total_time = float(total_time)
            if origin_port_id.strip() == "":
                raise ValueError("Origin port ID cannot be empty")
            if origin_port_name.strip() == "":
                raise ValueError("Origin port name cannot be empty")
            if destination_port_id.strip() == "":
                raise ValueError("Destination port ID cannot be empty")
            if destination_port_name.strip() == "":
                raise ValueError("Destination port name cannot be empty")
            if route_mode.strip() == "":
                raise ValueError("Route mode cannot be empty")
            if total_cost <= 0:
                raise ValueError("Total cost must be greater than 0")
            if total_distance <= 0:
                raise ValueError("Total distance must be greater than 0")
            if total_time <= 0:
                raise ValueError("Total time must be greater than 0")
            if len(visited_ports) == 0:
                raise ValueError("Visited ports list cannot be empty")

        except Exception as e:
            raise Exception(f"Error registering optimal route: {e}")

        return OptimalRoute(
            origin_port_id=origin_port_id,
            origin_port_name=origin_port_name,
            destination_port_id=destination_port_id,
            destination_port_name=destination_port_name,
            route_mode=route_mode,
            total_cost=total_cost,
            total_distance=total_distance,
            total_time=total_time,
            visited_ports=visited_ports
        )