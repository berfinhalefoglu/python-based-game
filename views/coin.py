# coin.py
from constants import CELL_SIZE,YELLOW,COLORS
from game_manager import GameObject
import pygame

class Coin(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, CELL_SIZE - 20, COLORS['COIN'])

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                         (self.x + self.size // 2, self.y + self.size // 2), 
                         self.size // 2)
