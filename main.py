# -*- coding: utf-8 -*-
import random
import sys

import pygame

import fx
from space_ships import *
from fx import *
from object import *
from spritesheet import *
from gui import *


SIZE = WIDTH, HEIGHT = 1000, 500
vec2 = pygame.math.Vector2
vec3 = pygame.math.Vector3
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
ALPHA = 30


class App:
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load("data/music/master/in-the-wreckage.wav")
    pygame.mixer.music.play(-1)

    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('data/bg.jpg')

        self.sound = pygame.mixer.Sound('data/music/gui/scan.wav')
        self.alpha_surface = pygame.Surface(SIZE)
        self.alpha_surface.set_alpha(ALPHA)

        # -----------------------------------------
        self.stars = list()
        for f in range(2):
            anim_list = []
            sprite = SpriteSheet(pygame.image.load(f'data/sprites/objects/stars/star_sheet_{random.randint(1, 6)}.png').convert_alpha())
            for x in range(50):
                anim_list.append(sprite.get_image(x, 200, 200, (0, 0, 0)).convert_alpha())
            self.stars.append(Star(anim_list))
        # -----------------------------------------

        # -----------------------------------------
        self.holes = list()
        for f in range(1):
            anim_list2 = []
            sprite2 = SpriteSheet(pygame.image.load(
                f'data/sprites/objects/black_holes/black_hole ({random.randint(1, 8)}).png').convert_alpha())
            for x in range(50):
                anim_list2.append(sprite2.get_image(x, 200, 200, (0, 0, 0), 3).convert_alpha())
            self.holes.append(BlackHole(anim_list2))
        # -----------------------------------------

        # -----------------------------------------
        self.planets = list()
        for f in range(1):
            anim_list3 = []
            sprite3 = SpriteSheet(pygame.image.load(
                f'data/sprites/objects/planets/planets/planets ({random.randint(1, 16)}).png').convert_alpha())
            for x in range(50):
                anim_list3.append(sprite3.get_image(x, 100, 100, (0, 0, 0)).convert_alpha())
            self.planets.append(Planet(anim_list3))
        # -----------------------------------------

        # -----------------------------------------
        self.gas_planets = list()
        for f in range(2):
            anim_list4 = []
            sprite4 = SpriteSheet(pygame.image.load(
                f'data/sprites/objects/planets/gas_giants/rings/gas_giant ({random.randint(1, 5)}).png').convert_alpha())
            for x in range(50):
                anim_list4.append(sprite4.get_image(x, 300, 300, (0, 0, 0)).convert_alpha())
            self.gas_planets.append(GasGiant(anim_list4))
        # -----------------------------------------

        # -----------------------------------------
        self.gas_planets2 = list()
        for f in range(1):
            anim_list5 = []
            sprite5 = SpriteSheet(pygame.image.load(
                f'data/sprites/objects/planets/gas_giants/gas_giant ({random.randint(1, 6)}).png').convert_alpha())
            for x in range(50):
                anim_list5.append(sprite5.get_image(x, 100, 100, (0, 0, 0)).convert_alpha())
            self.gas_planets2.append(GasGiant(anim_list5))
        # -----------------------------------------

        self.hyper = Hyperspace(self)

    def run(self):
        running = True
        while running:
            self.screen.blit(self.alpha_surface, (0, 0))
            self.hyper.run()

            [i.draw(self.screen) for i in self.stars]
            [i.draw(self.screen) for i in self.holes]
            [i.draw(self.screen) for i in self.planets]
            [i.draw(self.screen) for i in self.gas_planets]
            [i.draw(self.screen) for i in self.gas_planets2]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    [i.check(event.pos) for i in self.stars]
                    [i.check(event.pos) for i in self.holes]
                    [i.check(event.pos) for i in self.planets]
                    [i.check(event.pos) for i in self.gas_planets]
                    [i.check(event.pos) for i in self.gas_planets2]

            pygame.display.update()
            self.clock.tick(120)

    @staticmethod
    def draw_ship(ship):
        ship.update()


if __name__ == '__main__':
    app = App()
    app.run()
    pygame.quit()
    sys.exit()
