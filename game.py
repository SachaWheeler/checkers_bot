from checkers.game import Game
from checkers.board_searcher import BoardSearcher
import pprint

game = Game()
print("Game started")

positions = [
    [29, None, 30, None, 31, None, 32, None],
    [None, 25, None, 26, None, 27, None, 28],
    [21, None, 22, None, 23, None, 24, None],
    [None, 17, None, 18, None, 19, None, 20],
    [13, None, 14, None, 15, None, 16, None],
    [None, 9, None, 10, None, 11, None, 12],
    [5, None, 6, None, 7, None, 8, None],
    [None, 1, None, 2, None, 3, None, 4]
]

PAWNS = [None, 'o', 'x']
KINGS = [None, 'O', 'X']

def player_icon(piece):
    if piece.king:
        return KINGS[piece.player]
    else:
        return PAWNS[piece.player]

def display_board(game):
    line = ""
    print(f"Player {PAWNS[game.whose_turn()]}'s turn")

    count = 0
    for row in positions:
        line = ""
        for position in row:
            if position:
                count += 1
                piece = game.board.searcher.get_piece_by_position(position)
                line += f"({' ' if position < 10 else ''}{position}) {player_icon(piece) if piece else '_ '} "
            else:
                line += "   "
        print(line)

KING_VALUE = 3  # n x PAWN value (1)
HOME_ROW_VALUE = 1
CENTRE_16_VALUE = 1
JEOPARDY_VALUE = -1.5

def get_best_move():
    MIN, MAX = get_min_max()
    return MAX

def get_min_max():
    player = game.whose_turn()
    moves = game.get_possible_moves()
    # create new temporary board for each move
    scores_dict = {}
    for idx, move in enumerate(moves):

        score = 0
        temp_board = game.board.create_new_board_from_move(move)
        searcher = BoardSearcher()
        searcher.build(temp_board)

        # number of pieces in jeapody after move
        jeopardy = []
        for capture_move in temp_board.get_possible_capture_moves():
            print("move: ", move)
            # print("agg: ", capture_move)
            if capture_move[0] not in jeopardy:
                jeopardy.append(capture_move[0])
            score += len(jeopardy) * JEOPARDY_VALUE
            print("in jeopardy: ", jeopardy)
        # print(val, score

        position_forward = {1: [], 2: []}
        for piece in temp_board.searcher.uncaptured_pieces:
            # print(piece.position, piece.player, piece.king)
            factor = 1 if piece.player == player else -1

            # number of pawns, kings that aren't blocked
            val = KING_VALUE if piece.king and piece.is_movable() else 1
            score += factor * val

            # home row cover vs opp
            if player == 1 and piece.position in [ 1,  2,  3,  4] or \
               player == 2 and piece.position in [29, 30, 31, 32]:
                    score += factor * HOME_ROW_VALUE

            # count of center 16 vs opp
            if piece.position in [10, 11, 14, 15, 18, 19, 22, 23]:
                score += factor * CENTRE_16_VALUE

            # average position forward
            piece_row = int((piece.position-1)/4)
            if piece.player is not player:
                piece_row = 8 - piece_row
            position_forward[piece.player].append(piece_row)

            # pieces about to crown - penultimate row and an available move
            if player == 1 and piece.position in [25, 26, 27, 28] or \
               player == 2 and piece.position in [ 5,  6,  7,  8]:
                if not piece.king and piece.is_movable():  # we can crown
                    score += factor * KING_VALUE

        # position_forward
        player_ave = sum(position_forward[piece.player]) / len(position_forward[piece.player])
        opp_ave = sum(position_forward[piece.other_player]) / len(position_forward[piece.other_player])
        score += round(player_ave - opp_ave)
        scores_dict[idx] = score

    print("final: ")
    pprint.pprint(scores_dict)
    max_id = max(scores_dict, key=scores_dict.get)
    print("max: ", max_id, scores_dict[max_id], moves[max_id])
    print("max moves: ", [idx for idx, value in scores_dict.items() if value == scores_dict[max_id]])
    min_id = min(scores_dict, key=scores_dict.get)
    print("min: ", min_id, scores_dict[min_id], moves[min_id])
    print("min moves: ", [idx for idx, value in scores_dict.items() if value == scores_dict[min_id]])

    move_max = moves[max(scores_dict, key=scores_dict.get)]
    move_min = moves[min(scores_dict, key=scores_dict.get)]
    return (move_min, move_max)

while not game.is_over():

    display_board(game)
    print(game.get_possible_moves()) #[[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]
    move = get_best_move()
    print(f"moving player {game.whose_turn()} from {move[0]} to {move[1]}")
    game.move(move)  # [21, 17]

    x = input("hit a key for the next move")
    if x in ['x', 'q']:
        break
print(f"Player {game.get_winner()} wins")

exit(0)
