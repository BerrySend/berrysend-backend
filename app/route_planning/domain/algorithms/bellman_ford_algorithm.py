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

        # Name -> [(neighbour, weight), ...]
        self.edges = []

    def add_port(self, port):
        """
        Adds a port to the port dictionary and initializes its edges.

        This method will add a given port to the `ports` dictionary using the port's
        name as the key. Additionally, if the port's name is not already present in the
        `edges` dictionary, it will initialize an empty list for it.

        :param port: An object representing the port to be added.
        :type port: Any
        :return: None
        """
        self.ports[port.name] = port
        if port.name not in self.edges:
            self.edges[port.name] = []

    def add_connection(self, connection):
        """
        Adds a connection between two ports with a specified distance.

        This method updates the internal structure to include a new connection
        from `connection.port1` to `connection.port2`, along with its
        corresponding weight.

        :param connection: Object that contains attributes `port1`, `port2`,
            and `weight`.
        :type connection: object
        :return: None
        """
        self.edges[connection.port1].append((connection.port2, connection.distance))

    def apply_bellman_ford(self, origin, destination):
        """
        Calculates the shortest path from the origin to the destination using the
        Bellman-Ford algorithm. It also detects negative weight cycles in the graph.
        The method computes both the shortest distance and the corresponding path
        as a list of nodes.

        :param origin: Starting vertex for the shortest path calculation
        :type origin: int

        :param destination: Target vertex for the shortest path calculation
        :type destination: int

        :return: A tuple containing the shortest distance to the destination
            and a list representing the path to reach it
        :rtype: tuple[float, list[int]]

        :raises Exception: If a negative weight cycle is detected
        """
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
            for conn in self.edges:
                # Defines the variables for the current edge
                u, v, w = conn.port1, conn.port2, conn.weight

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
        for conn in self.edges:
            u, v, w = conn.port1, conn.port2, conn.weight
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