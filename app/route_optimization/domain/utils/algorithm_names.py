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

def normalize_algorithm(value: str) -> AlgorithmName:
    """
    Converts the given algorithm name into a standardized format. If the provided
    name has a recognized alias, it will be converted to its corresponding canonical
    name. Otherwise, the input value will be used as the algorithm name.

    :param value: The name of the algorithm to normalize.
    :type value: str
    :return: The normalized algorithm name as an instance of ``AlgorithmName``.
    :rtype: AlgorithmName
    """
    value = value.lower()
    if value in ALGORITHM_ALIASES:
        return ALGORITHM_ALIASES[value]
    return AlgorithmName(value)