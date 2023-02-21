from checkers.constants import RED
def log(f, text):
    print(text, end='')
    f.write(text)

def log_name(f, playcount, WHITE_WEIGHTS, RED_WEIGHTS):
     game_title = (f"{playcount} - "
             f"WHITE:K_{WHITE_WEIGHTS['KING']}|"
             f"C_{WHITE_WEIGHTS['CENTRE']}|"
             f"F_{WHITE_WEIGHTS['FORWARD']}|"
             f"H_{WHITE_WEIGHTS['HOME']}"
             f"_vs_"
             f"RED:K_{RED_WEIGHTS['KING']}|"
             f"C_{RED_WEIGHTS['CENTRE']}|"
             f"F_{RED_WEIGHTS['FORWARD']}|"
             f"H_{RED_WEIGHTS['HOME']}"
             "\n")
     log(f, game_title)

def log_game_state(f, player, board):
    PLAYER = "Red" if player == RED else "White"
    game_state = (
            f"{PLAYER} move: "
            f"R: {board.red_left - board.red_kings},{board.red_kings} - "
            f"W: {board.white_left - board.white_kings},{board.white_kings}\n"
            )
    log(f, game_state)
