"""
Application service for ports.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.route_planning.domain.models.port import Port
from app.route_planning.domain.services.port_service import PortService
from app.route_planning.infrastructure.repositories.port_repository import PortRepository
from app.shared.infrastructure.readers.csv_reader import read_csv_from_url

class PortApplicationService:
    def __init__(self, db: AsyncSession):
        """
        Initialize the port application service with port service, port repository, and CSV file reader.

        :param db: The database session.
        """
        self.port_service = PortService()
        self.port_repository = PortRepository(db)

    async def seed_ports(self, file_url: str) -> None:
        """
        Reads the CSV file of ports, validates it with the port service, and creates the ports in the database.

        :param file_url: The url of the CSV file.
        :exception ValueError: If the data format of the CSV file is invalid.
        """
        print(f"Attempting to seed ports from {file_url}...")

        rows = await read_csv_from_url(file_url)

        if rows is None:
            print(f"WARNING: Failed to fetch CSV from {file_url}. Skipping port seeding.")
            print("The application will continue without seeded ports.")
            return

        if len(rows) == 0:
            print(f"WARNING: CSV file from {file_url} is empty. No ports to seed.")
            return

        print(f"Successfully fetched {len(rows)} rows from CSV. Starting to seed ports...")

        row_id = 1

        for row in rows:
            try:
                name: str = row["name"].strip()
                country: str = row["country"].strip()
                port_type: str = row["type"].strip()
                latitude: float = float(row["latitude"])
                longitude: float = float(row["longitude"])

                port = self.port_service.create_port(
                    name=name,
                    country=country,
                    port_type=port_type,
                    latitude=latitude,
                    longitude=longitude
                )

                await self.port_repository.create(port)

                print(f"Created port {port.name} at row {row_id}")
            except (ValueError, KeyError):
                print(f"Invalid data format for row number {row_id}")

            row_id += 1

    async def update_port(self, port_id: str, name: str, port_type: str) -> "Port | None":
        """
        Updates the port information.

        :param port_id: The id of the port to update.
        :param name: The new name of the port.
        :param port_type: The new type of the port.
        :return: The updated port if found or success, otherwise None.
        :exception ValueError: If the port id is invalid or the port is not found.
        """
        try:
            if port_id is None or port_id.strip() == "":
                raise ValueError("To update a port, you must provide a valid port id.")

            port_to_update: Port = await self.port_repository.get_by_id(port_id)
            if not port_to_update:
                raise ValueError("Port not found.")

            updated_port: Port = self.port_service.update_port_info(port_to_update, name, port_type)
            return updated_port
        except ValueError as e:
            raise ValueError(f"Error trying to update port: {e}")


    async def get_all_ports(self) -> list["Port"]:
        """
        Retrieves all ports from the database.

        :return: The list of ports or an empty list if no ports are found.
        """
        try:
            ports: list["Port"] = await self.port_repository.get_all()
            return ports
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve ports: {e}.")

    async def get_port_by_id(self, port_id: str) -> "Port | None":
        """
        Retrieves a port by its id.

        :param port_id: The id of the port.
        :return: The port with the given id, if found, otherwise None.
        """
        try:
            if port_id is None or port_id.strip() == "":
                raise ValueError("To get a port, you must provide a valid port id.")

            port: Port = await self.port_repository.get_by_id(port_id)
            return port
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve port: {e}")