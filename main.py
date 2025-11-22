# main.py
import argparse
import sys
import time
from search import PegSolitaireSolver


def print_board_ascii(state_tuple):
    # Print board logic based on 7x7 grid
    grid_map = [
        [0, 0, 1, 2, 3, 0, 0],
        [0, 0, 4, 5, 6, 0, 0],
        [7, 8, 9, 10, 11, 12, 13],
        [14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25, 26, 27],
        [0, 0, 28, 29, 30, 0, 0],
        [0, 0, 31, 32, 33, 0, 0],
    ]
    for r in range(7):
        row = ""
        for c in range(7):
            idx = grid_map[r][c]
            if idx == 0:
                row += " "
            else:
                row += "X" if state_tuple[idx] == 1 else "O"
        print(row)
    print("-" * 10)


def main():
    parser = argparse.ArgumentParser(description="Peg Solitaire Solver")
    parser.add_argument("variant", choices=["A", "B"], help="Variant A (Classic) or B (Max Peg)")
    parser.add_argument("method", choices=["BFS", "DFS", "IDDFS", "DFS-R", "DFS-H", "A*", "UCS"], help="Search Method")
    parser.add_argument("time_limit", type=int, help="Time limit in seconds")

    args = parser.parse_args()

    print(f"Starting Solver: Variant={args.variant}, Method={args.method}, Time={args.time_limit}s")

    solver = PegSolitaireSolver(args.variant, args.method, args.time_limit)
    status, node = solver.solve()

    # Outputs required by PDF
    elapsed = time.time() - solver.start_time

    print(f"\n--- REPORT ---")
    print(f"Variant: {args.variant}, Method: {args.method}, Time Limit: {args.time_limit}")

    if status == "TIMEOUT":
        print("Goal not reached - Time Limit.")

    if args.variant == "A":
        if status == "SUCCESS":
            print("Goal reached: one peg in the center (31 moves).")
        else:
            rem = node.get_peg_count() if node else "N/A"
            print(f"Goal not reached - best attempt ended with {rem} pegs remaining.")
    else:  # Variant B
        rem = node.get_peg_count() if node else "N/A"
        print(f"Best terminal state found with {rem} remaining pegs.")

    print(f"Elapsed Time: {elapsed:.4f}s")
    print(f"Nodes Expanded: {solver.nodes_expanded}")
    print(f"Peak Memory: {solver.max_frontier}")

    if node:
        # Reconstruct path
        path = []
        curr = node
        while curr.parent:
            path.append((curr.action, curr.state))
            curr = curr.parent
        path.append((None, curr.state))
        path.reverse()

        print("\nMove Sequence:")
        for action, state in path:
            if action:
                print(f"Move: {action[0]}-{action[1]}-{action[2]}")  # from-over-to format
            else:
                print("Initial State")
            print_board_ascii(state)


if __name__ == "__main__":
    main()
