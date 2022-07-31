"""A piece class, the parent of all pieces"""


import random
import typing

from wild_chess.gui import gui
from wild_chess.logic import pieces
from wild_chess.utils import data


# Create a class board and subclass it to have two teams
class Board:
    """A chess board."""

    board: list[list[typing.Optional[pieces.ChessPiece]]]
    player1: data.PlayerAttributes
    player2: data.PlayerAttributes
    current_player: data.PlayerAttributes
    turns: dict[str, list[list[typing.Optional[pieces.ChessPiece]]]]

    def __init__(self, player1: str, player2: str) -> None:
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
        self.player1 = data.PlayerAttributes(player1, "white")
        self.player2 = data.PlayerAttributes(player2, "black")
        self.current_player = self.player1
        self.game = gui.Game()
        self.turns = {}
        self.total_turns: int = 0

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
            pieces.Pawn,
        ]

        for i in range(8):
            random_piece = random.choice(all_special_pieces)
            if i == 4:
                self.board[0][4] = pieces.King((0, 4), player1.name, player1.color)
                self.board[7][4] = pieces.King((7, 4), player2.name, player2.color)
            else:
                random_piece2 = random.choice(all_special_pieces)
                self.board[0][i] = random_piece2((0, i), player1.name, player1.color)
                self.board[7][i] = random_piece2((7, i), player2.name, player2.color)
            self.board[1][i] = random_piece((1, i), player1.name, player1.color)
            self.board[6][i] = random_piece((6, i), player2.name, player2.color)

    def check_check(
        self, player: data.PlayerAttributes) -> bool:
        """
        Check if the player is in check.

        :param player:
        :param board:
        :return:
        """
        board = self.board
        enemy_pieces = [j for i in self.board for j in i if j and j.color != player.color]
        for piece in enemy_pieces:
            for move in piece.possible_moves(board):
                try:
                    if board[move[0]][move[1]].piece_type == "King":
                        return True
                except:
                    pass
        return False

    def check_checkmate(self, player: data.PlayerAttributes) -> bool:
        """
        Check if the player is in checkmate.

        :param player:
        :return:
        """
        player_pieces = [j for i in self.board for j in i if j and j.color == player.color]
        for piece in player_pieces:
            if piece.piece_type == "King":
                return False
        return True

    def check_en_passant(
        self,
        player: data.PlayerAttributes,
        old: typing.Tuple[int, int],
        new: typing.Tuple[int, int],
        board: typing.List[typing.List[typing.Optional[pieces.ChessPiece]]] = None,
    ) -> tuple[int, int] | None:
        """
        Check if the player is in el passant.

        :param player:
        :param old:
        :param new:
        :param board:
        :return:
        """
        if not board:
            board = self.board
        if not isinstance(self.board[old[0]][old[1]], pieces.Pawn):
            return None
        if (x := board[old[0]][old[1] - 1]) is not None and isinstance(x, pieces.Pawn) and x.color != player.color:
            if player.color == "white":
                if (old[0] + 1, old[1] - 1) == new:
                    return old[0], old[1] - 1
            else:
                if (old[0] - 1, old[1] - 1) == new:
                    return old[0], old[1] - 1
        if (x := board[old[0]][old[1] + 1]) is not None and isinstance(x, pieces.Pawn) and x.color != player.color:
            if player.color == "white":
                if (old[0] + 1, old[1] + 1) == new:
                    return old[0], old[1] + 1
            else:
                if (old[0] - 1, old[1] + 1) == new:
                    return old[0], old[1] + 1
        return None

    @staticmethod
    def start(player1: str, player2: str) -> None:
        """
        Start the game.

        :param player1:
        :type player1: str
        :param player2:
        :type player2: str
        :return:
        :rtype: Board
        """
        board = Board(player1, player2)
        board.begin()

    def begin(self) -> None:
        """Begin the game."""
        self.generate_pieces(self.player1, self.player2)
        self.turns["board"] = self.board
        self.game.init(self)
