from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, Path, Response
from fastapi.openapi.models import Example
from sqlalchemy.ext.asyncio import AsyncSession

from app.port_management.application.port_connection_application_service import PortConnectionApplicationService
from app.port_management.domain.models.port_connection import PortConnection
from app.port_management.interfaces.assemblers.connection_response_from_entity_assembler import \
    assemble_connection_response_from_entity
from app.port_management.interfaces.schemas.responses.port_connection_response import PortConnectionResponse
from app.shared.infrastructure.persistence.session_generator import get_db

# Create a router for the port connections
router = APIRouter(prefix="/api/v1/port-connections", tags=["Port Connections"])


def get_connection_app_service(db: AsyncSession = Depends(get_db)) -> "PortConnectionApplicationService":
    return PortConnectionApplicationService(db)


@router.get("/{port_connection_id}", response_model=PortConnectionResponse, status_code=status.HTTP_200_OK)
async def get_connection_by_id(
        port_id: Annotated[str, Path(
            title="The ID of the connection to get",
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
                    description="A valid connection id with a uuid type.",
                    value={
                        "id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
            }
        )],
        response: Response,
        connection_app_service: PortConnectionApplicationService = Depends(get_connection_app_service)
) -> Any:
    """
    Endpoint to fetch a connection by its unique identifier.

    This function handles the HTTP GET request to retrieve a specific port
    connection using the provided connection ID. The function uses a service
    to interact with the underlying connection data and returns the corresponding
    response. It validates the ID format, processes the request, and returns the
    connection details if found.

    :param port_id: The unique identifier of the connection to retrieve.
                    This must be a UUID string.
    :param response: The HTTP response to be modified and returned.
    :param connection_app_service: An instance of PortConnectionApplicationService
                                    used to fetch connection information.
    :return: Response containing the connection details or an error message.
    """
    try:
        connection = await connection_app_service.get_connection_by_id(port_id)
        if not connection:
            response = status.HTTP_404_NOT_FOUND
            return {"error": "Connection not found"}

        response = assemble_connection_response_from_entity(connection)
        return response
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}


@router.get("/", response_model=list[PortConnection], status_code=status.HTTP_200_OK)
async def get_all_connections(
        response: Response,
        port_app_service: PortConnectionApplicationService = Depends(get_connection_app_service)
) -> Any:
    """
    Endpoint to retrieve all port connections.

    :param response: To set the status code.
    :param port_app_service: Injected port connection application service.

    :return: A list of all port connections.
    """
    try:
        connections = await port_app_service.get_all_connections()
        if len(connections) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Connections not found"}

        responses = []
        for connection in connections:
            responses.append(assemble_connection_response_from_entity(connection))
        return connections
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}