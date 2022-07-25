"""Pygame GUI"""


import pygame
import pygame.freetype

# import board_backend


# Referenced from Eddie Sharicks's 'Chess Engine in Python' series
# https://youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_

WINDOW_WIDTH = pygame.display.Info().current_w  # Horizontal Resolution of window
WINDOW_HEIGHT = pygame.display.Info().current_h * 0.95  # Vertical Resolution of window
BOARD_WIDTH = BOARD_HEIGHT = WINDOW_HEIGHT * 0.85  # Resolution of only the board i.e. play area
BOARD_DFE = (
    WINDOW_HEIGHT
    # Board Distance From Edge - Distance of the top left and top right corner of the board from the corner of the window
    * 0.05
)
DIMENSION = 8  # Dimensions of Chess Board (8x8)
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION  # Per Square size
FPS = 15  # FPS For animations
BORDER_OFFSET_L = BORDER_OFFSET_R = 2  # Width of border on the perimeter of the chess board
IMAGES: dict[str, str] = {}  # Dictionary storing the images of pieces


def load_images() -> None:
    """Function to load images of chess pieces into dictionary"""
    pieces = []
    piece_colors = ("black", "white")
    piece_types = ("pawn", "rook", "knight", "bishop", "queen", "king")

    for piece_color in piece_colors:
        for piece_type in piece_types:
            pieces.append(f"{piece_type}.{piece_color}")

    for piece in pieces:
        IMAGES[piece] = f"assets/img/chess_pieces/{piece}.png"


def get_screen_res() -> tuple[int, int]:
    """Function to get the user's screen resolution"""
    display_info = pygame.display.Info()
    return (display_info.current_w, display_info.current_h)


# TODO: Need to add a parameter for game_state object here
def draw_board(screen: pygame.Surface) -> None:
    """Function to draw playable board inside the pygame window"""
    # Getting window width and height again due to possible screen resize
    window_width = pygame.display.Info().current_w
    window_height = pygame.display.Info().current_h * 0.95
    board_height = window_height * 0.85  # Resolution of only the board i.e. play area
    board_dfe = (
        window_height
        # Board Distance From Edge - Distance of the top left and top right corner of the board from the corner of the window
        * 0.05
    )
    square_size = board_height // 8
    # Main play area border
    board_color = (255, 0, 0)
    offset_l = BORDER_OFFSET_L
    offset_r = BORDER_OFFSET_R + BORDER_OFFSET_L

    pygame.draw.rect(
        screen,
        board_color,
        pygame.Rect(
            board_dfe + window_width / 2 - window_height / 2 - offset_l,
            board_dfe - offset_l,
            (square_size * DIMENSION) + offset_r,
            (square_size * DIMENSION) + offset_r,
        ),
        offset_l,
    )

    # Draw squares inside board
    square_colors = ["#DFDFDF", "#202020"]  # White, Black

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            current_color = square_colors[(row + column) % 2]
            pygame.draw.rect(
                screen,
                current_color,
                pygame.Rect(
                    board_dfe + window_width / 2 - window_height / 2 + (column * square_size),
                    board_dfe + (row * square_size),
                    square_size,
                    square_size,
                ),
            )


def draw_text(screen: pygame.Surface) -> None:
    """Draw text in window"""
    font = pygame.font.SysFont("Times New Roman", 30)

    # TODO: Use player usernames instead
    player_1_text = "Player 1"
    player_2_text = "Player 2"

    versus_text = f"{player_1_text} VS {player_2_text}"
    versus_text_pos = (BOARD_DFE + (BOARD_WIDTH // 2), (BOARD_DFE * 2) + BOARD_HEIGHT)

    surface_versus_text = font.render(versus_text, True, (0, 0, 0))
    text_rect = surface_versus_text.get_rect(center=versus_text_pos)

    screen.blit(surface_versus_text, text_rect)


def update(screen: pygame.Surface) -> None:
    """Update the given screen."""
    draw_board(screen)
    load_images()


def main() -> None:
    """Main Function"""
    pygame.display.set_caption("Wild Chess")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # game_state = board_backend.game_state() #load game state
    # load_images()  # load images of chess pieces only once

    screen.fill("#FFFFFF")  # Filling only at beginning for code efficiency
    update(screen)  # type: ignore

    # for image in IMAGES:
    #     screen.blit(pygame.transform.scale(pygame.image.load(IMAGES[image]), (SQUARE_SIZE, SQUARE_SIZE)), (500, 490))

    # Font Resizing to be worked on
    draw_text(screen)  # type: ignore

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if WINDOW_WIDTH != pygame.display.Info().current_w or WINDOW_HEIGHT != pygame.display.Info().current_h:
                screen.fill("#FFFFFF")
                update(screen)  # type: ignore

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
