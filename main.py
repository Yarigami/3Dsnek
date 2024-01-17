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
        self.current_map = 1  # Add a variable to track the current map
        self.obstacles = []
        self.new_game()
        self.new_game_flag = False
        self.game_over_declared = False

    def create_map(self, MAP_SIZE):
        Entity(model='quad', scale=MAP_SIZE, position=(MAP_SIZE // 2, MAP_SIZE // 2, 0), color=color.dark_gray)
        Entity(model=Grid(MAP_SIZE, MAP_SIZE), scale=MAP_SIZE,
               position=(MAP_SIZE // 2, MAP_SIZE // 2, -0.01), color=color.black)

        # Add obstacles based on the current map
        if self.current_map == 2:
            # Add obstacles for map 2
            self.add_obstacle(position=(5, 5))
            self.add_obstacle(position=(15, 15))

        elif self.current_map == 3:
            # Add obstacles for map 2
            self.add_obstacle(position=(5, 5))
            self.add_obstacle(position=(15, 15))
            self.add_obstacle(position=(25, 25))
            self.add_obstacle(position=(35, 35))
            self.add_obstacle(position=(45, 45))

    def add_obstacle(self, position):
        obstacle = Entity(model='cube', scale=1, position=(position[0], position[1], 0), color=color.yellow)
        self.obstacles.append(obstacle)

    def new_game(self):
        # Clear all entities created in the previous game
        self.obstacles.clear()
        for entity in scene.entities:
            destroy(entity)

        self.create_map(self.MAP_SIZE)
        if hasattr(self, 'apple') and self.apple:
            destroy(self.apple)
            
        self.apple = Apple(self.MAP_SIZE, self.obstacles, model='sphere', color=color.red)
        self.snake1 = Snake(self.MAP_SIZE, controls=['w', 'a', 's', 'd'], color=color.green)
        self.snake2 = Snake(self.MAP_SIZE, controls=['i', 'j', 'k', 'l'], color=color.blue)

        # Calculate camera position and rotation based on map size
        camera_distance = max(self.MAP_SIZE, 15)  # Adjust this value based on your preference
        camera_position = (self.MAP_SIZE // 2, -self.MAP_SIZE, -camera_distance)
        camera_rotation_x = -55

        camera.position = camera_position
        camera.rotation_x = camera_rotation_x

        self.new_game_flag = False
        self.game_over_declared = False

        invoke(print_on_screen, '', position=(0, 0), scale=5, duration=1)

    def input(self, key, is_raw=False):
        super().input(key)

        if key == '1' or key == '2' or key == '3':
            self.destroy_all_entities()
            if key == '1':
                self.MAP_SIZE = 20
                self.current_map = 1
            elif key == '2':
                self.MAP_SIZE = 30
                self.current_map = 2
            elif key == '3':
                self.MAP_SIZE = 40

            self.new_game()

        if self.check_game_over(self.snake1) or self.check_game_over(self.snake2):
            self.new_game_flag = True

        if self.new_game_flag and held_keys['left mouse']:
            scene.clear()
            self.new_game()

        if not self.check_game_over(self.snake1) and not self.check_game_over(self.snake2):
            self.snake1.control(key)
            self.snake2.control(key)

    def destroy_all_entities(self):
        # Clear all entities in the scene
        for entity in scene.entities:
            destroy(entity)

    def check_apple_eaten(self, snake):
        if snake.segment_positions[-1] == self.apple.position:
            snake.add_segment()
            self.apple.new_position()

    def check_game_over(self, snake):
        head_position = snake.segment_positions[-1]
        
        # Cek apakah ular menyentuh obstacles
        for obstacle in self.obstacles:
            
            distance = (head_position - obstacle.position).length()
            if distance < 1:  
                self.declare_game_over(snake)
                return True  

        # Cek apakah ular berada di luar batas
        if not (0 < head_position.x < self.MAP_SIZE and 0 < head_position.y < self.MAP_SIZE):
            self.declare_game_over(snake)
            return True

        # Cek apakah ular menyentuh dirinya sendiri
        if len(snake.segment_positions) != len(set(snake.segment_positions)):
            self.declare_game_over(snake)
            return True

        return False  # Game terus berlanjut

    def declare_game_over(self, snake):
        if not self.game_over_declared:
            snake.direction = Vec3(0, 0, 0)
            snake.permissions = dict.fromkeys(snake.permissions, 0)
            self.game_over_declared = True

            # Don't declare a winner immediately, accumulate points
            self.snake1_score = self.snake1.score
            self.snake2_score = self.snake2.score

            if self.snake1_score > self.snake2_score:
                winner = 'Player 1'
            elif self.snake2_score > self.snake1_score:
                winner = 'Player 2'
            else:
                winner = 'It\'s a Tie'

            print_on_screen(f'{winner} Wins', position=(0, 0), scale=5, duration=1, origin=(0, 0))

    def update(self):
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
