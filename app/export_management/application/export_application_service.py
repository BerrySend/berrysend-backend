from sqlalchemy.ext.asyncio import AsyncSession

from app.export_management.domain.models.export import Export
from app.export_management.domain.services.support.export_service import ExportService
from app.export_management.infrastructure.repositories.export_repository import ExportRepository
from app.route_optimization.domain.models.optimal_route import OptimalRoute
from app.route_optimization.infrastructure.repositories.optimal_route_repository import OptimalRouteRepository


class ExportApplicationService:
    def __init__(self, db: AsyncSession):
        self.export_service = ExportService()
        self.export_repository = ExportRepository(db)
        self.route_repository = OptimalRouteRepository(db)

    async def register_export(self,
                              comercial_description: str,
                              transportation_mode: str,
                              us_fob: float,
                              gross_weight: float,
                              net_weight: float,
                              unit: str,
                              quantity: float,
                              optimized_route_id: str,
                              user_id: str
    ) -> "Export | None":
        """
        Registers new export information and persists it in the repository.

        :param comercial_description: Name or description of the commodity being exported.
        :param transportation_mode: Mode of transportation used for the export (e.g., sea, air).
        :param us_fob: Free on Board (FOB) value of the export in USD.
        :param gross_weight: Total gross weight of the shipment.
        :param net_weight: Net weight of the shipment after deductions.
        :param unit: Unit of measurement for the shipment (e.g., kg, lbs).
        :param quantity: Quantity of the commodities being exported.
        :param optimized_route_id: Identifier for the optimized route of the export.
        :param user_id: Identifier for the user initiating the export.
        :return: An instance of the created Export object or None if the creation fails.
        """
        try:
            export = self.export_service.register_export(
                name=comercial_description,
                mode=transportation_mode,
                us_fob=us_fob,
                gross_weight=gross_weight,
                net_weight=net_weight,
                unit=unit,
                quantity=quantity,
                route_id=optimized_route_id,
                user_id=user_id
            )

            if not export:
                raise ValueError("Failed to create export.")

            await self.export_repository.create(export)

        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        return export

    async def assign_route_id_to_export(self, export_id: str, new_route_id: str) -> "Export | None" :
        """
        Assigns a new route ID to an existing export.

        This method updates the route ID associated with an export. It retrieves
        the export by its ID, ensures that the export exists, and then assigns the
        new route ID to the export. After updating the export, it synchronizes the
        change with the repository.

        :param export_id: Unique identifier of the export to update.
        :param new_route_id: New route ID to assign to the export.
        :return: Updated export object if successful, or None if unsuccessful.
        """
        try:
            if export_id is None or export_id.strip() == "":
                raise ValueError("To update an export, you must provide a valid export id.")

            export = await self.export_repository.get_by_id(export_id)

            if not export:
                raise ValueError("Export not found.")

            updated_export = self.export_service.assign_port_id_to_export(export, new_route_id)

            await self.export_repository.update(updated_export)
        except ValueError as e:
            raise ValueError(f"Error trying to update export: {e}")

        return updated_export

    async def get_export_by_id(self, export_id: str) -> "Export | None":
        """
        Retrieves an export by its unique identifier.

        This asynchronous method fetches an export record from the export repository
        based on the provided export_id. If the export_id is invalid, or if the record
        is not found, an error is raised. The function returns either the corresponding
        export object or None if no matching export is present.

        :param export_id: The unique identifier of the export to be retrieved.
        :return: An Export object if found, or None if no matching export exists.

        :raises ValueError: If the export_id is invalid or if the export is not found.
        """
        try:
            if export_id is None or export_id.strip() == "":
                raise ValueError("To retrieve an export, you must provide a valid export id.")

            export = await self.export_repository.get_by_id(export_id)

            if not export:
                raise ValueError("Export not found.")

        except ValueError as e:
            raise ValueError(f"Error trying to retrieve export: {e}")

        return export

    async def get_all_exports(self) -> list["Export"]:
        """
        Retrieve all export records.

        This asynchronous function fetches all export records from the export
        repository. If no records are found, an exception is raised. The
        function ensures proper exception handling to provide meaningful
        error messages.

        :return: A list of all export records from the repository.
        :rtype: list[Export]

        :raises ValueError: If no exports are found in the repository or if
                            an error occurs during the retrieval process.
        """
        try:
            exports = await self.export_repository.get_all()

            if not exports:
                raise ValueError("No exports found.")
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve exports: {e}")

        return exports

    async def get_exports_by_user_id(self, user_id: str) -> list["Export"]:
        """
        Retrieve all export records for a specific user.

        This asynchronous function fetches all export records from the export
        repository that belong to the specified user. Returns an empty list if
        no exports are found for the user.

        :param user_id: The unique identifier of the user.
        :type user_id: str
        :return: A list of export records belonging to the user.
        :rtype: list[Export]

        :raises ValueError: If an error occurs during the retrieval process.
        """
        try:
            if user_id is None or user_id.strip() == "":
                raise ValueError("To retrieve exports, you must provide a valid user id.")

            exports = await self.export_repository.get_by_user_id(user_id)
            return exports
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve exports by user: {e}")

    async def get_route_by_export_id(self, export_id: str) -> "OptimalRoute | None":
        """
        Retrieve an optimal route based on the provided export ID.

        This asynchronous method interacts with the export repository and route
        repository to fetch the optimal route associated with a given export ID. If the
        export ID is invalid, or if the associated export or route cannot be found, it
        raises an appropriate error. Returns the optimal route if found, otherwise
        None. The method is primarily designed to work within an environment where
        both export and route data are available for retrieval.

        :param export_id: The ID of the export whose associated optimal route is
            to be retrieved.
        :type export_id: str
        :return: The optimal route associated with the provided export ID, or None if
            no such route exists.
        :rtype: OptimalRoute | None
        :raises ValueError: If the export ID is invalid, or if the export or associated
            route cannot be found.
        """
        try:
            if export_id is None or export_id.strip() == "":
                raise ValueError("To retrieve a route, you must provide a valid export id.")

            export = await self.export_repository.get_by_id(export_id)

            if not export:
                raise ValueError("Export not found.")

            route = await self.route_repository.get_by_id(export.optimized_route_id)

            if not route:
                raise ValueError("Route not found.")
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve route: {e}")

        return route