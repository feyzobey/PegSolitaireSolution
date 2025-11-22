# search.py
import time
import random
import heapq
from collections import deque
from constants import INITIAL_BOARD
from models import Node, get_possible_moves, apply_move
from heuristics import heuristic_dfs_node_selection, heuristic_astar_admissible

class PegSolitaireSolver:
    def __init__(self, variant, method, time_limit):
        self.variant = variant
        self.method = method
        self.time_limit = time_limit
        self.start_time = 0
        self.nodes_expanded = 0
        self.max_frontier = 0
        self.root = Node(tuple(INITIAL_BOARD))
        self.best_terminal_node = None

    def check_limits(self):
        if time.time() - self.start_time > self.time_limit:
            return "TIMEOUT"
        return "OK"

    def solve(self):
        self.start_time = time.time()
        if self.method == 'IDDFS': return self.run_iddfs()
        if self.method in ['A*', 'UCS']: return self.run_informed_search()
        return self.run_uninformed_search() # BFS, DFS variants

    def run_uninformed_search(self):
        structure = 'STACK' if 'DFS' in self.method else 'QUEUE'
        frontier = deque([self.root])
        visited = {self.root.state} # Duplicate detection

        while frontier:
            if len(frontier) > self.max_frontier: self.max_frontier = len(frontier)
            if self.check_limits() == "TIMEOUT": return ("TIMEOUT", self.best_terminal_node)

            node = frontier.pop() if structure == 'STACK' else frontier.popleft()
            self.nodes_expanded += 1

            # Version A Goal Check
            if self.variant == 'A' and node.get_peg_count() == 1 and node.state[17] == 1:
                return ("SUCCESS", node)

            children_moves = get_possible_moves(node.state)
            
            # Version B Tracking
            if self.variant == 'B' and not children_moves:
                if self.best_terminal_node is None or node.cost < self.best_terminal_node.cost:
                    self.best_terminal_node = node

            # Handling Orderings
            if self.method == 'DFS-R':
                random.shuffle(children_moves)
            elif self.method == 'DFS-H':
                # Sort so best heuristic is popped first (LIFO) -> Push Worst..Best
                children_moves.sort(key=lambda m: heuristic_dfs_node_selection(node.state, m), reverse=True)
            
            # Push Logic (Reverse for Stack to preserve Canonical order on Pop)
            moves_to_push = children_moves
            if structure == 'STACK' and self.method not in ['DFS-R', 'DFS-H']:
                moves_to_push = reversed(children_moves)

            for move in moves_to_push:
                new_state = apply_move(node.state, move)
                if new_state not in visited:
                    visited.add(new_state)
                    frontier.append(Node(new_state, parent=node, action=move, cost=node.cost + 1))

        return ("FAILURE", self.best_terminal_node)

    def run_informed_search(self):
        # A* and UCS (UCS is A* with h=0)
        frontier = []
        counter = 0
        self.root.heuristic = heuristic_astar_admissible(self.root) if self.method == 'A*' else 0
        heapq.heappush(frontier, (self.root.cost + self.root.heuristic, counter, self.root))
        visited = {self.root.state: 0} # Store min cost to state

        while frontier:
            if len(frontier) > self.max_frontier: self.max_frontier = len(frontier)
            if self.check_limits() == "TIMEOUT": return ("TIMEOUT", self.best_terminal_node)

            _, _, node = heapq.heappop(frontier)
            self.nodes_expanded += 1

            moves = get_possible_moves(node.state)
            
            if self.variant == 'B' and not moves:
                # Optimized for B: First terminal found in A* is optimal if h is admissible
                if self.best_terminal_node is None or node.cost < self.best_terminal_node.cost:
                    self.best_terminal_node = node
                    return ("SUCCESS", node)

            for move in moves:
                new_state = apply_move(node.state, move)
                new_cost = node.cost + 1
                if new_state not in visited or new_cost < visited[new_state]:
                    visited[new_state] = new_cost
                    child = Node(new_state, parent=node, action=move, cost=new_cost)
                    child.heuristic = heuristic_astar_admissible(child) if self.method == 'A*' else 0
                    counter += 1
                    heapq.heappush(frontier, (child.cost + child.heuristic, counter, child))
        
        return ("FAILURE", self.best_terminal_node)

    def run_iddfs(self):
        depth = 0
        while True:
            if self.check_limits() == "TIMEOUT": return ("TIMEOUT", None)
            res = self.dls(self.root, depth, {self.root.state})
            if res != "CUTOFF": return res
            depth += 1
            if depth > 32: return ("FAILURE", None)

    def dls(self, node, limit, path):
        if self.variant == 'A' and node.get_peg_count() == 1 and node.state[17] == 1:
            return ("SUCCESS", node)
        if node.cost >= limit: return "CUTOFF"

        self.nodes_expanded += 1
        moves = get_possible_moves(node.state)
        
        for move in reversed(moves): # Reverse for stack behavior
            new_state = apply_move(node.state, move)
            if new_state not in path:
                path.add(new_state)
                res = self.dls(Node(new_state, parent=node, action=move, cost=node.cost+1), limit, path)
                if res != "CUTOFF": return res
                path.remove(new_state)
        return "CUTOFF"