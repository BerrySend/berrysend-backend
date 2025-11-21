from app.route_optimization.domain.models.optimal_route import OptimalRoute
from app.route_optimization.interfaces.schemas.responses.optimized_route_response import OptimizedRouteResponse


def assemble_optimized_route_response_from_entity(optimized_route_entity: OptimalRoute) -> "OptimizedRouteResponse":
    """
    Assembles an optimized route response object from a given optimized route entity. This helper function
    takes an `OptimalRoute` entity object and constructs an `OptimizedRouteResponse` by transferring relevant
    attributes from the source to the response object.

    The function ensures consistency when translating domain entities to response objects, making it
    useful in contexts where the response needs to be passed outward through APIs or services.

    :param optimized_route_entity: An instance of `OptimalRoute` containing details about the optimized
        route such as visited ports, total distance, time, and costs.
    :returns: An instance of `OptimizedRouteResponse` encapsulating the data from the provided entity.
    """
    return OptimizedRouteResponse(
        id=optimized_route_entity.id,
        visited_ports=optimized_route_entity.visited_ports,
        total_distance=optimized_route_entity.total_distance,
        total_time=optimized_route_entity.total_time,
        total_cost=optimized_route_entity.total_cost,
    )