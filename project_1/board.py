import sys
import pygame
from constants import *
from gui_elements import Button, Star
from game_logic import check_win, get_ai_move

class Board:
    def __init__(self, WIN):  # Add WIN as a parameter
        self.WIN = WIN  # Store WIN as an instance variable
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = "black"
        self.game_state = MENU
        self.game_mode = None
        self.stars = [Star() for _ in range(100)]
        
        # Initialize buttons
        self.ai_mode_button = Button(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 50, "Play vs AI", PURPLE)
        self.human_mode_button = Button(WIDTH // 2 - 200, HEIGHT // 2 + 50, 400, 50, "Play vs Human", BLUE)
        self.restart_button = Button(WIDTH // 2 - 180, HEIGHT // 2 + 50, 160, 50, "Play Again", PURPLE)
        self.quit_button = Button(WIDTH // 2 + 20, HEIGHT // 2 + 50, 160, 50, "Quit", RED)

    def draw_stars(self):
        for star in self.stars:
            star.update()
            star.draw(self.WIN)

    def draw_menu(self):
        self.WIN.fill(BG_COLOR)
        self.draw_stars()
        
        title = FONT_LARGE.render("Cosmic Gomoku", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.WIN.blit(title, title_rect)
        
        self.ai_mode_button.draw(self.WIN)
        self.human_mode_button.draw(self.WIN)
        
        pygame.display.update()

    def get_board_position(self, pos):
        x, y = pos
        row = (y - BOARD_OFFSET_Y) // CELL_SIZE
        col = (x - BOARD_OFFSET_X) // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            return row, col
        return None

    def handle_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.ai_mode_button.handle_event(event):
                self.game_mode = "ai"
                self.game_state = PLAYING
                self.reset_game()
                return
                
            if self.human_mode_button.handle_event(event):
                self.game_mode = "human"
                self.game_state = PLAYING
                self.reset_game()
                return

    def draw_grid(self):
        self.WIN.fill(BG_COLOR)
        self.draw_stars()
        
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE)
        pygame.draw.rect(self.WIN, BOARD_COLOR, board_rect)
        
        for i in range(ROWS + 1):
            start_x = BOARD_OFFSET_X
            start_y = BOARD_OFFSET_Y + i * CELL_SIZE
            end_x = BOARD_OFFSET_X + BOARD_SIZE
            end_y = start_y
            pygame.draw.line(self.WIN, GRAY, (start_x, start_y), (end_x, end_y), 1)
            
            start_x = BOARD_OFFSET_X + i * CELL_SIZE
            start_y = BOARD_OFFSET_Y
            end_x = start_x
            end_y = BOARD_OFFSET_Y + BOARD_SIZE
            pygame.draw.line(self.WIN, GRAY, (start_x, start_y), (end_x, end_y), 1)
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is not None:
                    x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                    y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                    color = BLACK if self.board[row][col] == "black" else WHITE
                    pygame.draw.circle(self.WIN, color, (x, y), CELL_SIZE // 2 - 5)
        
        turn_text = f"{'Your' if self.current_player == 'black' else 'AI'}'s Turn" if self.game_mode == "ai" else f"{'Black' if self.current_player == 'black' else 'White'}'s Turn"
        
        text_surface = FONT_MEDIUM.render(turn_text, True, GOLD)
        self.WIN.blit(text_surface, (20, 20))
        
        pygame.display.update()

    def draw_hover(self, row, col):
        if self.board[row][col] is None and 0 <= row < ROWS and 0 <= col < COLS:
            x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
            surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(surface, HIGHLIGHT_COLOR, 
                               (CELL_SIZE // 2, CELL_SIZE // 2), 
                               CELL_SIZE // 2 - 5)
            self.WIN.blit(surface, (x - CELL_SIZE // 2, y - CELL_SIZE // 2))
            pygame.display.update()

    def reset_game(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = "black"
        self.game_state = PLAYING
        self.draw_grid()

    def place_stone(self, row, col):
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.draw_grid()
            
            win_result = check_win(row, col, self.current_player)
            if win_result:
                self.draw_winning_line(win_result)
                pygame.time.delay(500)
                self.display_winner_message(self.current_player)
                self.game_state = GAME_OVER
            else:
                self.current_player = "white" if self.current_player == "black" else "black"
                if self.game_mode == "ai" and self.current_player == "white":
                    self.game_state = AI_THINKING
                    self.draw_grid()
                    pygame.time.delay(500)
                    row, col = get_ai_move()
                    self.game_state = PLAYING
                    self.place_stone(row, col)
