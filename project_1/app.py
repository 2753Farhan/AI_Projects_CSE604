import pygame
import sys
from board import Board
from constants import *

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Gomoku")

def main():
    board = Board(WIN)  # Pass WIN to Board
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(60)
        
        if board.game_state == MENU:
            board.draw_menu()
            board.handle_menu()
            
        elif board.game_state == PLAYING or board.game_state == AI_THINKING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if board.game_state == PLAYING:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if (board.game_mode == "human" or 
                            (board.game_mode == "ai" and board.current_player == "black")):
                            pos = board.get_board_position(event.pos)
                            if pos:
                                row, col = pos
                                board.place_stone(row, col)
                    
                    elif event.type == pygame.MOUSEMOTION:
                        if (board.game_mode == "human" or 
                            (board.game_mode == "ai" and board.current_player == "black")):
                            pos = board.get_board_position(event.pos)
                            board.draw_grid()
                            if pos:
                                row, col = pos
                                board.draw_hover(row, col)
                                
        elif board.game_state == GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if board.restart_button.handle_event(event):
                    board.game_state = MENU
                if board.quit_button.handle_event(event):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
