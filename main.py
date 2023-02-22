from os import environ, path
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # remove pygame announcement
import pygame
import time
import os
from checkers.constants import (WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE,
                                WEIGHTS, WEIGHTS_KING, WEIGHTS_CENTRE16, WEIGHTS_FORWARD, WEIGHTS_HOME_ROW,
                                WEIGHTS_DICT, array_to_weights, log_result,
                                MINIMAX_DEPTH)
from checkers.logging import log, log_name, log_game_state
from checkers.game import Game
from minimax.algorithm import minimax
import pprint
import itertools

FPS = 60

pygame.init()
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
    GAME_SCORE = {
        'count': play_count,
        'RK_W': RED_WEIGHTS['KING'],
        'RC_W': RED_WEIGHTS['CENTRE'],
        'RF_W': RED_WEIGHTS['FORWARD'],
        'RH_W': RED_WEIGHTS['HOME'],
        'WK_W': WHITE_WEIGHTS['KING'],
        'WC_W': WHITE_WEIGHTS['CENTRE'],
        'WF_W': WHITE_WEIGHTS['FORWARD'],
        'WH_W': WHITE_WEIGHTS['HOME'],
        'R_P': 0,
        'R_K': 0,
        'W_P': 0,
        'W_K': 0,
        'WINNER': None,
        'WIN_P': 0,
        'WIN_K': 0,
        'LOSE_P': 0,
        'LOSE_K': 0,
        'turns': 0,
        }

    log_name(f, play_count, WHITE_WEIGHTS, RED_WEIGHTS)
    turns = 0
    board_history = []  # create a clean log of board positions

    prev_board = None
    while run:
        clock.tick(FPS)

        # pygame.event.get()
        # each turn
        turns += 1
        (player, opponent, WEIGHTS) = ("White", "Red", WHITE_WEIGHTS) if game.turn == WHITE else ("Red", "White", RED_WEIGHTS)

        alpha, beta = float('-inf'), float('inf')
        value, new_board = minimax(game.get_board(), MINIMAX_DEPTH, True, game, WEIGHTS, alpha, beta)
        if new_board:
            GAME_SCORE['R_P'] = new_board.red_left - new_board.red_kings
            GAME_SCORE['R_K'] = new_board.red_kings
            GAME_SCORE['W_P'] = new_board.white_left - new_board.white_kings
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
            run = False
            break
        board_history.append(board_str)

        if new_board is not None:
            log_game_state(f, game.turn, new_board)

        game.ai_move(new_board)

        prev_board = new_board

        if game.winner() != None:
            log(f, f"{opponent} won after {turns} turns.\n")
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

        game.update()
    # print("end of game triggered")
    (winner, loser) = 'W', 'R' if GAME_SCORE['WINNER'] == 'White' else ('R', 'W')
    GAME_SCORE['WIN_K'] = GAME_SCORE[f'{winner}_K']
    GAME_SCORE['WIN_P'] = GAME_SCORE[f'{winner}_P']
    GAME_SCORE['LOSE_K'] = GAME_SCORE[f'{loser}_K']
    GAME_SCORE['LOSE_P'] = GAME_SCORE[f'{loser}_P']
    log_result(GAME_SCORE, results_file)
    exit(0)

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

    strategies = [WEIGHTS_KING, WEIGHTS_CENTRE16, WEIGHTS_FORWARD, WEIGHTS_HOME_ROW]
    all_games = list(itertools.product(*strategies))

    timestr = time.strftime("%Y%m%d-%H%M%S")
    results_file = f"results/{timestr}results.csv"
    if not os.path.isfile(results_file):
        with open(results_file, "a") as csv_file:
            csv_file.write("count, RK_W, RC_W, RF_W, RH_W, "
                    "WK_W, WC_W, WF_W, WH_W,"
                    "Winner, WIN_P, WIN_K, LOSE_P, LOSE_K, turns\n")

    for x, y in itertools.permutations(all_games, 2):
        for X, Y in itertools.permutations([x, y], 2):
            WHITE_WEIGHTS = array_to_weights(X, WHITE)
            RED_WEIGHTS = array_to_weights(Y, RED)
            play_count += 1
            main(play_count, WHITE_WEIGHTS, RED_WEIGHTS, f)

exit(0)




