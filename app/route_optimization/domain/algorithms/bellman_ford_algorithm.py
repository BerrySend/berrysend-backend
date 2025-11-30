"""
Bellman-Ford algorithm for general optimization in routes
"""


class BellmanFordAlgorithm:
    def __init__(self):
        """
        Represents a graph structure maintaining ports and edges.

        The class provides data structures to store ports and their associated
        edges. Ports are represented as a dictionary where the key is the port
        name, and edges are stored as a list of tuples consisting of a neighbor
        and a corresponding weight.

        Attributes
            ports : dict
                Dictionary mapping port names as keys to associated port objects or
                placeholders.
            edges : list
                List of edges represented as tuples, where each tuple contains a
                neighbor and a weight.
        """
        # Name -> Port
        self.ports = {}

        # list of (u, v, weight)
        self.edges = []

    def add_port(self, port, port_name=None):
        """
        Adds a port to the port dictionary.

        This method will add a given port to the `ports` dictionary using the port's
        name as the key.

        :param port: The port to be added.
        :param port_name: The name of the port. Defaults to the port's name.
        """
        self.ports[port_name] = port

    def add_connection(self, port1, port2, weight=0):
        """
        Adds a connection between two ports with a specified distance.

        This method updates the internal structure to include a new connection
        from `connection.port1` to `connection.port2`, along with its
        corresponding weight.

        :param port1: The name of the first port.
        :param port2: The name of the second port.
        :param weight: The distance between the two ports. Defaults to 0.

        :return: None
        """
        self.edges.append((port1, port2, weight))

    def apply_bellman_ford(self, origin: str, destination: str, export_weight: float) -> tuple[float, list[str]]:
        """
        Calculates the shortest path from the origin to the destination using the
        Bellman-Ford algorithm. It also detects negative weight cycles in the graph.
        The method computes both the shortest distance and the corresponding path
        as a list of nodes.

        :param export_weight: The weight of a product to export.
        :type export_weight: Float

        :param origin: Starting vertex for the shortest path calculation
        :type origin: str

        :param destination: Target vertex for the shortest path calculation
        :type destination: str

        :return: A tuple containing the shortest distance to the destination
            and a list representing the path to reach it
        :rtype: tuple[float, list[str]]

        :raises Exception: If a negative weight cycle is detected
        """
        # If the origin or destination ports have insufficient capacity, return infinity and an empty route list
        if self.ports[origin].capacity < export_weight:
            return float('inf'), []

        if self.ports[destination].capacity < export_weight:
            return float('inf'), []

        # Initializes the distance from the origin to each node as a positive infinity value
        dist = {n: float('inf') for n in self.ports}

        # Sets the distance from the origin to itself to 0
        dist[origin] = 0

        # Initializes the node we came from to reconstruct the path later
        came_from = {}

        for _ in range(len(self.ports) - 1):
            # Sets a flag to indicate if any change was made during the iteration
            updated = False

            # For each edge in the graph
            for u, v, w in self.edges:

                # If the neighbor port has not enough capacity for the export weight, skip it
                if self.ports[v].capacity < export_weight:
                    continue

                # If the distance from the current node to the neighbor is lower than the
                # current distance, update the distance and the node we came from
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    came_from[v] = u
                    updated = True

            # If no change was made during the iteration, the algorithm is finished
            if not updated:
                break

        # Check for negative weight cycles
        for u, v, w in self.edges:
            if self.ports[v].capacity < export_weight:
                continue

            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                raise Exception("WARNING: Negative weight cycle detected!")

        # If the destination is unreachable, return infinity and an empty route list
        if dist[destination] == float('inf'):
            return float('inf'), []

        # Build the route from origin to destination
        route = []

        node = destination
        while node in came_from:
            route.append(node)
            node = came_from[node]

        # Adds the origin to the route
        route.append(origin)

        # Reverse the route to get the correct order
        route.reverse()

        return dist[destination], route