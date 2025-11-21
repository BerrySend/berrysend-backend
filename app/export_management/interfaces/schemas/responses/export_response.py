from pydantic import BaseModel, Field


class ExportResponse(BaseModel):
    """
    Represents the response data for an export within the system.

    This class is used to model the key details of an export operation, including
    identifiable attributes, descriptive fields, and quantitative measures. Each
    instance captures specifics about the mode of transportation, weights,
    quantities, and additional metadata, providing a comprehensive overview of the
    exported goods and the related process. It is intended for scenarios where the
    export operation details need to be stored, transferred, or processed.

    :ivar id: The unique identifier of the export.
    :type id: str
    :ivar comercial_description: The commercial description of the product to
        be exported.
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
    :ivar optimized_route_id: The identifier for the optimized route or
        transportation pathway used for the export.
    :type optimized_route_id: str
    :ivar user_id: The identifier for the user who initiated the export.
    :type user_id: str
    :ivar created_at: The date and time when the export was created.
    :type created_at: str
    """
    id: str = Field(title="The unique identifier of the export")
    comercial_description: str = Field(title="The commercial description of the product to be exported")
    transportation_mode: str = Field(title="The mode of transportation used for the export")
    us_fob: float = Field(title="The Free on Board (FOB) value of the export, in USD")
    gross_weight: float = Field(title="The gross weight of the exported goods plus packaging")
    net_weight: float = Field(title="The net weight of the exported goods")
    unit: str = Field(title="The unit of measurement for the exported goods")
    quantity: float = Field(title="The quantity of the exported goods, using the unit specified")
    optimized_route_id: str = Field(title="The identifier for the optimized route or transportation pathway used for the export")
    user_id: str = Field(title="The identifier for the user who initiated the export")
    created_at: str = Field(title="The date and time when the export was created")