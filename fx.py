import random
import math
import pygame

from main import *


NUM_VOXELS = 1000
COLORS = 'blue cyan violet purple'.split()
Z_DISTANCE = 140


class Voxel:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3D = self.get_pos3d()
        self.vel = random.uniform(0.45, 0.95)
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 5

    @staticmethod
    def get_pos3d(scale_pos=100):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3D.z -= self.vel
        self.pos3D = self.get_pos3d() if self.pos3D.z < 1 else self.pos3D

        self.screen_pos = vec2(self.pos3D.x, self.pos3D.y) / self.pos3D.z + CENTER
        self.size = (Z_DISTANCE - self.pos3D.z) / (self.pos3D.z * 0.5)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))


class Hyperspace:
    def __init__(self, app):
        self.voxels = [Voxel(app) for _ in range(NUM_VOXELS)]

    def run(self):
        [voxel.update() for voxel in self.voxels]
        self.voxels.sort(key=lambda voxel: voxel.pos3D.z, reverse=True)
        [voxel.draw() for voxel in self.voxels]
