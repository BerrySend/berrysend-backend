from fastapi import APIRouter, status, Depends
from fastapi.openapi.models import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.route_planning.application.port_connection_application_service import PortConnectionApplicationService
from app.route_planning.domain.models.port_connection import PortConnection
from app.route_planning.interfaces.schemas.responses.port_connection_response import PortConnectionResponse
from app.shared.infrastructure.persistence.session_generator import get_db

# Create a router for the port connections
router = APIRouter(prefix="/api/v1/port-connections", tags=["Port Connections"])


def get_connection_app_service(db: AsyncSession = Depends(get_db)) -> "PortConnectionApplicationService":
    return PortConnectionApplicationService(db)


@router.get("/", response_model=list[PortConnection], status_code=status.HTTP_200_OK)
async def get_all_connections(
        response: Response,
        port_app_service: PortConnectionApplicationService = Depends(get_connection_app_service)
):
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
            return []

        responses = []
        for connection in connections:
            responses.append(PortConnectionResponse(
                id=connection.id,
                port_a_id=connection.port_a_id,
                port_b_id=connection.port_b_id,
                distance_km=connection.distance_km,
                estimated_travel_time_hours=connection.time_hours,
                cost_usd=connection.cost_usd,
                route_type=connection.route_type,
                is_restricted=connection.is_restricted
            ))
        return connections
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}