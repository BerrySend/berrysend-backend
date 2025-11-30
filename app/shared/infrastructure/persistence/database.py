"""
Database initialization and connection management for the BerrySend API.
"""
from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings
from app.shared.infrastructure.models.base_model import BaseModelORM

# Database base URL for connection
DATABASE_URL: str = str(settings.database_url())

# Base variable for SQLAlchemy
Base = declarative_base()


async def create_tables():
    """
    Creates all tables defined in the models if they don't exist.
    
    This function imports all ORM models to ensure they are registered with
    BaseModelORM.metadata, then creates all tables using SQLAlchemy's create_all method.
    It uses a synchronous engine for table creation as create_all works better
    with synchronous engines.
    
    :exception Exception: If there is an error creating the tables.
    """
    try:
        # Import all models to ensure they are registered with BaseModelORM.metadata
        from app.port_management.infrastructure.models.port_model import PortModel
        from app.iam.infrastructure.models.user_model import UserModel
        from app.port_management.infrastructure.models.port_connection_model import PortConnectionModel

        # Create a synchronous engine for table creation
        # (create_all works better with sync engines)
        sync_url = DATABASE_URL.replace("+aiomysql", "").replace("mysql+aiomysql://", "mysql+pymysql://")
        sync_engine = create_engine(sync_url, echo=False)

        # Create all tables
        BaseModelORM.metadata.create_all(bind=sync_engine)
        sync_engine.dispose()

        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error trying to create tables: {e}")
        raise


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
        Checks if the database exists and creates it if it doesn't.
        
        This method connects to the MySQL server without specifying a database,
        checks if the target database exists by querying information_schema,
        and creates it if it doesn't exist.
        
        :exception Exception: If there is an error checking or creating the database.
        """
        try:
            # Build connection URL without the database name to connect to MySQL server
            # Remove the database name from the URL
            url_without_db = DATABASE_URL.replace("+aiomysql", "").rsplit("/", 1)[0]
            
            # Connect to MySQL server (without specifying a database)
            engine_tmp = create_engine(url_without_db, echo=False)
            
            with engine_tmp.connect() as conn:
                # Check if the database exists
                result = conn.execute(
                    text(
                        "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = :db_name"
                    ),
                    {"db_name": self.db_name}
                )
                db_exists = result.fetchone() is not None
                
                if db_exists:
                    print(f"The database '{self.db_name}' already exists.")
                else:
                    # Create the database if it doesn't exist
                    conn.execute(text(f"CREATE DATABASE `{self.db_name}`"))
                    conn.commit()
                    print(f"The database '{self.db_name}' has been created successfully.")
            
            engine_tmp.dispose()
        except Exception as e:
            print(f"Error trying to create the database '{self.db_name}': {e}")
            raise

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