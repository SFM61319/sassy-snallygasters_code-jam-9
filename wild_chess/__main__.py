"""Main file."""

import asyncio
#from wild_chess.server import server
from wild_chess.gui import gui
from wild_chess.utils import board

if __name__ == "__main__":
    game = gui.Game()
    gameBoard = board.Board('wite', 'blak')
    gameBoard.generate_pieces(gameBoard.player1, gameBoard.player2)
    game.init(gameBoard.board)
