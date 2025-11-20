class BellmanFordAlgorithm:
    def __init__(self, vertices):
        """
        Class to represent a graph with vertices and edges for operations such as edge addition.
        Provides functionality to manage a graph's structure through its vertices and edges.

        :param vertices: Number of vertices in the graph.
        :type vertices: int
        """

        # Total number of vertices in the graph
        self.V = vertices

        # List of edges in the graph with format (u, v, weight)
        self.edges = []

    def add_edge(self, u, v, weight):
        """
        Adds an edge between two nodes in the graph with a specified weight.

        This function allows adding directed or undirected edges by
        specifying the originating node, the target node, and the weight
        of the connection. These edges are stored in an internal list
        as tuples for further processing within the graph structure.

        :param u: The originating node of the edge.
        :type u: Any
        :param v: The destination node of the edge.
        :type v: Any
        :param weight: The weight or cost associated with the edge.
        :type weight: float

        :return: None
        """
        self.edges.append((u, v, weight))

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
        dist = [float('inf')] * self.V
        dist[origin] = 0
        predecessor = [None] * self.V

        # Iterate a maximum of V-1 times
        for i in range(self.V - 1):
            change = False
            for u, v, w in self.edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    predecessor[v] = u
                    change = True

            # If no change was made in this iteration, stop the algorithm
            if not change:
                break

            # If no change was made in this iteration, and the distance to the destination is still infinitive,
            # the algorithm will stop early
            if dist[destination] != float('inf') and not any(dist[u] + w < dist[v] for u, v, w in self.edges if v == destination):
                break

        # Detect negative weight cycles
        for u, v, w in self.edges:
            if dist[u] + w < dist[v]:
                raise Exception("WARNING: Negative weight cycle detected!")

        # Build the path
        path = []
        node = destination
        while node is not None:
            path.append(node)
            node = predecessor[node]
        path.reverse()

        return dist[destination], path