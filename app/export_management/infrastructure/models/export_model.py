from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.shared.infrastructure.models.base_model import BaseModelORM


class ExportModel(BaseModelORM):
    """
    Represents the Export model for managing export records in the database.

    This class defines the structure of an export record, including various details
    such as the commercial description, transportation mode, and multiple
    quantitative attributes related to the exports. It is intended to work as part
    of the ORM layer for database operations.

    :ivar comercial_description: The commercial description of the export.
    :type comercial_description: str
    :ivar transportation_mode: The mode of transportation used for the export.
    :type transportation_mode: str
    :ivar us_fob: The Free on Board (FOB) value of the export in USD.
    :type us_fob: float
    :ivar gross_weigh: The gross weight of the exported goods.
    :type gross_weigh: float
    :ivar net_weight: The net weight of the exported goods.
    :type net_weight: float
    :ivar unit: The unit of measurement for the exported goods.
    :type unit: str
    :ivar quantity: The quantity of the exported goods.
    :type quantity: float
    :ivar optimized_route_id: Identifier for the optimized route used for the export.
    :type optimized_route_id: str
    """
    __tablename__ = "exports"

    comercial_description: Mapped[str] = Column(String(255), nullable=False)
    transportation_mode: Mapped[str] = Column(String(255), nullable=False)
    us_fob: Mapped[float] = Column(Float, nullable=False)
    gross_weigh: Mapped[float] = Column(Float, nullable=False)
    net_weight: Mapped[float] = Column(Float, nullable=False)
    unit: Mapped[str] = Column(String(255), nullable=False)
    quantity: Mapped[float] = Column(Float, nullable=False)
    optimized_route_id: Mapped[str] = Column(String(255), ForeignKey("optimal_routes.id"))
    user_id: Mapped[str] = Column(String(255), ForeignKey("users.id"))

    # Relationships
    optimized_route = relationship("OptimizedRoute", foreign_keys=[optimized_route_id])
    user = relationship("User", foreign_keys=[user_id])