from app.port_management.domain.models.port import Port
from app.port_management.interfaces.schemas.responses.coordinates_response import Coordinates
from app.port_management.interfaces.schemas.responses.port_response import PortResponse


def assemble_port_response_from_entity(port_entity: Port, connections: int) -> PortResponse:
    """
    Converts a `Port` entity into a `PortResponse`.

    This function takes an instance of the `Port` entity class and transforms
    it into an instance of the `PortResponse` class by mapping relevant attributes
    from the source entity to the destination response object.

    :param connections: The number of connections associated with the port.
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
        type=port_entity.type,
        capacity=port_entity.capacity,
        connections=connections,
        coordinates=Coordinates(
            latitude=port_entity.latitude,
            longitude=port_entity.longitude
        )
    )