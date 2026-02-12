# models/enemy_model.py
import math
import random
from constants import CELL_SIZE

class EnemyModel:
    def __init__(self, x, y, enemy_type):  # Düzeltme: _init_ yerine __init__ kullanıldı
        """
        EnemyModel sınıfı, düşmanın pozisyonunu ve tipini temsil eder.

        Args:
            x (int): Düşmanın x koordinatı
            y (int): Düşmanın y koordinatı
            enemy_type (str): Düşmanın tipi (örneğin 'stiffy', 'scaredy', 'smarty', 'silly')
        """
        self.x = x
        self.y = y
        self.speed = 2  # Düşmanın hareket hızı
        self.enemy_type = enemy_type
        self.size = 30  # Düşmanın boyutu
        self.observers = []  # Observer design pattern için gözlemciler
        self.direction = [0, 0]  # Hareket yönü
        self.detection_radius = 200  # Tespit yarıçapı (örneğin, scaredy düşmanı için)

    def move(self, player_x, player_y):
        """
        Düşmanın hareketini kontrol eder. Davranış türüne bağlı olarak hareket mantığını uygular.

        Args:
            player_x (int): Oyuncunun x koordinatı
            player_y (int): Oyuncunun y koordinatı
        """
        if self.enemy_type == "stiffy":
            self._chase_behavior(player_x, player_y)
        elif self.enemy_type == "scaredy":
            self._flee_behavior(player_x, player_y)
        elif self.enemy_type == "smarty":
            self._smart_chase_behavior(player_x, player_y)
        elif self.enemy_type == "silly":
            self._random_behavior()

        self.notify_observers()  # Hareketten sonra gözlemcileri bilgilendir

    def _chase_behavior(self, player_x, player_y):
        """
        Oyuncuyu takip eden bir davranış sergiler.
        """
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist != 0:  # Oyuncuya doğru hareket et
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def _flee_behavior(self, player_x, player_y):
        """
        Oyuncudan kaçan bir davranış sergiler.
        """
        dx = self.x - player_x
        dy = self.y - player_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist != 0 and dist < self.detection_radius:  # Oyuncudan kaç
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def _smart_chase_behavior(self, player_x, player_y):
        """
        Daha akıllı bir şekilde oyuncuyu takip eden davranış.
        Gelecekte daha karmaşık hareket algoritmaları eklemek için bir yer.
        """
        # Akıllı takip mantığı burada geliştirilebilir
        self._chase_behavior(player_x, player_y)

    def _random_behavior(self):
        """
        Rastgele hareket eden bir davranış sergiler.
        """
        self.x += random.choice([-1, 0, 1]) * self.speed
        self.y += random.choice([-1, 0, 1]) * self.speed

    def add_observer(self, observer):
        """
        Yeni bir gözlemci ekler.

        Args:
            observer: Gözlemci nesnesi
        """
        self.observers.append(observer)

    def notify_observers(self):
        """
        Tüm gözlemcileri bilgilendirir.
        """
        for observer in self.observers:
            observer.update(self)
