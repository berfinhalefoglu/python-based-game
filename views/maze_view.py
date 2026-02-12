# views/maze_view.py

# maze.py
import pygame
from constants import CELL_SIZE,BLUE,COLORS
from game_manager import GameObject


# maze.py - Update the maze layout to match original game
class Maze:
    def __init__(self):
        # Updated maze layout to match the Atari version
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    # Draw walls with dark blue color
                    pygame.draw.rect(screen, BLUE,
                                   (x * CELL_SIZE, y * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE))
                else:
                    # Draw dotted lines for paths
                    if x > 0 and x < len(row)-1:
                        pygame.draw.line(screen, (255,215,0),  # Gold color
                                       (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2),
                                       ((x+1) * CELL_SIZE - CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2),
                                       2)
