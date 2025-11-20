from sqlalchemy import Column, String, Float, JSON
from sqlalchemy.orm import Mapped

from app.shared.infrastructure.models.base_model import BaseModelORM


class OptimalRouteModel(BaseModelORM):
    __tablename__ = "optimal_routes"

    origin_port_id: Mapped[str] = Column(String(255), nullable=False)
    origin_port_name: Mapped[str] = Column(String(255), nullable=False)
    destination_port_id: Mapped[str] = Column(String(255), nullable=False)
    destination_port_name: Mapped[str] = Column(String(255), nullable=False)
    route_mode: Mapped[str] = Column(String(255), nullable=False)
    total_distance: Mapped[float] = Column(Float, nullable=False)
    total_time: Mapped[float] = Column(Float, nullable=False)
    total_cost: Mapped[float] = Column(Float, nullable=False)
    visited_ports = Column(JSON, nullable=False)