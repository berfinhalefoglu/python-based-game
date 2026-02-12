# controllers/game_controller.py
import pygame
from models.player_model import PlayerModel
from models.enemy_model import EnemyModel
from models.maze_model import MazeModel
from views.player_view import PlayerView
from views.enemy_view import EnemyView
from views.maze_view import MazeView
from controllers.player_controller import PlayerController
from controllers.enemy_controller import EnemyController
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

class GameController:
    def __init__(self):  # Corrected the typo in the constructor method name
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True  # Added running attribute initialization

        # Initialize Models
        self.maze_model = MazeModel()
        self.player_model = PlayerModel()
        self.enemy_models = [
            EnemyModel(x * CELL_SIZE, y * CELL_SIZE, enemy_type)
            for x, y, enemy_type in [
                (2, 3, "stiffy"),
                (3, 4, "scaredy"),
                (4, 5, "smarty"),
                (5, 6, "silly")
            ]
        ]

        # Initialize Views
        self.maze_view = MazeView(CELL_SIZE)
        self.player_view = PlayerView()
        self.enemy_views = [EnemyView(enemy.enemy_type) for enemy in self.enemy_models]

        # Initialize Controllers
        self.player_controller = PlayerController(self.player_model, self.maze_model)
        self.enemy_controllers = [
            EnemyController(enemy_model, self.maze_model)
            for enemy_model in self.enemy_models
        ]

        # Connect Models and Views
        self.player_model.add_observer(self.player_view)
        for enemy_model, enemy_view in zip(self.enemy_models, self.enemy_views):
            enemy_model.add_observer(enemy_view)

    def run(self):
        while self.running:  # Oyun döngüsü çalışıyor
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Oyun hızını 60 FPS ile sınırla
        pygame.quit()  # Pygame'den çık

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Pencere kapatıldığında döngüyü sonlandır
                self.running = False

        keys = pygame.key.get_pressed()
        self.player_controller.handle_input(keys)

    def update(self):
        for enemy_controller in self.enemy_controllers:
            enemy_controller.update(self.player_model.x, self.player_model.y)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Arka planı siyah yap
        self.maze_view.draw(self.screen, self.maze_model)
        self.player_view.draw(self.screen)
        for enemy_view in self.enemy_views:
            enemy_view.draw(self.screen)
        pygame.display.flip()  # Görüntüyü güncelle
