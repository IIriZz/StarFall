import pygame
import random


SIZE = WIDTH, HEIGHT = 1000, 500
VEC2 = pygame.math.Vector2
VEC3 = pygame.math.Vector3
CENTER = VEC2(WIDTH // 2, HEIGHT // 2)

NUM_VOXELS = 10000
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
Z_DISTANCE = 140

ALL_SPRITES = pygame.sprite.Group()