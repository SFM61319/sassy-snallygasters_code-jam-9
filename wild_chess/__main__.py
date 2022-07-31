"""Main file."""


from wild_chess.server import main
from wild_chess.utils import board

if __name__ == "__main__":
    game = board.Board.start("Asher", "Ninja")
    main.main()  # its a blocking function for trial purpose keep below till we shift game in server
