from typing import Optional

from pydantic import BaseModel, Field, validator, field_validator

from app.route_optimization.interfaces.schemas.requests.parameters_request import ParametersRequest
from app.route_optimization.interfaces.utils.algorithm_names import ALGORITHM_ALIASES


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

    @field_validator("algorithm_name", mode="before")
    @classmethod
    def normalize_algorithm_name(cls, v):
        """
        This method is a field validator designed to normalize the value of the
        `algorithm_name` field before it is assigned. It ensures that the input
        value is standardized and checks against predefined aliases. If the
        normalized name corresponds to an alias, it returns the standardized
        name. If no match is found, a ValueError is raised to indicate an
        invalid algorithm name.

        :param v: The value of the algorithm name to be validated and normalized.
        :type v: str
        :return: The normalized algorithm name if it matches an alias.
        :rtype: str
        :raises ValueError: If the name does not match any defined aliases.
        """
        key = str(v).lower().replace("-", "").replace(" ", "")
        if key in ALGORITHM_ALIASES:
            return ALGORITHM_ALIASES[key]
        raise ValueError(f"Invalid algorithm name: {v}")