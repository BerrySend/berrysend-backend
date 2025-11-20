from app.route_optimization.domain.algorithms import DijkstraAlgorithm
from app.port_management.domain.models.port import Port
from app.port_management.domain.models.port_connection import PortConnection


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
        for port in ports:
            self.algorithm.add_port(port, port.name)

        for conn in connections:
            self.algorithm.add_connection(conn.port_a_name, conn.port_b_name, conn.time_hours)

    def compute_algorithm(self, origin_port_name: str, destination_port_name: str):
        """
        Computes the shortest path using Dijkstra's algorithm between the given
        origin and destination ports.

        :param origin_port_name: The name of the origin port as a string.
        :param destination_port_name: The name of the destination port as a string.

        :return: A tuple containing the shortest distance and the corresponding path.
        """
        return self.algorithm.apply_dijkstra(origin_port_name, destination_port_name)