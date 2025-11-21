"""
Service class for managing exports in the export management context.
"""
from app.export_management.domain.models.export import Export


class ExportService:
    def __init__(self):
        """
        Initializes the export service.
        """
        pass

    @staticmethod
    def register_export(name: str,
                        mode: str,
                        us_fob: float,
                        gross_weight: float,
                        net_weight: float,
                        unit: str,
                        quantity: float,
                        route_id: str,
                        user_id: str
    ) -> "Export":
        """
        Registers a new export item with detailed validation of input parameters for ensuring
        data integrity. The method validates that all required attributes are present and comply
        with expected formats, such as numerical positivity and non-empty strings for critical
        fields like name or mode. Any invalid input is met with an exception indicating the
        specific issue.

        :param name: Export item's commercial description.
        :type name: str
        :param mode: Transportation mode for the export (e.g., "Air", "Sea").
        :type mode: str
        :param us_fob: Free on board (FOB) value in USD.
        :type us_fob: float
        :param gross_weight: Total gross weight of the export in the appropriate weight unit.
        :type gross_weight: float
        :param net_weight: Total net weight of the export in the appropriate weight unit.
        :type net_weight: float
        :param unit: Measurement unit for the export item (e.g., "kg", "lb").
        :type unit: str
        :param quantity: Total quantity of items being exported.
        :type quantity: float
        :param route_id: ID corresponding to the optimized route or port for the export.
        :type route_id: str
        :param user_id: ID of the user who initiated the export.
        :type user_id: str

        :return: An instance of Export holding the provided and validated data.
        :rtype: Export
        :raises ValueError: Raised if any parameter fails validation, such as empty strings,
            negative numbers, or data type mismatches.
        """
        try:
            gross_weight = float(gross_weight)
            net_weight = float(net_weight)
            quantity = float(quantity)
            us_fob = float(us_fob)
            if name.strip() == "":
                raise ValueError("Name cannot be empty")
            if mode.strip() == "":
                raise ValueError("Mode cannot be empty")
            if unit.strip() == "":
                raise ValueError("Unit cannot be empty")
            if route_id.strip() == "":
                raise ValueError("Port ID cannot be empty")
            if user_id.strip() == "":
                raise ValueError("User ID cannot be empty")
            if us_fob < 0:
                raise ValueError("US FOB must be greater than 0")
            if gross_weight < 0:
                raise ValueError("Gross weight must be greater than 0")
            if net_weight < 0:
                raise ValueError("Net weight must be greater than 0")
            if quantity < 0:
                raise ValueError("Quantity must be greater than 0")
        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        return Export(
            comercial_description=name,
            transportation_mode=mode,
            us_fob=us_fob,
            gross_weight=gross_weight,
            net_weight=net_weight,
            unit=unit,
            quantity=quantity,
            optimized_route_id=route_id,
            user_id=user_id
        )

    @staticmethod
    def assign_port_id_to_export(export: Export, port_id: str) -> "Export":
        """
        Assigns a port ID to the given export.

        This method sets the provided port ID to the export's optimized route
        identifier. The port ID cannot be empty or invalid in format. If the
        port ID is invalid or empty, a ValueError will be raised.

        :param export: The Export object to which the port ID will be assigned.
        :type export: Export
        :param port_id: The port ID to assign to the Export's optimized route
            identifier.
        :type port_id: str
        :return: The updated Export object with the assigned port ID.
        :rtype: Export
        :raises ValueError: If the port ID is empty or invalid.
        """
        try:
            if port_id.strip() == "":
                raise ValueError("Port ID cannot be empty")
        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        export.optimized_route_id = port_id
        return export