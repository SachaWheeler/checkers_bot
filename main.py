# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # remove pygame announcement
import pygame
from checkers.constants import (WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE,
                                WEIGHTS_KING, WEIGHTS_CENTRE16, WEIGHTS_FORWARD, WEIGHTS_HOME_ROW,
                                WEIGHTS_DICT)
from checkers.game import Game
from minimax.algorithm import minimax
import pprint

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main(WHITE_WEIGHTS, RED_WEIGHTS):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:  # always an AI player
            print("white's turn")
            pprint.pprint(WHITE_WEIGHTS)
            # value, new_board = minimax(game.get_board(), 4, WHITE, game, WHITE_WEIGHTS)
            value, new_board = minimax(game.get_board(), 4, True, game, WHITE_WEIGHTS)
            game.ai_move(new_board)
        elif RED_WEIGHTS is not None:  # human or AI for RED
            print("red's turn")
            pprint.pprint(RED_WEIGHTS)
            # value, new_board = minimax(game.get_board(), 4, RED, game, RED_WEIGHTS)
            value, new_board = minimax(game.get_board(), 4, True, game, RED_WEIGHTS)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        if RED_WEIGHTS is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()

    pygame.quit()

WHITE_WEIGHTS = WEIGHTS_DICT.copy()
WHITE_WEIGHTS['PLAYER'] = WHITE
WHITE_WEIGHTS['KING'] = 1.5

RED_WEIGHTS = WEIGHTS_DICT.copy()

for KING_WEIGHT in WEIGHTS_KING:
    for CENTRE_WEIGHT in WEIGHTS_CENTRE16:
        for FORWARD_WEIGHT in WEIGHTS_FORWARD:
            for HOME_WEIGHT in WEIGHTS_HOME_ROW:
                RED_WEIGHTS['KING'] = KING_WEIGHT
                RED_WEIGHTS['CENTRE'] = CENTRE_WEIGHT
                RED_WEIGHTS['FORWARD'] = FORWARD_WEIGHT
                RED_WEIGHTS['HOME'] = HOME_WEIGHT
                RED_WEIGHTS['PLAYER'] = RED

                print("Red")
                pprint.pprint(RED_WEIGHTS)
                print("White")
                pprint.pprint(WHITE_WEIGHTS)

                main(WHITE_WEIGHTS, RED_WEIGHTS)

                exit(0)




