class PlayerDecorator:
    def __init__(self, player):
        self._player = player
        self.duration = 300
        self.timer = 0

    def move(self, keys):
        if self.timer < self.duration:
            self.timer += 1
            self._special_move(keys)
        else:
            self._player.move(keys)

    def _special_move(self, keys):
        pass

class SpeedBoostDecorator(PlayerDecorator):
    def _special_move(self, keys):
        self._player.speed = 4
        self._player.move(keys)
        if self.timer >= self.duration:
            self._player.speed = 2

class WallBreakDecorator(PlayerDecorator):
    def _special_move(self, keys):
        self._player.can_break_walls = True
        self._player.move(keys)
        if self.timer >= self.duration:
            self._player.can_break_walls = False

class InvisibilityDecorator(PlayerDecorator):
    def _special_move(self, keys):
        self._player.is_invisible = True
        self._player.move(keys)
        if self.timer >= self.duration:
            self._player.is_invisible = False
