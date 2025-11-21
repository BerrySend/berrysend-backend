"""
Application service for optimal routes.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.port_management.infrastructure.repositories.port_connection_repository import PortConnectionRepository
from app.port_management.infrastructure.repositories.port_repository import PortRepository
from app.route_optimization.domain.models.optimal_route import OptimalRoute
from app.route_optimization.domain.services.orchestration.a_start_algorithm_service import AStarAlgorithmService
from app.route_optimization.domain.services.orchestration.bellman_ford_algorithm_service import \
    BellmanFordAlgorithmService
from app.route_optimization.domain.services.orchestration.dijkstra_algorithm_service import DijkstraAlgorithmService
from app.route_optimization.domain.services.support.optimal_route_service import OptimalRouteService
from app.route_optimization.infrastructure.repositories.optimal_route_repository import OptimalRouteRepository


class OptimalRouteApplicationService:
    def __init__(self, db: AsyncSession):
        """
        Initializes an instance of a class responsible for managing and coordinating
        services and repository for calculating optimal routes.

        :param db: Database session to be used for managing repository interactions.
        :type db: AsyncSession
        """
        self.optimal_route_service = OptimalRouteService()
        self.optimal_route_repository = OptimalRouteRepository(db)
        self.ports_repository = PortRepository(db)
        self.connections_repository = PortConnectionRepository(db)

    async def build_optimal_route_with_a_star(self, start_port_name: str, end_port_name: str, mode: str):
        """
        Builds an optimal route between two ports using the A* algorithm, based on the specified mode
        (maritime or air). It calculates the shortest path considering distance, time, and cost.

        :param start_port_name: The name of the starting port.
        :type start_port_name: str
        :param end_port_name: The name of the destination port.
        :type end_port_name: str
        :param mode: The mode of transportation, e.g., "maritime" or "air".
        :type mode: str
        :return: A tuple containing the optimal route as a list of ports, the total distance, the total
            time in hours, and the total cost in USD.
        :rtype: Tuple[List[str], float, float, float]
        :raises ValueError: If there is an error while retrieving ports and connections.
        :raises Exception: If there is an error while calculating the optimal route using the A* algorithm.
        """
        try:
            ports = []
            connections = []

            if mode == "maritime":
                ports = await self.ports_repository.get_all_maritime_ports()
                connections = await self.connections_repository.get_all_maritime_connections()
            elif mode == "air":
                ports = await self.ports_repository.get_all_air_ports()
                connections = await self.connections_repository.get_all_air_connections()
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve ports and connections: {e}.")

        try:
            a_star_service = AStarAlgorithmService()
            a_star_service.build_graph(ports, connections)
            total_distance, optimal_route = a_star_service.compute_algorithm(start_port_name, end_port_name)
        except Exception as e:
            raise Exception(f"Error trying to compute optimal route: {e}.")

        connections_list = []

        for i in range(len(optimal_route)):
            if i == len(optimal_route) - 1:
                break

            port_i = optimal_route[i]
            port_j = optimal_route[i + 1]
            connection = await self.connections_repository.get_connection_by_origin_and_destination_name(port_i, port_j)
            connections_list.append(connection)

        total_time: float = 0
        total_cost: float = 0

        for conn in connections_list:
            total_time += conn.time_hours
            total_cost += conn.cost_usd

        origin_port = await self.ports_repository.get_port_by_name(start_port_name)
        destination_port = await self.ports_repository.get_port_by_name(end_port_name)

        optimal_route_obj = self.optimal_route_service.register_optimal_route(
            origin_port_id=origin_port.id,
            origin_port_name=origin_port.name,
            destination_port_id=destination_port.id,
            destination_port_name=destination_port.name,
            route_mode=mode,
            algorithm_used="AStar",
            total_cost=total_cost,
            total_distance=total_distance,
            total_time=total_time,
            visited_ports=optimal_route
        )

        await self.optimal_route_repository.create(optimal_route_obj)

        return optimal_route, total_distance, total_time, total_cost

    async def build_optimal_route_with_bellman_ford(self, start_port_name: str, end_port_name: str, cost_m: float,
                                                    distance_m: float, time_m: float, mode: str):
        """
        Builds the optimal route between two ports using the Bellman-Ford algorithm.

        This method leverages the Bellman-Ford algorithm to calculate the optimal route
        between the specified start and end ports based on the provided cost, distance,
        and time multipliers. The process includes the retrieval of ports and connections,
        construction of the graph, and computation of the shortest path in terms of
        weight. The method also aggregates the total distance, time, and cost of the
        calculated optimal route.

        :param mode: The transportation mode, either "maritime" or "air".
        :param start_port_name: The name of the starting port.
        :param end_port_name: The name of the destination port.
        :param cost_m: Multiplier for the cost weight in the algorithm.
        :param distance_m: Multiplier for the distance weight in the algorithm.
        :param time_m: Multiplier for the time weight in the algorithm.
        :return: A tuple containing the optimal route as a list of port names,
                 total distance in kilometers, total time in hours, and total
                 cost in USD.
        """
        try:
            ports = []
            connections = []

            if mode == "maritime":
                ports = await self.ports_repository.get_all_maritime_ports()
                connections = await self.connections_repository.get_all_maritime_connections()
            elif mode == "air":
                ports = await self.ports_repository.get_all_air_ports()
                connections = await self.connections_repository.get_all_air_connections()
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve ports and connections: {e}.")

        try:
            bellman_ford_service = BellmanFordAlgorithmService(cost_m, distance_m, time_m)
            bellman_ford_service.build_graph(ports, connections)
            total_weight, optimal_route = bellman_ford_service.compute_algorithm(start_port_name, end_port_name)

            connections_list = []

            for i in range(len(optimal_route)):
                if i == len(optimal_route) - 1:
                    break

                port_i = optimal_route[i]
                port_j = optimal_route[i + 1]
                connection = await self.connections_repository.get_connection_by_origin_and_destination_name(port_i,
                                                                                                             port_j)
                connections_list.append(connection)

            total_distance: float = 0
            total_time: float = 0
            total_cost: float = 0

            for conn in connections_list:
                total_distance += conn.distance_km
                total_time += conn.time_hours
                total_cost += conn.cost_usd

        except Exception as e:
            raise Exception(f"Error trying to compute optimal route: {e}.")

        origin_port = await self.ports_repository.get_port_by_name(start_port_name)
        destination_port = await self.ports_repository.get_port_by_name(end_port_name)

        optimal_route_obj = self.optimal_route_service.register_optimal_route(
            origin_port_id=origin_port.id,
            origin_port_name=origin_port.name,
            destination_port_id=destination_port.id,
            destination_port_name=destination_port.name,
            route_mode=mode,
            algorithm_used="Bellman-Ford",
            total_cost=total_cost,
            total_distance=total_distance,
            total_time=total_time,
            visited_ports=optimal_route
        )

        await self.optimal_route_repository.create(optimal_route_obj)

        return optimal_route, total_distance, total_time, total_cost

    async def build_optimal_route_with_dijkstra(self, start_port_name: str, end_port_name: str, mode: str):
        """
        Builds the optimal route using the Dijkstra algorithm for a given start and end port
        based on the selected transportation mode.

        This coroutine retrieves the necessary ports and connections data, constructs a graph,
        and computes the optimal route using the Dijkstra algorithm. The resulting route
        includes information about total time, cost, and distance. The processed route is
        then registered and stored in the repository.

        :param start_port_name: Name of the starting port.
        :param end_port_name: Name of the destination port.
        :param mode: Transportation mode, either "maritime" or "air".
        :return: A tuple containing the optimal route (list of visited ports)
                 and the total time required (float).
        :rtype: tuple
        :raises ValueError: If there is an error retrieving ports or connections.
        :raises Exception: For errors during the computation of the optimal route.
        """
        try:
            ports = []
            connections = []

            if mode == "maritime":
                ports = await self.ports_repository.get_all_maritime_ports()
                connections = await self.connections_repository.get_all_maritime_connections()
            elif mode == "air":
                ports = await self.ports_repository.get_all_air_ports()
                connections = await self.connections_repository.get_all_air_connections()

        except ValueError as e:
            raise ValueError(f"Error trying to retrieve ports and connections: {e}.")

        try:
            dijkstra_service = DijkstraAlgorithmService()
            dijkstra_service.build_graph(ports, connections)
            total_time, optimal_route = dijkstra_service.compute_algorithm(start_port_name, end_port_name)
        except Exception as e:
            raise Exception(f"Error trying to compute optimal route: {e}.")

        origin_port = await self.ports_repository.get_port_by_name(start_port_name)
        destination_port = await self.ports_repository.get_port_by_name(end_port_name)

        connections_list = []

        for i in range(len(optimal_route)):
            if i == len(optimal_route) - 1:
                break

            port_i = optimal_route[i]
            port_j = optimal_route[i + 1]
            connection = await self.connections_repository.get_connection_by_origin_and_destination_name(port_i, port_j)
            connections_list.append(connection)

        total_distance: float = 0
        total_cost: float = 0

        for conn in connections_list:
            total_distance += conn.distance_km
            total_cost += conn.cost_usd

        optimal_route_obj = self.optimal_route_service.register_optimal_route(
            origin_port_id=origin_port.id,
            origin_port_name=origin_port.name,
            destination_port_id=destination_port.id,
            destination_port_name=destination_port.name,
            route_mode=mode,
            algorithm_used="Dijkstra",
            total_cost=total_cost,
            total_distance=total_distance,
            total_time=total_time,
            visited_ports=optimal_route
        )

        await self.optimal_route_repository.create(optimal_route_obj)

        return optimal_route, total_distance, total_time, total_cost

    async def get_optimal_route_by_id(self, optimal_route_id: str) -> "OptimalRoute | None":
        """
        Retrieve an optimal route by its unique identifier.

        This asynchronous function attempts to fetch a specific optimal route from
        the repository using its ID. If the provided ID is empty or the optimal
        route is not found, an error will be raised indicating the failure
        to retrieve the desired route.

        :param optimal_route_id: The unique identifier of the optimal route
            to retrieve.
        :return: The `OptimalRoute` object if found, otherwise None.
        """
        try:
            if optimal_route_id.strip() == "":
                raise ValueError("To retrieve an optimal route, you must provide a valid optimal route id.")

            optimal_route = await self.optimal_route_repository.get_by_id(optimal_route_id)

            if optimal_route is None:
                raise ValueError("Optimal route not found.")

            return optimal_route
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve optimal route: {e}")
