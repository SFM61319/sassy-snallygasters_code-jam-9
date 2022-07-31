"""Main file."""
import asyncio
from wild_chess.utils import board
from server.main import main


if __name__ == "__main__":
    game = board.Board.start('Asher', 'Ninja')
    main()  # its a blocking function for trial purpose keep below till we shift game in server
