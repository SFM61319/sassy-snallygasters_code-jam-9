"""Pygame GUI"""
# pylint: disable=R0902, R0914, R1702, R0912, R0915, fixme

import pathlib
import typing

import pygame

from wild_chess.logic import pieces

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

    def __draw_board(self) -> None:
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

    def __draw_pieces(self, board: list[list[pieces.ChessPiece | None]]) -> None:
        for row in range(self.SQUARES):
            for column in range(self.SQUARES):
                if board[row][column] is not None:
                    if not self.images:
                        self.__load_images()
                    image = self.images[f"{board[row][column].piece_type.lower()}.{board[row][column].color}"]  # type: ignore
                    image = pygame.transform.scale(image, (self.square_size, self.square_size))              # type: ignore
                    self.screen.blit(
                        image,
                        (
                            self.board_dfe + self.window_width / 2 - self.window_height / 2 + (column * self.square_size),
                            self.board_dfe + (row * self.square_size),
                        ),
                    )

    def __move_piece(self, initial: tuple, final: tuple, board: list[list[pieces.ChessPiece | None]]) -> None:
        """Move piece to new position"""
        board[initial[0]][initial[1]].move(final, board)

    def __draw_text(self, text: str, font_size: int, position: tuple, color: tuple[int, int, int]) -> None:
        """Draw text in window"""
        font = pygame.font.SysFont("Times New Roman", font_size)

        render_text = font.render(text, True, color)
        text_rect = render_text.get_rect(center=position)

        self.screen.blit(render_text, text_rect)

    def __update(self, possibles: list[tuple[int, int]], board: list[list[pieces.ChessPiece | None]]) -> None:
        """Update screen."""
        self.__draw_board()
        self.__moves_highlight(possibles, board)

    def __draw_button(self, color: tuple[int, int, int]) -> None:
        """Draws button on main menu"""
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

    def __board_grid_detection(self, mouse_x: int, mouse_y: int) -> tuple[int, int] | None:
        """Check if mouse is in the bounds of the board and return position on the chess grid"""
        if (
            self.board_dfe + self.window_width / 2 - self.window_height / 2
            <= mouse_x
            <= self.board_dfe + self.window_width / 2 - self.window_height / 2 + self.board_width
            and self.board_dfe <= mouse_y <= self.board_dfe + self.board_height
        ):
            column_grid = (mouse_x - (self.board_dfe + self.window_width // 2 - self.window_height // 2)) // self.square_size
            row_grid = (mouse_y - (self.board_dfe)) // self.square_size
            if 0 <= column_grid < self.SQUARES and 0 <= row_grid < self.SQUARES:
                return (column_grid, row_grid)
            return None
        return None

    def __moves_highlight(self, possibles: list[tuple[int, int]], board: list[list[pieces.ChessPiece | None]]) -> None:
        """Function to highlight the possible squares"""
        move_colors = ["#67f757", "#f75757"]  # Green, Red
        current_color = move_colors[0]
        for possible in possibles:
            if board[possible[1]][possible[0]] is None:
                current_color = move_colors[0]
            else:
                current_color = move_colors[1]
            pygame.draw.rect(
                self.screen,
                current_color,
                pygame.Rect(
                    self.board_dfe + self.window_width / 2 - self.window_height / 2 + (possible[0] * self.square_size),
                    self.board_dfe + (possible[1] * self.square_size),
                    self.square_size,
                    self.square_size,
                ),
            )
        # self.__draw_pieces(board)

    def __on_button(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if mouse is on the "ENTER" button in the menu"""
        if (
            self.window_width / 2 - self.window_width / 12 <= mouse_x <= self.window_width / 2 + self.window_width / 12
            and self.window_height / 2 - self.window_height / 24 <= mouse_y <= self.window_height / 2 + self.window_height / 24
        ):
            return True
        return False

    def init(self, board: list[list[pieces.ChessPiece | None]]) -> None:  # noqa: C901
        """Starts the GUI."""
        pygame.display.init()
        pygame.display.set_caption("Wild Chess")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        clock = pygame.time.Clock()
        menu = True

        self.__load_images()  # load images of chess pieces only once
        self.screen.fill("#202020")  # Filling only at beginning for code efficiency
        if not menu:
            self.__draw_board()
            self.__draw_pieces(board)

        running = True
        piece_active = False  # Piece is selected
        piece_selected: tuple[int, int] = ()  # Current position of selected piece
        possible_moves: list[tuple[int, int]] = []  # Possible moves for the selected piece
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    if menu and self.__on_button:
                        menu = False
                        self.__draw_board()
                        self.__draw_pieces(board)

                    elif not menu:
                        grid = self.__board_grid_detection(mouse_x, mouse_y)
                        if grid is not None:
                            grid_x, grid_y = grid[0], grid[1]

                            if piece_active is False and board[grid_y][grid_x] is not None:
                                piece_selected = grid
                                possible_moves = board[grid_y][grid_x].possible_moves(board)  # type: ignore
                                possible_moves = [m[::-1] for m in possible_moves]
                                self.__update(possible_moves, board)
                                self.__draw_pieces(board)
                                piece_active = True

                            elif piece_active is True and grid in possible_moves and piece_selected[::-1] != grid:
                                self.__move_piece((piece_selected[::-1]), (grid[::-1]), board)
                                self.__draw_board()
                                self.__draw_pieces(board)
                                piece_selected = ()
                                piece_active = False
                                possible_moves = []

                            elif piece_active is True and grid not in possible_moves:
                                self.__draw_board()
                                self.__draw_pieces(board)
                                piece_selected = ()
                                piece_active = False
                                possible_moves = []

                            else:
                                piece_selected = ()
                                piece_active = False
                                possible_moves = []
                                self.__draw_board()
                                self.__draw_pieces(board)

                        else:
                            continue

            current_width, current_height = self.get_screen_res()
            current_height = round(current_height * 0.95)
            if menu:
                self.screen.fill("#202020")
                self.__draw_button((0, 120, 212))
                self.__draw_text("Enter", 30, (self.window_width / 2, self.window_height / 2), (0, 0, 0))
                if self.__on_button(mouse_x, mouse_y):
                    self.__draw_button((0, 80, 172))
                    self.__draw_text("Enter", 30, (self.window_width / 2, self.window_height / 2), (255, 255, 255))

            else:
                # if grid_check is not None: #Test Code - To be removed
                #     print (grid_check)

                # TODO: Use player usernames instead # pylint: disable=W0511
                self.__draw_text(
                    "P1 VS P2", 30, ((self.window_width // 2, (self.board_dfe * 2) + self.board_height)), (255, 255, 255)
                )

                if self.window_width != current_width or self.window_height != current_height:
                    self.screen.fill("#202020")
                    self.__draw_board()
                    self.__draw_pieces(board)

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
