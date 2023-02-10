from checkers.game import Game

game = Game()
print(game.whose_turn()) #1 or 2

print(game.get_possible_moves()) #[[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]

# game.move([9, 13])

# print(game.is_over()) #True or False

# game.get_winner() #None or 1 or 2

print("moves")
print(game.moves) #[[int, int], [int, int], ...]

game.consecutive_noncapture_move_limit = 20
game.move_limit_reached() #True or False

for piece in game.board.pieces:
    moves = piece.get_possible_positional_moves()
    if moves:
	    print(piece.player, piece.king, piece.position) #1-32
	    # print(piece.other_player) #1 or 2
	    # print(piece.captured) #True or False
	    print(piece.get_possible_capture_moves())
	    print(piece.get_possible_positional_moves())
