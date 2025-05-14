# ai_rover_simulation/rover.py

import cv2
import numpy as np
import random
import math

class Rover:
    def __init__(self, x, y, angle, map_shape, terrain):
        self.x = x
        self.y = y
        self.angle = angle  # in degrees
        self.map_height, self.map_width = map_shape
        self.terrain = terrain
        self.radius = 10
        self.step_size = 5
        self.turn_angle = 20
        self.last_turn = 0

    def draw(self, frame):
        cv2.circle(frame, (int(self.x), int(self.y)), self.radius, (255, 0, 0), -1)
        dx = int(self.radius * np.cos(np.radians(self.angle)))
        dy = int(self.radius * np.sin(np.radians(self.angle)))
        cv2.line(frame, (int(self.x), int(self.y)),
                 (int(self.x + dx), int(self.y + dy)), (255, 255, 255), 2)

    def autonomous_move(self):
        # Check for obstacle in front
        front_x = int(self.x + 15 * np.cos(np.radians(self.angle)))
        front_y = int(self.y + 15 * np.sin(np.radians(self.angle)))

        if self._is_obstacle(front_x, front_y):
            # Turn randomly to avoid obstacle
            self.angle += random.choice([-1, 1]) * self.turn_angle
            self.angle %= 360
        else:
            self._move_forward()

    def _move_forward(self):
        new_x = self.x + self.step_size * np.cos(np.radians(self.angle))
        new_y = self.y + self.step_size * np.sin(np.radians(self.angle))

        # Stay within map bounds
        if 0 < new_x < self.map_width and 0 < new_y < self.map_height:
            if not self._is_obstacle(int(new_x), int(new_y)):
                self.x = new_x
                self.y = new_y
            else:
                self.angle += random.choice([-1, 1]) * self.turn_angle

    def _is_obstacle(self, x, y):
        # Assume dark areas (low intensity) are obstacles
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            pixel = self.terrain[int(y), int(x)]
            if np.mean(pixel) < 50:  # very dark = obstacle
                return True
        return False
