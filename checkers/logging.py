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
            f"R: {board.red_left},{board.red_kings} - "
            f"W: {board.white_left},{board.white_kings}\n"
            )
    log(f, game_state)

def log_result(SCORE, results_file):
    """
    {
    'count': 1,
    'RK_W': 0.0,
    'RC_W': 0.0,
    'RF_W': 0.0,
    'RH_W': 0.2,
    'WK_W': 0.0,
    'WC_W': 0.0,
    'WF_W': 0.0,
    'WH_W': 0.0,
    'WINNER': 'White',
    'W_P': 6,
    'W_K': 1,
    'R_P': 1,
    'R_K': 0,
    'turns': 49}
    """

    with open(results_file, "a") as csv_file:
        csv_file.write(f"{SCORE['count']}, "
                        f"{SCORE['RK_W']}, {SCORE['RC_W']}, {SCORE['RF_W']}, {SCORE['RH_W']}, "
                        f"{SCORE['WK_W']}, {SCORE['WC_W']}, {SCORE['WF_W']}, {SCORE['WH_W']}, "
                        f"{SCORE['WINNER']}, "
                        f"{SCORE['W_P']}, {SCORE['W_K']}, "
                        f"{SCORE['R_P']}, {SCORE['R_K']}, "
                        f"{SCORE['turns']}\n")

