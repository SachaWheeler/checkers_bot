import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, WIDTH
from checkers.board import Board

class Game:
    def __init__(self, win, titles):
        self._init()
        self.win = win
        self.titles = titles  # [white, red]

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

        title_font = pygame.font.Font(None, 20)
        text_font = pygame.font.Font(None, 24)

        white_status = f"White: {self.board.white_left},{self.board.white_kings}"
        red_status = f"Red  : {self.board.red_left},{self.board.red_kings}"

        white_desc_text = title_font.render(self.titles[0], True, WHITE, (0, 0, 0))
        red_desc_text = title_font.render(self.titles[1], True, WHITE, (0, 0, 0))

        white_status_text = text_font.render(white_status, True, WHITE, (0, 0, 0))
        red_status_text = text_font.render(red_status, True, WHITE, (0, 0, 0))

        self.win.blit(red_desc_text, (20 , 820))
        self.win.blit(white_desc_text, (WIDTH // 2 + 20 , 820))
        self.win.blit(red_status_text, (20 , 840))
        self.win.blit(white_status_text, (WIDTH // 2 + 20 , 840))
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
