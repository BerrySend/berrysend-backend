"""
Application service for managing port connections in the route planning domain.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.route_planning.domain.services.support.port_connection_service import PortConnectionService
from app.route_planning.infrastructure.repositories.port_connection_repository import PortConnectionRepository
from app.shared.infrastructure.readers.csv_reader import read_csv_from_url
from app.route_planning.domain.models.port_connection import PortConnection

class PortConnectionApplicationService:
    def __init__(self, db: AsyncSession):
        """
        Initialize the port connection application service with the port connection service and repository.

        :param db: The database session.
        """
        self.port_connection_service = PortConnectionService()
        self.port_connection_repository = PortConnectionRepository(db)

    async def seed_connections(self, file_url: str) -> None:
        """
        Reads the CSV file of port connections, validates it with the port connection service,
        and creates the port connections in the database.

        :param file_url: The url of the CSV file.

        :exception ValueError: If the data format of the CSV file is invalid.
        """
        print(f"Attempting to seed connections from {file_url}...")

        connection_rows = await read_csv_from_url(file_url)

        if connection_rows is None:
            print(f"WARNING: Failed to fetch CSV from {file_url}. Skipping connection seeding.")
            print("The application will continue without seeded connections.")
            return

        if len(connection_rows) == 0:
            print(f"WARNING: CSV file from {file_url} is empty. No connections to seed.")
            return

        print(f"Successfully fetched {len(connection_rows)} rows from CSV. Starting to seed connections...")

        row_id = 1

        for row in connection_rows:
            try:
                port_a_id: str = row["port_a_id"].strip()
                port_b_id: str = row["port_b_id"].strip()
                distance_km: float = float(row["distance_km"])
                time_hours: float = float(row["time_hours"])
                cost_usd: float = float(row["cost_usd"])
                route_type: str = row["route_type"].strip()
                is_restricted: bool = row["is_restricted"].strip().lower() == False

                connection = self.port_connection_service.add_port_connection(
                    port_a_id,
                    port_b_id,
                    distance_km,
                    time_hours,
                    cost_usd,
                    route_type,
                    is_restricted
                )

                await self.port_connection_repository.create(connection)

                print(f"Added connection {connection.id} at row {row_id}")
            except (ValueError, KeyError):
                print(f"Invalid data format for row number {row_id}")

            row_id += 1

    async def get_all_connections(self) -> list["PortConnection"]:
        """
        Retrieve all port connections from the repository.

        :return: A list of all port connections.

        :exception Exception: If there is an error while retrieving the connections.
        """
        try:
            connections: list["PortConnection"] = await self.port_connection_repository.get_all()
            return connections
        except Exception as e:
            raise Exception(f"Error retrieving connections: {e}")

    async def get_connections_by_port_id(self, connection_id: str) -> list["PortConnection"]:
        """
        Retrieve a port connection by its ID.

        :param connection_id: The ID of the port connection.
        :return: The port connection if found, otherwise None.

        :exception ValueError: If the connection ID is invalid.
        :exception Exception: If there is an error while retrieving the connection.
        """
        try:
            if connection_id is None or connection_id.strip() == "":
                raise ValueError("To retrieve a connection, you must provide a valid connection ID.")

            connections = await self.port_connection_repository.get_connections_by_port_id(connection_id)
            return connections
        except Exception as e:
            raise Exception(f"Error retrieving connection: {e}")

    async def delete_connection(self, connection_id: str) -> None:
        """
        Delete a port connection by its ID.

        :param connection_id: The ID of the port connection to delete.
        :return: The deleted port connection if found, otherwise None.

        :exception ValueError: If the connection ID is invalid.
        :exception Exception: If there is an error while deleting the connection.
        """
        try:
            if connection_id is None or connection_id.strip() == "":
                raise ValueError("To delete a connection, you must provide a valid connection ID.")

            deleted_connection = await self.port_connection_repository.delete(connection_id)
            return deleted_connection
        except Exception as e:
            raise Exception(f"Error deleting connection: {e}")

    async def update_connection(self, connection_id: str, distance_km: float, time_hours: float, cost_usd: float, is_restricted: bool) -> "PortConnection | None":
        """
        Update a port connection's details.

        :param connection_id: The ID of the port connection to update.
        :param distance_km: The new distance, in kilometers.
        :param time_hours: The new time in hours.
        :param cost_usd: The new cost in USD.
        :param is_restricted: The new restriction status.
        :return: The updated port connection if found, otherwise None.

        :exception ValueError: If the connection ID is invalid or the connection is not found.
        :exception Exception: If there is an error while updating the connection.
        """
        try:
            if connection_id is None or connection_id.strip() == "":
                raise ValueError("To update a connection, you must provide a valid connection ID.")

            connection_to_update: PortConnection = await self.port_connection_repository.get_by_id(connection_id)
            if not connection_to_update:
                raise ValueError("Connection not found.")

            updated_connection: PortConnection = self.port_connection_service.update_connection_info(
                connection_to_update,
                distance_km,
                time_hours,
                cost_usd,
                is_restricted
            )
            return updated_connection
        except Exception as e:
            raise Exception(f"Error updating connection: {e}")

    async def get_connection_by_id(self, connection_id: str) -> "PortConnection | None":
        """
        Retrieve a port connection by its identifier.

        :param connection_id: The ID of the connection.
        :return: A port connection if found, otherwise None.

        :exception ValueError: If the connection ID is invalid.
        :exception Exception: If there is an error while retrieving the connection.
        """
        try:
            if connection_id is None or connection_id.strip() == "":
                raise ValueError("To retrieve a connection, you must provide a valid connection ID.")

            connection = await self.port_connection_repository.get_by_id(connection_id)
            return connection
        except Exception as e:
            raise Exception(f"Error retrieving the connection: {e}")