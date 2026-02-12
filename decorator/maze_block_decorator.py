# maze_block_decorators.py
from constants import CELL_SIZE

class MazeDecorator:
    def __init__(self, maze):
        self._maze = maze
        self.special_cells = {}  # (x, y): effect_type

class SlipperyMazeDecorator(MazeDecorator):
    def apply_effect(self, player):
        cell = (int(player.x // CELL_SIZE), int(player.y // CELL_SIZE))
        if cell in self.special_cells:
            player.x += player.direction[0] * 2
            player.y += player.direction[1] * 2

class SlowingMazeDecorator(MazeDecorator):
    def apply_effect(self, player):
        cell = (int(player.x // CELL_SIZE), int(player.y // CELL_SIZE))
        if cell in self.special_cells:
            player.speed *= 0.5