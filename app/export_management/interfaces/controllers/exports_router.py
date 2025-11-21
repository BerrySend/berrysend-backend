from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, Path
from fastapi.openapi.models import Example, Response
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.export_management.application.export_application_service import ExportApplicationService
from app.export_management.interfaces.assemblers.export_response_from_entity_assembler import \
    assemble_export_response_from_entity
from app.export_management.interfaces.schemas.requests.export_request import ExportRequest
from app.export_management.interfaces.schemas.responses.export_response import ExportResponse
from app.shared.infrastructure.persistence.session_generator import get_db

# Create a router for the exports
router = APIRouter(prefix="/api/v1/exports", tags=["Exports"])


# Get export application service
def get_export_app_service(db: AsyncSession = Depends(get_db)) -> "ExportApplicationService":
    return ExportApplicationService(db)


@router.get("/{export_id}", response_model=ExportResponse, status_code=status.HTTP_200_OK)
async def get_export_by_id(
        export_id: Annotated[str, Path(
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
                    description="A valid export id with a uuid type.",
                    value={
                        "id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
            }
        )],
        response: Response,
        export_app_service: ExportApplicationService = Depends(get_export_app_service)
) -> Any:
    """
    Handles a GET request to fetch an export record by its unique identifier.

    This endpoint retrieves the details of an export record from the service based on
    the provided `export_id`. The record is returned as a response model. If no record
    is found or an error occurs during processing, appropriate error responses are returned.

    :param export_id: The unique identifier of the export record to retrieve. Must be a valid
        UUID to ensure proper identification.
    :param response: The response object for setting the HTTP status code manually if necessary.
    :param export_app_service: The dependency-injected export application service that
        manages the retrieval and processing of export records.
    :return: The export details as a structured response model or an error message if
        processing fails.
    """
    try:
        export = await export_app_service.get_export_by_id(export_id)
        if not export:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Export for given id not found"}

        response = assemble_export_response_from_entity(export)
        return response
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@router.post("/", response_model=ExportResponse, status_code=status.HTTP_201_CREATED)
async def register_export(
        export: ExportRequest,
        response: Response,
        export_app_service: ExportApplicationService = Depends(get_export_app_service)
) -> Any:
    """
    Registers a new export record using the provided export details.

    This endpoint accepts data for creating a new export, including necessary
    information such as transportation mode, weights, quantities, and related
    optimized route identifiers. The registered export is then returned as a
    response. If an error occurs during registration, an appropriate error
    response is returned.

    :param export: The data necessary for creating the export registration.
    :type export: ExportRequest
    :param response: Instance of the response class to set status codes and details.
    :type response: Response
    :param export_app_service: Service dependency to handle export operations.
    :type export_app_service: ExportApplicationService
    :return: The response containing the registered export details or an error
        detailing why the request failed.
    :rtype: Any
    """
    try:
        export = await export_app_service.register_export(
            export.comercial_description,
            export.transportation_mode,
            export.us_fob,
            export.gross_weight,
            export.net_weight,
            export.unit,
            export.quantity,
            export.optimized_route_id,
            export.user_id
        )

        if not export:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Failed to create export."}

        response = assemble_export_response_from_entity(export)
        return response
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@router.patch("/{export_id}/routes/{route_id}/assign", response_model=ExportResponse, status_code=status.HTTP_200_OK)
async def assign_route_id_to_export(
        response: Response,
        export_id: Annotated[str, Path(
            title="The ID of the export to assign the new route",
            openapi_examples={
                "invalid": Example(
                    summary="Invalid",
                    description="When using a non-uuid value for the id, an error is returned.",
                    value={
                        "id": "hi"
                    }
                )
            }
        )],
        route_id: Annotated[str, Path(
            title="The ID of the route to assign",
            openapi_examples={
                "invalid": Example(
                    summary="Invalid",
                    description="When using a non-uuid value for the id, an error is returned.",
                    value={
                        "id": "hi"
                    }
                )
            }
        )],
        export_app_service: ExportApplicationService = Depends(get_export_app_service)
) -> Any:
    """
    Assigns a route ID to a specific export and updates the associated export entity.

    This function processes a PATCH request to assign a route ID to a specific export by its
    export ID. It uses the export application's service layer to perform the update. If
    the specified export ID does not exist, a 404 status code is returned. In case of any
    unexpected error, a 400 status code with the error message is returned.

    :param response: FastAPI Response object used to manipulate HTTP response properties.
    :param export_id: The unique identifier of the export. Should be provided as a valid UUID.
    :param route_id: The ID of the route to be assigned to the export.
    :param export_app_service: Dependency injection for the export application service instance.
    :return: Response dict containing either the updated export details or an error message.
    """
    try:
        export = await export_app_service.assign_route_id_to_export(export_id, route_id)
        if not export:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Export for given id not found"}

        response = assemble_export_response_from_entity(export)
        return response
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}