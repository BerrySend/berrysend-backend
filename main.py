"""
Main initialization for the API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.port_management.application.port_application_service import PortApplicationService
from app.port_management.application.port_connection_application_service import PortConnectionApplicationService

from app.shared.infrastructure.persistence.database import Database, create_tables
from app.config import settings
from app.port_management.interfaces.controllers.ports_router import router as ports_router
from app.port_management.interfaces.controllers.port_connections_router import router as connections_router
from app.iam.interfaces.controllers.auth_controller import auth_router
from app.route_optimization.interfaces.controllers.optimized_routes_router import router as routes_router
from app.route_optimization.interfaces.controllers.algorithms_router import algorithms_router
from app.export_management.interfaces.controllers.exports_router import router as exports_router

# Import all the ORM models here BEFORE creating tables
# This ensures SQLAlchemy knows about all models when creating the schema
from app.port_management.infrastructure.models.port_model import PortModel
from app.iam.infrastructure.models.user_model import UserModel
from app.port_management.infrastructure.models.port_connection_model import PortConnectionModel

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

    # Create all tables if they don't exist
    await create_tables()
    print("Database tables ready...")

    # Seed the CSV files into the database
    async with db_instance.SessionLocal() as session:
        port_app_service = PortApplicationService(session)
        connection_app_service = PortConnectionApplicationService(session)
        try:
            maritime_ports_url = settings.MARITIME_PORTS_CSV_URL
            await port_app_service.seed_ports(maritime_ports_url)
            print(f"Trying to seed maritime ports from url: {maritime_ports_url}.")

            air_ports_url = settings.AIR_PORTS_CSV_URL
            await port_app_service.seed_ports(air_ports_url)
            print(f"Trying to seed air ports from url: {air_ports_url}.")

            maritime_connections_url = settings.MARITIME_CONNECTIONS_CSV_URL
            await connection_app_service.seed_connections(maritime_connections_url)
            print(f"Trying to seed maritime connections from url: {maritime_connections_url}.")

            air_connections_url = settings.AIR_CONNECTIONS_CSV_URL
            await connection_app_service.seed_connections(air_connections_url)
            print(f"Trying to seed air connections from url: {air_connections_url}.")

            print("Port seeding completed successfully.")
        except Exception as e:
            print(f"WARNING: Seeding failed with error: {str(e)}")
            print("The application will continue without seeding.")

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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React default
        "http://localhost:5173",      # Vite default
        "http://localhost:4200",      # Angular default
        "http://localhost:8080",      # Vue default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:8080",
        # Agregar aquí la URL de producción del frontend cuando esté desplegado
    ],
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, PATCH, OPTIONS
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)

@app.get("/health")
async def health_check():
    """Check if the database and tables are ready"""
    try:
        async with db_instance.SessionLocal() as session:
            await session.execute(text("SELECT 1"))

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "healthy", "database": "connected"}
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        )

# Include the routers for all the endpoints
app.include_router(auth_router)
app.include_router(ports_router)
app.include_router(connections_router)
app.include_router(routes_router)
app.include_router(algorithms_router)
app.include_router(exports_router)