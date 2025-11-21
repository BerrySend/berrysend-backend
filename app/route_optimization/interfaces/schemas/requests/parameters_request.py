from pydantic import BaseModel, Field


class ParametersRequest(BaseModel):
    """
    Represents a request model for parameter configuration.

    This class is used to define and manage multipliers related to cost,
    distance, and time in a specific request. It serves as a structure to pass
    these configuration parameters across different parts of the application.

    :ivar cost_multiplier: Multiplier applied to cost calculations.
    :ivar distance_multiplier: Multiplier applied to distance calculations.
    :ivar time_multiplier: Multiplier applied to time calculations.
    """
    cost_multiplier: float = Field(title="The cost multiplier for calculation of weight for Bellman-Ford Algorithm")
    distance_multiplier: float = Field(title="The distance multiplier for calculation of weight for Bellman-Ford Algorithm")
    time_multiplier: float = Field(title="The time multiplier for calculation of weight for Bellman-Ford Algorithm")