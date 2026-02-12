
# Python Maze Game (Design Patterns)

A small maze-based game project built to demonstrate core Design Patterns in practice.
The focus is on clean separation of responsibilities (model/state/view/controller style) and reusable gameplay components.

## Design Patterns Used

### 1) Singleton — Game State Management
- `GameManager` is implemented as a Singleton to keep a single source of truth for game state (score, pause state).
- Prevents multiple managers from being created during runtime.

### 2) Factory — Enemy Creation
- `EnemyFactory.create_enemy(type, x, y, maze)` creates different enemy types from a single entry point.
- Makes adding new enemy types easy without changing the main game flow.

### 3) Builder — Level / Maze Construction
- `MazeBuilder` and its subclasses (e.g., `Level1Builder`, `Level2Builder`) build different maze layouts.
- Encapsulates level generation logic and keeps the main game code clean.

### 4) Decorator — Special Floor Effects
- Decorators such as `SlipperyMazeDecorator` / `SlowingMazeDecorator` apply additional behaviors without modifying the base maze.
- Adds new effects by extending decorators instead of rewriting core logic.

## Architecture (Model / View / Controller style)
- **Model:** maze grid + game state (score, pause)
- **View:** drawing logic for game objects (rendering via pygame)
- **Controller:** enemy AI/movement and gameplay control logic

## Project Files
- `game_manager.py` → Singleton game state + base `GameObject`
- `enemy_factory.py` → Factory for enemy creation
- `enemy_controller.py` → Enemy behavior / movement logic
- `maze_builder.py` → Builder for maze/levels
- `maze_block_decorator.py` → Decorators for special tiles
- `constants.py` → Shared constants (screen size, colors, cell size)

## How to Run
1. Install dependencies:
   ```bash
   pip install pygame


Run the main entry file (add your actual entry file name here):

python main.py

What I Learned

Applying patterns to reduce coupling and improve extensibility

Designing scalable enemy/level systems

Maintaining readable, modular code in a game loop
