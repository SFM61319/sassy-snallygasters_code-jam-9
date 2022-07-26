"""All pieces are defined here"""


from __future__ import annotations

import itertools
import typing


class ChessPiece:
    """Base class for chess pieces"""

    PATH: typing.Final[str] = "wild_chess/assets/img/chess_pieces/"
    color: str
    possible_moves: typing.Callable[[], typing.List[tuple[int, int]]]

    def __init__(self, position: tuple[int, int], player: str) -> None:
        self.position = position
        self.player = player

    def move(self, new_position: tuple[int, int]) -> None:
        """
        Move the piece to a new position.

        :param new_position:
        :type new_position: tuple[int, int]
        """
        self.position = new_position

    @staticmethod
    def find_diagonals(position: tuple[int, int], board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """
        Finds diagonals.

        :param position:
        :type position: tuple[int, int]
        :param board:
        :type board: typing.Any]]
        :return:
        :rtype: list[tuple[int, int]]
        """
        positions = []
        y, x = position

        def diagonal(dx: int, dy: int) -> None:
            for p in itertools.count(start=1):
                new_x = x + dx * p
                new_y = y + dy * p

                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    positions.append((new_x, new_y))

                    if board[new_y][new_x] is not None:
                        break

                else:
                    break

        for i in (-1, 1):
            for j in (-1, 1):
                diagonal(i, j)

        return positions

    @staticmethod
    def find_sides(position: tuple[int, int], board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """
        Finds sides.

        :param position:
        :type position: tuple[int, int]
        :param board:
        :type board: list[list[ChessPiece]]
        :return:
        :rtype: list[tuple[int, int]]
        """
        positions = []

        for i in range(8):
            if position[0] == i:
                for j in range(8):
                    if position[1] == j:
                        continue

                    positions.append((i, j))

                    if board[i][j] is not None:
                        break

            elif position[1] == i:
                for j in range(8):
                    if position[0] == j:
                        continue

                    positions.append((j, i))

                    if board[j][i] is not None:
                        break

        return positions

    @staticmethod
    def filter_moves(possibility: list[tuple[int, int]], board: list[list[ChessPiece]], player: str) -> list[tuple[int, int]]:
        """
        Filter the moves to only those that are valid.

        :param possibility:
        :type possibility: list[tuple[int, int]]
        :param board:
        :type board: list[list[ChessPiece]]
        :param player:
        :type player: list[tuple[int, int]]
        :return:
        :rtype: list[tuple[int, int]]
        """
        possibility = [i for i in possibility if 0 <= i[0] < 8 and 0 <= i[1] < 8]
        moves = []

        for move in possibility:
            if board[move[0]][move[1]] is None:
                moves.append(move)

            elif board[move[0]][move[1]].player != player:
                moves.append(move)

        return moves


class Pawn(ChessPiece):
    """The pawn piece"""

    piece_type: str = "Pawn"
    takeable: bool = True

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.PATH + color + ".pawn.png"
        self.possibility: list[tuple[int, int]] = []
        self.color = color
        self.moves: list[tuple[int, int]] = []

    # TODO: Heavily refactor and clean this method, and the whole file
    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the pawn."""
        self.possibility = []
        if self.color == "white":
            if self.position[1] == 1:
                self.possibility.append((self.position[0], self.position[1] + 2))
            self.possibility.append((self.position[0], self.position[1] + 1))
            self.possibility.append(x) if (x := (self.position[0] + 1, self.position[1] + 1)) and board[x[0]][
                x[1]
            ] is not None and board[x[0]][x[1]].player != self.player else None
            self.possibility.append(x) if (x := (self.position[0] + 1, self.position[1] - 1)) and board[x[0]][
                x[1]
            ] is not None and board[x[0]][x[1]].player != self.player else None
            self.possibility.append((self.position[0] + 1, self.position[1] - 1))
            if (x := board[self.position[0] - 1][self.position[1]]) is not None and x.color != self.color:
                self.possibility.append((self.position[0] - 1, self.position[1] + 1))
            if (x := board[self.position[0] + 1][self.position[1]]) is not None and x.color != self.color:
                self.possibility.append((self.position[0] + 1, self.position[1] + 1))
        else:
            if self.position[1] == 6:
                self.possibility.append((self.position[0], self.position[1] - 2))
            self.possibility.append((self.position[0], self.position[1] - 1))
            self.possibility.append(x) if (x := (self.position[0] - 1, self.position[1] - 1)) and board[x[0]][
                x[1]
            ] is not None and board[x[0]][x[1]].player != self.player else None
            self.possibility.append(x) if (x := (self.position[0] - 1, self.position[1] + 1)) and board[x[0]][
                x[1]
            ] is not None and board[x[0]][x[1]].player != self.player else None
            if (x := board[self.position[0] - 1][self.position[1]]) is not None and x.color != self.color:
                self.possibility.append((self.position[0] - 1, self.position[1] - 1))
            if (x := board[self.position[0] + 1][self.position[1]]) is not None and x.color != self.color:
                self.possibility.append((self.position[0] + 1, self.position[1] - 1))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves

    def check_promotion(self) -> bool:
        """
        Check if the pawn has reached the end of the board.
        If so, promote it to a queen.
        """
        if self.color == "white":
            if self.position[1] == 7:
                return True
        else:
            if self.position[1] == 0:
                return True
        return False


class Rook(ChessPiece):
    """The rook piece"""

    piece_type: str = "Rook"
    takeable: bool = True

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.PATH + color + ".rook.png"
        self.possibility: list[tuple[int, int]] = []
        self.color = color
        self.moves: list[tuple[int, int]] = []

    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the rook."""
        self.possibility = []
        self.possibility.extend(self.find_sides(self.position, board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class Knight(ChessPiece):
    """The knight piece"""

    piece_type: str = "Knight"
    takeable: bool = True

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.PATH + color + ".knight.png"
        self.possibility: list[tuple[int, int]] = []
        self.color = color
        self.moves: list[tuple[int, int]] = []

    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the knight."""
        self.possibility = []
        self.possibility.append((self.position[0] + 2, self.position[1] + 1))
        self.possibility.append((self.position[0] + 2, self.position[1] - 1))
        self.possibility.append((self.position[0] - 2, self.position[1] + 1))
        self.possibility.append((self.position[0] - 2, self.position[1] - 1))
        self.possibility.append((self.position[0] + 1, self.position[1] + 2))
        self.possibility.append((self.position[0] + 1, self.position[1] - 2))
        self.possibility.append((self.position[0] - 1, self.position[1] + 2))
        self.possibility.append((self.position[0] - 1, self.position[1] - 2))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class Bishop(ChessPiece):
    """The bishop piece"""

    piece_type: str = "Bishop"
    takeable: bool = True

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.PATH + color + ".bishop.png"
        self.possibility: list[tuple[int, int]] = []
        self.color = color
        self.moves: list[tuple[int, int]] = []

    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the bishop."""
        self.possibility = []
        self.possibility.extend(self.find_diagonals(self.position, board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class Queen(ChessPiece):
    """The queen piece"""

    piece_type: str = "Queen"
    takeable: bool = True

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.PATH + color + ".queen.png"
        self.possibility: list[tuple[int, int]] = []
        self.color = color
        self.moves: list[tuple[int, int]] = []

    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the queen."""
        self.possibility = []
        self.possibility.extend(self.find_sides(self.position, board))
        self.possibility.extend(self.find_diagonals(self.position, board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class King(ChessPiece):
    """The king piece"""

    piece_type: str = "King"
    takeable: bool = False

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.PATH + color + ".king.png"
        self.possibility: list[tuple[int, int]] = []
        self.color = color
        self.moves: list[tuple[int, int]] = []

    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the king."""
        self.possibility = []
        self.possibility.append((self.position[0] + 1, self.position[1] + 1))
        self.possibility.append((self.position[0] + 1, self.position[1] - 1))
        self.possibility.append((self.position[0] - 1, self.position[1] + 1))
        self.possibility.append((self.position[0] - 1, self.position[1] - 1))
        self.possibility.append((self.position[0] + 1, self.position[1]))
        self.possibility.append((self.position[0] - 1, self.position[1]))
        self.possibility.append((self.position[0], self.position[1] + 1))
        self.possibility.append((self.position[0], self.position[1] - 1))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves
