"""wild_chess/main.py"""
# pylint: disable=E1101
import pygame

# import board_backend

# Referenced from Eddie Sharicks's 'Chess Engine in Python series'
# https://youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY

WINDOW_WIDTH = 720  # Horizontal Resolution of window
WINDOW_HEIGHT = 720  # Vertical Resolution of window
BOARD_WIDTH = BOARD_HEIGHT = 512  # Resolution of only the board i.e. play area
BOARD_DFE = (
    100  # Board Distance From Edge - Distance of the top left and top right corner of the board from the corner of the window
)
DIMENSION = 8  # Dimensions of Chess Board (8x8)
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION  # Per Square size
FPS = 15  # FPS For animations
BORDER_OFFSET_L = BORDER_OFFSET_R = 2  # Width of border on the perimeter of the chess board
IMAGES = {}  # Dictionary storing the images of pieces


def load_images() -> None:
    """Funtion to load images of chess pieces into dictionary"""
    pieces = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("./images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def get_screen_res() -> tuple:
    """Function to get the user's screen resolution"""
    screen_height, screen_width = (
        pygame.display.Info().current_w,
        pygame.display.Info().current_h,
    )
    return (screen_height, screen_width)


def draw_board(screen: pygame.Surface) -> None:  # Need to add a parameter for game_state object here
    """Function to draw playable board inside the pygame window"""
    # Main play area border
    board_color = (255, 0, 0)
    offset_l = BORDER_OFFSET_L
    offset_r = BORDER_OFFSET_R + BORDER_OFFSET_L
    pygame.draw.rect(
        screen,
        board_color,
        pygame.Rect(
            BOARD_DFE - offset_l,
            BOARD_DFE - offset_l,
            (SQUARE_SIZE * DIMENSION) + offset_r,
            (SQUARE_SIZE * DIMENSION) + offset_r,
        ),
        offset_l,
    )

    # Draw squares inside board
    square_colors = [("#dfdfdf"), ("#202020")]  # White, Black
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            current_color = square_colors[((row + column) % 2)]
            pygame.draw.rect(
                screen,
                current_color,
                pygame.Rect(BOARD_DFE + (column * SQUARE_SIZE), BOARD_DFE + (row * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE),
            )


def main() -> None:
    """Main Function"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Wild Chess")
    clock = pygame.time.Clock()

    # game_state = board_backend.game_state() #load game state
    # load_images() #load chess pieces
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("#FFFFFF")  # Filling each frame since resizing causes issues
        draw_board(screen)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
