"""
Main initialization for the API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.shared.infrastructure.persistence.database import Database, Base

# The database global instance
db_instance = Database()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Async method to manage the lifespan of the application.

    Args:
        _app: The FastAPI application.
    """
    print("Starting the application...")
    db_instance.connect()
    Base.metadata.create_all(bind=db_instance.engine)
    print("Database connection established...")
    yield
    print("Closing the application...")

# Creates the FastAPI app
app = FastAPI(
    title="BerrySend Backend",
    description="API to register exports of blue berries anc calculate the shortest route",
    version="1.0.0",
    lifespan=lifespan
)

def get_db():
    """
    Method that gets database instance

    Returns: The database instance
    """
    with db_instance as db:
        yield db