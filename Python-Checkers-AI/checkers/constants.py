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

SIMPLE_STRATEGY = False
SCORE_KING = 0.5
SCORE_CENTRE16 = 0.5
SCORE_FORWARD = 0.7
