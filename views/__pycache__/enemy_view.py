
# views/enemy_view.py
import pygame
from constants import COLORS

class EnemyView:
    def _init_(self, enemy_type):
        self.x = 0
        self.y = 0
        self.size = 30
        self.enemy_type = enemy_type
        self.color = COLORS[enemy_type.upper()]

    def update(self, model):
        self.x = model.x
        self.y = model.y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                         (int(self.x + self.size // 2),
                          int(self.y + self.size // 2)),
                         self.size // 2)
