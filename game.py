from checkers.game import Game
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
players = [None, 'o', 'x']

def print_board():
    line = ""
    print(f"Player {players[game.whose_turn()]}'s turn")

    count = 0
    for row in positions:
        line = ""
        for position in row:
            if position:
                count += 1
                piece = game.board.searcher.get_piece_by_position(position)
                line += f"({' ' if position < 10 else ''}{position}) {players[piece.player] if piece else '_ '} "
            else:
                line += "   "
        print(line)

KING_VALUE = 3  # n x PAWN value (1)
HOME_ROW_VALUE = 1
CENTRE_16_VALUE = 1

def get_best_move():
    player = game.whose_turn()
    moves = game.get_possible_moves()
    # create new temporary board for each move
    scores_dict = {}
    for idx, move in enumerate(moves):
        # print(idx)
        score = 0
        temp_board = game.board.create_new_board_from_move(move)
        # pprint.pprint(temp_board)
        # assess who has more pieces and kings
        for piece in temp_board.searcher.uncaptured_pieces:
            # print(piece.position, piece.player, piece.king)
            factor = 1 if piece.player == player else -1

            # number of pawns, kings that aren't blocked
            val = KING_VALUE if piece.king and piece.is_movable() else 1
            score += factor * val

            # home row cover vs opp
            if player == 1 and piece.position in [1, 2, 3, 4] or \
                player == 2 and piece.position in [29, 30, 31, 32]:
                    score += factor * HOME_ROW_VALUE

            # count of center 16 vs opp
            if piece.position in [10, 11, 14, 15, 18, 19, 22, 23]:
                    score += factor * CENTRE_16_VALUE

            # pieces about to crown vs opp
            # number of pices in jearpody vs opp
            # print(val, score)

        scores_dict[idx] = score

    print("x")
    pprint.pprint(scores_dict)
    best_move = moves[max(scores_dict, key=scores_dict.get)]
    return best_move

while not game.is_over():

    print_board()
    print(game.get_possible_moves()) #[[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]
    move = get_best_move()
    print(f"moving player {game.whose_turn()} from {move[0]} to {move[1]}")
    game.move(move)  # [21, 17]

    x = input("hit a key for the next move")
    if x in ['x', 'q']:
        break
print(f"Player {game.get_winner()} wins")

exit(0)
