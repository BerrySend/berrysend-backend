"""
Service class for managing port connections in the route planning domain.
"""
from app.port_management.domain.models.port_connection import PortConnection

class PortConnectionService:
    def __init__(self):
        """
        Initializer for PortConnectionService class.
        """
        pass

    @staticmethod
    def add_port_connection(
        port_a_id: str,
        port_b_id: str,
        distance_km: float,
        time_hours: float,
        cost_usd: float,
        route_type: str,
        is_restricted: bool = False
    ) -> "PortConnection":
        """
        Adds a port connection to the route planning domain.

        :param port_a_id: The id of port A
        :param port_b_id: The id of port B
        :param distance_km: The distance in km
        :param time_hours: The time in hours
        :param cost_usd: The cost in usd
        :param route_type: The route type
        :param is_restricted: Indicates whether it is restricted
        :return: The created PortConnection object

        :raises ValueError: If the values entered are invalid
        """
        try:
            distance_km = float(distance_km)
            time_hours = float(time_hours)
            cost_usd = float(cost_usd)
            is_restricted = bool(is_restricted)

            if time_hours <= 0:
                raise ValueError("Time in hours must be greater than 0")
            if cost_usd <= 0:
                raise ValueError("Cost in USD must be greater than 0")
            if distance_km <= 0:
                raise ValueError("Distance in km must be greater than 0")
            if port_a_id.strip() == "":
                raise ValueError("Id of port A cannot be an empty string")
            if port_b_id.strip() == "":
                raise ValueError("Id of port B cannot be an empty string")
            if port_b_id == port_a_id:
                raise ValueError("The id of both ports have to be different")
            if route_type.strip() == "":
                raise ValueError("Route type cannot be empty")
        except (ValueError, TypeError):
            raise ValueError("Invalid data format")

        return PortConnection(
            port_a_id = port_a_id,
            port_b_id = port_b_id,
            distance_km = distance_km,
            time_hours = time_hours,
            cost_usd = cost_usd,
            route_type = route_type,
            is_restricted = is_restricted
        )

    @staticmethod
    def update_connection_info(
        port_connection: PortConnection,
        distance_km: float = 0,
        time_hours: float = 0,
        cost_usd: float = 0,
        is_restricted: bool = False
    ) -> "PortConnection":
        """
        Updates the information of a connection between two ports.

        :param port_connection: The port connection whose information is to be updated
        :param distance_km: The distance in km to update
        :param time_hours: The time in hours to update
        :param cost_usd: The cost in usd to update
        :param route_type: The route type to update
        :param is_restricted: The indicator of whether it is restricted
        :return: The updated PortConnection object

        :raises ValueError: If the values entered are invalid
        """
        try:
            if distance_km != 0:
                distance_km = float(distance_km)
            if time_hours != 0:
                time_hours = float(time_hours)
            if cost_usd != 0:
                cost_usd = float(cost_usd)
        except (ValueError, TypeError):
            raise ValueError("Invalid data format")

        port_connection.distance_km = distance_km
        port_connection.time_hours = time_hours
        port_connection.cost_usd = cost_usd
        port_connection.is_restricted = is_restricted

        return port_connection