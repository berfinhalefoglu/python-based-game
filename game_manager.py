# game_manager.py
"""
Implements the Singleton pattern for managing game state.
Ensures only one instance of game manager exists throughout the game.
"""
class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.score = 0
            self.paused = False  # Oyun durumu
            self.initialized = True

    def toggle_pause(self):
        """Oyunu durdur veya devam ettir."""
        self.paused = not self.paused

    def update_score(self, points):
        """Skoru güncelle."""
        self.score += points

    def get_score(self):
        """Mevcut skoru döndür."""
        return self.score

import pygame

class GameObject:
    def __init__(self, x, y, size, color, speed=2):
        self.x = x
        self.y = y
        self.size = size
        self.color = color or (255, 255, 255)
        self.speed = speed
        self.rect = pygame.Rect(x, y, size, size)

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
