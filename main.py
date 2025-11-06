"""
Main initialization for the API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.route_planning.application.port_application_service import PortApplicationService
from app.shared.infrastructure.persistence.database import Database, Base
from app.config import settings

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

    async with db_instance.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database connection established...")

    # Seed the CSV files into the database
    async with db_instance.SessionLocal() as session:
        port_app_service = PortApplicationService(session)
        await port_app_service.seed_ports(settings.MARITIME_PORTS_CSV_URL)

    try:
        yield
    finally:
        print("Closing the application...")
        if db_instance.engine:
            await db_instance.shutdown()
        print("Database connection closed.")

    print("Closing the application...")

# Creates the FastAPI app
app = FastAPI(
    title="BerrySend Backend",
    description="API to register exports of blue berries anc calculate the shortest route",
    version="1.0.0",
    lifespan=lifespan
)