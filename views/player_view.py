import pygame
from constants import COLORS
# views/player_view.py
import pygame
from constants import COLORS

class PlayerView:
    def _init_(self):
        self.x = 0
        self.y = 0
        self.size = 30
        self.color = COLORS['PLAYER']

    def update(self, model):
        self.x = model.x
        self.y = model.y
        if model.state == "powered":
            self.color = COLORS['POWERUP_SPEED']
        elif model.state == "injured":
            self.color = COLORS['PLAYER_INJURED']
        else:
            self.color = COLORS['PLAYER']

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                         (int(self.x + self.size // 2),
                          int(self.y + self.size // 2)),
                         self.size // 2)
