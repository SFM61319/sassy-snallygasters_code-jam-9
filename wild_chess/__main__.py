"""Main file."""

from wild_chess.utils import board
from server.main import main

if __name__ == "__main__":
    main()
    game = board.Board.start('Asher', 'Ninja')
