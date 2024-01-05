# main.py

from ursina import *
from game_objects import *


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.black
        window.borderless = False
        # window.fullscreen_size = 1920, 1080
        # window.fullscreen = True
        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        self.MAP_SIZE = 20
        self.new_game()
        camera.position = (self.MAP_SIZE // 2, -20.5, -20)
        camera.rotation_x = -57

    def create_map(self, MAP_SIZE):
        Entity(model='quad', scale=MAP_SIZE, position=(MAP_SIZE // 2, MAP_SIZE // 2, 0), color=color.dark_gray)
        Entity(model=Grid(MAP_SIZE, MAP_SIZE), scale=MAP_SIZE,
               position=(MAP_SIZE // 2, MAP_SIZE // 2, -0.01), color=color.black)

    def new_game(self):
        scene.clear()
        self.create_map(self.MAP_SIZE)
        self.apple = Apple(self.MAP_SIZE, model='sphere', color=color.red)
        self.snake1 = Snake(self.MAP_SIZE, controls=['w', 'a', 's', 'd'], color=color.green)
        self.snake2 = Snake(self.MAP_SIZE, controls=['i', 'j', 'k', 'l'], color=color.blue)

    def input(self, key, is_raw=False):
        super().input(key)
        self.snake1.control(key)
        self.snake2.control(key)

        if key == '2':
            camera.rotation_x = 0
            camera.position = (self.MAP_SIZE // 2, self.MAP_SIZE // 2, -50)
        elif key == '3':
            camera.position = (self.MAP_SIZE // 2, -20.5, -20)
            camera.rotation_x = -57

    def check_apple_eaten(self, snake):
        if snake.segment_positions[-1] == self.apple.position:
            snake.add_segment()
            self.apple.new_position()

    def check_game_over(self, snake):
        segment_positions = snake.segment_positions
        if 0 < segment_positions[-1][0] < self.MAP_SIZE and 0 < segment_positions[-1][1] < self.MAP_SIZE \
                and len(segment_positions) == len(set(segment_positions)):
            return
        print_on_screen(f'GAME OVER - Player {snake.controls[0].upper()}', position=(-0.7, 0.1), scale=5, duration=1)
        snake.direction = Vec3(0, 0, 0)
        snake.permissions = dict.fromkeys(snake.permissions, 0)
        invoke(self.new_game, delay=1)

    def update(self):
        print_on_screen(f'Score Player 1: {self.snake1.score}', position=(-0.85, 0.45), scale=3, duration=1 / 20)
        print_on_screen(f'Score Player 2: {self.snake2.score}', position=(-0.85, 0.4), scale=3, duration=1 / 20)
        self.check_apple_eaten(self.snake1)
        self.check_apple_eaten(self.snake2)
        self.check_game_over(self.snake1)
        self.check_game_over(self.snake2)
        self.snake1.run()
        self.snake2.run()


if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()
