"""
A* Algorithm for optimization of travel distances in planning routes
"""
import heapq
import math


class AStarAlgorithm:
    def __init__(self):
        """
        Initializes an instance of the class with default attributes.

        :ivar ports: Mapping of port names to the corresponding Port object.
        :vartype ports: dict

        :ivar edges: A mapping of port names to a list of tuples. Each tuple
            contains a neighbor's name and the distance to it in kilometers.
        :vartype adj: dict
        """

        # Name -> Port
        self.ports = {}

        # Name -> [(neighbour, distance_km), ...]
        self.edges = {}

    def add_port(self, port):
        """
        Adds a port to the collection of ports and its adjacency list.

        This function adds the given port to the `ports` dictionary, associating it
        with its name. If the port is not already present in the adjacency list,
        it will also initialize an empty list for it in the `adj` adjacency list.

        :param port: The port object to be added to the collection.
        :type port: Port
        """
        self.ports[port.name] = port
        if port.name not in self.edges:
            self.edges[port.name] = []

    def add_connection(self, connection):
        """
        Adds a connection between two ports with a specified distance to the adjacency list.

        :param connection: The connection object that contains information about the ports and
            the distance between them.
        :type connection: Connection
        :return: None
        """
        self.edges[connection.port1].append((connection.port2, connection.distance))

    def heuristic(self, current_node, destination_node):
        """
        Calculates the heuristic distance in kilometers between two nodes (ports)
        using the Haversine formula. This formula computes the great-circle distance
        between two points on a sphere given their longitudes and latitudes.

        :param current_node: The identifier of the current node (port).
        :type current_node: Any
        :param destination_node: The identifier of the destination node (port).
        :type destination_node: Any

        :return: The heuristic distance in kilometers between `current_node`
            and `destination_node`.
        :rtype: float
        """
        p1 = self.ports[current_node]
        p2 = self.ports[destination_node]
        earth_radius = 6371  # km
        phi1, phi2 = math.radians(p1.lat), math.radians(p2.lat)
        delta_phi = math.radians(p2.lat - p1.lat)
        delta_lambda = math.radians(p2.lon - p1.lon)
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earth_radius * c

    def apply_a_star(self, origin, destination):
        """
        Calculates the shortest path from a starting point to a destination using the
        A* pathfinding algorithm. It uses a priority queue to determine the next
        node to explore based on the f_score, which combines the cost of the path
        from the origin to a given node (g_score) and a heuristic estimate of the
        remaining distance to the destination.

        :param origin: The starting node for the A* search
        :type origin: Any

        :param destination: The target node for the A* search
        :type destination: Any

        :return: A tuple where the first element is the cost of the shortest path,
            and the second element is a list representing the sequence of nodes
            in the shortest path. If no path exists, it returns (infinity, empty list).
        :rtype: Tuple[float, List[Any]]
        """
        open_set = []
        heapq.heappush(open_set, (0, origin))
        came_from = {} # Rebuild the route

        g_score = {n: float('inf') for n in self.ports}
        g_score[origin] = 0

        f_score = {n: float('inf') for n in self.ports}
        f_score[origin] = self.heuristic(origin, destination)

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == destination:
                # Rebuild the route
                route = []
                while current in came_from:
                    route.append(current)
                    current = came_from[current]
                route.append(origin)
                route.reverse()
                return g_score[destination], route

            for neighbour, weight in self.edges[current]:
                tentative_g_score = g_score[current] + weight
                if tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + self.heuristic(neighbour, destination)
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))

        # No path found :(
        return float('inf'), []