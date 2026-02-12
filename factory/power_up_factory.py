from game_manager import GameObject
from constants import CELL_SIZE, COLORS

class PowerUp(GameObject):
    def __init__(self, x, y, effect=None, color=None, duration=300):
        super().__init__(x, y, CELL_SIZE - 20, color or (255, 255, 255))
        self.effect = effect
        self.duration = duration
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active

class PowerUpFactory:
    @staticmethod
    def create_powerup(powerup_type, x, y):
        color_mapping = {
            "speed": COLORS.get('POWERUP_SPEED', (0, 255, 0)),
            "invisibility": COLORS.get('POWERUP_INVISIBLE', (192, 192, 192)),
            "wall_break": COLORS.get('POWERUP_WALL_BREAK', (255, 165, 0))
        }
        color = color_mapping.get(powerup_type, (255, 255, 255))
        return PowerUp(x, y, effect=powerup_type, color=color, duration=300)
