from app.route_planning.domain.algorithms.a_star_algorithm import AStarAlgorithm
from app.route_planning.domain.models.port import Port
from app.route_planning.domain.models.port_connection import PortConnection


class AStarAlgorithmService:
    def __init__(self):
        """
        Represents an initialization method for setting up the A* algorithm object.

        This function initializes the required components for later tasks
        or algorithms with the `AStarAlgorithm` instance properly assigned. It
        does not accept any parameters nor return a value.

        :ivar algorithm: An instance of the `AStarAlgorithm` class. This can
            be used to execute pathfinding or other related tasks.
        :type algorithm: AStarAlgorithm
        """
        self.algorithm = AStarAlgorithm()

    def build_graph(self, ports: list[Port], connections: list[PortConnection]):
        """
        Builds a graph by adding ports and their connections to the internal algorithm.

        This method processes the provided ports and connections to construct a graph
        representation using the underlying algorithm. Each port is added with its
        associated name, and for each connection, the corresponding port names and
        distance are used to establish the connection.

        :param ports: List of Port objects which represent nodes in the graph.
        :param connections: List of PortConnection objects which define the edges
            between the nodes, including the distance in kilometers.
        :return: None
        """
        for port in ports:
            self.algorithm.add_port(port, port.name)

        for conn in connections:
            self.algorithm.add_connection(conn.port_a_name, conn.port_b_name, conn.distance_km)

    def compute_algorithm(self, start_port_name: str, end_port_name: str) -> list[str]:
        """
        Computes and returns the shortest path between two ports using the A* algorithm.

        This function leverages the A* algorithm, which is implemented in the `algorithm`
         attribute to determine the optimal path between the specified start and end
        ports. The result is a list of strings representing the nodes (ports) in the
        calculated path.

        :param start_port_name: The name of the starting port (node).
        :type start_port_name: str
        :param end_port_name: The name of the destination port (node).
        :type end_port_name: str
        :return: A list of port names representing the shortest path from start to end.
        :rtype: list[str]
        """
        return self.algorithm.apply_a_star(start_port_name, end_port_name)