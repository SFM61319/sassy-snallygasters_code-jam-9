"""All pieces are defined here"""


from __future__ import annotations

import typing


class ChessPiece:
    """Base class for chess pieces"""

    piece_type: str
    PATH: typing.Final[str] = "wild_chess/assets/img/chess_pieces"
    color: str
    possible_moves: typing.Callable[[list[list[ChessPiece]]], list[tuple[int, int]]]
    image: str

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        self.position = position
        self.player = player
        self.color = color

    def move(self, new_position: tuple[int, int], board: list[list[ChessPiece | None]], en_passant: tuple[int, int] = None) -> None:
        """
        Move the piece to a new position.

        :param new_position:
        :param board:
        :param en_passant:
        :type new_position: tuple[int, int]
        """
        board[new_position[0]][new_position[1]] = self
        board[self.position[0]][self.position[1]] = None
        if en_passant:
            board[en_passant[0]][en_passant[1]] = None
        self.position = new_position

    def find_diagonals(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """
        Finds diagonals.

        :param board:
        :type board: typing.Any]]
        :return:
        :rtype: list[tuple[int, int]]
        """
        positions = []
        # blacklist = []

        def check(x: int, y: int) -> bool:
            point = board[x][y]
            dx = abs(x - self.position[0])
            dy = abs(y - self.position[1])
            '''
            nearby_positions = [(x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)]
            near = [p for p in nearby_positions if 0 <= p[0] < 8 and 0 <= p[1] < 8]
            for p in near:
                d1x = abs(p[0] - self.position[0])
                d1y = abs(p[1] - self.position[1])
                if p in blacklist and d1x == d1y and d1x > 0:
                    blacklist.append(p)
                    return True
            '''
            if (dx == dy) and (dx > 0):
                positions.append((x, y))
            if point and point.color != self.color and (dx == dy) and (dx > 0):
                positions.append((x, y))
                # blacklist.append((x, y))
                return True
            return False

        def right(x: int) -> None:
            for j in range(self.position[1] + 1, 8):
                broken = check(x, j)
                if broken:
                    return
            else:
                return

        def left(x: int) -> None:
            for j in range(self.position[1] - 1, -1, -1):
                broken = check(x, j)
                if broken:
                    return
            else:
                return

        for i in range(self.position[0] + 1, 8):
            right(i)
            left(i)

        for i in range(self.position[0] - 1, -1, -1):
            right(i)
            left(i)

        return positions

    def find_sides(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """
        Finds sides.

        :param board:
        :type board: list[list[ChessPiece]]
        :return:
        :rtype: list[tuple[int, int]]
        """
        positions = []
        for i in range(self.position[0] + 1, 8):
            point = board[i][self.position[1]]
            positions.append((i, self.position[1]))
            '''
            if point and point.color != self.color:
                break
            '''

        for i in range(self.position[0] - 1, -1, -1):
            point = board[i][self.position[1]]
            positions.append((i, self.position[1]))
            '''
            if point and point.color != self.color:
                break
            '''

        for i in range(self.position[1] + 1, 8):
            point = board[self.position[0]][i]
            positions.append((self.position[0], i))
            '''
            if point and point.color != self.color:
                break
            '''

        for i in range(self.position[1] - 1, -1, -1):
            point = board[self.position[0]][i]
            positions.append((self.position[0], i))
            '''
            if point and point.color != self.color:
                break
            '''

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
        super().__init__(position, player, color)
        self.image = f"{self.PATH}/pawn.{color}.png"
        self.possibility: list[tuple[int, int]] = []
        self.moves: list[tuple[int, int]] = []

    # TODO: Heavily refactor and clean this method, and the whole file
    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the pawn."""
        self.possibility = []
        if self.color == "white":
            if self.position[0] == 1:
                self.possibility.append((self.position[0] + 2, self.position[1]))

            self.possibility.append((self.position[0] + 1, self.position[1]))

            x = (self.position[0] + 1, self.position[1] + 1)
            if x and board[x[0]][x[1]] is not None and board[x[0]][x[1]].player != self.player:
                self.possibility.append(x)

            x = (self.position[0] + 1, self.position[1] - 1)
            if x and board[x[0]][x[1]] is not None and board[x[0]][x[1]].player != self.player:
                self.possibility.append(x)

            self.possibility.append(x)

            y = board[self.position[0]][self.position[1] - 1]
            if y is not None and y.color != self.color:
                self.possibility.append((self.position[0] + 1, self.position[1] - 1))

            y = board[self.position[0]][self.position[1] + 1]
            if y is not None and y.color != self.color:
                self.possibility.append((self.position[0] + 1, self.position[1] + 1))

        else:
            if self.position[0] == 6:
                self.possibility.append((self.position[0] - 2, self.position[1]))

            self.possibility.append((self.position[0] - 1, self.position[1]))

            x = (self.position[0] - 1, self.position[1] - 1)
            if x and board[x[0]][x[1]] is not None and board[x[0]][x[1]].player != self.player:
                self.possibility.append(x)

            x = (self.position[0] - 1, self.position[1] + 1)
            if x and board[x[0]][x[1]] is not None and board[x[0]][x[1]].player != self.player:
                self.possibility.append(x)

            y = board[self.position[0]][self.position[1] - 1]
            if y is not None and y.color != self.color:
                self.possibility.append((self.position[0] - 1, self.position[1] - 1))

            y = board[self.position[0]][self.position[1] + 1]
            if y is not None and y.color != self.color:
                self.possibility.append((self.position[0] - 1, self.position[1] + 1))

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
        super().__init__(position, player, color)
        self.image = f"{self.PATH}/rook.{color}.png"
        self.possibility: list[tuple[int, int]] = []
        self.moves: list[tuple[int, int]] = []

    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the rook."""
        self.possibility = []
        self.possibility.extend(self.find_sides(board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class Knight(ChessPiece):
    """The knight piece"""

    piece_type: str = "Knight"
    takeable: bool = True

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player, color)
        self.image = f"{self.PATH}/knight.{color}.png"
        self.possibility: list[tuple[int, int]] = []
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
        super().__init__(position, player, color)
        self.image = f"{self.PATH}/bishop.{color}.png"
        self.possibility: list[tuple[int, int]] = []
        self.moves: list[tuple[int, int]] = []

    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the bishop."""
        self.possibility = []
        self.possibility.extend(self.find_diagonals(board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class Queen(ChessPiece):
    """The queen piece"""

    piece_type: str = "Queen"
    takeable: bool = True

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player, color)
        self.image = f"{self.PATH}/queen.{color}.png"
        self.possibility: list[tuple[int, int]] = []
        self.moves: list[tuple[int, int]] = []

    def possible_moves(self, board: list[list[ChessPiece]]) -> list[tuple[int, int]]:
        """Get the possible moves for the queen."""
        self.possibility = []
        self.possibility.extend(self.find_sides(board))
        self.possibility.extend(self.find_diagonals(board))
        self.moves = self.filter_moves(self.possibility, board, self.player)
        return self.moves


class King(ChessPiece):
    """The king piece"""

    piece_type: str = "King"
    takeable: bool = False

    def __init__(self, position: tuple[int, int], player: str, color: str) -> None:
        super().__init__(position, player, color)
        self.image = f"{self.PATH}/king.{color}.png"
        self.possibility: list[tuple[int, int]] = []
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
