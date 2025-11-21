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

    async def build_optimal_route(
        self,
        start_port_name: str,
        end_port_name: str,
        mode: str,
        export_weight: float,
        algorithm_name: str,
        cost_m: float | None = None,
        distance_m: float | None = None,
        time_m: float | None = None
    ):
        """
        Builds an optimal route between two ports using a specified algorithm:
        A*, Bellman-Ford, or Dijkstra.

        All previous algorithm-specific functions are unified here.
        Bellman-Ford accepts optional multipliers (cost_m, distance_m, time_m).
        """

        # ---------------------------------------------------------
        # (1) Retrieve ports and connections
        # ---------------------------------------------------------
        try:
            if mode == "maritime":
                ports = await self.ports_repository.get_all_maritime_ports()
                connections = await self.connections_repository.get_all_maritime_connections()
            elif mode == "air":
                ports = await self.ports_repository.get_all_air_ports()
                connections = await self.connections_repository.get_all_air_connections()
            else:
                raise ValueError(f"Invalid mode '{mode}'. Must be 'maritime' or 'air'.")
        except ValueError as e:
            raise ValueError(f"Error trying to retrieve ports and connections: {e}")

        # ---------------------------------------------------------
        # (2) Select algorithm service
        # ---------------------------------------------------------
        algo = algorithm_name.lower()
        try:
            if algo == "astar" or algo == "a*":
                service = AStarAlgorithmService()
                algorithm_used = "AStar"

            elif algo == "bellman-ford" or algo == "bellmanford":
                # Validate BF parameters
                cost_m = cost_m or 1
                distance_m = distance_m or 1
                time_m = time_m or 1

                service = BellmanFordAlgorithmService(cost_m, distance_m, time_m)
                algorithm_used = "Bellman-Ford"

            elif algo == "dijkstra":
                service = DijkstraAlgorithmService()
                algorithm_used = "Dijkstra"

            else:
                raise ValueError(f"Unsupported algorithm '{algorithm_name}'.")
        except Exception as e:
            raise Exception(f"Error initializing algorithm: {e}")

        # Build the graph
        service.build_graph(ports, connections)

        # ---------------------------------------------------------
        # (3) Execute selected algorithm
        # ---------------------------------------------------------
        try:
            total_weight, optimal_route = service.compute_algorithm(
                start_port_name,
                end_port_name,
                export_weight
            )
        except Exception as e:
            raise Exception(f"Error trying to compute optimal route: {e}")

        # ---------------------------------------------------------
        # (4) Build connection list (route edges)
        # ---------------------------------------------------------
        connections_list = []
        for i in range(len(optimal_route) - 1):
            origin = optimal_route[i]
            dest = optimal_route[i + 1]

            connection = await self.connections_repository.get_connection_by_origin_and_destination_name(
                origin, dest
            )
            connections_list.append(connection)

        # ---------------------------------------------------------
        # (5) Aggregate totals depending on the algorithm
        # ---------------------------------------------------------
        total_distance = sum(conn.distance_km for conn in connections_list)
        total_time = sum(conn.time_hours for conn in connections_list)
        total_cost = sum(conn.cost_usd for conn in connections_list)

        # For A* and Dijkstra, the algorithm returns time or distance instead of weight
        if algo == "a*" or algo == "astar":
            # service returned (distance, route)
            total_distance = total_weight

        elif algo == "dijkstra":
            # service returned (time, route)
            total_time = total_weight

        # Bellman-Ford keeps all 3 actual values

        # ---------------------------------------------------------
        # (6) Register route
        # ---------------------------------------------------------
        origin_port = await self.ports_repository.get_port_by_name(start_port_name)
        destination_port = await self.ports_repository.get_port_by_name(end_port_name)

        optimal_route_obj = self.optimal_route_service.register_optimal_route(
            origin_port_id=origin_port.id,
            origin_port_name=origin_port.name,
            destination_port_id=destination_port.id,
            destination_port_name=destination_port.name,
            route_mode=mode,
            algorithm_used=algorithm_used,
            total_cost=total_cost,
            total_distance=total_distance,
            total_time=total_time,
            visited_ports=optimal_route
        )

        await self.optimal_route_repository.create(optimal_route_obj)

        # ---------------------------------------------------------
        # (7) Return
        # ---------------------------------------------------------
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
