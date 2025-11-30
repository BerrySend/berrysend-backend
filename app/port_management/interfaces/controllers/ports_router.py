from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, Path, Response, HTTPException
from fastapi.openapi.models import Example
from sqlalchemy.ext.asyncio import AsyncSession

from app.port_management.application.port_application_service import PortApplicationService
from app.port_management.application.port_connection_application_service import PortConnectionApplicationService
from app.port_management.domain.models.port import Port
from app.port_management.interfaces.assemblers.connection_response_from_entity_assembler import \
    assemble_connection_response_from_entity
from app.port_management.interfaces.assemblers.port_response_from_entity_assembler import \
    assemble_port_response_from_entity
from app.port_management.interfaces.controllers.port_connections_router import get_connection_app_service
from app.port_management.interfaces.schemas.responses.port_connection_response import PortConnectionResponse
from app.port_management.interfaces.schemas.responses.port_response import PortResponse
from app.shared.infrastructure.persistence.session_generator import get_db

# Create a router for the ports
router = APIRouter(prefix="/api/v1/ports", tags=["Ports"])


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
                    value={
                        "id": "hi"
                    }
                ),
                "valid": Example(
                    summary="Normal",
                    description="A valid port id with a uuid type.",
                    value={
                        "id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
            }
        )],
        response: Response,
        port_app_service: PortApplicationService = Depends(get_port_app_service),
        connections_app_service: PortConnectionApplicationService = Depends(get_connection_app_service)
) -> Any:
    """
    Endpoint to retrieve a port by its id.

    :param connections_app_service: Injected port connection application service.
    :param response: To set the status code.
    :param port_id: The id of the port.
    :param port_app_service: Injected port application service.
    :return: The port with the given id if found, otherwise None.
    """
    try:
        port: Port = await port_app_service.get_port_by_id(port_id)
        if not port:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Port for given id not found"
            )

        connections = await connections_app_service.get_connections_by_port_id(port_id)
        connections_number = len(connections)

        response = assemble_port_response_from_entity(port, connections_number)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=list[PortResponse], status_code=status.HTTP_200_OK)
async def get_all_ports(
        search: str | None = None,
        port_app_service: PortApplicationService = Depends(get_port_app_service),
        connections_app_service: PortConnectionApplicationService = Depends(get_connection_app_service)
) -> Any:
    """
    Retrieve all ports, optionally filtered by search term.

    :param search: Optional search term to filter ports by name or country
    :param connections_app_service: Injected port connection application service.
    :param port_app_service: The port application service.
    :return: A list of ports if found, otherwise an empty list.
    """
    try:
        ports: list[Port] = await port_app_service.get_all_ports()
        
        # Filter by search term if provided
        if search and search.strip():
            search_lower = search.strip().lower()
            ports = [
                port for port in ports
                if (search_lower in port.name.lower() if port.name else False) or
                   (search_lower in port.country.lower() if port.country else False)
            ]
        
        if len(ports) == 0:
            # Return empty list instead of 404 when no ports match
            return []
        
        ports_response = []
        for port in ports:
            try:
                connections = await connections_app_service.get_connections_by_port_id(port.id)
                connections_number = len(connections)
            except Exception:
                # If connections fail, set to 0 and continue
                connections_number = 0
            
            ports_response.append(assemble_port_response_from_entity(port, connections_number))

        return ports_response
    except Exception as e:
        # Log the error but return a proper error response
        print(f"Error in get_all_ports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving ports: {str(e)}"
        )

@router.get("/{port_id}/connections", response_model=list[PortConnectionResponse], status_code=status.HTTP_200_OK)
async def get_connections_by_port_id(
        port_id: str,
        response: Response,
        connection_app_service: PortConnectionApplicationService = Depends(get_connection_app_service),
) -> Any:
    """
    Endpoint to retrieve all port connections for a given port id.

    :param response: To set the status code.
    :param port_id: The id of the port.
    :param connection_app_service: Injected port application service.

    :return: A list of port connections for the given port id if found, otherwise None.
    """
    try:
        connections = await connection_app_service.get_connections_by_port_id(port_id)
        if len(connections) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Connections for given port id not found"
            )

        responses = []
        for connection in connections:
            responses.append(assemble_connection_response_from_entity(connection))
        return responses
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )