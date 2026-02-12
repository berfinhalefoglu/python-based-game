# player_controller.py
from game_manager import GameObject
from constants import CELL_SIZE, RED, SCREEN_WIDTH, SCREEN_HEIGHT,COLORS
import pygame
from state.player_states import NormalState,PoweredUpState, InjuredState

class Player(GameObject):
    def __init__(self, x, y, maze):
        super().__init__(x, y, CELL_SIZE - 20, COLORS['PLAYER'])

        self.maze = maze
        self.score = 0
        self.state = NormalState()  # Başlangıç durumu normal

    def change_state(self, new_state):
        """Oyuncunun durumunu değiştirir."""
        self.state = new_state

    def move(self, keys):
        """Oyuncu hareketlerini işler ve wrap-around özelliğini uygular."""
        self.state.handle_state(self)  # Duruma göre hız güncellenir

        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Yeni koordinatları hesapla
        self.x += dx
        self.y += dy

        # Ekranın bir ucundan çıkıp diğer ucundan girme
        if self.x < 0:
            self.x = SCREEN_WIDTH - CELL_SIZE
        elif self.x >= SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT - CELL_SIZE
        elif self.y >= SCREEN_HEIGHT:
            self.y = 0

        # Çarpışma kontrolü (labirent sınırları dahil)
        cell_x = self.x // CELL_SIZE
        cell_y = self.y // CELL_SIZE

        if (0 <= cell_x < len(self.maze.grid[0]) and
            0 <= cell_y < len(self.maze.grid) and
            not self.maze.grid[cell_y][cell_x]):
            self.update_rect()  # Yeni koordinatları güncelle
