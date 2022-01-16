import random
import math
import pygame

from main import *
from const import *


class Voxel:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3D = self.get_pos3d()
        self.vel = random.uniform(0.45, 0.95)
        self.color = random.choice(COLORS)
        self.screen_pos = VEC2(0, 0)
        self.size = 5

    @staticmethod
    def get_pos3d(scale_pos=100):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return VEC3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3D.z -= self.vel
        self.pos3D = self.get_pos3d() if self.pos3D.z < 1 else self.pos3D

        self.screen_pos = VEC2(self.pos3D.x, self.pos3D.y) / self.pos3D.z + CENTER
        self.size = (Z_DISTANCE - self.pos3D.z) / (self.pos3D.z * 0.1)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))


class VoxelStar:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3D = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.screen_pos = VEC2(0, 0)
        self.size = 10

    @staticmethod
    def get_pos3d(scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return VEC3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3D.z -= self.vel
        self.pos3D = self.get_pos3d() if self.pos3D.z < 1 else self.pos3D

        self.screen_pos = VEC2(self.pos3D.x, self.pos3D.y) / self.pos3D.z + CENTER
        self.size = (Z_DISTANCE - self.pos3D.z) / (self.pos3D.z * 0.8)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))


class Hyperspace:
    def __init__(self, app):
        self.voxels = [Voxel(app) for _ in range(NUM_VOXELS)]

    def run(self):
        [voxel.update() for voxel in self.voxels]
        self.voxels.sort(key=lambda voxel: voxel.pos3D.z, reverse=True)
        [voxel.draw() for voxel in self.voxels]


class Starfield:
    def __init__(self, app):
        self.stars = [VoxelStar(app) for _ in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3D.z, reverse=True)
        [star.draw() for star in self.stars]


class Explosion(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(EXPLOSION_GROUP)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
