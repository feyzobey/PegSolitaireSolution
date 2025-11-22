# heuristics.py
from models import apply_move, get_possible_moves


def heuristic_dfs_node_selection(state_tuple, move):
    """
    [cite_start]Method (e): Node-Selection Heuristic for DFS[cite: 47].
    Prioritizes moves that land on or near the center (17).
    Returns a score (lower is better).
    """
    _, _, to = move
    # Preference: Landing on center (17) is best (-10).
    if to == 17:
        return -10
    # Secondary: Landing in the inner cross (neighbors of 17)
    if to in [10, 16, 18, 24]:
        return -5
    return 0


def heuristic_astar_admissible(node):
    """
    [cite_start]Method (f): Admissible heuristic for A* (Version B)[cite: 35, 37].
    h(n) <= actual remaining moves to reach ANY terminal state.

    Logic:
    - If no moves available: h(n) = 0 (Terminal reached).
    - If moves available: We must make at least 1 more move to get stuck.
      So h(n) = 1 is strictly admissible.
    """
    moves = get_possible_moves(node.state)
    if not moves:
        return 0
    return 1
