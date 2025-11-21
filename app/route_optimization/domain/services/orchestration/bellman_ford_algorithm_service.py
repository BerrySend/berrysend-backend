from app.route_optimization.domain.algorithms.bellman_ford_algorithm import BellmanFordAlgorithm
from app.port_management.domain.models.port import Port
from app.port_management.domain.models.port_connection import PortConnection
from app.route_optimization.domain.services.engine.weight_calculation_service import WeightCalculationService


class BellmanFordAlgorithmService:
    def __init__(self, cost_m: float, dist_m: float, time_m: float):
        """
        Initializes a route optimization system using the Bellman-Ford algorithm for graph traversal
        and a custom weight calculation service based on provided cost, distance, and time metrics.

        :param cost_m: A multiplier representing the weight contribution of cost to total edge weight.
        :type cost_m: float
        :param dist_m: A multiplier representing the weight contribution of distance to total edge weight.
        :type dist_m: float
        :param time_m: A multiplier representing the weight contribution of time to total edge weight.
        :type time_m: float
        """
        self.algorithm = BellmanFordAlgorithm()
        self.weight_calculation_service = WeightCalculationService(cost_m, dist_m, time_m)

    def build_graph(self, ports: list[Port], connections: list[PortConnection]):
        """
        Builds a graph by adding ports and connections to the underlying algorithm.

        Detailed Summary:
        This method facilitates the creation of a graph by processing the provided
        list of ports and port connections. Each port is registered with the
        algorithm, and each connection's weight is calculated and then added
        to establish relationships between the ports.

        :param ports: A list of Port objects to be added to the graph.
        :type ports: list[Port]
        :param connections: A list of PortConnection objects defining relationships
            between the provided ports, which are also added to the graph.
        :type connections: list[PortConnection]
        :return: None
        """
        for port in ports:
            self.algorithm.add_port(port, port.name)

        for conn in connections:
            if not conn.is_restricted:
                final_weight = self.weight_calculation_service.calculate(conn)
                self.algorithm.add_connection(conn.port_a_name, conn.port_b_name, final_weight)

    def compute_algorithm(self, start_port_name: str, end_port_name: str) -> tuple[float, list[str]]:
        """
        Compute the shortest path between two ports using the Bellman-Ford algorithm.
        This method leverages the algorithm module to determine the optimal route
        from the provided starting port to the destination port.

        :param start_port_name: Name of the starting port
        :type start_port_name: str
        :param end_port_name: Name of the destination port
        :type end_port_name: str
        :return: Result of the Bellman-Ford algorithm application, representing the computed path
        :rtype: tuple[float, list[str]]
        """
        return self.algorithm.apply_bellman_ford(start_port_name, end_port_name)