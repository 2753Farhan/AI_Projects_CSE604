# constants.py
import pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 600
ROWS, COLS = 10, 10
CELL_SIZE = BOARD_SIZE // COLS
BOARD_OFFSET_X = (WIDTH - BOARD_SIZE) // 2
BOARD_OFFSET_Y = (HEIGHT - BOARD_SIZE) // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (65, 105, 225)
GRAY = (130, 130, 130)
RED = (220, 50, 50)
GOLD = (255, 215, 0)
PURPLE = (147, 112, 219)
BG_COLOR = (25, 25, 50)
BOARD_COLOR = (40, 40, 70)
HIGHLIGHT_COLOR = (100, 100, 255, 128)
STAR_COLOR = (255, 255, 200)

# Game states
MENU = "menu"
PLAYING = "playing"
AI_THINKING = "ai_thinking"
GAME_OVER = "game_over"

# AI settings
MAX_DEPTH = 3

# Fonts
FONT_LARGE = pygame.font.SysFont("arial", 48, bold=True)
FONT_MEDIUM = pygame.font.SysFont("arial", 36)
FONT_SMALL = pygame.font.SysFont("arial", 24)
