import pygame
import sys
from math import inf
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 600
ROWS, COLS = 10, 10
CELL_SIZE = BOARD_SIZE // COLS
BOARD_OFFSET_X = (WIDTH - BOARD_SIZE) // 2
BOARD_OFFSET_Y = (HEIGHT - BOARD_SIZE) // 2

# Enhanced Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (65, 105, 225)
GRAY = (130, 130, 130)
RED = (220, 50, 50)
GOLD = (255, 215, 0)
PURPLE = (147, 112, 219)
BG_COLOR = (25, 25, 50)
BOARD_COLOR = (64, 95, 137)
HIGHLIGHT_COLOR = (100, 100, 255, 128)
STAR_COLOR = (255, 255, 200)

# Initialize screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Gomoku")

# Game states
MENU = "menu"
PLAYING = "playing"
AI_THINKING = "ai_thinking"
GAME_OVER = "game_over"

# Board setup
board = [[None for _ in range(COLS)] for _ in range(ROWS)]
current_player = "black"
game_state = MENU
game_mode = None  # "ai" or "human"

# AI settings
MAX_DEPTH = 3

# Enhanced Fonts
FONT_LARGE = pygame.font.SysFont("arial", 48, bold=True)
FONT_MEDIUM = pygame.font.SysFont("arial", 36)
FONT_SMALL = pygame.font.SysFont("arial", 24)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False

    def draw(self):
        color = (min(self.color[0] + 30, 255), 
                min(self.color[1] + 30, 255), 
                min(self.color[2] + 30, 255)) if self.hover else self.color
        pygame.draw.rect(WIN, color, self.rect, border_radius=10)
        pygame.draw.rect(WIN, WHITE, self.rect, 2, border_radius=10)
        text_surface = FONT_MEDIUM.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        WIN.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                return True
        return False

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.5)
        self.brightness = random.randint(150, 255)

    def update(self):
        self.y = (self.y + self.speed) % HEIGHT
        
    def draw(self):
        pygame.draw.circle(WIN, (self.brightness, self.brightness, self.brightness), 
                         (int(self.x), int(self.y)), self.size)

# Create stars
stars = [Star() for _ in range(100)]

# Buttons
ai_mode_button = Button(WIDTH//2 - 200, HEIGHT//2 - 50, 400, 50, "Play vs AI", PURPLE)
human_mode_button = Button(WIDTH//2 - 200, HEIGHT//2 + 50, 400, 50, "Play vs Human", BLUE)
restart_button = Button(WIDTH//2 - 180, HEIGHT//2 + 50, 160, 50, "Play Again", PURPLE)
quit_button = Button(WIDTH//2 + 20, HEIGHT//2 + 50, 160, 50, "Quit", RED)

# [Previous AI-related classes and functions remain the same: GameState, evaluate_position, 
# get_sequence, is_sequence_open, minimax, get_ai_move]
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

def evaluate_position(state, player):
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    weights = {
        5: 100000,    # Win
        4: {
            'open': 50000,    # Open four (winning threat)
            'closed': 10000   # Closed four
        },
        3: {
            'open': 5000,     # Open three (major threat)
            'closed': 1000,   # Closed three
            'blocking': 7500  # Blocking opponent's 3 in a row
        },
        2: {
            'open': 500,      # Open two
            'closed': 100     # Closed two
        }
    }
    
    for row in range(ROWS):
        for col in range(COLS):
            if state.board[row][col] is None:
                continue
            
            for dr, dc in directions:
                sequence, gap_position, is_double_open = get_sequence(state.board, row, col, dr, dc)
                if not sequence:
                    continue
                
                length = len(sequence)
                current_player = sequence[0]
                
                if row > 0 and col > 0:
                    prev_r, prev_c = row - dr, col - dc
                    if (0 <= prev_r < ROWS and 0 <= prev_c < COLS and 
                        state.board[prev_r][prev_c] == current_player):
                        continue
                
                pattern_type = 'open' if is_double_open else 'closed'
                
                # Calculate pattern score
                if length >= 5:
                    pattern_score = weights[5]
                elif length >= 4:
                    pattern_score = weights[4][pattern_type]
                elif length >= 3:
                    # Modified logic for three-in-a-row patterns
                    if is_double_open:
                        if current_player != player:
                            # If it's opponent's three in a row and double open,
                            # consider it as blocking priority
                            pattern_score = weights[3]['blocking']
                        else:
                            pattern_score = weights[3]['open']
                    else:
                        pattern_score = weights[3][pattern_type]
                elif length >= 2:
                    pattern_score = weights[2][pattern_type]
                else:
                    continue
                
                # Adjust scores for opponent's threats
                if current_player != player:
                    if length >= 4:
                        pattern_score *= 1.2
                    if is_double_open and length >= 3:
                        pattern_score *= 1.1
                
                multiplier = 1 if current_player == player else -1
                score += multiplier * pattern_score
                
                # Add position bonus
                center_row, center_col = ROWS // 2, COLS // 2
                distance_to_center = abs(row - center_row) + abs(col - center_col)
                position_bonus = 50 * (1 / (distance_to_center + 1))
                score += position_bonus * multiplier
    
    return score

def get_sequence(board, row, col, dr, dc):
    sequence = []
    player = board[row][col]
    
    # Check backwards first to find start of sequence
    r, c = row - dr, col - dc
    backwards_empty = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] is None:
        backwards_empty += 1
        r, c = r - dr, c - dc
    
    # Now check forwards
    r, c = row, col
    gap_found = False
    gap_position = None
    forwards_empty = 0
    
    for i in range(5):
        if not (0 <= r < ROWS and 0 <= c < COLS):
            break
        
        current = board[r][c]
        if current == player:
            sequence.append(current)
        elif current is None and not gap_found:
            gap_found = True
            gap_position = len(sequence)
            forwards_empty += 1
        elif current is None:
            forwards_empty += 1
            break
        else:
            break
        
        r, c = r + dr, c + dc
    
    is_double_open = (backwards_empty > 0 and forwards_empty > 0)
    return sequence, gap_position, is_double_open

def is_sequence_open(board, row, col, dr, dc):
    player = board[row][col]
    sequence_length = len(get_sequence(board, row, col, dr, dc))
    
    r, c = row - dr, col - dc
    before_open = (0 <= r < ROWS and 0 <= c < COLS and 
                  board[r][c] is None)
    
    r, c = row + (sequence_length * dr), col + (sequence_length * dc)
    after_open = (0 <= r < ROWS and 0 <= c < COLS and 
                 board[r][c] is None)
    
    if before_open and after_open:
        return 2
    elif before_open or after_open:
        return 1
    return 0

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
        opponent = "white" if player == "black" else "black"
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

def draw_stars():
    for star in stars:
        star.update()
        star.draw()

def draw_menu():
    WIN.fill(BG_COLOR)
    draw_stars()
    
    title = FONT_LARGE.render("Cosmic Gomoku", True, GOLD)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//3))
    WIN.blit(title, title_rect)
    
    ai_mode_button.draw()
    human_mode_button.draw()
    
    pygame.display.update()
    
def get_board_position(pos):
    x, y = pos
    row = (y - BOARD_OFFSET_Y) // CELL_SIZE
    col = (x - BOARD_OFFSET_X) // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None

def handle_menu():
    global game_state, game_mode
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if ai_mode_button.handle_event(event):
            game_mode = "ai"
            game_state = PLAYING
            reset_game()
            return
            
        if human_mode_button.handle_event(event):
            game_mode = "human"
            game_state = PLAYING
            reset_game()
            return

def draw_grid():
    WIN.fill(BG_COLOR)
    draw_stars()
    
    board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE)
    pygame.draw.rect(WIN, BOARD_COLOR, board_rect)
    
    for i in range(ROWS + 1):
        start_x = BOARD_OFFSET_X
        start_y = BOARD_OFFSET_Y + i * CELL_SIZE
        end_x = BOARD_OFFSET_X + BOARD_SIZE
        end_y = start_y
        pygame.draw.line(WIN, GRAY, (start_x, start_y), (end_x, end_y), 1)
        
        start_x = BOARD_OFFSET_X + i * CELL_SIZE
        start_y = BOARD_OFFSET_Y
        end_x = start_x
        end_y = BOARD_OFFSET_Y + BOARD_SIZE
        pygame.draw.line(WIN, GRAY, (start_x, start_y), (end_x, end_y), 1)
    
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] is not None:
                x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                color = BLACK if board[row][col] == "black" else WHITE
                for i in range(5):
                    radius = CELL_SIZE // 2 - 5 - i
                    alpha = 255 - i * 30
                    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surface, (*color, alpha), (radius, radius), radius)
                    WIN.blit(surface, (x - radius, y - radius))
    
    # Update turn indicator based on game mode
    if game_mode == "ai":
        turn_text = f"{'Your' if current_player == 'black' else 'AI'}'s Turn"
        if game_state == AI_THINKING:
            turn_text = "AI is thinking..."
    else:
        turn_text = f"{'Black' if current_player == 'black' else 'White'}'s Turn"
    
    text_surface = FONT_MEDIUM.render(turn_text, True, GOLD)
    WIN.blit(text_surface, (20, 20))
    
    pygame.display.update()
    
    
def draw_hover(row, col):
    if board[row][col] is None and 0 <= row < ROWS and 0 <= col < COLS:
        x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
        surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(surface, HIGHLIGHT_COLOR, 
                         (CELL_SIZE // 2, CELL_SIZE // 2), 
                         CELL_SIZE // 2 - 5)
        WIN.blit(surface, (x - CELL_SIZE // 2, y - CELL_SIZE // 2))
        pygame.display.update()

def check_win(row, col, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        start, end = (row, col), (row, col)
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                end = (r, c)
            else:
                break
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                start = (r, c)
            else:
                break
        if count >= 5:
            return start, end
    return

def draw_winning_line(win_result):
    start, end = win_result
    start_pos = (BOARD_OFFSET_X + start[1] * CELL_SIZE + CELL_SIZE // 2, 
                BOARD_OFFSET_Y + start[0] * CELL_SIZE + CELL_SIZE // 2)
    end_pos = (BOARD_OFFSET_X + end[1] * CELL_SIZE + CELL_SIZE // 2, 
              BOARD_OFFSET_Y + end[0] * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.line(WIN, RED, start_pos, end_pos, 8)
    pygame.display.update()



def display_winner_message(player):
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 180))
    WIN.blit(surface, (0, 0))
    
    if game_mode == "ai":
        message = f"{'You won!' if player == 'black' else 'AI won!'}"
    else:
        message = f"{'Black' if player == 'black' else 'White'} won!"
    
    text = FONT_LARGE.render(message, True, GOLD)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()))
    
    restart_button.draw()
    quit_button.draw()
    pygame.display.update()

def reset_game():
    global board, current_player, game_state
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    current_player = "black"
    game_state = PLAYING
    draw_grid()

def place_stone(row, col):
    global current_player, game_state
    
    if board[row][col] is None:
        board[row][col] = current_player
        draw_grid()
        
        win_result = check_win(row, col, current_player)
        if win_result:
            draw_winning_line(win_result)
            pygame.time.delay(500)
            display_winner_message(current_player)
            game_state = GAME_OVER
        else:
            current_player = "white" if current_player == "black" else "black"
            if game_mode == "ai" and current_player == "white":
                game_state = AI_THINKING
                draw_grid()
                pygame.time.delay(500)
                row, col = get_ai_move()
                game_state = PLAYING
                place_stone(row, col)

def main():
    global game_state
    
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(60)
        
        if game_state == MENU:
            draw_menu()
            handle_menu()
            
        elif game_state == PLAYING or game_state == AI_THINKING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if game_state == PLAYING:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if (game_mode == "human" or 
                            (game_mode == "ai" and current_player == "black")):
                            pos = get_board_position(event.pos)
                            if pos:
                                row, col = pos
                                place_stone(row, col)
                    
                    elif event.type == pygame.MOUSEMOTION:
                        if (game_mode == "human" or 
                            (game_mode == "ai" and current_player == "black")):
                            pos = get_board_position(event.pos)
                            draw_grid()
                            if pos:
                                row, col = pos
                                draw_hover(row, col)
                                
        elif game_state == GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if restart_button.handle_event(event):
                    game_state = MENU
                if quit_button.handle_event(event):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()