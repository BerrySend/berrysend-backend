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
            # Always use multimodal to support intermodal connections
            # This allows routes between maritime and air ports
            maritime_ports = await self.ports_repository.get_all_maritime_ports()
            air_ports = await self.ports_repository.get_all_air_ports()
            ports = maritime_ports + air_ports
            
            maritime_connections = await self.connections_repository.get_all_maritime_connections()
            air_connections = await self.connections_repository.get_all_air_connections()
            connections = maritime_connections + air_connections
            
            # Keep mode for record-keeping purposes
            actual_mode = mode if mode in ["maritime", "air", "multimodal"] else "multimodal"
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
                # Validate BF parameters - use 'if is None' to allow 0 values
                cost_m = cost_m if cost_m is not None else 1.0
                distance_m = distance_m if distance_m is not None else 1.0
                time_m = time_m if time_m is not None else 1.0

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
        # (3) Get port entities to retrieve their names for the algorithm
        #     Accept both IDs and names - try ID first, then name
        # ---------------------------------------------------------
        # Try as ID first
        start_port = await self.ports_repository.get_by_id(start_port_name)
        if not start_port:
            # Try as name if ID lookup failed
            start_port = await self.ports_repository.get_port_by_name(start_port_name)
        
        end_port = await self.ports_repository.get_by_id(end_port_name)
        if not end_port:
            # Try as name if ID lookup failed
            end_port = await self.ports_repository.get_port_by_name(end_port_name)
        
        if not start_port:
            raise ValueError(f"Start port '{start_port_name}' not found")
        if not end_port:
            raise ValueError(f"End port '{end_port_name}' not found")

        # ---------------------------------------------------------
        # (4) Execute selected algorithm
        # ---------------------------------------------------------
        try:
            total_weight, optimal_route = service.compute_algorithm(
                start_port.name,
                end_port.name,
                export_weight
            )
            
            if total_weight == float('inf'):
                raise ValueError(f"No route found between {start_port.name} and {end_port.name}. Ports may not be connected or capacity insufficient.")
            
        except ValueError as e:
            # Re-raise ValueError as-is (will be caught by HTTPException handler in controller)
            raise
        except Exception as e:
            raise ValueError(f"Error trying to compute optimal route: {e}")

        # ---------------------------------------------------------
        # (5) Build connection list (route edges)
        # ---------------------------------------------------------
        connections_list = []
        for i in range(len(optimal_route) - 1):
            origin = optimal_route[i]
            dest = optimal_route[i + 1]

            connection = await self.connections_repository.get_connection_by_origin_and_destination_name(
                origin, dest
            )
            if connection:
                connections_list.append(connection)
            else:
                print(f"WARNING: Connection not found between {origin} -> {dest}")

        # ---------------------------------------------------------
        # (5) Aggregate totals depending on the algorithm
        # ---------------------------------------------------------
        if len(connections_list) == 0:
            raise ValueError(f"No connections found for route: {optimal_route}")
        
        # Calculate REAL totals from connections (not from algorithm weight)
        total_distance = sum(conn.distance_km for conn in connections_list)
        total_time = sum(conn.time_hours for conn in connections_list)
        total_cost = sum(conn.cost_usd for conn in connections_list)

        # NOTE: total_weight from algorithms is their optimization metric,
        # but we always return REAL distance/time/cost values to the user

        # ---------------------------------------------------------
        # (6) Register route
        # ---------------------------------------------------------
        optimal_route_obj = self.optimal_route_service.register_optimal_route(
            origin_port_id=start_port.id,
            origin_port_name=start_port.name,
            destination_port_id=end_port.id,
            destination_port_name=end_port.name,
            route_mode=actual_mode,
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
        return optimal_route_obj

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
