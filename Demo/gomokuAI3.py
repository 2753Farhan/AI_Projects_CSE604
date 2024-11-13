import pygame
import sys
from math import inf
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Initialize screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku (Five in a Row) with AI")

# Board setup
board = [[None for _ in range(COLS)] for _ in range(ROWS)]
current_player = "black"  # Players alternate between "black" and "blue"

# Font
FONT = pygame.font.SysFont("comicsans", 30)

# AI settings
MAX_DEPTH = 3  # Maximum depth for minimax search

class GameState:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        
    def get_valid_moves(self):
        moves = []
        # Focus search on positions adjacent to existing stones
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is None and self.has_adjacent_stone(row, col):
                    moves.append((row, col))
        return moves if moves else [(row, col) for row in range(ROWS) 
                                  for col in range(COLS) 
                                  if self.board[row][col] is None]

    def has_adjacent_stone(self, row, col):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if (0 <= r < ROWS and 0 <= c < COLS and 
                    self.board[r][c] is not None):
                    return True
        return False

def evaluate_position(state, player):
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for row in range(ROWS):
        for col in range(COLS):
            if state.board[row][col] is None:
                continue
                
            for dr, dc in directions:
                sequence = get_sequence(state.board, row, col, dr, dc)
                if sequence:
                    length = len(sequence)
                    is_open = is_sequence_open(state.board, row, col, dr, dc)
                    
                    # Calculate score based on sequence properties
                    if sequence[0] == player:
                        multiplier = 1
                    else:
                        multiplier = -1.1  # Slightly prioritize blocking opponent
                    
                    # Score based on length and openness
                    if length >= 5:
                        score += multiplier * 10000
                    elif length == 4 and is_open:
                        score += multiplier * 1000
                    elif length == 4:
                        score += multiplier * 100
                    elif length == 3 and is_open:
                        score += multiplier * 50
                    elif length == 3:
                        score += multiplier * 10
                    elif length == 2 and is_open:
                        score += multiplier * 5
                    
    return score

def get_sequence(board, row, col, dr, dc):
    """Get sequence of same-colored stones starting from (row, col)"""
    sequence = []
    player = board[row][col]
    r, c = row, col
    
    while (0 <= r < ROWS and 0 <= c < COLS and 
           board[r][c] == player):
        sequence.append(player)
        r, c = r + dr, c + dc
        
    return sequence if len(sequence) >= 2 else []

def is_sequence_open(board, row, col, dr, dc):
    """Check if sequence has empty spaces at either end"""
    player = board[row][col]
    
    # Check before sequence
    r, c = row - dr, col - dc
    before_open = (0 <= r < ROWS and 0 <= c < COLS and 
                  board[r][c] is None)
    
    # Find end of sequence
    r, c = row, col
    while (0 <= r < ROWS and 0 <= c < COLS and 
           board[r][c] == player):
        r, c = r + dr, c + dc
    
    after_open = (0 <= r < ROWS and 0 <= c < COLS and 
                 board[r][c] is None)
    
    return before_open or after_open

def minimax(state, depth, alpha, beta, maximizing_player, player):
    if depth == 0:
        return evaluate_position(state, player), None
        
    valid_moves = state.get_valid_moves()
    if not valid_moves:
        return 0, None
        
    best_move = random.choice(valid_moves)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            row, col = move
            new_state = GameState(state.board)
            new_state.board[row][col] = player
            
            eval, _ = minimax(new_state, depth - 1, alpha, beta, False, player)
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
                
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
                
        return max_eval, best_move
    else:
        min_eval = float('inf')
        opponent = "blue" if player == "black" else "black"
        for move in valid_moves:
            row, col = move
            new_state = GameState(state.board)
            new_state.board[row][col] = opponent
            
            eval, _ = minimax(new_state, depth - 1, alpha, beta, True, player)
            
            if eval < min_eval:
                min_eval = eval
                best_move = move
                
            beta = min(beta, eval)
            if beta <= alpha:
                break
                
        return min_eval, best_move

def get_ai_move():
    state = GameState(board)
    _, move = minimax(state, MAX_DEPTH, float('-inf'), float('inf'), True, current_player)
    return move

def draw_grid():
    WIN.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(WIN, GRAY, rect, 1)
            if board[row][col] is not None:
                color = BLACK if board[row][col] == "black" else BLUE
                pygame.draw.circle(WIN, color, rect.center, CELL_SIZE // 2 - 5)
    pygame.display.update()

def check_win(row, col, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        start, end = (row, col), (row, col)
        
        # Check in positive direction
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                end = (r, c)
            else:
                break
        
        # Check in negative direction
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                start = (r, c)
            else:
                break

        if count >= 5:
            return start, end
    
    return None

def draw_winning_line(win_result):
    start, end = win_result
    start_pos = (start[1] * CELL_SIZE + CELL_SIZE // 2, start[0] * CELL_SIZE + CELL_SIZE // 2)
    end_pos = (end[1] * CELL_SIZE + CELL_SIZE // 2, end[0] * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.line(WIN, RED, start_pos, end_pos, 5)
    pygame.display.update()

def display_winner_message(player):
    WIN.fill(WHITE)
    message = f"{player.capitalize()} wins!"
    text = FONT.render(message, True, RED)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

def reset_game():
    global board, current_player
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    current_player = "black"
    draw_grid()

def place_stone(row, col):
    global current_player
    if board[row][col] is None:
        board[row][col] = current_player
        draw_grid()
        
        win_result = check_win(row, col, current_player)
        if win_result:
            draw_winning_line(win_result)
            pygame.display.update()
            pygame.time.delay(1000)
            display_winner_message(current_player)
            pygame.time.delay(2000)
            reset_game()
        else:
            current_player = "blue" if current_player == "black" else "black"
            
            # If it's AI's turn (blue player)
            if current_player == "blue":
                row, col = get_ai_move()
                place_stone(row, col)

def main():
    run = True
    draw_grid()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == "black":
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                place_stone(row, col)

if __name__ == "__main__":
    main()