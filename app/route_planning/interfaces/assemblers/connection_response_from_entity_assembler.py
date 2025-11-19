from app.route_planning.domain.models.port_connection import PortConnection
from app.route_planning.interfaces.schemas.responses.port_connection_response import PortConnectionResponse


def assemble_connection_response_from_entity(connection_entity: PortConnection) -> PortConnectionResponse:
    """
    Assembles a PortConnectionResponse object from a given PortConnection entity.

    This function takes a PortConnection entity and maps its attributes to create
    and return a corresponding PortConnectionResponse object. This is useful
    for transforming data between domain and response models in an application.

    :param connection_entity: The PortConnection entity containing connection
        details that need to be transformed into a response object.
    :type connection_entity: PortConnection
    :return: A PortConnectionResponse object constructed from the data within the
        provided PortConnection entity.
    :rtype: PortConnectionResponse
    """
    return PortConnectionResponse(
        id=connection_entity.id,
        port_a_id=connection_entity.port_a_id,
        port_b_id=connection_entity.port_b_id,
        distance_km=connection_entity.distance_km,
        estimated_travel_time_hours=connection_entity.time_hours,
        cost_usd=connection_entity.cost_usd,
        route_type=connection_entity.route_type,
        is_restricted=connection_entity.is_restricted
    )