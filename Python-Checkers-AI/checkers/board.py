import pygame
from .constants import (BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE,
                        CENTRE_16,
                        SCORE_KING, SCORE_CENTRE16, SCORE_FORWARD, SCORE_HOME_ROW,
                        SIMPLE_STRATEGY)
from .piece import Piece
import pprint

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self, STRATEGY):
        # print(f"evaluating: {STRATEGY}")
        PLAYER = STRATEGY['PLAYER']
        FACTOR = -1 if PLAYER == RED else 1

        pawns_score = (self.white_left - self.red_left) * 1 if PLAYER == WHITE else -1  # pawns

        kings_score = pawns_score * STRATEGY['KING']            # kings
        centre16_score = forward_score = home_row_score = 0

        for row in self.board:  # position scores
            for piece in row:
                if piece != 0:
                    PLAYER_PIECE = piece.color == PLAYER
                    # CENTRE 16 scores
                    if piece.row in CENTRE_16 and piece.col in CENTRE_16:
                        if PLAYER_PIECE:
                            centre16_score += STRATEGY['CENTRE']
                        else:
                            centre16_score -= STRATEGY['CENTRE']

                    # forward scores for pawns
                    if not piece.king:
                        row_id = piece.row if piece.color == WHITE else (7 - piece.row)
                        if PLAYER_PIECE:
                            forward_score += row_id * STRATEGY['FORWARD']
                        else:
                            forward_score -= row_id * STRATEGY['FORWARD']

                        # and homerow score
                        if piece.row == 0 and piece.color == WHITE or piece.row == 7 and piece.color == RED:
                            if PLAYER_PIECE:
                                home_row_score += FACTOR * STRATEGY['HOME']
                            else:
                                home_row_score -= FACTOR * STRATEGY['HOME']

        pawns_score= float("{:.1f}".format(pawns_score))
        kings_score= float("{:.1f}".format(kings_score))
        centre16_score= float("{:.1f}".format(centre16_score))
        forward_score= float("{:.1f}".format(forward_score))
        home_row_score= float("{:.1f}".format(home_row_score))
        # print(pawns_score, kings_score, centre16_score, forward_score, home_row_score)
        return pawns_score + kings_score + centre16_score + forward_score + home_row_score

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        PIECE_IS_PAWN = not piece.king
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # if row == ROWS - 1 or row == 0:
        if PIECE_IS_PAWN and row in [ROWS - 1, 0]:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))

        # pprint.pprint(moves)
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
