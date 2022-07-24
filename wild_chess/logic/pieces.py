"""All pieces are defined here"""
from typing import List

from wild_chess.utils.piece import Piece

# pylint: disable=R0913
# pylint: disable=R0903


class Pawn(Piece):
    """The pawn piece"""

    def __init__(self, team: str, piece_type: str, takeable: bool, image: str, possible_moves: List) -> None:
        super().__init__(team, piece_type, takeable, image, possible_moves)
        self.possible_moves = possible_moves
        self.has_moved = False

    def movement(self) -> None:
        """Handles movement of pieces"""
        self.possible_moves = [1, 1]
