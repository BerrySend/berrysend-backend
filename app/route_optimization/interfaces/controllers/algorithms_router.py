from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

# Router para algoritmos disponibles
algorithms_router = APIRouter(prefix="/api/v1/algorithms", tags=["Algorithms"])


@algorithms_router.get("/", status_code=status.HTTP_200_OK)
async def get_algorithms():
    """
    Get list of available route optimization algorithms.
    
    Returns:
        List of algorithms with their properties
    """
    algorithms = [
        {
            "id": "dijkstra",
            "name": "Dijkstra",
            "description": "Encuentra la ruta más corta considerando un solo criterio (tiempo por defecto)",
            "requires_parameters": False,
            "complexity": "O((V + E) log V)",
            "best_for": "Rutas más rápidas o más cortas sin ponderación múltiple"
        },
        {
            "id": "astar",
            "name": "A* (A-Star)",
            "description": "Algoritmo heurístico que optimiza la búsqueda usando distancia euclidiana como guía",
            "requires_parameters": False,
            "complexity": "O(b^d) - depende de la heurística",
            "best_for": "Rutas óptimas con mejora de rendimiento mediante heurística"
        },
        {
            "id": "bellman-ford",
            "name": "Bellman-Ford",
            "description": "Permite ponderar múltiples criterios (costo, distancia, tiempo) con multiplicadores personalizados",
            "requires_parameters": True,
            "parameters": {
                "cost_multiplier": {
                    "type": "float",
                    "min": 0,
                    "max": 1,
                    "default": 0.33,
                    "description": "Peso del costo en la decisión"
                },
                "distance_multiplier": {
                    "type": "float",
                    "min": 0,
                    "max": 1,
                    "default": 0.33,
                    "description": "Peso de la distancia en la decisión"
                },
                "time_multiplier": {
                    "type": "float",
                    "min": 0,
                    "max": 1,
                    "default": 0.34,
                    "description": "Peso del tiempo en la decisión"
                }
            },
            "constraint": "La suma de los multiplicadores debe ser 1.0",
            "complexity": "O(V * E)",
            "best_for": "Rutas balanceadas considerando múltiples factores"
        }
    ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=algorithms
    )
