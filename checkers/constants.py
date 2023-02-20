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
