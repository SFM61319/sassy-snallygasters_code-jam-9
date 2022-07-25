"""A piece class, the parent of all pieces"""


import typing

from wild_chess.logic import pieces
from wild_chess.utils import data


# Create a class board and subclass it to have two teams
class Board:
    """A chess board."""

    board: list[list[typing.Optional[pieces.ChessPiece]]]

    def __init__(self) -> None:
        self.board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]

    # TODO: Refactor this method
    def generate_pieces(self, player1: data.PlayerAttributes, player2: data.PlayerAttributes) -> None:
        """
        Generate the pieces for the board.

        :param player1:
        :param player2:
        :return:
        """
        for i in range(8):
            self.board[1][i] = pieces.Pawn((1, i), player1.name, player1.color)
            self.board[6][i] = pieces.Pawn((6, i), player2.name, player2.color)

        self.board[0][0] = pieces.Rook((0, 0), player1.name, player1.color)
        self.board[0][7] = pieces.Rook((0, 7), player1.name, player1.color)
        self.board[7][0] = pieces.Rook((7, 0), player2.name, player2.color)
        self.board[7][7] = pieces.Rook((7, 7), player2.name, player2.color)
        self.board[0][1] = pieces.Knight((0, 1), player1.name, player1.color)
        self.board[0][6] = pieces.Knight((0, 6), player1.name, player1.color)
        self.board[7][1] = pieces.Knight((7, 1), player2.name, player2.color)
        self.board[7][6] = pieces.Knight((7, 6), player2.name, player2.color)
        self.board[0][2] = pieces.Bishop((0, 2), player1.name, player1.color)
        self.board[0][5] = pieces.Bishop((0, 5), player1.name, player1.color)
        self.board[7][2] = pieces.Bishop((7, 2), player2.name, player2.color)
        self.board[7][5] = pieces.Bishop((7, 5), player2.name, player2.color)
        self.board[0][3] = pieces.Queen((0, 3), player1.name, player1.color)
        self.board[7][3] = pieces.Queen((7, 3), player2.name, player2.color)
        self.board[0][4] = pieces.King((0, 4), player1.name, player1.color)
        self.board[7][4] = pieces.King((7, 4), player2.name, player2.color)


# TODO: Refactor this class
class Team(Board):
    """Dummy piece class, to be edited later and as required"""

    def __init__(self, player1: str, player2: str) -> None:
        self.player1 = data.PlayerAttributes(player1, "white")
        self.player2 = data.PlayerAttributes(player2, "black")
        super().__init__()
        self.generate_pieces(self.player1, self.player2)
