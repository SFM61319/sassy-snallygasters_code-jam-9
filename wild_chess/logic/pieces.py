"""All pieces are defined here"""
from typing import List, Dict, Union, Tuple


# pylint: disable=R0913
# pylint: disable=R0903


class ChessPiece:

    def __init__(self, position: Tuple[int, int], player: str) -> None:
        self.position = position
        self.player = player


class Pawn(ChessPiece):
    """The pawn piece"""
    piece_type: str = "Pawn"
    takeable: bool = True
    image: str = ""
    possible_moves: Dict[str, Union[int, List[str]]] = {"Direction": ["Forward"], "Limit": 1}

    def __init__(self, position: Tuple[int, int], player: str) -> None:
        super().__init__(position, player)


class Rook(ChessPiece):
    """The rook piece"""
    piece_type: str = "Rook"
    takeable: bool = True
    image: str = ""
    possible_moves: Dict[str, Union[int, List[str]]] = {"Direction": ["Forward", "Sides"], "Limit": None}

    def __init__(self, position: Tuple[int, int], player: str) -> None:
        super().__init__(position, player)


class Knight(ChessPiece):
    """The knight piece"""
    piece_type: str = "Knight"
    takeable: bool = True
    image: str = ""
    possible_moves: Dict[str, Union[int, List[str]]] = {"Direction": ["Crooked-Diagonal"], "Limit": 1}

    def __init__(self, position: Tuple[int, int], player: str) -> None:
        super().__init__(position, player)


class Bishop(ChessPiece):
    """The bishop piece"""
    piece_type: str = "Bishop"
    takeable: bool = True
    image: str = ""
    possible_moves: Dict[str, Union[int, List[str]]] = {"Direction": ["Diagonal"], "Limit": None}

    def __init__(self, position: Tuple[int, int], player: str) -> None:
        super().__init__(position, player)


class Queen(ChessPiece):
    """The queen piece"""
    piece_type: str = "Queen"
    takeable: bool = True
    image: str = ""
    possible_moves: Dict[str, Union[int, List[str]]] = {"Direction": ["Forward", "Sides", "Diagonal"], "Limit": None}

    def __init__(self, position: Tuple[int, int], player: str) -> None:
        super().__init__(position, player)


class King(ChessPiece):
    """The king piece"""
    piece_type: str = "King"
    takeable: bool = False
    image: str = ""
    possible_moves: Dict[str, Union[int, List[str]]] = {"Direction": ["Forward", "Sides", "Diagonal"], "Limit": 1}

    def __init__(self, position: Tuple[int, int], player: str) -> None:
        super().__init__(position, player)
