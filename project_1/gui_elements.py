# gui_elements.py
import pygame
import random
from constants import *

class Button:
    def __init__(self, x, y, width, height, text, color,WIN):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        self.WIN = WIN

    def draw(self):
        color = (min(self.color[0] + 30, 255), 
                min(self.color[1] + 30, 255), 
                min(self.color[2] + 30, 255)) if self.hover else self.color
        pygame.draw.rect(self.WIN, color, self.rect, border_radius=10)
        pygame.draw.rect(self.WIN, WHITE, self.rect, 2, border_radius=10)
        text_surface = FONT_MEDIUM.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.WIN.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                return True
        return False

class Star:
    def __init__(self,WIN):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.5)
        self.brightness = random.randint(150, 255)
        self.WIN = WIN

    def update(self):
        self.y = (self.y + self.speed) % HEIGHT
        
    def draw(self):
        pygame.draw.circle(self.WIN, (self.brightness, self.brightness, self.brightness), 
                         (int(self.x), int(self.y)), self.size)
