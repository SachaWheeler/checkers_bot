# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
from os import environ, path
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # remove pygame announcement
import pygame
from checkers.constants import (WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE,
                                WEIGHTS_KING, WEIGHTS_CENTRE16, WEIGHTS_FORWARD, WEIGHTS_HOME_ROW,
                                WEIGHTS_DICT,
                                log, log_name, log_game_state, opponent)
from checkers.game import Game
from minimax.algorithm import minimax
import pprint

FPS = 60

pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main(play_count, WHITE_WEIGHTS, RED_WEIGHTS, f):
    run = True
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(WIN)

    log_name(f, play_count, WHITE_WEIGHTS, RED_WEIGHTS)
    turns = 0

    prev_board = None
    while run:
        clock.tick(FPS)

        pygame.event.get()
        # each turn
        turns += 1
        player = "White" if game.turn == WHITE else "Red"
        opposing = opponent(game.turn)
        WEIGHTS = WHITE_WEIGHTS if game.turn == WHITE else RED_WEIGHTS
        value, new_board = minimax(game.get_board(), 4, True, game, WEIGHTS)

        if new_board is None:
            # game is over for player with no available moves
            log(f, f"{opposing} won after {turns} turns.\n")
            run = False
            break

        if new_board is not None:
            log_game_state(f, game.turn, new_board)

        game.ai_move(new_board)

        prev_board = new_board

        if game.winner() != None:
            log(f, f"{opposing} won after {turns} turns.\n")
            run = False
            break

        if RED_WEIGHTS is None:  # human opponent
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

i = 0
while path.exists("logs/log%s.txt" % i):
    i += 1

play_count = 0
with open("logs/log%s.txt" % i, 'w') as f:
    for KING_WEIGHT in WEIGHTS_KING:
        for CENTRE_WEIGHT in WEIGHTS_CENTRE16:
            for FORWARD_WEIGHT in WEIGHTS_FORWARD:
                for HOME_WEIGHT in WEIGHTS_HOME_ROW:
                    RED_WEIGHTS['KING'] = KING_WEIGHT
                    RED_WEIGHTS['CENTRE'] = CENTRE_WEIGHT
                    RED_WEIGHTS['FORWARD'] = FORWARD_WEIGHT
                    RED_WEIGHTS['HOME'] = HOME_WEIGHT
                    RED_WEIGHTS['PLAYER'] = RED

                    play_count += 1
                    main(play_count, WHITE_WEIGHTS, RED_WEIGHTS, f)

exit(0)




