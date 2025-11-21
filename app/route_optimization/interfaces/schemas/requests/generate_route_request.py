from typing import Optional

from pydantic import BaseModel, Field

from app.route_optimization.interfaces.schemas.requests.parameters_request import ParametersRequest


class GenerateRouteRequest(BaseModel):
    """
    Represents a request to generate a route using the Bellman-Ford algorithm.

    This class is used to encapsulate all the necessary details needed when requesting
    a route generation between two ports using a specific mode of transportation and
    routing algorithm. The request includes the source, destination, mode of transportation,
    algorithm name, and specific parameters.

    :ivar source: The starting port for the route.
    :type source: str
    :ivar destination: The destination port for the route.
    :type destination: str
    :ivar mode: The mode of transportation for the route (e.g., maritime, air).
    :type mode: str
    :ivar export_weight: The weight of the route to export.
    :type export_weight: float
    :ivar algorithm_name: The name of the routing algorithm to plan the route.
    :type algorithm_name: str
    :ivar parameters: The parameters for the route generation.
    :type parameters: ParametersRequest
    """
    source: str = Field(title="The starting port for the route.")
    destination: str = Field(title="The destination port for the route.")
    mode: str = Field(title="The mode of transportation for the route (e.g., maritime, air).")
    export_weight: float = Field(title="The weight of the route to export.")
    algorithm_name: str = Field(title="The name of the routing algorithm to plan the route.")
    parameters: Optional[ParametersRequest] = Field(
        default=None,
        title="Optional parameters for algorithms that require additional inputs (e.g., Bellman-Ford)."
    )