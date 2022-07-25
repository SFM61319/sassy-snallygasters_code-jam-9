"""A piece class, the parent of all pieces"""
from ..logic.pieces import *
from ..utils.data import PlayerAttributes
from typing import List, Tuple, Optional
import random

# pylint: disable=R0913
# pylint: disable=R0903

# create a class board and subclass it to have two teams


class Board:
    board: List[List[Optional[ChessPiece]]]

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def generate_pieces(self, player1: PlayerAttributes, player2: PlayerAttributes) -> None:
        """
        Generate the pieces for the board.
        :param player1:
        :param player2:
        :return:
        """
        for i in range(8):
            self.board[1][i] = Pawn((1, i), player1.name, player1.color)
            self.board[6][i] = Pawn((6, i), player2.name, player2.color)
        self.board[0][0] = Rook((0, 0), player1.name, player1.color)
        self.board[0][7] = Rook((0, 7), player1.name, player1.color)
        self.board[7][0] = Rook((7, 0), player2.name, player2.color)
        self.board[7][7] = Rook((7, 7), player2.name, player2.color)
        self.board[0][1] = Knight((0, 1), player1.name, player1.color)
        self.board[0][6] = Knight((0, 6), player1.name, player1.color)
        self.board[7][1] = Knight((7, 1), player2.name, player2.color)
        self.board[7][6] = Knight((7, 6), player2.name, player2.color)
        self.board[0][2] = Bishop((0, 2), player1.name, player1.color)
        self.board[0][5] = Bishop((0, 5), player1.name, player1.color)
        self.board[7][2] = Bishop((7, 2), player2.name, player2.color)
        self.board[7][5] = Bishop((7, 5), player2.name, player2.color)
        self.board[0][3] = Queen((0, 3), player1.name, player1.color)
        self.board[7][3] = Queen((7, 3), player2.name, player2.color)
        self.board[0][4] = King((0, 4), player1.name, player1.color)
        self.board[7][4] = King((7, 4), player2.name, player2.color)


class Team(Board):
    """Dummy piece class, to be edited later and as required"""

    def __init__(self, player1: str, player2: str) -> None:
        self.player1 = PlayerAttributes(player1, "white")
        self.player2 = PlayerAttributes(player2, "black")
        super().__init__()
        self.generate_pieces(self.player1, self.player2)
