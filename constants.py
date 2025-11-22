# constants.py

# [cite_start]Board Layout (Indices 1-33) based on Figure 1 in PDF [cite: 7]
# 0 is unused. 1 means peg, 0 means empty.
INITIAL_BOARD = [0] * 34
for i in range(1, 34):
    INITIAL_BOARD[i] = 1
INITIAL_BOARD[17] = 0 # Center starts empty [cite: 5]

def generate_move_table():
    """
    Precomputes valid moves based on Figure 1 numbering.
    Returns a dictionary: moves[from_hole] = [(over_hole, to_hole), ...]
    """
    moves = {}
    # [cite_start]Triples: (from, over, to) based on orthogonal jumps [cite: 5]
    raw_moves = [
        # Row 1
        (1, 2, 3), (1, 4, 9), (2, 5, 10), (3, 2, 1), (3, 6, 11),
        # Row 2
        (4, 5, 6), (4, 9, 16), (5, 10, 17), (6, 5, 4), (6, 11, 18),
        # Row 3
        (7, 8, 9), (7, 14, 21), (8, 9, 10), (8, 15, 22), (9, 4, 1), (9, 8, 7), (9, 10, 11), (9, 16, 23),
        (10, 5, 2), (10, 9, 8), (10, 11, 12), (10, 17, 24),
        (11, 6, 3), (11, 10, 9), (11, 12, 13), (11, 18, 25),
        (12, 11, 10), (12, 19, 26), (13, 12, 11), (13, 20, 27),
        # Row 4
        (14, 15, 16), (15, 16, 17), (16, 9, 4), (16, 15, 14), (16, 17, 18), (16, 23, 28),
        (17, 10, 5), (17, 16, 15), (17, 18, 19), (17, 24, 29),
        (18, 11, 6), (18, 17, 16), (18, 19, 20), (18, 25, 30),
        (19, 18, 17), (20, 19, 18),
        # Row 5
        (21, 14, 7), (21, 22, 23), (22, 15, 8), (22, 23, 24),
        (23, 16, 9), (23, 22, 21), (23, 24, 25), (23, 28, 31),
        (24, 17, 10), (24, 23, 22), (24, 25, 26), (24, 29, 32),
        (25, 18, 11), (25, 24, 23), (25, 26, 27), (25, 30, 33),
        (26, 19, 12), (26, 25, 24), (27, 20, 13), (27, 26, 25),
        # Row 6
        (28, 23, 16), (28, 29, 30), (29, 24, 17), (30, 25, 18), (30, 29, 28),
        # Row 7
        (31, 28, 23), (31, 32, 33), (32, 29, 24), (33, 30, 25), (33, 32, 31)
    ]
    
    for f, o, t in raw_moves:
        if f not in moves: moves[f] = []
        moves[f].append((o, t))
    return moves

MOVES_MAP = generate_move_table()