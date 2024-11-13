from constants import *

class GameState:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        
    def get_valid_moves(self):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is None and self.has_adjacent_stone(row, col):
                    moves.append((row, col))
        return moves if moves else [(row, col) for row in range(ROWS) for col in range(COLS) if self.board[row][col] is None]

    def has_adjacent_stone(self, row, col):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if (0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] is not None):
                    return True
        return False
