"""Pygame GUI"""
# pylint: disable=R0902

import pathlib
import typing
from xmlrpc.client import Boolean

import pygame

from ..logic import pieces

# import board_backend


class Game:
    """
    Game UI

    Usage:
        game = Game()
        game.init()
    """

    SQUARES: typing.Literal[8] = 8
    FPS: typing.Literal[60] = 60
    IMAGE_ASSETS_PATH: pathlib.Path = pathlib.Path("assets/img/chess_pieces")

    screen: pygame.surface.Surface
    window_width: int
    window_height: int
    board_width: int
    board_height: int
    board_dfe: int
    square_size: int
    border_offset: tuple[int, int, int, int]  # left, top, right, bottom
    images: dict[str, pathlib.Path]

    def __init__(self) -> None:
        pygame.init()
        self.use_defaults()
        self.images = {}

    def __load_images(self) -> None:
        """Function to load images of chess pieces into dictionary"""
        piece_types = ("pawn", "rook", "knight", "bishop", "queen", "king")

        for piece_type in piece_types:
            self.images[f"{piece_type}.white"] = pygame.image.load(self.IMAGE_ASSETS_PATH / f"{piece_type}.white.png")
            self.images[f"{piece_type}.black"] = pygame.image.load(self.IMAGE_ASSETS_PATH / f"{piece_type}.black.png")

    def __draw_board(self, board: list[list[pieces.ChessPiece]]) -> None:
        """Draws the UI."""
        self.use_defaults()
        board_color = (0, 120, 212)
        offset_l = self.border_offset[0]
        offset_r = self.border_offset[2] + offset_l

        pygame.draw.rect(
            self.screen,
            board_color,
            pygame.Rect(
                self.board_dfe + self.window_width / 2 - self.window_height / 2 - offset_l,
                self.board_dfe - offset_l,
                (self.square_size * self.SQUARES) + offset_r,
                (self.square_size * self.SQUARES) + offset_r,
            ),
            offset_l,
        )

        # Draw squares inside board
        square_colors = ["#DFDFDF", "#202020"]  # White, Black

        for row in range(self.SQUARES):
            for column in range(self.SQUARES):
                current_color = square_colors[(row + column) % 2]
                pygame.draw.rect(
                    self.screen,
                    current_color,
                    pygame.Rect(
                        self.board_dfe + self.window_width / 2 - self.window_height / 2 + (column * self.square_size),
                        self.board_dfe + (row * self.square_size),
                        self.square_size,
                        self.square_size,
                    ),
                )

                if board[row][column] is not None:
                    if not self.images:
                        self.__load_images()
                    image = self.images[f"{board[row][column].piece_type.lower()}.{board[row][column].color}"]
                    image = pygame.transform.scale(image, (self.square_size, self.square_size))
                    self.screen.blit(
                        image,
                        (
                            self.board_dfe + self.window_width / 2 - self.window_height / 2 + (column * self.square_size),
                            self.board_dfe + (row * self.square_size),
                        ),
                    )

    def __draw_text(self, text: str, position: tuple, color: tuple) -> None:
        """Draw text in window"""
        font = pygame.font.SysFont("Times New Roman", 30)

        # TODO: Use player usernames instead # pylint: disable=W0511

        render_text = font.render(text, True, color)
        text_rect = render_text.get_rect(center=position)

        self.screen.blit(render_text, text_rect)

    def __update(self, board: list[list[pieces.ChessPiece]]) -> None:
        """Update screen."""
        self.__draw_board(board)
        self.__load_images()

    def __draw_button(self, color) -> None:
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(
                self.window_width / 2 - self.window_width / 12,
                self.window_height / 2 - self.window_height / 24,
                self.window_width / 6,
                self.window_height / 12,
            ),
        )

    def __on_button(self, mouse_x, mouse_y) -> Boolean:
        if (
            mouse_x >= self.window_width / 2 - self.window_width / 12
            and mouse_x <= self.window_width / 2 + self.window_width / 12
            and mouse_y >= self.window_height / 2 - self.window_height / 24
            and mouse_y <= self.window_height / 2 + self.window_height / 24
        ):
            return True
        return False

    def init(self, board: list[list[pieces.ChessPiece]]) -> None:
        """Starts the GUI."""
        pygame.display.init()
        pygame.display.set_caption("Wild Chess")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        clock = pygame.time.Clock()
        menu = True

        self.screen.fill("#202020")  # Filling only at beginning for code efficiency
        if not menu:
            self.__load_images()  # load images of chess pieces only once
            self.__update(board)
            self.__draw_text("P1 VS P2", (self.board_dfe + (self.board_width // 2), (self.board_dfe * 2) + self.board_height), (0, 0, 0))

        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.__on_button:
                        menu = False
                        self.__update(board)

            current_width, current_height = self.get_screen_res()
            if menu:
                self.__draw_button((0, 120, 212))
                self.__draw_text("Enter", (self.window_width / 2, self.window_height / 2), (0, 0, 0))
                if self.__on_button(mouse_x, mouse_y):
                    self.__draw_button((0, 80, 172))
                    self.__draw_text("Enter", (self.window_width / 2, self.window_height / 2), (0, 0, 0))
            else:
                if self.window_width != current_width or self.window_height != current_height:
                    self.screen.fill("#202020")
                    self.__update(board)
            clock.tick(self.FPS)
            pygame.display.flip()

    @staticmethod
    def get_screen_res() -> tuple[int, int]:
        """Function to get the user's screen resolution"""
        display_info = pygame.display.Info()
        return display_info.current_w, display_info.current_h

    def use_defaults(self) -> None:
        """Resets the properties to the default values"""
        screen_res = self.get_screen_res()

        self.window_width = screen_res[0]
        self.window_height = round(screen_res[1] * 0.95)

        self.board_width = self.board_height = round(self.window_height * 0.85)
        self.board_dfe = round(self.window_height * 0.05)
        self.square_size = self.board_height // self.SQUARES
        self.border_offset = (2, 0, 2, 0)
