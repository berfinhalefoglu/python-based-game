# models/player_model.py
class PlayerModel:
    def _init_(self):
        self.x = 50
        self.y = 50
        self.speed = 2
        self.score = 0
        self.state = "normal"
        self.size = 30
        self.observers = []

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def change_state(self, state):
        self.state = state
        if state == "powered":
            self.speed = 4
        elif state == "injured":
            self.speed = 1
        else:
            self.speed = 2
        self.notify_observers()
