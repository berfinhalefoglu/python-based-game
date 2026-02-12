from abc import ABC, abstractmethod

class PlayerState(ABC):  # Tüm durumlar için bir temel sınıf
    @abstractmethod
    def handle_state(self, player):
        pass

class NormalState(PlayerState):
    def handle_state(self, player):
        player.speed = 2  # Normal hız

class PoweredUpState(PlayerState):
    def handle_state(self, player):
        player.speed = 4  # Güçlendirilmiş hız

class InjuredState(PlayerState):
    def handle_state(self, player):
        player.speed = 1  # Yavaşlatılmış hız
