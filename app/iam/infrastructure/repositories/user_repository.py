from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.iam.domain.models.user import User
from app.iam.infrastructure.models.user_model import UserModel
from app.shared.infrastructure.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User, UserModel]):
    def __init__(self, db: AsyncSession):
        """
        Initialize the user repository.

        :param db: The database session.
        """
        super().__init__(db, UserModel)

    def to_model(self, entity: User) -> "UserModel":
        """
        Converts a user entity into a user model.

        :param entity: The user entity to transform.
        :return: The corresponding user model.
        """
        return UserModel(
            id=entity.id,
            full_name=entity.full_name,
            email=entity.email,
            hashed_password=entity.hashed_password,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def to_entity(self, model: UserModel) -> "User":
        """
        Converts a user model into a user entity.

        :param model: The user model to transform.
        :return: The corresponding user entity.
        """
        return User(
            id=model.id,
            full_name=model.full_name,
            email=model.email,
            hashed_password=model.hashed_password,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_by_email(self, email: str) -> "User | None":
        """
        Fetches a user by its email.

        :param email: The email of the user.
        :return: The user with the given email, if found, otherwise None.
        """
        result = await self._db.execute(
            select(self._model).where(self._model.email == email)
        )
        model = result.scalar_one_or_none()
        return self.to_entity(model) if model else None

    async def exists_by_email(self, email: str) -> bool:
        """
        Checks if a user with the given email exists in the database.

        :param email: The email of the user.
        :return: True if the user exists with the given email, False otherwise.
        """
        query = select(exists().where(self._model.email == email))
        result = await self._db.execute(query)
        return result.scalar()