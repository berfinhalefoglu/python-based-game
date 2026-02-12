# main.py
from controllers.game_controller import GameController
from game import Game

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
