# models.py
from constants import MOVES_MAP

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state          # Tuple representing the board
        self.parent = parent        # Parent Node
        self.action = action        # (from, over, to) move that created this node
        self.cost = cost            # g(n): number of moves made so far
        self.heuristic = 0          # h(n)
        
    def __lt__(self, other):
        # Priority queue comparison for A* / UCS based on f(n)
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def get_peg_count(self):
        return sum(self.state)

def get_possible_moves(state_tuple):
    """
    [cite_start]Returns valid moves sorted by Canonical Child Order[cite: 65].
    Order: Ascending by (removed, from, to).
    """
    moves = []
    for i in range(1, 34):
        if state_tuple[i] == 1: # If there is a peg
            if i in MOVES_MAP:
                for over, to in MOVES_MAP[i]:
                    # Check: 'over' has peg AND 'to' is empty
                    if state_tuple[over] == 1 and state_tuple[to] == 0:
                        moves.append((i, over, to))
    
    # [cite_start]CRITICAL: Canonical Sort [cite: 65]
    # Sort key: (over/removed, from, to)
    moves.sort(key=lambda x: (x[1], x[0], x[2]))
    return moves

def apply_move(state_tuple, move):
    """Returns new state tuple after move (from, over, to)"""
    f, o, t = move
    new_state = list(state_tuple)
    new_state[f] = 0
    new_state[o] = 0
    new_state[t] = 1
    return tuple(new_state)