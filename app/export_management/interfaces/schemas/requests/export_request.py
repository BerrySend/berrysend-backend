from pydantic import BaseModel, Field


class ExportRequest(BaseModel):
    """Represents a request for exporting goods, including relevant commercial, logistical,
    and user-related details.

    This class is used to encapsulate all necessary details required for processing an export
    request, such as description, transportation specifics, weights, and user associations.
    It provides the structure for managing and validating export-related information.

    :ivar comercial_description: The commercial description of the product to be exported.
    :type comercial_description: str
    :ivar transportation_mode: The mode of transportation used for the export.
    :type transportation_mode: str
    :ivar us_fob: The Free on Board (FOB) value of the export, in USD.
    :type us_fob: float
    :ivar gross_weight: The gross weight of the exported goods plus packaging.
    :type gross_weight: float
    :ivar net_weight: The net weight of the exported goods.
    :type net_weight: float
    :ivar unit: The unit of measurement for the exported goods.
    :type unit: str
    :ivar quantity: The quantity of the exported goods, using the unit specified.
    :type quantity: float
    :ivar optimized_route_id: The identifier for the optimized route or transportation
        pathway used for the export.
    :type optimized_route_id: str
    :ivar user_id: The identifier for the user who initiated the export.
    :type user_id: str
    """
    comercial_description: str = Field(title="The commercial description of the product to be exported")
    transportation_mode: str = Field(title="The mode of transportation used for the export")
    us_fob: float = Field(title="The Free on Board (FOB) value of the export, in USD")
    gross_weight: float = Field(title="The gross weight of the exported goods plus packaging")
    net_weight: float = Field(title="The net weight of the exported goods")
    unit: str = Field(title="The unit of measurement for the exported goods")
    quantity: float = Field(title="The quantity of the exported goods, using the unit specified")
    optimized_route_id: str = Field(title="The identifier for the optimized route or transportation pathway used for the export")
    user_id: str = Field(title="The identifier for the user who initiated the export")