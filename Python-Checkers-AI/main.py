# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # remove pygame announcement
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
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

def main(WHITE_STRATEGY, RED_STRATEGY):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:  # always an AI player
            print("white's turn")
            pprint.pprint(WHITE_STRATEGY)
            # value, new_board = minimax(game.get_board(), 4, WHITE, game, WHITE_STRATEGY)
            value, new_board = minimax(game.get_board(), 4, True, game, WHITE_STRATEGY)
            game.ai_move(new_board)
        elif RED_STRATEGY is not None:  # human or AI for RED
            print("red's turn")
            pprint.pprint(RED_STRATEGY)
            # value, new_board = minimax(game.get_board(), 4, RED, game, RED_STRATEGY)
            value, new_board = minimax(game.get_board(), 4, True, game, RED_STRATEGY)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        if RED_STRATEGY is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()

    pygame.quit()

STRATEGY_KING = [int(x/2 * 10) * 0.1 for x in range(4, 10)]  # 3 - [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
STRATEGY_CENTRE16 = [int(int(x * 10) * 0.1)/10 for x in range(1, 11)]  # 0.5
STRATEGY_FORWARD = [int(int(x * 10) * 0.1)/10 for x in range(1, 11)]  # 0.3
STRATEGY_HOME_ROW = [int(int(x*2 * 10) * 0.1)/10 for x in range(1, 11)]  # 1

STRATEGY_DICT = {
    'KING': 0,
    'CENTRE': 0,
    'FORWARD': 0,
    'HOME': 0
}

WHITE_STRATEGY = STRATEGY_DICT.copy()
WHITE_STRATEGY['PLAYER'] = WHITE
WHITE_STRATEGY['KING'] = 1.5

RED_STRATEGY = STRATEGY_DICT.copy()

for KING_WEIGHT in STRATEGY_KING:
    for CENTRE_WEIGHT in STRATEGY_CENTRE16:
        for FORWARD_WEIGHT in STRATEGY_FORWARD:
            for HOME_WEIGHT in STRATEGY_HOME_ROW:
                RED_STRATEGY['KING'] = KING_WEIGHT
                RED_STRATEGY['CENTRE'] = CENTRE_WEIGHT
                RED_STRATEGY['FORWARD'] = FORWARD_WEIGHT
                RED_STRATEGY['HOME'] = HOME_WEIGHT
                RED_STRATEGY['PLAYER'] = RED

                print("Red")
                pprint.pprint(RED_STRATEGY)
                print("White")
                pprint.pprint(WHITE_STRATEGY)

                main(WHITE_STRATEGY, RED_STRATEGY)

                exit(0)




