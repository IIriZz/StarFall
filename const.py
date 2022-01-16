import pygame
import random
import ctypes

from gui import *

user32 = ctypes.windll.user32

SIZE = WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
VEC2 = pygame.math.Vector2
VEC3 = pygame.math.Vector3
CENTER = VEC2(WIDTH // 2, HEIGHT // 2)

NUM_VOXELS = 1000
NUM_STARS = 1000

ALPHA_VOXEL = 111
ALPHA_STARS = 120

COLORS = [
    pygame.color.Color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))),
    pygame.color.Color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))),
    pygame.color.Color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))),
    pygame.color.Color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))),
    pygame.color.Color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))),
    pygame.color.Color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))),
    pygame.color.Color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))),
    pygame.color.Color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))),
]
Z_DISTANCE = 40

ALL_SPRITES = pygame.sprite.Group()
ASTEROIDS_GROUP = pygame.sprite.Group()
EXPLOSION_GROUP = pygame.sprite.Group()
