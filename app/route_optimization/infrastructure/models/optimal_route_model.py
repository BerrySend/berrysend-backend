from sqlalchemy import Column, String, Float, JSON, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.shared.infrastructure.models.base_model import BaseModelORM


class OptimalRouteModel(BaseModelORM):
    """
    Represents the data model for optimal routes in a logistics or transportation system.

    This class is designed to store and retrieve data regarding optimal routes between
    ports, including details about origin and destination ports, route metrics such
    as distance, time, and cost, as well as the sequence of visited ports. It is used
    with an ORM (Object-Relational Mapping) for database interaction.

    :ivar origin_port_id: The unique identifier for the origin port.
    :type origin_port_id: str
    :ivar origin_port_name: The name of the origin port.
    :type origin_port_name: str
    :ivar destination_port_id: The unique identifier for the destination port.
    :type destination_port_id: str
    :ivar destination_port_name: The name of the destination port.
    :type destination_port_name: str
    :ivar route_mode: The mode of transportation used for the route (e.g., maritime, air).
    :type route_mode: str
    :ivar total_distance: The total distance of the route in kilometers.
    :type total_distance: float
    :ivar total_time: The total time required to travel the route, in hours.
    :type total_time: float
    :ivar total_cost: The total transportation cost for the route in currency units.
    :type total_cost: float
    :ivar visited_ports: A list of port names visited during the route.
    """
    __tablename__ = "optimal_routes"

    origin_port_id: Mapped[str] = Column(String(255), ForeignKey("ports.id"))
    origin_port_name: Mapped[str] = Column(String(255), nullable=False)
    destination_port_id: Mapped[str] = Column(String(255), ForeignKey("ports.id"))
    destination_port_name: Mapped[str] = Column(String(255), nullable=False)
    algorithm_used: Mapped[str] = Column(String(255), nullable=False)
    route_mode: Mapped[str] = Column(String(255), nullable=False)
    total_distance: Mapped[float] = Column(Float, nullable=False)
    total_time: Mapped[float] = Column(Float, nullable=False)
    total_cost: Mapped[float] = Column(Float, nullable=False)
    visited_ports = Column(JSON, nullable=False)

    # Relationships
    origin_port = relationship("PortModel", foreign_keys=[origin_port_id])
    destination_port = relationship("PortModel", foreign_keys=[destination_port_id])