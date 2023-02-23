from os import environ, path
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # remove pygame announcement
import pygame
import time
import os
from checkers.constants import (WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLUE, GREY,
                                WEIGHTS, WEIGHTS_KING, WEIGHTS_CENTRE16, WEIGHTS_FORWARD, WEIGHTS_HOME_ROW,
                                WEIGHTS_DICT, array_to_weights, log_result,
                                get_score,
                                MINIMAX_DEPTH, ALPHA, BETA)
from checkers.logging import log, log_name, log_game_state, get_game_str
from checkers.game import Game
from minimax.algorithm import minimax
import pprint
import itertools

FPS = 60

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main(play_count, WHITE_WEIGHTS, RED_WEIGHTS, f):
    run = True

    pygame.init()
    # all_fonts = pygame.font.get_fonts()
    # pprint.pprint(all_fonts)
    # exit(0)
    white_title = get_game_str(WHITE_WEIGHTS)
    red_title = get_game_str(RED_WEIGHTS)
    pygame.display.set_caption('Checkers')
    clock = pygame.time.Clock()

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    game = Game(WIN, [white_title, red_title])
    GAME_SCORE = get_score(WHITE_WEIGHTS, RED_WEIGHTS)
    GAME_SCORE['count'] = play_count

    log_name(f, play_count, WHITE_WEIGHTS, RED_WEIGHTS)
    turns = 0
    board_history = []  # create a clean log of board positions

    prev_board = None
    while run:
        clock.tick(FPS)

        # each turn
        turns += 1
        (player, opponent, WEIGHTS) = ("White", "Red", WHITE_WEIGHTS) if game.turn == WHITE else ("Red", "White", RED_WEIGHTS)

        value, new_board = minimax(game.get_board(), MINIMAX_DEPTH, True,
                                   game, WEIGHTS, ALPHA, BETA)

        if new_board:
            GAME_SCORE['R_P'] = max(new_board.red_left - new_board.red_kings, 0)
            GAME_SCORE['R_K'] = new_board.red_kings
            GAME_SCORE['W_P'] = max(new_board.white_left - new_board.white_kings, 0)
            GAME_SCORE['W_K'] = new_board.white_kings


        if new_board is None:
            # game is over for player with no available moves
            log(f, f"{player} has no valid moves. {opponent} won after {turns} turns.\n")
            GAME_SCORE['WINNER'] = opponent
            GAME_SCORE['turns'] = turns
            run = False
            break

        board_str = new_board.to_string()
        if board_str in board_history:  # we've been here before
            log(f, f"game ended in a draw\n")
            GAME_SCORE['turns'] = turns
            run = False
            break
        board_history.append(board_str)

        if new_board is not None:
            log_game_state(f, game.turn, new_board)

        game.ai_move(new_board)

        prev_board = new_board

        if game.winner() != None:
            log(f, f"{player} won after {turns} turns.\n")
            GAME_SCORE['WINNER'] = player
            GAME_SCORE['turns'] = turns
            run = False
            break

        #if RED_WEIGHTS is None:  # human opponent
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        """
        if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        game.select(row, col)
        """

        # pygame.display.flip()
        game.update()
        # pygame.image.save(WIN, f"screens/{play_count}-{turns}.jpeg")
    # print("end of game triggered")
    GAME_SCORE['turns'] = turns
    log_result(GAME_SCORE, results_file)
    # save screen
    pygame.image.save(WIN, f"screens/{play_count:04}-{GAME_SCORE['WINNER']}.jpeg")

    pygame.quit()
    # exit(0)

i = 0
while path.exists("logs/log%s.txt" % i):
    i += 1

play_count = 0
with open("logs/log%s.txt" % i, 'w') as f:

    strategies = [WEIGHTS_KING, WEIGHTS_CENTRE16, WEIGHTS_FORWARD, WEIGHTS_HOME_ROW]
    all_games = list(itertools.product(*strategies))

    timestr = time.strftime("%Y%m%d-%H%M%S")
    results_file = f"results/{timestr}-results.csv"
    if not os.path.isfile(results_file):
        with open(results_file, "a") as csv_file:
            csv_file.write("count, RK_W, RC_W, RF_W, RH_W, "
                    "WK_W, WC_W, WF_W, WH_W,"
                    "Winner, W_P, W_K, R_P, R_K, turns\n")

    for x, y in itertools.permutations(all_games, 2):
        for X, Y in itertools.permutations([x, y], 2):
            WHITE_WEIGHTS = array_to_weights(X, WHITE)
            RED_WEIGHTS = array_to_weights(Y, RED)
            play_count += 1
            main(play_count, WHITE_WEIGHTS, RED_WEIGHTS, f)

exit(0)




