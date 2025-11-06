"""
Main initialization for the API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.route_planning.application.port_application_service import PortApplicationService
from app.shared.infrastructure.persistence.database import Database, Base
from app.config import settings
from app.route_planning.interfaces.controllers.ports_router import router as ports_router

# Import all the ORM models here BEFORE creating tables
# This ensures SQLAlchemy knows about all models when creating the schema
from app.route_planning.infrastructure.models.port_model import PortModel

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
    print("Database connection established...")

    # Seed the CSV files into the database
    async with db_instance.SessionLocal() as session:
        port_app_service = PortApplicationService(session)
        try:
            await port_app_service.seed_ports(settings.MARITIME_PORTS_CSV_URL)
            print("Port seeding completed successfully.")
        except Exception as e:
            print(f"WARNING: Port seeding failed with error: {str(e)}")
            print("The application will continue without seeded ports.")

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

@app.get("/health")
async def health_check():
    """Check if the database and tables are ready"""
    try:
        async with db_instance.SessionLocal() as session:
            # Try a simple query
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Include the routers for all the endpoints
app.include_router(ports_router)