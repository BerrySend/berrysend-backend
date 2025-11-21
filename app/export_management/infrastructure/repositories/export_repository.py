from sqlalchemy.ext.asyncio import AsyncSession

from app.export_management.domain.models.export import Export
from app.export_management.infrastructure.models.export_model import ExportModel
from app.shared.infrastructure.repositories.base_repository import BaseRepository, TEntity, TModel


class ExportRepository(BaseRepository[Export, ExportModel]):
    def __init__(self, db: AsyncSession):
        """
        Initialize the export repository.

        :param db: The database session.
        """
        super().__init__(db, ExportModel)

    def to_model(self, entity: Export) -> "ExportModel":
        """
        Converts an entity of type `Export` to its equivalent `ExportModel` representation.

        :param entity: The `Export` entity instance to be converted.
        :type entity: Export
        :return: An instance of `ExportModel` containing the corresponding data from the
                 input `Export` entity.
        :rtype: ExportModel
        """
        return ExportModel(
            id=entity.id,
            comercial_description=entity.comercial_description,
            transportation_mode=entity.transportation_mode,
            us_fob=entity.us_fob,
            gross_weight=entity.gross_weight,
            net_weight=entity.net_weight,
            unit=entity.unit,
            quantity=entity.quantity,
            optimized_route_id=entity.optimized_route_id,
            user_id=entity.user_id
        )

    def to_entity(self, model: ExportModel) -> "Export":
        """
        Converts an instance of ExportModel to an instance of Export class.

        This method takes an `ExportModel` object as input and maps its attributes
        to an `Export` object, ensuring that all corresponding fields
        are transferred correctly.

        :param model: The `ExportModel` instance to be converted.
        :type model: ExportModel
        :return: An instance of the `Export` class created using the data from the
            given `ExportModel` instance.
        :rtype: Export
        """
        return Export(
            id=model.id,
            comercial_description=model.comercial_description,
            transportation_mode=model.transportation_mode,
            us_fob=model.us_fob,
            gross_weight=model.gross_weight,
            net_weight=model.net_weight,
            unit=model.unit,
            quantity=model.quantity,
            optimized_route_id=model.optimized_route_id,
            user_id=model.user_id
        )