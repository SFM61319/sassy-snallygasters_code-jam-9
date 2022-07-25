"""All pieces are defined here"""
import itertools
from typing import Any, List, Tuple

# pylint: disable=R0913
# pylint: disable=R0903


class ChessPiece:

    path: str = "wild_chess/assets/img/chess_pieces/"

    def __init__(self, position: Tuple[int, int], player: str) -> None:
        self.position = position
        self.player = player

    def move(self, new_position: Tuple[int, int]) -> None:
        """
        Move the piece to a new position.
        :param new_position:
        :return:
        """
        self.position = new_position

    @staticmethod
    def find_diagonals(position: Tuple[int, int], board: List[List[Any]]) -> List[Tuple[int, int]]:
        positions = []
        y, x = position

        def diagonal(dx: int, dy: int) -> None:
            for p in itertools.count(start=1):
                newx = x + dx * p
                newy = y + dy * p

                if 0 <= newx < 8 and 0 <= newy < 8:
                    positions.append((newx, newy))
                    if board[newy][newx] is not None:
                        break
                else:
                    break

        for i in (-1, 1):
            for j in (-1, 1):
                diagonal(i, j)

        return positions

    @staticmethod
    def find_sides(position: Tuple[int, int], board: List[List[Any]]) -> List[Tuple[int, int]]:
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
    def filter_moves(
        possibility: List[Tuple[int, int]], board: List[List["ChessPiece"]], player: str
    ) -> List[Tuple[int, int]]:
        """
        Filter the moves to only those that are valid.
        :param possibility:
        :param board:
        :param player:
        :return:
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

    def __init__(self, position: Tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.path + color + ".pawn.png"
        self.possibility: List[Tuple[int, int]] = []
        self.color = color
        self.moves: List[Tuple[int, int]] = []

    def possible_moves(self, board: List[List[ChessPiece]]) -> List[Tuple[int, int]]:
        """
        Get the possible moves for the pawn.
        :return:
        """
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
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class Rook(ChessPiece):
    """The rook piece"""

    piece_type: str = "Rook"
    takeable: bool = True

    def __init__(self, position: Tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.path + color + ".rook.png"
        self.possibility: List[Tuple[int, int]] = []
        self.color = color
        self.moves: List[Tuple[int, int]] = []

    def possible_moves(self, board: List[List[ChessPiece]]) -> List[Tuple[int, int]]:
        """
        Get the possible moves for the rook.
        :return:
        """
        self.possibility = []
        self.possibility.extend(self.find_sides(self.position, board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class Knight(ChessPiece):
    """The knight piece"""

    piece_type: str = "Knight"
    takeable: bool = True

    def __init__(self, position: Tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.path + color + ".knight.png"
        self.possibility: List[Tuple[int, int]] = []
        self.color = color
        self.moves: List[Tuple[int, int]] = []

    def possible_moves(self, board: List[List[ChessPiece]]) -> List[Tuple[int, int]]:
        """
        Get the possible moves for the knight.
        :return:
        """
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

    def __init__(self, position: Tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.path + color + ".bishop.png"
        self.possibility: List[Tuple[int, int]] = []
        self.color = color
        self.moves: List[Tuple[int, int]] = []

    def possible_moves(self, board: List[List[ChessPiece]]) -> List[Tuple[int, int]]:
        """
        Get the possible moves for the bishop.
        :return:
        """
        self.possibility = []
        self.possibility.extend(self.find_diagonals(self.position, board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class Queen(ChessPiece):
    """The queen piece"""

    piece_type: str = "Queen"
    takeable: bool = True

    def __init__(self, position: Tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.path + color + ".queen.png"
        self.possibility: List[Tuple[int, int]] = []
        self.color = color
        self.moves: List[Tuple[int, int]] = []

    def possible_moves(self, board: List[List[ChessPiece]]) -> List[Tuple[int, int]]:
        """
        Get the possible moves for the queen.
        :return:
        """
        self.possibility = []
        self.possibility.extend(self.find_sides(self.position, board))
        self.possibility.extend(self.find_diagonals(self.position, board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class King(ChessPiece):
    """The king piece"""

    piece_type: str = "King"
    takeable: bool = False

    def __init__(self, position: Tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player)
        self.image = self.path + color + ".king.png"
        self.possibility: List[Tuple[int, int]] = []
        self.color = color
        self.moves: List[Tuple[int, int]] = []

    def possible_moves(self, board: List[List[ChessPiece]]) -> List[Tuple[int, int]]:
        """
        Get the possible moves for the king.
        :return:
        """
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
