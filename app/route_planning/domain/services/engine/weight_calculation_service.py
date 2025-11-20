"""
Engine service for calculating a unique weight of a port connection by using its restrictions
"""
from app.route_planning.domain.models.port_connection import PortConnection


class WeightCalculationService:
    def __init__(self, cost_multiplier: float, distance_multiplier: float, time_multiplier: float):
        """
        Initializes the core attributes used to calculate various multipliers. These multipliers
        are applied to costs, distances, and time calculations. Each multiplier affects respective
        calculations independently.

        :param cost_multiplier: Multiplier applied to cost computations.
        :type cost_multiplier: float
        :param distance_multiplier: Multiplier applied to distance computations.
        :type distance_multiplier: float
        :param time_multiplier: Multiplier applied to time computations.
        :type time_multiplier: float
        """
        self.cost_multiplier = cost_multiplier
        self.distance_multiplier = distance_multiplier
        self.time_multiplier = time_multiplier

    def calculate(self, connection: PortConnection) -> float:
        """
        Calculates the total cost of a port connection based on provided multipliers.

        This static method uses cost, distance, and time multipliers to compute the
        final cost of a given port connection. The multipliers modify their respective
        attributes (`cost_usd`, `time_hours`, `distance_km`) of the `PortConnection`
        object to determine the total connection cost.

        :param connection: The port connection data containing the cost, time, and
            distance attributes necessary for the calculation.
        :type connection: PortConnection

        :return: The computed cost of the port connection which is based on multipliers.
        :rtype: float
        """
        return (
                connection.cost_usd * self.cost_multiplier +
                connection.time_hours * self.time_multiplier +
                connection.distance_km * self.distance_multiplier
        )