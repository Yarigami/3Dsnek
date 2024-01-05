from ursina import *
from random import randrange


class Apple(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.new_position()

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5, randrange(self.MAP_SIZE) + 0.5, -0.5)


class Snake:
    def __init__(self, MAP_SIZE, controls, color):
        self.MAP_SIZE = MAP_SIZE
        self.segment_length = 1
        self.position_length = self.segment_length + 1
        self.segment_positions = [Vec3(randrange(MAP_SIZE) + 0.5, randrange(MAP_SIZE) + 0.5, -0.5)]
        self.segment_entities = [Entity(model='sphere', color=color, position=self.segment_positions[0])]
        self.controls = controls
        self.directions = {controls[1]: Vec3(-1, 0, 0), controls[3]: Vec3(1, 0, 0),
                           controls[0]: Vec3(0, 1, 0), controls[2]: Vec3(0, -1, 0)}
        self.direction = Vec3(0, 0, 0)
        self.permissions = {controls[0]: 1, controls[1]: 1, controls[2]: 1, controls[3]: 1}
        self.taboo_movement = {controls[1]: controls[3], controls[0]: controls[2],
                               controls[2]: controls[0], controls[3]: controls[1]}
        self.speed, self.score = 12, 0
        self.frame_counter = 0

    def add_segment(self):
        self.segment_length += 1
        self.position_length += 1
        self.score += 1
        self.speed = max(self.speed - 1, 5)
        self.create_segment(self.segment_positions[0])

    def create_segment(self, position):
        color = self.segment_entities[0].color
        entity = Entity(position=position)
        Entity(model='sphere', color=color, position=position).add_script(
            SmoothFollow(speed=12, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0, entity)
        if len(self.segment_entities) > 1:
            entity.add_script(SmoothFollow(speed=12, target=self.segment_entities[1], offset=(0, 0, 0)))

    def run(self):
        self.frame_counter += 1
        if not self.frame_counter % self.speed:
            self.segment_positions.append(self.segment_positions[-1] + self.direction)
            self.segment_positions = self.segment_positions[-self.segment_length:]
            for segment, segment_position in zip(self.segment_entities, self.segment_positions):
                segment.position = segment_position

    def control(self, key):
        for pressed_key in self.controls:
            if pressed_key == key and self.permissions[pressed_key]:
                self.direction = self.directions[pressed_key]
                self.permissions = dict.fromkeys(self.permissions, 1)
                self.permissions[self.taboo_movement[pressed_key]] = 0
                break
