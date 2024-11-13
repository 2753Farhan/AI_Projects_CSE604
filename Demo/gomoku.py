import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # New color for the second player
GRAY = (200, 200, 200)
RED = (255, 0, 0)  # Line color for winning sequence

# Initialize screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku (Five in a Row)")

# Board setup
board = [[None for _ in range(COLS)] for _ in range(ROWS)]
current_player = "black"  # Players alternate between "black" and "blue"

# Font
FONT = pygame.font.SysFont("comicsans", 30)

def draw_grid():
    WIN.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(WIN, GRAY, rect, 1)

            # Draw stones if they exist
            if board[row][col] is not None:
                color = BLACK if board[row][col] == "black" else BLUE
                pygame.draw.circle(WIN, color, rect.center, CELL_SIZE // 2 - 5)

    pygame.display.update()

def place_stone(row, col):
    global current_player
    if board[row][col] is None:  # Place stone if cell is empty
        board[row][col] = current_player
        
        # Update the display to show the placed stone
        draw_grid()
        
        # Check if the current player wins
        win_result = check_win(row, col, current_player)
        if win_result:
            # Draw the winning line
            draw_winning_line(win_result)
            pygame.display.update()
            pygame.time.delay(1000)  # Pause for 1 second to show the line
            
            # Display the winning message
            display_winner_message(current_player)
            pygame.time.delay(2000)  # Pause for 2 seconds to show the winner message
            
            # Reset the game for a new round
            reset_game()
        else:
            # Switch player
            current_player = "blue" if current_player == "black" else "black"

def check_win(row, col, player):
    # Check all four directions for a consecutive 5 stones
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        start, end = (row, col), (row, col)
        
        # Check in the positive direction
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                end = (r, c)
            else:
                break
        
        # Check in the negative direction
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                start = (r, c)
            else:
                break

        # If we found 5 in a row, return the start and end points for drawing the line
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

def main():
    run = True
    draw_grid()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                place_stone(row, col)
                draw_grid()

if __name__ == "__main__":
    main()
