from copy import deepcopy
import pygame
from checkers.constants import ALPHA, BETA, RED, WHITE, DRAW_ALL_SUB_MOVES

def minimax(position, depth, max_player, game, WEIGHTS, alpha, beta):
    PLAYER = WEIGHTS['PLAYER']
    OPPONENT = WHITE if PLAYER == RED else RED
    # print(WEIGHTS)
    if depth == 0 or position.winner() != None:
        return position.evaluate(WEIGHTS), position

    (best_val, f) = (ALPHA, max) if max_player else (BETA, min)
    best_move = None

    for move in get_all_moves(position, PLAYER, game):
        evaluation = minimax(move, depth-1, not max_player, game, WEIGHTS, alpha, beta)[0]
        best_val = f(best_val, evaluation)
        if best_val == evaluation:
            best_move = move
        alpha = f(alpha, best_val)
        if beta <= alpha:
            break

    return best_val, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if DRAW_ALL_SUB_MOVES:
                draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

