"""Pygame GUI"""


import pathlib
import typing

import pygame

# import board_backend


class Game:
    """
    Game UI

    Usage:
        game = Game()
        game.init()
    """

    SQUARES: typing.Literal[8] = 8
    FPS: typing.Literal[15] = 15
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
            self.images[f"{piece_type}.white"] = self.IMAGE_ASSETS_PATH / f"{piece_type}.white.png"
            self.images[f"{piece_type}.black"] = self.IMAGE_ASSETS_PATH / f"{piece_type}.black.png"

    def __draw_board(self) -> None:
        """Draws the UI."""
        self.use_defaults()
        board_color = (255, 0, 0)
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

    def __draw_text(self) -> None:
        """Draw text in window"""
        font = pygame.font.SysFont("Times New Roman", 30)

        # TODO: Use player usernames instead
        player_1_text = "Player 1"
        player_2_text = "Player 2"

        versus_text = f"{player_1_text} VS {player_2_text}"
        versus_text_pos = (self.board_dfe + (self.board_width // 2), (self.board_dfe * 2) + self.board_height)

        surface_versus_text = font.render(versus_text, True, (0, 0, 0))
        text_rect = surface_versus_text.get_rect(center=versus_text_pos)

        self.screen.blit(surface_versus_text, text_rect)

    def __update(self) -> None:
        """Update screen."""
        self.__draw_board()
        self.__load_images()

    def init(self) -> None:
        """Starts the GUI."""
        pygame.display.init()
        pygame.display.set_caption("Wild Chess")

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        clock = pygame.time.Clock()

        # game_state = board_backend.game_state() # load game state
        # load_images()  # load images of chess pieces only once

        self.screen.fill("#FFFFFF")  # Filling only at beginning for code efficiency
        self.__update()

        # for image in IMAGES:
        #     screen.blit(pygame.transform.scale(pygame.image.load(IMAGES[image]), (SQUARE_SIZE, SQUARE_SIZE)), (500, 490))

        # Font Resizing to be worked on
        self.__draw_text()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                current_width, current_height = self.get_screen_res()
                if self.window_width != current_width or self.window_height != current_height:
                    self.screen.fill("#FFFFFF")
                    self.__update()

            clock.tick(self.FPS)
            pygame.display.flip()

    def get_screen_res(self) -> tuple[int, int]:
        """Function to get the user's screen resolution"""
        display_info = pygame.display.Info()
        return (display_info.current_w, display_info.current_h)

    def use_defaults(self) -> None:
        """Resets the properties to the default values"""
        screen_res = self.get_screen_res()

        self.window_width = screen_res[0]
        self.window_height = round(screen_res[1] * 0.95)

        self.board_width = self.board_height = round(self.window_height * 0.85)
        self.board_dfe = round(self.window_height * 0.05)
        self.square_size = self.board_height // self.SQUARES
        self.border_offset = (2, 0, 2, 0)
