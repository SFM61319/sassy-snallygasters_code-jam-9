"""A piece class, the parent of all pieces"""
# from typing import List, Tuple

# pylint: disable=R0913
# pylint: disable=R0903

# Create a class board and subclass it to have two teams


from typing import List


class Board:
    """Should be a list of 8x8 coordinates"""


class Team:
    """Dummy team class, to be edited later and as required"""

    def __init__(self, player: str) -> None:
        self.player = player  # this variable also controls the color
        self.position: List = []  # this variable stores the position of the piece in a team
