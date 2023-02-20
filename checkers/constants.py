import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

CENTRE_16 = [2, 3, 4, 5]

WEIGHTS_KING = [int(x/2 * 10) * 0.1 for x in range(4, 10)]  # 3 - [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
WEIGHTS_CENTRE16 = [int(int(x * 10) * 0.1)/10 for x in range(1, 11)]  # 0.5
WEIGHTS_FORWARD = [int(int(x * 10) * 0.1)/10 for x in range(1, 11)]  # 0.3
WEIGHTS_HOME_ROW = [int(int(x*2 * 10) * 0.1)/10 for x in range(1, 11)]  # 1

WEIGHTS_DICT = {
    'KING': 0,
    'CENTRE': 0,
    'FORWARD': 0,
    'HOME': 0
}

def log(f, text):
    print(text, end='')
    f.write(text)

def log_name(f, WHITE_WEIGHTS, RED_WEIGHTS):
     game_title = (f"WHITE:K_{WHITE_WEIGHTS['KING']}|"
             f"C_{WHITE_WEIGHTS['CENTRE']}|"
             f"F_{WHITE_WEIGHTS['FORWARD']}|"
             f"H_{WHITE_WEIGHTS['HOME']}"
             f"_vs_"
             f"RED:K_{RED_WEIGHTS['KING']}|"
             f"C_{RED_WEIGHTS['CENTRE']}|"
             f"F_{RED_WEIGHTS['FORWARD']}|"
             f"H_{RED_WEIGHTS['HOME']}"
             "\n")
     log(f, game_title)

def log_game_state(f, player, board):
    PLAYER = "Red" if player == RED else "White"
    game_state = (
            f"{PLAYER} move: "
            f"R: {board.red_left - board.red_kings} P, {board.red_kings} K - "
            f"W: {board.white_left - board.white_kings} P, {board.white_kings} K\n"
            )
    log(f, game_state)
