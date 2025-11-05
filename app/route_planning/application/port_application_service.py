"""
Application service for ports.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.route_planning.domain.models.port import Port
from app.route_planning.domain.services.port_service import PortService
from app.route_planning.infrastructure.repositories.port_repository import PortRepository
from app.shared.infrastructure.readers.csv_reader import CsvFileReader

class PortApplicationService:
    def __init__(self, db: AsyncSession):
        """
        Initialize the port application service with port service, port repository, and CSV file reader.

        :param db: The database session.
        """
        self.port_service = PortService()
        self.port_repository = PortRepository(db)
        self.file_reader = CsvFileReader()

    async def seed_ports(self, file_url: str) -> None:
        """
        Reads the CSV file of ports, validates it with the port service, and creates the ports in the database.

        :param file_url: The url of the CSV file.
        :exception ValueError: If the data format of the CSV file is invalid.
        """
        rows = self.file_reader.read(file_url)
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

    async def get_all_ports(self) -> list["Port"]:
        """
        Retrieves all ports from the database.

        :return: The list of ports or an empty list if no ports are found.
        """
        try:
            ports: list["Port"] = await self.port_repository.get_all()
            return ports
        except ValueError:
            raise ValueError("No ports found.")

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
        except ValueError:
            raise ValueError("No port found.")