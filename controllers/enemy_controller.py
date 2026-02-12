# enemy.py
from game_manager import GameObject
import math
import pygame
from constants import CELL_SIZE, RED, SCREEN_WIDTH, SCREEN_HEIGHT,COLORS

class Enemy(GameObject):
    def __init__(self, x, y, maze):
        super().__init__(x, y, CELL_SIZE - 20, COLORS['STIFFY'])
        self.maze = maze
        self.base_speed = 2
        self.speed = self.base_speed
        self.acceleration = 0.1  # Hızlanma faktörü
        self.max_speed = 3.5     # Maksimum hız
        self.direction = [0, 0]  # Hareket yönü
        self.portal_cooldown = 0 # Portal kullanım bekleme süresi
        self.last_positions = [] # Son pozisyonları takip etmek için
        self.target_position = None
        self.path_finding_cooldown = 0
        
    def draw(self, screen):
        # Düşman karakterini çiz
        pygame.draw.circle(screen, self.color, 
                         (int(self.x + self.size // 2), 
                          int(self.y + self.size // 2)), 
                         self.size // 2)
        
        # Portal göstergeleri
        self.draw_portal_indicators(screen)
        
    def draw_portal_indicators(self, screen):
        """Koridorlar arası geçiş noktalarını göster"""
        cell_x = int(self.x // CELL_SIZE)
        cell_y = int(self.y // CELL_SIZE)
        
        # Yatay ve dikey geçiş noktalarını kontrol et
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            next_x = cell_x + dx
            next_y = cell_y + dy
            
            # Eğer geçiş noktası varsa
            if self.is_valid_portal(next_x, next_y):
                portal_x = (cell_x * CELL_SIZE + dx * CELL_SIZE // 2 + CELL_SIZE // 2)
                portal_y = (cell_y * CELL_SIZE + dy * CELL_SIZE // 2 + CELL_SIZE // 2)
                
                # Portal göstergesini çiz
                pygame.draw.circle(screen, (0, 255, 255), (portal_x, portal_y), 5)
                
                # Portal aktif değilse üzerine çarpı çiz
                if self.portal_cooldown > 0:
                    pygame.draw.line(screen, (255, 0, 0), 
                                   (portal_x - 5, portal_y - 5),
                                   (portal_x + 5, portal_y + 5), 2)
                    pygame.draw.line(screen, (255, 0, 0),
                                   (portal_x - 5, portal_y + 5),
                                   (portal_x + 5, portal_y - 5), 2)

    def is_valid_portal(self, x, y):
        """Geçerli bir portal noktası mı kontrol et"""
        if (0 <= x < len(self.maze.grid[0]) and 
            0 <= y < len(self.maze.grid)):
            return not self.maze.grid[y][x]
        return False

    def find_best_path(self, player):
        """A* benzeri basit yol bulma"""
        if self.path_finding_cooldown > 0:
            self.path_finding_cooldown -= 1
            return
            
        target_x = int(player.x // CELL_SIZE)
        target_y = int(player.y // CELL_SIZE)
        current_x = int(self.x // CELL_SIZE)
        current_y = int(self.y // CELL_SIZE)
        
        # En yakın geçiş noktasını bul
        min_dist = float('inf')
        best_portal = None
        
        for y in range(len(self.maze.grid)):
            for x in range(len(self.maze.grid[0])):
                if not self.maze.grid[y][x]:  # Boş hücre
                    dist_to_player = math.sqrt((x - target_x)**2 + (y - target_y)**2)
                    dist_to_self = math.sqrt((x - current_x)**2 + (y - current_y)**2)
                    total_dist = dist_to_player + dist_to_self
                    
                    if total_dist < min_dist:
                        min_dist = total_dist
                        best_portal = (x * CELL_SIZE + CELL_SIZE//2, 
                                     y * CELL_SIZE + CELL_SIZE//2)
        
        if best_portal:
            self.target_position = best_portal
            self.path_finding_cooldown = 30  # Her 0.5 saniyede bir güncelle

    def update_movement(self, player):
        """Hareketi güncelle"""
        # Yol bulma
        self.find_best_path(player)
        
        if self.target_position:
            target_x, target_y = self.target_position
        else:
            target_x = player.x
            target_y = player.y
            
        # Hedefe olan yönü hesapla
        dx = target_x - (self.x + self.size // 2)
        dy = target_y - (self.y + self.size // 2)
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize et ve hızı uygula
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            
            # Hızı artır (maksimum hıza kadar)
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        
            # Yeni pozisyonu hesapla
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Pozisyonu güncelle
            self.x = new_x
            self.y = new_y
            
        # Son pozisyonları kaydet
        self.last_positions.append((self.x, self.y))
        if len(self.last_positions) > 10:  # Son 10 pozisyonu tut
            self.last_positions.pop(0)

    def move(self, player):
        """Ana hareket fonksiyonu"""
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1
            
        self.update_movement(player)
        
        # Wrap-around kontrolü
        if self.x < 0:
            self.x = SCREEN_WIDTH - CELL_SIZE
            self.portal_cooldown = 30  # Portal kullanımı sonrası bekleme
        elif self.x >= SCREEN_WIDTH:
            self.x = 0
            self.portal_cooldown = 30
            
        if self.y < 0:
            self.y = SCREEN_HEIGHT - CELL_SIZE
            self.portal_cooldown = 30
        elif self.y >= SCREEN_HEIGHT:
            self.y = 0
            self.portal_cooldown = 30
            
        # Duvar çarpışma kontrolü
        cell_x = int(self.x // CELL_SIZE)
        cell_y = int(self.y // CELL_SIZE)
        
        if (0 <= cell_x < len(self.maze.grid[0]) and 
            0 <= cell_y < len(self.maze.grid)):
            if self.maze.grid[cell_y][cell_x]:  # Duvar varsa
                # En son geçerli pozisyona geri dön
                if self.last_positions:
                    self.x, self.y = self.last_positions[0]
                self.speed = self.base_speed  # Hızı sıfırla
                
        self.update_rect()