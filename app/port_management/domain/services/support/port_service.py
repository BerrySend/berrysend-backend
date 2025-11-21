"""
Service class for managing ports in the route planning domain.
"""
from app.port_management.domain.models.port import Port

class PortService:
    def __init__(self):
        """
        Initializes the port service.
        """
        pass

    @staticmethod
    def create_port(name: str, country: str, in_graph_type: str, latitude: float, longitude: float, capacity: float, port_type: str) -> "Port":
        """
        Creates a new port.

        :param name: The name of the port.
        :param country: The country where the port is located.
        :param in_graph_type: The type of the port (e.g., initial, intermediate, destination).
        :param latitude: The latitude coordinate of the port.
        :param longitude: The longitude coordinate of the port.
        :param capacity: The capacity of the port, in tons.
        :param port_type: The type of the port (e.g., maritime, air, both).

        :return: A newly created instance of Port.

        :raises ValueError: If the latitude or longitude are invalid or the name, country, or port type are empty.
        """
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            capacity = float(capacity)
            if latitude < -90 or latitude > 90:
                raise ValueError("Latitude must be between -90 and 90")
            if longitude < -180 or longitude > 180:
                raise ValueError("Longitude must be between -180 and 180")
            if name.strip() == "":
                raise ValueError("Name cannot be empty")
            if country.strip() == "":
                raise ValueError("Country cannot be empty")
            if port_type.strip() == "":
                raise ValueError("Port type cannot be empty")
            if capacity <= 0:
                raise ValueError("Capacity must be greater than 0")
            if in_graph_type.strip() == "":
                raise ValueError("In-graph type cannot be empty")
        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        return Port(name=name, country=country, latitude=latitude, longitude=longitude, in_graph_type=in_graph_type, capacity=capacity, port_type=port_type)

    @staticmethod
    def update_port_info(port: Port, name: str="", port_type: str="", capacity: float =0) -> "Port":
        """
        updates the information of a port

        :param port: The port to be updated.
        :param name: The updated name of the port.
        :param port_type: The updated type of the port.
        :param capacity: The updated capacity of the port.

        :return: The updated port.

        :raises ValueError: If the name or port type are empty.
        """
        try:
            if name != "":
                if name.strip() == "":
                    raise ValueError("Input name cannot be empty.")
                port.name = name
            if port_type != "":
                if port_type.strip() == "":
                    raise ValueError("Input port type cannot be empty.")
                port.type = port_type
            if capacity != 0:
                port.capacity = capacity
        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        return port