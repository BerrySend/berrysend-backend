from enum import Enum


class AlgorithmName(str, Enum):
    ASTAR = "a*"
    DIJKSTRA = "dijkstra"
    BELLMAN = "bellmanford"

ALGORITHM_ALIASES = {
    "a*": AlgorithmName.ASTAR,
    "astar": AlgorithmName.ASTAR,
    "a-star": AlgorithmName.ASTAR,
    "bellman": AlgorithmName.BELLMAN,
    "bellmanford": AlgorithmName.BELLMAN,
    "bellman-ford": AlgorithmName.BELLMAN,
}