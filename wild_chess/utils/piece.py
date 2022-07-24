"""A piece class, the parent of all pieces"""
from typing import List

# pylint: disable=R0913
# pylint: disable=R0903


class Piece:
    """Dummy piece class, to be edited later and as required"""

    def __init__(self, team: str, piece_type: str, takeable: bool, image: str, possible_moves: List) -> None:
        self.team = team  # this variable also controls the color
        self.piece_type = piece_type
        self.takeable = takeable  # if a piece is a king it can't be taken
        self.image = image
        self.possible_moves = possible_moves
