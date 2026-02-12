import pygame
import random
from views.maze_view import Maze
from views.player_view import Player
from views.coin import Coin
from factory.power_up_factory import PowerUp
from constants import CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from game_manager import GameManager
from state.player_states import PoweredUpState, InjuredState
from factory import EnemyFactory
from builder.maze_builder import Level2Builder

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Lock 'n' Chase")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Pause Button
        self.pause_button = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40)

         # Level 2 Button
        self.level_2_button = pygame.Rect(SCREEN_WIDTH - 150, 60, 140, 40)
        # Maze
        self.maze = Maze()

        # Player
        self.player = Player(CELL_SIZE * 6 + 10, CELL_SIZE + 10, self.maze)

        # Coins
        self.coins = self.generate_coins()

        # Enemies
        self.enemies = self.generate_enemies()

        # Game Manager
        self.game_manager = GameManager()
        self.game_manager.set_coins(len(self.coins))  # Total coins for this level

    def generate_coins(self):
        """Generate coins and power-ups randomly on the maze grid."""
        coins = []
        for y, row in enumerate(self.maze.grid):
            for x, cell in enumerate(row):
                if cell == 0:
                    if random.random() < 0.1:  # 10% chance for a power-up
                        coins.append(PowerUp(x * CELL_SIZE + 10, y * CELL_SIZE + 10, effect="speed_booster"))
                    else:
                        coins.append(Coin(x * CELL_SIZE + 10, y * CELL_SIZE + 10))
        return coins

    def generate_enemies(self):
        """Generate enemies at fixed positions."""
        positions = [
            (CELL_SIZE * 2 + 10, CELL_SIZE * 3 + 10),
            (CELL_SIZE * 3 + 10, CELL_SIZE * 4 + 10),
            (CELL_SIZE * 4 + 10, CELL_SIZE * 5 + 10),
            (CELL_SIZE * 5 + 10, CELL_SIZE * 6 + 10)
        ]
        return [EnemyFactory.create_enemy(random.choice(["stiffy", "scaredy", "smarty", "silly"]), x, y, self.maze)
                for x, y in positions]

    def draw(self):
        """Draw all game elements on the screen."""
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        self.player.draw(self.screen)
        
        for coin in self.coins:
            coin.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw Score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'SCORE: {self.game_manager.get_score()}', True, (255, 255, 0))
        self.screen.blit(score_text, (10, 10))

        # Draw Pause Button
        pygame.draw.rect(self.screen, (200, 0, 0), self.pause_button)
        pause_text = font.render("PAUSE" if not self.game_manager.paused else "RESUME", True, (255, 255, 255))
        self.screen.blit(pause_text, (SCREEN_WIDTH - 140, 15))

        pygame.display.flip()

    def handle_collisions(self):
        """Handle player collisions with coins and enemies."""
        # Coin collection
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.game_manager.update_score(10)
                self.game_manager.collect_coin()  # Decrease remaining coin count
                if isinstance(coin, PowerUp):
                    self.player.change_state(PoweredUpState())

        # Enemy collision
        for enemy in self.enemies:
            enemy.move(self.player)
            if self.player.rect.colliderect(enemy.rect):
                self.player.change_state(InjuredState())

    def next_level_setup(self):
        """Setup the next level."""
        if self.game_manager.level == 2:
            builder = Level2Builder()
            builder.build_walls()
            builder.add_special_floors()

            # Update maze, coins, and enemies for the new level
            self.maze.grid = builder.maze
            self.coins = self.generate_coins()
            self.enemies = self.generate_enemies()
            self.game_manager.set_coins(len(self.coins))

    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_button.collidepoint(event.pos):
                    self.game_manager.toggle_pause()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()

            if not self.game_manager.paused:
                keys = pygame.key.get_pressed()
                self.player.move(keys)
                self.handle_collisions()

                if self.game_manager.coins_remaining == 0:
                    self.next_level_setup()  # Move to the next level

            self.draw()
            self.clock.tick(60)

        pygame.quit()
