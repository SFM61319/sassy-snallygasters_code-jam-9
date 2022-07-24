"""A piece class, the parent of all pieces"""
from typing import List, Tuple

# pylint: disable=R0913
# pylint: disable=R0903

# create a class board and subclass it to have two teams


class Board:
    ...


class Team:
    """Dummy piece class, to be edited later and as required"""

    def __init__(self, player: str) -> None:
        self.player = player  # this variable also controls the color
        self.position = []  # this variable stores the position of the piece in a team
