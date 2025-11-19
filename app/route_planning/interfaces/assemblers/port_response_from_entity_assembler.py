from app.route_planning.domain.models.port import Port
from app.route_planning.interfaces.schemas.responses.port_response import PortResponse


def assemble_port_response_from_entity(port_entity: Port) -> PortResponse:
    """
    Converts a `Port` entity into a `PortResponse`.

    This function takes an instance of the `Port` entity class and transforms
    it into an instance of the `PortResponse` class by mapping relevant attributes
    from the source entity to the destination response object.

    :param port_entity: The `Port` entity that contains data to construct a
        `PortResponse` object.
    :type port_entity: Port
    :return: A `PortResponse` object that maps the attributes of the given
        `Port` entity.
    :rtype: PortResponse
    """
    return PortResponse(
        id=port_entity.id,
        name=port_entity.name,
        country=port_entity.country,
        latitude=port_entity.latitude,
        longitude=port_entity.longitude,
        type=port_entity.type
    )