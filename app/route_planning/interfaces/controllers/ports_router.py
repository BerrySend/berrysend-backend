from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, Path, Response
from fastapi.openapi.models import Example
from sqlalchemy.ext.asyncio import AsyncSession

from app.route_planning.application.port_application_service import PortApplicationService
from app.route_planning.domain.models.port import Port
from app.route_planning.interfaces.schemas.responses.port_response import PortResponse
from app.shared.infrastructure.persistence.session_generator import get_db

# Create a router for the ports
router = APIRouter(prefix="/api/v1/ports", tags=["ports"])

# Get port application service
def get_port_app_service(db: AsyncSession = Depends(get_db)) -> "PortApplicationService":
    return PortApplicationService(db)

@router.get("/{port_id}", response_model=PortResponse, status_code=status.HTTP_200_OK)
async def get_port_by_id(
    port_id: Annotated[str, Path(
        title="The ID of the port to get",
        openapi_examples={
            "invalid": Example(
                summary="Invalid",
                description="When using a non-uuid value for the id, an error is returned.",
                value= {
                    "id": "hi"
                }
            ),
            "valid": Example(
                summary="Normal",
                description="A valid port id with a uuid type.",
                value= {
                    "id": "123e4567-e89b-12d3-a456-426614174000"
                }
            )
        }
    )],
    response: Response,
    port_app_service: PortApplicationService = Depends(get_port_app_service)
) -> Any:
    """
    Endpoint to retrieve a port by its id.

    :param response: To set the status code.
    :param port_id: The id of the port.
    :param port_app_service: Injected port application service.
    :return: The port with the given id if found, otherwise None.
    """
    try:
        port: Port = await port_app_service.get_port_by_id(port_id)
        if not port:
            response.status_code = status.HTTP_404_NOT_FOUND
            return None
        return PortResponse(
            id=port.id,
            name=port.name,
            latitude=port.latitude,
            longitude=port.longitude,
            country=port.country,
            type=port.type
        )
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None

@router.get("/", response_model=list[PortResponse], status_code=status.HTTP_200_OK)
async def get_all_ports(
    response: Response,
    port_app_service: PortApplicationService = Depends(get_port_app_service)
) -> Any:
    """
    Retrieve all ports.

    :param response: To set the status code.
    :param port_app_service: The port application service.
    :return: A list of ports if found, otherwise an empty list.
    """
    try:
        ports: list[Port] = await port_app_service.get_all_ports()
        if len(ports) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return []
        ports_response = [PortResponse(**port.__dict__) for port in ports]
        return ports_response
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return []

