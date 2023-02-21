import pygame
import random


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

MINIMAX_DEPTH = 3

CENTRE_16 = [2, 3, 4, 5]

WEIGHTS_KING = [int(x/2 * 10) * 0.1 for x in range(1, 10)]  # 3 - [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
"""
WEIGHTS_CENTRE16 = [int(int(x/2 * 10) * 0.1)/10 for x in range(1, 11)]  # 0.5 [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
WEIGHTS_FORWARD = [int(int(x/2 * 10) * 0.1)/10 for x in range(1, 11)]  # 0.3 [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
WEIGHTS_HOME_ROW = [int(int(x * 10) * 0.1)/10 for x in range(1, 11)]  # 1 [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
"""
WEIGHTS_CENTRE16 = WEIGHTS_KING.copy()
WEIGHTS_FORWARD = WEIGHTS_KING.copy()
WEIGHTS_HOME_ROW = WEIGHTS_KING.copy()

random.shuffle(WEIGHTS_KING)
random.shuffle(WEIGHTS_CENTRE16)
random.shuffle(WEIGHTS_FORWARD)
random.shuffle(WEIGHTS_HOME_ROW)

WEIGHTS_DICT = {
    'KING': 0,
    'CENTRE': 0,
    'FORWARD': 0,
    'HOME': 0
}
