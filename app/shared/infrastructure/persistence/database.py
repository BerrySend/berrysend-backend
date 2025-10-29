"""
Database initialization and connection management for the BerrySend API.
"""
from dotenv import dotenv_values
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Import the .env file for the usage of the variables in a dictionary
config = dotenv_values(".env")

# Assign the .env file variables to local variables
MYSQL_USER = config["MYSQL_USER"]
MYSQL_PASSWORD = config["MYSQL_PASSWORD"]
MYSQL_HOST = config["MYSQL_HOST"]
MYSQL_PORT = config["MYSQL_PORT"]
MYSQL_DB = config["MYSQL_DB"]

# Base URL
BASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"

# Database base URL for connection
DATABASE_URL = f"{BASE_URL}/{MYSQL_DB}"

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
        self.db_name = MYSQL_DB
        self.engine = None
        self.SessionLocal = None
        self.session = None

    def create_database_if_not_exists(self):
        """
        Creates the database if it doesn't exist.

        """
        try:
            engine_tmp = create_engine(BASE_URL)
            with engine_tmp.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{self.db_name}`"))
                print(f"The database '{self.db_name}' has been created or checked...")
        except Exception as e:
            print(f"Error trying to create the database '{self.db_name}': {e}")

    def connect(self):
        """
        Connects to the database and creates the database connection.

        """
        self.create_database_if_not_exists()
        self.engine = create_engine(DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        print(f"Connected to the database: '{self.db_name}'.")

    def __enter__(self):
        """
        Enters the context manager.

        """
        if not self.engine:
            self.connect()
        self.session = self.SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.
        Args:
            exc_type: The exception type.
            exc_value: The exception value.
            traceback: The exception traceback.

        """
        self.session.close()