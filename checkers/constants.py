import pygame
import random
import csv
import pprint


WIDTH, HEIGHT = 800, 900
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

ALPHA, BETA = float('-inf'), float('inf')
MINIMAX_DEPTH = 3
DRAW_ALL_SUB_MOVES = False

CENTRE_16 = [2, 3, 4, 5]

# WEIGHTS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
WEIGHTS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
WEIGHTS_KING = WEIGHTS.copy()
WEIGHTS_CENTRE16 = WEIGHTS.copy()
WEIGHTS_FORWARD = WEIGHTS.copy()
WEIGHTS_HOME_ROW = WEIGHTS.copy()

WEIGHTS_DICT = {
    'KING': 0,
    'CENTRE': 0,
    'FORWARD': 0,
    'HOME': 0
}

