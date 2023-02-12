from checkers.game import Game
from checkers.board_searcher import BoardSearcher
import pprint

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKRED = '\033[31m'
    OKYELLOW = '\033[33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


PAWNS = [None, 'o', 'x']
KINGS = [None, 'O', 'X']

def player_icon(piece):
    if piece.king:
        return KINGS[piece.player]
    else:
        return PAWNS[piece.player]

def display_board(game, move=None):
    highlight = lowlight = None
    if move:  # highlight the source and destination squares
        highlight = move[1]
        lowlight = move[0]
        start = bcolors.OKRED
        end = bcolors.ENDC

    if not game.is_over():
        print(f"Player {KINGS[game.whose_turn()]}'s turn")

    count = 0
    line = ""
    for row in positions:
        line = ""
        for position in row:
            if position:
                count += 1
                piece = game.board.searcher.get_piece_by_position(position)
                line += f"({' ' if position < 10 else ''}{position}) "
                if position == highlight:
                    line += bcolors.OKRED
                if position == lowlight:
                    line += bcolors.OKYELLOW
                line += f"{player_icon(piece) if piece else '_ '}"
                if position in [highlight, lowlight]:
                    line += bcolors.ENDC
                line += " "
            else:
                line += "   "
        print(line)

KING_VALUE = 3  # n x PAWN value (1)
HOME_ROW_VALUE = 1
CENTRE_16_VALUE = 1
JEOPARDY_VALUE = -1.5
FORWARD_VALUE = 1

def get_max_move(player=None, moves=None, recurse=True):
    MIN, MAX = get_min_max(player, moves, recurse)
    return MAX

def get_min_move(player=None, moves=None, recurse=True):
    MIN, MAX = get_min_max(player, moves, recurse)
    return MIN

def get_min_max(player=None, moves=None, recurse=True):
    if player is None:
        player = game.whose_turn()
    if moves is None:
        moves = game.get_possible_moves()

    # create new temporary board for each move
    scores_dict = {}
    for idx, move in enumerate(moves):
        # for each proposed move
        score = 0
        temp_board = game.board.create_new_board_from_move(move)
        searcher = BoardSearcher()
        searcher.build(temp_board)

        # number of pieces in jeapody after move
        """
        jeopardised = {1: 0, 2: 0}
        capture_moves = False
        for capture_move in temp_board.get_possible_capture_moves():
            aggressor = capture_move[0]
            piece = temp_board.searcher.get_piece_by_position(aggressor)
            jeopardised[piece.player] += 1
            capture_moves = True

        pprint.pprint(jeopardised)
        score += (jeopardised[player] - jeopardised[1+player%2] ) * JEOPARDY_VALUE
        print(jeopardised[player], jeopardised[1+player%2])
        """

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

            # average position forward of pawns
            if not piece.king:
                piece_row = int((piece.position-1)/4)
                if piece.player is not player:
                    piece_row = 8 - piece_row
                position_forward[piece.player].append(piece_row)

                # pieces about to crown - penultimate row and an available move
                if player == 1 and piece.position in [25, 26, 27, 28] and piece.is_movable() or \
                    player == 2 and piece.position in [ 5,  6,  7,  8] and piece.is_movable() or \
                    player == 1 and piece.position in [21, 22, 23, 24] and piece.get_possible_capture_moves() or \
                    player == 2 and piece.position in [ 9, 10, 11, 12] and piece.get_possible_capture_moves():
                        score += factor * KING_VALUE

        # position_forward
        if not len(position_forward[piece.player]) or not len(position_forward[piece.other_player]):
            # print(position_forward, idx, move)
            return (None, move)  # MIN, MAX - this move is a winning move

        player_ave_position = sum(position_forward[piece.player]) / len(position_forward[piece.player])
        opp_ave_position = sum(position_forward[piece.other_player]) / len(position_forward[piece.other_player])
        score += round(player_ave_position - opp_ave_position) * FORWARD_VALUE

        scores_dict[idx] = score

    # pprint.pprint(scores_dict)
    max_id = max(scores_dict, key=scores_dict.get)
    max_moves = [moves[idx] for idx, value in scores_dict.items() if value == scores_dict[max_id]]

    min_id = min(scores_dict, key=scores_dict.get)
    min_moves = [moves[idx] for idx, value in scores_dict.items() if value == scores_dict[min_id]]

    if len(max_moves) > 1 and recurse:  # should we go deeper
        move_max = get_min_move(player=1+game.whose_turn()%2, moves=max_moves, recurse=False)
    else:
        move_max = moves[max(scores_dict, key=scores_dict.get)]

    if len(min_moves) > 1 and recurse:  # should we go deeper
        move_min = get_min_move(player=1+game.whose_turn()%2, moves=min_moves, recurse=False)
    else:
        move_min = moves[min(scores_dict, key=scores_dict.get)]

    print("min: ", move_min, "max: ", move_max)
    return (move_min, move_max)

game = Game()
print("Game started")
GAME_MOVES = 0

move = None
while not game.is_over():

    display_board(game, move)
    # print(game.get_possible_moves()) #[[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]
    move = get_max_move()
    if move:
        print(f"moving player {KINGS[game.whose_turn()]} from {move[0]} to {move[1]}")
        game.move(move)  # [21, 17]
        GAME_MOVES += 1
        print("--------------------------------------------------------------")
    else:
        print("game over")
        display_board(game, move)
        print(game.get_winner())
        break

    x = input("hit a key for the next move")
    if x in ['x', 'q']:
        break
display_board(game)
print(f"Player {KINGS[game.get_winner()]} wins")

GAME_STATS = f"""
    Game:
        number of turns: {GAME_MOVES}
        winner         : {KINGS[game.get_winner()]}
    """
for player in [1, 2]:
    GAME_STATS += f"""
    Stats for {KINGS[player]}:
        pieces: {len([pawn for pawn in game.board.searcher.get_pieces_by_player(player) if not pawn.king])}
        kings: {len([pawn for pawn in game.board.searcher.get_pieces_by_player(player) if pawn.king])}

    """
print(GAME_STATS)
exit(0)
