"""A piece class, the parent of all pieces"""


import random
import typing

from wild_chess.logic import pieces
from wild_chess.utils import data
from wild_chess.gui import Game


# Create a class board and subclass it to have two teams
class Board:
    """A chess board."""

    board: list[list[typing.Optional[pieces.ChessPiece]]]

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
        self, player: data.PlayerAttributes, board: typing.List[typing.List[typing.Optional[pieces.ChessPiece]]] = None
    ) -> bool:
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
        opponent_pieces = [j for i in board for j in i if j and j.color == colors[0]]
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
            player_pieces = [j for i in self.board for j in i if j and j.color == player.color]
            for i in player_pieces:
                for j in i.possible_moves():
                    dummy_board[j[0]][j[1]] = i
                    dummy_board[i.position[0]][i.position[1]] = None
                    if not self.check_check(player, dummy_board):
                        return False
                    dummy_board[i.position[0]][i.position[1]] = i
                    dummy_board[j[0]][j[1]] = None
            return True
        return False

    def check_en_passant(
        self, player: data.PlayerAttributes, old: typing.Tuple[int, int], new: typing.Tuple[int, int]
    ) -> tuple[int, int] | None:
        """
        Check if the player is in el passant.

        :param player:
        :param old:
        :param new:
        :return:
        """
        if not isinstance(self.board[old[0]][old[1]], pieces.Pawn):
            return None
        if (x := self.board[old[0] - 1][old[1]]) is not None and isinstance(x, pieces.Pawn) and x.color != player.color:
            if player.color == "white":
                if (old[0] - 1, old[1] + 1) == new:
                    return old[0] - 1, old[1]
            else:
                if (old[0] - 1, old[1] - 1) == new:
                    return old[0] - 1, old[1]
        if (x := self.board[old[0] + 1][old[1]]) is not None and isinstance(x, pieces.Pawn) and x.color != player.color:
            if player.color == "white":
                if (old[0] + 1, old[1] + 1) == new:
                    return old[0] + 1, old[1]
            else:
                if (old[0] + 1, old[1] - 1) == new:
                    return old[0] + 1, old[1]
        return None

    def check_king_mouse_slip(
        self,
        player: data.PlayerAttributes,
        old: typing.Tuple[int, int],
    ) -> bool:
        """The king can take his own pieces"""
        x = self.board[old[0] + 1][old[1]]
        if isinstance(x, pieces.Pawn) and x.color == player.color:
            return True
        return False

    def check_knight_mouse_slip(self, player: data.PlayerAttributes, old: typing.Tuple[int, int]) -> bool:
        """The knight moves straight up when pawn, instead of how it originally moves"""
        x = self.board[old[0] + 1][old[1] + 1]
        if isinstance(x, pieces.Pawn) and x.color != player.color:
            return True
        return False

    def check_queen_mouse_slip(self, player: data.PlayerAttributes, old: typing.Tuple[int, int]) -> bool:
        """The queen moves like a knight"""
        x = self.board[old[0] - 1][old[1] + 1]
        y = self.board[old[0] + 1][old[1] - 1]

        if (isinstance(x, pieces.Pawn) and x.color != player.color) or (
            isinstance(y, pieces.Pawn) and y.color != player.color
        ):
            return True
        return False

    def start(self) -> None:
        self.generate_pieces(self.player1, self.player2)
        checkmate = False
        while not checkmate:
            # self.print_board() display board
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2
            print(f"{self.current_player.name}'s turn")
            # old, new = self.get_move() ask move return old pos and new pos
            old, new = self.get_move()
            en_passant = self.check_en_passant(self.current_player, old, new)
            if en_passant:
                print("En passant")
            if self.check_check(self.current_player):
                dummy = self.board.copy()
                dummy[old[0]][old[1]].move(new, self.board, en_passant)
                if self.check_check(self.current_player, dummy):
                    print("Check")  # check if the move is valid
                print("Check")
            if self.check_checkmate(self.current_player):
                print("Checkmate")
                checkmate = True
            self.board[old[0]][old[1]].move(new, self.board, en_passant)
            # self.print_board() display board again
            if self.check_checkmate(self.current_player):
                print("Checkmate")
                checkmate = True
            # repeat till over
            # rough logic
