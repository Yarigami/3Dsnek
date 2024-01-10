from ursina import *
from game_objects import *

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.black
        window.borderless = False
        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        self.MAP_SIZE = 20
        self.new_game()
        camera.position = (self.MAP_SIZE // 2, -20.5, -20)
        camera.rotation_x = -57
        self.new_game_flag = False
        self.game_over_declared = False  # New variable to track if game over message has been printed

    def create_map(self, MAP_SIZE):
        Entity(model='quad', scale=MAP_SIZE, position=(MAP_SIZE // 2, MAP_SIZE // 2, 0), color=color.dark_gray)
        Entity(model=Grid(MAP_SIZE, MAP_SIZE), scale=MAP_SIZE,
               position=(MAP_SIZE // 2, MAP_SIZE // 2, -0.01), color=color.black)

    def new_game(self):
        scene.clear()
        self.create_map(self.MAP_SIZE)
        if hasattr(self, 'apple') and self.apple:
            destroy(self.apple)
        # if hasattr(self, 'snake1') and self.snake1:
        #     destroy(self.snake1)
        # if hasattr(self, 'snake2') and self.snake2:
        #     destroy(self.snake2)
        self.apple = Apple(self.MAP_SIZE, model='sphere', color=color.red)
        self.snake1 = Snake(self.MAP_SIZE, controls=['w', 'a', 's', 'd'], color=color.green)
        self.snake2 = Snake(self.MAP_SIZE, controls=['i', 'j', 'k', 'l'], color=color.blue)
        self.new_game_flag = False
        self.game_over_declared = False  # Reset the game_over_declared variable

        # Clear the screen after starting a new game
        invoke(print_on_screen, '', position=(0, 0), scale=5, duration=1)

    def input(self, key, is_raw=False):
        super().input(key)

        # Clear the screen and start a new game only when the game is over and any key is pressed
        if self.check_game_over(self.snake1) or self.check_game_over(self.snake2):
            self.new_game_flag = True

        if self.new_game_flag and key:
            scene.clear()
            self.new_game()

        # Handle snake controls if the game is not over
        if not self.check_game_over(self.snake1) and not self.check_game_over(self.snake2):
            self.snake1.control(key)
            self.snake2.control(key)

        # Handle camera views based on key presses
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
            return False
        if not self.game_over_declared:  # Check if game over message has not been declared yet
            if snake == self.snake1:
                print_on_screen('Player 2 Wins', position=(0, 0), scale=5, duration=1, origin=(0, 0))
            else:
                print_on_screen('Player 1 Wins', position=(0, 0), scale=5, duration=1, origin=(0, 0))
            self.game_over_declared = True  # Mark game over message as declared
            snake.direction = Vec3(0, 0, 0)
            snake.permissions = dict.fromkeys(snake.permissions, 0)
        return True

    def update(self):
        # Display scores only if the game is not over
        if not self.check_game_over(self.snake1) and not self.check_game_over(self.snake2):
            print_on_screen(f'Score Player 1: {self.snake1.score}', position=(-0.85, 0.45), scale=3, duration=1 / 20)
            print_on_screen(f'Score Player 2: {self.snake2.score}', position=(-0.85, 0.35), scale=3, duration=1 / 20)

            self.check_apple_eaten(self.snake1)
            self.check_apple_eaten(self.snake2)

            self.snake1.run()
            self.snake2.run()

if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()
