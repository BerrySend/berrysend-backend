from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, Path, Response
from fastapi.openapi.models import Example
from sqlalchemy.ext.asyncio import AsyncSession

from app.route_optimization.application.optimal_route_application_service import OptimalRouteApplicationService
from app.route_optimization.domain.models.optimal_route import OptimalRoute
from app.route_optimization.interfaces.assemblers.optimized_route_response_from_entity_assembler import \
    assemble_optimized_route_response_from_entity
from app.route_optimization.interfaces.schemas.responses.optimized_route_response import OptimizedRouteResponse
from app.shared.infrastructure.persistence.session_generator import get_db

# Create a router for optimizing routes
router = APIRouter(prefix="/api/v1/routes", tags=["Routes"])


# Get optimal route application service
def get_optimized_route_app_service(db: AsyncSession = Depends(get_db)) -> "OptimalRouteApplicationService":
    return OptimalRouteApplicationService(db)


@router.get("/{route_id}", response_model=OptimizedRouteResponse, status_code=status.HTTP_200_OK)
async def get_route_by_id(
        route_id: Annotated[str, Path(
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
        route_app_service: OptimalRouteApplicationService = Depends(get_optimized_route_app_service)
) -> Any:
    """
    Retrieve an optimized route by its unique identifier.

    This function fetches an optimized route using its unique ID from the application service.
    The ID provided should follow a UUID format. If a route corresponding to the given ID
    is not found, an error response with a `404` status code is returned. In cases where
    the provided ID is invalid or does not follow the expected format, a `400` status code
    with error details is returned.

    :param route_id: The unique identifier (UUID) for the optimized route to fetch.
    :param response: The Response object, used to set the response status code.
    :param route_app_service: The application service for fetching the optimized route.
    :return: Upon success, returns a dictionary representation of the optimized route.
             On failure, returns an error dictionary with a corresponding status code.
    """
    try:
        route: OptimalRoute = await route_app_service.get_optimal_route_by_id(route_id)
        if not route:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Optimal route for given id not found"}

        response = assemble_optimized_route_response_from_entity(route)
        return response
    except ValueError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}