import pygame

from random import randint
from const import *


class Star:
    def __init__(self, anim_sprite):
        super().__init__()
        self.image = anim_sprite
        self.rect = anim_sprite.rect

    @staticmethod
    def return_type():
        return 'Star'


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__(ASTEROIDS_GROUP)

        self.image = sprite
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(sprite)

    @staticmethod
    def return_type():
        return 'Asteroid'


class Planet:
    def __init__(self, anim_sprite):
        super().__init__()
        self.image = anim_sprite
        self.rect = anim_sprite.rect

    @staticmethod
    def return_type():
        return 'Planet'


class GasGiant:
    @staticmethod
    def return_type():
        return 'Gas Giant'


class BlackHole:
    def __init__(self, anim_sprite):
        self.image = anim_sprite
        self.rect = pygame.Rect(0, 0, 200, 200)
        print(self.rect)
        self.clicked = False
        self.action = False

        self.sound = pygame.mixer.Sound('data/music/gui/zoom.wav')

    def update(self):
        self.image.update()

    @staticmethod
    def return_type():
        return 'Black hole'

    def active_hyperspace(self, app):
        import fx
        self.hyperspace = fx.Hyperspace(app)
        self.hyperspace.run()
