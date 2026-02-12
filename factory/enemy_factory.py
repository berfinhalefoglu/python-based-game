# factory.py
from abc import ABC, abstractmethod
from constants import CELL_SIZE,COLORS
from game_manager import GameObject
import random
import math

class Enemy(GameObject):
    def __init__(self, x, y, maze, speed, enemy_type):
        # enemy_type'a göre renk seçimi yapılıyor
        color = COLORS.get(enemy_type.upper(), COLORS['STIFFY'])  # Default olarak STIFFY rengi
        super().__init__(x, y, CELL_SIZE - 20, color)
        
        self.maze = maze
        self.speed = speed
        self.detection_radius = 4 * CELL_SIZE  # Default detection radius
        self.direction_timer = 0
        self.direction_change_interval = 60
        self.current_direction = [0, 0]
        
    def get_distance_to_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        return math.sqrt(dx * dx + dy * dy)
    
    def is_player_detected(self, player):
        return self.get_distance_to_player(player) <= self.detection_radius
    
    def move_randomly(self):
        self.direction_timer += 1
        if self.direction_timer >= self.direction_change_interval:
            possible_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            self.current_direction = random.choice(possible_directions)
            self.direction_timer = 0
            
        new_x = self.x + self.current_direction[0] * self.speed
        new_y = self.y + self.current_direction[1] * self.speed
        
        cell_x = int(new_x // CELL_SIZE)
        cell_y = int(new_y // CELL_SIZE)
        
        if (0 <= cell_x < len(self.maze.grid[0]) and 
            0 <= cell_y < len(self.maze.grid) and 
            not self.maze.grid[cell_y][cell_x]):
            self.x = new_x
            self.y = new_y
            self.update_rect()
        else:
            self.direction_timer = self.direction_change_interval

    def chase_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist != 0:
            dx = (dx / dist) * self.speed
            dy = (dy / dist) * self.speed
            
            new_x = self.x + dx
            new_y = self.y + dy
            
            cell_x = int(new_x // CELL_SIZE)
            cell_y = int(new_y // CELL_SIZE)
            
            if (0 <= cell_x < len(self.maze.grid[0]) and 
                0 <= cell_y < len(self.maze.grid) and 
                not self.maze.grid[cell_y][cell_x]):
                self.x = new_x
                self.y = new_y
                self.update_rect()

class Stiffy(Enemy):
    """Yavaş ama kararlı takipçi"""
    def __init__(self, x, y, maze):
        super().__init__(x, y, maze, speed=1.5, enemy_type="STIFFY")
    
    def move(self, player):
        if self.is_player_detected(player):
            self.chase_player(player)
        else:
            self.move_randomly()

class Scaredy(Enemy):
    """Oyuncuyu görünce kaçan korkak düşman"""
    def __init__(self, x, y, maze):
        super().__init__(x, y, maze, speed=1.8, enemy_type="SCAREDY")
    
    def move(self, player):
        if self.is_player_detected(player):
            dx = self.x - player.x
            dy = self.y - player.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist != 0:
                dx = (dx / dist) * self.speed
                dy = (dy / dist) * self.speed
                
                new_x = self.x + dx
                new_y = self.y + dy
                
                cell_x = int(new_x // CELL_SIZE)
                cell_y = int(new_y // CELL_SIZE)
                
                if (0 <= cell_x < len(self.maze.grid[0]) and 
                    0 <= cell_y < len(self.maze.grid) and 
                    not self.maze.grid[cell_y][cell_x]):
                    self.x = new_x
                    self.y = new_y
                    self.update_rect()
        else:
            self.move_randomly()

class Smarty(Enemy):
    """Akıllı ve hızlı takipçi"""
    def __init__(self, x, y, maze):
        super().__init__(x, y, maze, speed=2, enemy_type="SMARTY")
    
    def move(self, player):
        if self.is_player_detected(player):
            predicted_x = player.x + (player.x - self.x) * 0.2
            predicted_y = player.y + (player.y - self.y) * 0.2
            
            dx = predicted_x - self.x
            dy = predicted_y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist != 0:
                dx = (dx / dist) * self.speed
                dy = (dy / dist) * self.speed
                
                new_x = self.x + dx
                new_y = self.y + dy
                
                cell_x = int(new_x // CELL_SIZE)
                cell_y = int(new_y // CELL_SIZE)
                
                if (0 <= cell_x < len(self.maze.grid[0]) and 
                    0 <= cell_y < len(self.maze.grid) and 
                    not self.maze.grid[cell_y][cell_x]):
                    self.x = new_x
                    self.y = new_y
                    self.update_rect()
        else:
            self.move_randomly()

class Silly(Enemy):
    """Rastgele hareket eden düşman"""
    def __init__(self, x, y, maze):
        super().__init__(x, y, maze, speed=1.3, enemy_type="SILLY")
        self.chase_mode = False
        self.chase_timer = 0
        self.chase_duration = 120
    
    def move(self, player):
        if self.is_player_detected(player):
            if random.random() < 0.02:
                self.chase_mode = True
                self.chase_timer = 0
        
        if self.chase_mode:
            self.chase_timer += 1
            if self.chase_timer >= self.chase_duration:
                self.chase_mode = False
            self.chase_player(player)
        else:
            self.move_randomly()

class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, x, y, maze):
        enemies = {
            "stiffy": Stiffy,
            "scaredy": Scaredy,
            "smarty": Smarty,
            "silly": Silly
        }
        
        enemy_class = enemies.get(enemy_type.lower())
        if enemy_class:
            return enemy_class(x, y, maze)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")