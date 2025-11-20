"""
Service class for managing ports in the route planning domain.
"""
from app.route_planning.domain.models.port import Port

class PortService:
    def __init__(self):
        """
        Initializes the port service.
        """
        pass

    @staticmethod
    def create_port(name: str, country: str, port_type: str, latitude: float, longitude: float) -> "Port":
        """
        Creates a new port.

        :param name: The name of the port.
        :param country: The country where the port is located.
        :param port_type: The type of the port (e.g., initial, intermediate, destination).
        :param latitude: The latitude coordinate of the port.
        :param longitude: The longitude coordinate of the port.
        :return: A newly created instance of Port.

        :raises ValueError: If the latitude or longitude are invalid or the name, country, or port type are empty.
        """
        try:
            latitude = float(latitude)
            longitude = float(longitude)
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
        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        return Port(name=name, country=country, latitude=latitude, longitude=longitude, type=port_type)

    @staticmethod
    def update_port_info(port: Port, name: str="", port_type: str="") -> "Port":
        """
        updates the information of a port

        :param port: The port to be updated.
        :param name: The updated name of the port.
        :param port_type: The updated type of the port.
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
        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        return port