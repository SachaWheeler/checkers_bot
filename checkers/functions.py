import pprint


def array_to_weights(variables, player):
    (K, C, F, H) = variables
    return {
            'KING': K,
            'CENTRE': C,
            'FORWARD': F,
            'HOME': H,
            'PLAYER': player
            }


def get_score(WHITE_WEIGHTS, RED_WEIGHTS):
    return {
        # 'count': play_count,
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
        'turns': 0
    }


def get_game_str(WEIGHTS):
    return (
            f"Kings: {WEIGHTS['KING']}, "
            f"Centre: {WEIGHTS['CENTRE']}, "
            f"Forward: {WEIGHTS['FORWARD']}, "
            f"Home: {WEIGHTS['HOME']}")

