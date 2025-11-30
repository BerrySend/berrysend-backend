from app.port_management.domain.models.port import Port
from app.port_management.domain.models.port_connection import PortConnection
from app.route_optimization.domain.algorithms.dijkstra_algorithm import DijkstraAlgorithm


class DijkstraAlgorithmService:
    def __init__(self):
        """
        Represents the initialization of an instance that employs the DijkstraAlgorithm
        for its operations. This initializes the required components to handle algorithmic
        tasks pertaining to Dijkstra's shortest path method.

        :ivar algorithm: An instance of the DijkstraAlgorithm used internally
                         to compute the shortest paths.
        :type algorithm: DijkstraAlgorithm
        """
        self.algorithm = DijkstraAlgorithm()

    def build_graph(self, ports: list[Port], connections: list[PortConnection]) -> None:
        """
        Builds a graph representation using the provided ports and connections. This function
        integrates the ports and their corresponding connections into the algorithm by registering
        them accordingly.

        :param ports: A list of available ports in the system.
        :param connections: A list of connections between ports, including their details such
            as the connecting ports and the time required for traversal.
        :return: None
        """
        # Create set of port names for quick lookup
        port_names = {port.name for port in ports}
        
        for port in ports:
            self.algorithm.add_port(port, port.name)

        for conn in connections:
            # Only add connection if both ports exist in the graph
            if conn.port_a_name in port_names and conn.port_b_name in port_names:
                # Use cost instead of time to differentiate from A* (distance-based)
                self.algorithm.add_connection(conn.port_a_name, conn.port_b_name, conn.cost_usd)

    def compute_algorithm(self, origin_port_name: str, destination_port_name: str, export_weight: float) -> tuple[float, list[str]]:
        """
        Computes the shortest path using Dijkstra's algorithm between the given
        origin and destination ports.

        :param export_weight: The weight of product to export as a float value.
        :param origin_port_name: The name of the origin port as a string.
        :param destination_port_name: The name of the destination port as a string.

        :return: A tuple containing the shortest distance and the corresponding path.
        """
        return self.algorithm.apply_dijkstra(origin_port_name, destination_port_name, export_weight)