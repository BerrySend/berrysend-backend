from app.export_management.domain.models.export import Export
from app.export_management.interfaces.schemas.responses.export_response import ExportResponse


def assemble_export_response_from_entity(entity: Export) -> "ExportResponse":
    """
    Transforms an Export entity into an ExportResponse object.

    This function takes an Export entity and converts its attributes into an
    ExportResponse object, ensuring proper serialization where required.

    :param entity: The Export entity to transform.
    :type entity: Export

    :return: An ExportResponse object populated with data from the provided
        Export entity.
    :rtype: ExportResponse
    """
    return ExportResponse(
        id=entity.id,
        comercial_description=entity.comercial_description,
        transportation_mode=entity.transportation_mode,
        us_fob=entity.us_fob,
        gross_weight=entity.gross_weight,
        net_weight=entity.net_weight,
        unit=entity.unit,
        quantity=entity.quantity,
        optimized_route_id=entity.optimized_route_id,
        user_id=entity.user_id,
        created_at=entity.created_at.isoformat()
    )