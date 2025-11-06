"""
Database initialization and connection management for the BerrySend API.
"""
from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# Database base URL for connection
DATABASE_URL: str = str(settings.database_url())

# Base variable for SQLAlchemy
Base = declarative_base()

class Database:
    """
    Handles the database connection and automatic creation of it.

    """
    def __init__(self):
        """
        Initialize the database connection.

        """
        self.db_name = str(settings.MYSQL_DB)
        self.engine = None
        self.SessionLocal = None
        self.session = None

    def create_database_if_not_exists(self):
        """
        Creates the database if it doesn't exist.
        """
        try:
            engine_tmp = create_engine(DATABASE_URL.replace("+aiomysql", ""), echo=False)
            with engine_tmp.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{self.db_name}`"))
                print(f"The database '{self.db_name}' has been created or checked...")
            engine_tmp.dispose()
        except Exception as e:
            print(f"Error trying to create the database '{self.db_name}': {e}")

    def connect(self):
        """
        Connects to the database and creates the database connection.

        """
        self.create_database_if_not_exists()
        self.engine = create_async_engine(DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker( # type: ignore[arg-type]
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
        print(f"Connected to the database: '{self.db_name}'.")

    async def __aenter__(self):
        """
        Enters the context manager.

        """
        if not self.engine:
            await self.connect()
        self.session = self.SessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.
        Args:
            exc_type: The exception type.
            exc_value: The exception value.
            traceback: The exception traceback.
        """
        await self.session.close()

    async def shutdown(self):
        """
        When the application is shutting down, close the database connection.
        """
        await self.engine.dispose()