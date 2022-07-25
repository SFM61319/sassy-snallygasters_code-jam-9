"""Basic movement file, input handler is missing, not compatible with board yet"""
from pieces import Bishop, King, Knight, Pawn, Queen, Rook

# dummy positions, must be changed from the board class
pawn = Pawn((0, 0), "")
bishop = Bishop((0, 0), "")
knight = Knight((0, 0), "")
rook = Rook((0, 0), "")
queen = Queen((0, 0), "")
king = King((0, 0), "")


def pawn_move() -> None:
    """The pawn moves in the x direction, except when taking, then it moves diagonally"""
    x, y = pawn.position

    y += 1
    pawn.position = (x, y)
    pawn.has_moved = True


def bishop_move() -> None:
    """The bishop moves in the x and y direction"""
    x, y = bishop.position

    x += 1
    y += 1

    bishop.position = (x, y)
    bishop.has_moved = True


def knight_move() -> None:
    """The knight moves in the x and y direction, except when taking, then it moves diagonally"""
    x, y = knight.position

    x += 2
    y += 1

    knight.position = (x, y)
    knight.has_moved = True


def rook_move() -> None:
    """The rook moves in the x direction"""
    x, y = rook.position

    y += 1
    rook.position = (x, y)
    rook.has_moved = True


def queen_move() -> None:
    """The queen moves in x and y direction"""
    x, y = queen.position

    x += 1

    queen.position = (x, y)
    queen.has_moved = True
