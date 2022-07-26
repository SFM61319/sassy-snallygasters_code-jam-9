"""A piece class, the parent of all pieces"""


import random
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
        all_special_pieces: list[type[pieces.ChessPiece]] = [
            pieces.Rook,
            pieces.Knight,
            pieces.Bishop,
            pieces.Queen,
            pieces.King,
            pieces.Bishop,
            pieces.Knight,
            pieces.Rook,
        ]
        random.shuffle(all_special_pieces)

        for i in range(8):
            self.board[1][i] = pieces.Pawn((1, i), player1.name, player1.color)
            self.board[6][i] = pieces.Pawn((6, i), player2.name, player2.color)

            random_piece = all_special_pieces.pop()

            self.board[0][i] = random_piece((0, i), player1.name, player1.color)
            self.board[7][i] = random_piece((7, i), player2.name, player2.color)

    def check_check(self, player: data.PlayerAttributes, board: typing.List[typing.List[pieces.ChessPiece]] = None) -> bool:
        """
        Check if the player is in check.

        :param player:
        :param board:
        :return:
        """
        if board is None:
            board = self.board
        colors = ["white", "black"]
        colors.remove(player.color)
        player_king = set([j.position for i in board for j in i if isinstance(j, pieces.King) and j.color == player.color][0])
        opponent_pieces = [j for i in board for j in i if j.color == colors[0]]
        moves = set([j.possible_moves() for j in opponent_pieces])
        if player_king & moves:
            return True
        return False

    def check_checkmate(self, player: data.PlayerAttributes) -> bool:
        """
        Check if the player is in checkmate.

        :param player:
        :return:
        """
        if self.check_check(player):
            dummy_board = self.board.copy()
            player_pieces = [j for i in self.board for j in i if j.color == player.color]
            for i in player_pieces:
                for j in i.possible_moves():
                    dummy_board[j[0]][j[1]] = i
                    dummy_board[i.position[0]][i.position[1]] = None
                    if not self.check_check(player, dummy_board):
                        return False
                    dummy_board[i.position[0]][i.position[1]] = i
                    dummy_board[j[0]][j[1]] = None
            return True

    def check_el_passant(
        self, player: data.PlayerAttributes, old: typing.Tuple[int, int], new: typing.Tuple[int, int]
    ) -> bool:
        """
        Check if the player is in el passant.

        :param player:
        :param old:
        :param new:
        :return:
        """
        if not isinstance(self.board[old[0]][old[1]], pieces.Pawn):
            return False
        if (x := self.board[old[0] - 1][old[1]]) is not None and isinstance(x, pieces.Pawn) and x.color != player.color:
            if player.color == "white":
                if (old[0] - 1, old[1] + 1) == new:
                    return True
            else:
                if (old[0] - 1, old[1] - 1) == new:
                    return True
        if (x := self.board[old[0] + 1][old[1]]) is not None and isinstance(x, pieces.Pawn) and x.color != player.color:
            if player.color == "white":
                if (old[0] + 1, old[1] + 1) == new:
                    return True
            else:
                if (old[0] + 1, old[1] - 1) == new:
                    return True
        return False


# TODO: Refactor this class
class Team(Board):
    """Dummy piece class, to be edited later and as required"""

    def __init__(self, player1: str, player2: str) -> None:
        self.player1 = data.PlayerAttributes(player1, "white")
        self.player2 = data.PlayerAttributes(player2, "black")
        super().__init__()
        self.generate_pieces(self.player1, self.player2)
