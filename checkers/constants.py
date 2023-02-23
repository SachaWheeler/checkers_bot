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

MINIMAX_DEPTH = 3

CENTRE_16 = [2, 3, 4, 5]

"""
WEIGHTS_KING = [int(int(x/2 * 10) * 0.1)/10 for x in range(1, 11)]  # [0.0, 0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.4, 0.4, 0.5]
WEIGHTS_CENTRE16 = [int(int(x/2 * 10) * 0.1)/10 for x in range(1, 11)]  # 0.5 [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
WEIGHTS_FORWARD = [int(int(x/2 * 10) * 0.1)/10 for x in range(1, 11)]  # 0.3 [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
WEIGHTS_HOME_ROW = [int(int(x * 10) * 0.1)/10 for x in range(1, 11)]  # 1 [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
"""
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

def array_to_weights(variables, player):
    (K, C, F, H) = variables
    return {
            'KING': K,
            'CENTRE': C,
            'FORWARD': F,
            'HOME': H,
            'PLAYER': player
            }

def log_result(SCORE, results_file):
    """
    {
    'count': 1,
    'RK_W': 0.0,
    'RC_W': 0.0,
    'RF_W': 0.0,
    'RH_W': 0.2,
    'WK_W': 0.0,
    'WC_W': 0.0,
    'WF_W': 0.0,
    'WH_W': 0.0,
    'WINNER': 'White',
    'W_P': 6,
    'W_K': 1,
    'R_P': 1,
    'R_K': 0,
    'turns': 49}
    """

    with open(results_file, "a") as csv_file:
        csv_file.write(f"{SCORE['count']}, "
                        f"{SCORE['RK_W']}, {SCORE['RC_W']}, {SCORE['RF_W']}, {SCORE['RH_W']}, "
                        f"{SCORE['WK_W']}, {SCORE['WC_W']}, {SCORE['WF_W']}, {SCORE['WH_W']}, "
                        f"{SCORE['WINNER']}, "
                        f"{SCORE['W_P']}, {SCORE['W_K']}, "
                        f"{SCORE['R_P']}, {SCORE['R_K']}, "
                        f"{SCORE['turns']}\n")

