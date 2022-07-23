"""Importing Essential Libraries"""
import random

import chess


def initial_pos() -> str:
    """Function to Generate Random Starting Positions of the Game."""
    pieces = ["p", "n", "b", "r", "q"]
    white = ""
    black = ""
    for x in range(0, 34):
        if x == 13:
            white += "K"
        elif x == 8:
            white += "/"
        elif x <= 16:
            white += random.choice(pieces).upper()
        elif x == 25:
            black += "/"
        elif x == 21:
            black += "K"
        else:
            black += random.choice(pieces)
    return str(f"{black}/8/8/8/8/{white} w KQkq - 0 1")


board = chess.Board(initial_pos())
print(board)
