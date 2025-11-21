from dataclasses import dataclass

from app.shared.domain.models.base_entity import BaseEntity


@dataclass
class Export(BaseEntity):
    """
    Represents an export entity with attributes describing the export details.

    This class is designed to model export transactions, including relevant
    logistics, economic, and physical characteristics such as weight, value,
    and mode of transportation.

    :ivar comercial_description: A description of the exported goods.
    :type comercial_description: str

    :ivar transportation_mode: Mode of transportation used for exporting the goods
        (e.g., sea, air, road).
    :type transportation_mode: str

    :ivar us_fob: Free on Board (FOB) value of the goods in U.S. dollars, representing
        the value of the goods at the export location.
    :type us_fob: float

    :ivar gross_weight: Total weight of the export shipment, including all packaging,
        measured in kilograms.
    :type gross_weight: float

    :ivar net_weight: The actual weight of the goods being exported, excluding any
        packaging, measured in kilograms.
    :type net_weight: float

    :ivar unit: Unit of measurement for specifying the quantity of the goods
        (e.g., kg, tons, pieces, boxes).
    :type unit: str

    :ivar quantity: Total quantity of goods being exported, using the specified unit.
    :type quantity: float

    :ivar optimized_route_id: Identifier for the optimized route or transportation pathway used
        for the export.
    :type optimized_route_id: str

    :ivar user_id: Identifier for the user who initiated the export.
    :type user_id: str
    """
    comercial_description: str
    transportation_mode: str
    us_fob: float
    gross_weight: float
    net_weight: float
    unit: str
    quantity: float
    optimized_route_id: str
    user_id: str