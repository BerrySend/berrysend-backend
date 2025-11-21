from sqlalchemy.ext.asyncio import AsyncSession

from app.route_optimization.domain.models.optimal_route import OptimalRoute
from app.route_optimization.infrastructure.models.optimal_route_model import OptimalRouteModel
from app.shared.infrastructure.repositories.base_repository import BaseRepository


class OptimalRouteRepository(BaseRepository[OptimalRoute, OptimalRouteModel]):
    def __init__(self, db: AsyncSession):
        """
        Initialize the optimal route repository.

        :param db: The database session.
        """
        super().__init__(db, OptimalRouteModel)

    def to_model(self, entity: OptimalRoute) -> "OptimalRouteModel":
        """
        Converts an OptimalRoute object to an OptimalRouteModel object.

        This method takes an entity of type OptimalRoute and maps its attributes
        to create and return a new OptimalRouteModel object. Each attribute of
        the provided entity is directly mapped to the respective property of
        OptimalRouteModel to ensure consistency.

        :param entity: The OptimalRoute object that contains the route details
            to be converted to the OptimalRouteModel representation. The entity
            must contain attributes such as `id`, `origin_port_id`,
            `origin_port_name`, `destination_port_id`, `destination_port_name`,
            `route_mode`, `total_cost`, `total_distance`, `total_time`, and
            `visited_ports`.
        :type entity: OptimalRoute

        :return: A new OptimalRouteModel object with values mapped from the
            provided OptimalRoute entity.
        :rtype: OptimalRouteModel
        """
        return OptimalRouteModel(
            id=entity.id,
            origin_port_id=entity.origin_port_id,
            origin_port_name=entity.origin_port_name,
            destination_port_id=entity.destination_port_id,
            destination_port_name=entity.destination_port_name,
            route_mode=entity.route_mode,
            total_cost=entity.total_cost,
            total_distance=entity.total_distance,
            total_time=entity.total_time,
            visited_ports=entity.visited_ports
        )

    def to_entity(self, model: OptimalRouteModel) -> "OptimalRoute":
        """
        Converts an OptimalRouteModel instance to an OptimalRoute entity.

        This method maps the fields of an `OptimalRouteModel` object to
        a newly created `OptimalRoute` instance.

        :param model: The OptimalRouteModel instance to be converted.
        :type model: OptimalRouteModel
        :return: A converted OptimalRoute entity with fields populated from the model.
        :rtype: OptimalRoute
        """
        return OptimalRoute(
            id=model.id,
            origin_port_id=model.origin_port_id,
            origin_port_name=model.origin_port_name,
            destination_port_id=model.destination_port_id,
            destination_port_name=model.destination_port_name,
            route_mode=model.route_mode,
            total_cost=model.total_cost,
            total_distance=model.total_distance,
            total_time=model.total_time,
            visited_ports=model.visited_ports
        )