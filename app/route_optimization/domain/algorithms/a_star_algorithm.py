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

    def add_port(self, port, port_name=None):
        """
        Adds a port to the collection of ports and its adjacency list.

        This function adds the given port to the `ports` dictionary, associating it
        with its name. If the port is not already present in the adjacency list,
        it will also initialize an empty list for it in the `adj` adjacency list.

        :param port: The port to be added.
        :param port_name: The name of the port. Defaults to the port's name.
        """
        self.ports[port_name] = port
        if port_name not in self.edges:
            self.edges[port_name] = []

    def add_connection(self, port1, port2, weight=0):
        """
        Adds a connection between two ports with a specified distance to the adjacency list.

        :param port1: The name of the first port.
        :param port2: The name of the second port.
        :param weight: The time taken to travel from port1 to port2. Defaults to 0.

        :return: None
        """
        self.edges[port1].append((port2, weight))

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
        # Gets the current port
        p1 = self.ports[current_node]

        # Gets the destination port
        p2 = self.ports[destination_node]

        # Setting the aproximate Earth radius in km
        earth_radius = 6371  # km

        # Calculating the distance using the Haversine formula
        phi1, phi2 = math.radians(p1.lat), math.radians(p2.lat)

        # Finds the delta pi by subtracting the latitudes
        delta_phi = math.radians(p2.lat - p1.lat)

        # Finds the delta lambda by subtracting the longitudes
        delta_lambda = math.radians(p2.lon - p1.lon)

        # Calculates the Haversine formula
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

        # Calculates the final distance
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Returns the distance in km
        return earth_radius * c

    def apply_a_star(self, origin, destination, export_weight) -> tuple[float, list[str]]:
        """
        Calculates the shortest path from a starting point to a destination using the
        A* pathfinding algorithm. It uses a priority queue to determine the next
        node to explore based on the f_score, which combines the cost of the path
        from the origin to a given node (g_score) and a heuristic estimate of the
        remaining distance to the destination.

        :param export_weight: The weight of product to export
        :type export_weight: float

        :param origin: The starting node for the A* search
        :type origin: Any

        :param destination: The target node for the A* search
        :type destination: Any

        :return: A tuple where the first element is the cost of the shortest path,
            and the second element is a list representing the sequence of nodes
            in the shortest path. If no path exists, it returns (infinity, empty list).
        :rtype: Tuple[float, List[Any]]
        """
        # If the origin or destination ports have insufficient capacity, return infinity and an empty route list
        if self.ports[origin].capacity < export_weight:
            return float('inf'), []

        if self.ports[destination].capacity < export_weight:
            return float('inf'), []

        # Initializes the open set as a priority queue for a list of candidate nodes to be visited
        open_set = []

        # Pushes the origin node to the open set
        heapq.heappush(open_set, (0, origin))

        # Initializes the route for future rebuilding
        came_from = {}

        # A* Formula
        # f(n) = g(n) + h(n)

        # Initializes 'g(n)' as infinity for all nodes
        g_score = {n: float('inf') for n in self.ports}

        # Initializes 'g(n)' as 0 for the origin
        g_score[origin] = 0

        # Initializes 'f(n)' as infinity for all nodes
        f_score = {n: float('inf') for n in self.ports}

        # Initializes 'f(n)' as g(n) + h(n) for the origin using the heuristic function
        f_score[origin] = self.heuristic(origin, destination)

        # Starts the algorithm
        while open_set:
            # Defines the current node as the one with the smallest f_score in the open set
            _, current = heapq.heappop(open_set)

            # If the destination node is reached, the route will be rebuilt
            if current == destination:
                # Rebuild the route
                route = []

                # Add the ports to the route in reverse order
                while current in came_from:
                    route.append(current)
                    current = came_from[current]

                # Adds the origin node to the route
                route.append(origin)

                # Reverse the route to get the correct order
                route.reverse()

                # Return the route and the distance
                return g_score[destination], route

            # Visit the neighbors
            for neighbour, weight in self.edges[current]:

                # Check if the neighbor port has enough capacity for the export weight
                if self.ports[neighbour].capacity < export_weight:
                    continue

                # Calculate the tentative g_score for the neighbor
                tentative_g_score = g_score[current] + weight

                # If the tentative g_score is lower than the current g_score, update the g_score and the node we came from
                if tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + self.heuristic(neighbour, destination)
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))

        # No path found :(
        return float('inf'), []