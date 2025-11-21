"""
Dijkstra algorithm for optimizing time for travels in routes planning
"""
import heapq


class DijkstraAlgorithm:
    def __init__(self):
        """
        Manages a graph representation of ports and the connections between
        them, including travel times.

        Attributes
            ports : dict
                A mapping of port names to an associated value (initially empty).
            edges : dict
                A mapping of port names to a list of tuples, where each tuple contains
                a neighboring port name and the travel time to that port (in hours).
        """
        # Name -> Port
        self.ports = {}

        # Name -> [(neighbour, time_hours), ...]
        self.edges = {}

    def add_port(self, port, port_name=None):
        """
        Adds a new port to the port collection and initializes its corresponding
        entry in the edge dictionary if it does not already exist.

        :param port: The port to be added.
        :param port_name: The name of the port. Defaults to the port's name.
        """
        self.ports[port_name] = port
        if port_name not in self.edges:
            self.edges[port_name] = []

    def add_connection(self, port1, port2, weight=0):
        """
        Adds a connection between two ports in the `edges` dictionary.

        :param port1: The name of the first port.
        :param port2: The name of the second port.
        :param weight: The time taken to travel from port1 to port2. Defaults to 0.

        :return: None
        """
        self.edges[port1].append((port2, weight))

    def apply_dijkstra(self, origin, destination, export_weight: float) -> tuple[float, list[str]]:
        """
        Applies Dijkstra's algorithm to find the shortest path between the given origin and
        destination in a graph.

        This method calculates the shortest distance and the corresponding path from the
        origin node to the destination node using a priority queue (min-heap). The graph is
        represented with weighted edges that are stored as adjacency lists.

        :param export_weight: The weight of product to export.
        :type export_weight: float

        :param origin: The starting node of the path.
        :type origin: str

        :param destination: The target node of the path.
        :type destination: str

        :return: A tuple containing the shortest distance and the list of nodes representing
            the path. If there is no valid path, returns a distance of infinity and an
            empty path list.
        :rtype: tuple[float, list[str]]
        """
        # If the origin or destination ports have insufficient capacity, return infinity and an empty route list
        if self.ports[origin].capacity < export_weight:
            return float('inf'), []

        if self.ports[destination].capacity < export_weight:
            return float('inf'), []

        # Min-heap of (total_distance, port_name)
        heap = [(0, origin)]

        # Distance from origin to each node set as a positive infinity value
        dist = {n: float('inf') for n in self.ports}

        # Distance from origin to origin, which is always 0
        dist[origin] = 0

        # Sets the node we came from to reconstruct the path later
        came_from = {}

        # Starts the algorithm
        while heap:
            # Initializes the current node and its distance with the smallest value in the heap
            current_distance, port = heapq.heappop(heap)

            # If the destination port is reached, the route will be rebuilt
            if port == destination:
                # List of nodes in the route
                route = []

                # Rebuild the route
                while port in came_from:
                    route.append(port)
                    port = came_from[port]

                # Add the origin node to the route
                route.append(origin)

                # Reverse the route to get the correct order
                route.reverse()

                # Return the route and the distance
                return current_distance, route

            # Ignore non-optimal values (for typical optimization)
            if current_distance > dist[port]:
                continue

            # Visit the neighbor ports
            for neighbour, weight_time in self.edges[port]:
                # If the neighbor port has insufficient capacity, skip it
                if self.ports[neighbour].capacity < export_weight:
                    continue

                # Calculate the new distance to the neighbor port
                new_distance = current_distance + weight_time

                # If the new distance is shorter than the current one, update the distance and the node we came from
                if new_distance < dist[neighbour]:
                    dist[neighbour] = new_distance
                    came_from[neighbour] = port
                    heapq.heappush(heap, (new_distance, neighbour))

        # If no route was found, return infinity and an empty route list
        return float('inf'), []