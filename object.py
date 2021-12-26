import pygame

from random import randint
from const import *


class Object:
    def __init__(self, anim_list, pos):
        self.animation_step = 50
        self.animation_update = pygame.time.get_ticks()
        self.animation_cooldown = 50
        self.frame = 0

        self.font = pygame.font.Font('data/font/Pixeltype.ttf', 50)

        self.list = anim_list
        self.loc = 0
        self.sound = pygame.mixer.Sound('data/music/gui/scan.wav')
        self.pos = pos
        self.rect = self.list[self.frame].get_rect(center=self.pos)

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_update >= self.animation_cooldown:
            self.frame += 1
            self.animation_update = current_time
            self.frame %= len(self.list)

        if self.loc == 0:
            self.list[self.frame] = pygame.transform.scale(self.list[self.frame], (200, 200))
            self.rect = self.list[self.frame].get_rect(center=self.pos)
            self.rect.x += 100
            screen.blit(self.list[self.frame], self.rect)
        else:
            self.list[self.frame] = pygame.transform.scale(self.list[self.frame], (400, 400))
            self.rect = self.list[self.frame].get_rect(center=(500, 250))
            self.txt = self.font.render(f'Object type: {self.return_type()}', False, 'White')
            self.text_rect = self.txt.get_rect(center=(500, 400))
            screen.blit(self.list[self.frame], self.rect)
            screen.blit(self.txt, self.text_rect)

    def check(self, pos):
        if self.rect.collidepoint(pos):
            self.sound.play()
            if self.loc == 0:
                self.loc = 1
            else:
                self.loc = 0

    def return_type(self):
        return type(self)


class Star(Object):
    def return_type(self):
        return 'Star'


class Asteroid(Object):
    def return_type(self):
        return 'Asteroid'


class Planet(Object):
    def return_type(self):
        return 'Planet'


class GasGiant(Planet):
    def return_type(self):
        return 'Gas Giant'


class BlackHole(Object):
    def return_type(self):
        return 'Black hole'

    def active_hyperspace(self, app):
        import fx


        self.hyperspace = fx.Hyperspace(app)
        self.hyperspace.run()
