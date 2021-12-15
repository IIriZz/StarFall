# -*- coding: utf-8 -*-

import sys

import pygame

import fx
from space_ships import *
from fx import *
from object import *
from spritesheet import *


SIZE = WIDTH, HEIGHT = 1000, 500
vec2 = pygame.math.Vector2
vec3 = pygame.math.Vector3
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
ALPHA = 30


class App:
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load("data/music/master/menu.wav")
    pygame.mixer.music.play(-1)

    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.alpha_surface = pygame.Surface(SIZE)
        self.alpha_surface.set_alpha(ALPHA)

        # -----------------------------------------
        anim_list = []
        sprite = SpriteSheet(pygame.image.load(f'data/sprites/objects/stars/star_sheet_{random.randint(1, 7)}.png').convert_alpha())
        for x in range(25):
            anim_list.append(sprite.get_image(x, 200, 200, (0, 0, 0)))
        self.planet = Object(anim_list, (400, 150))
        self.hyper = fx.Hyperspace(self)
        # -----------------------------------------

    def run(self):
        running = True
        while running:
            self.screen.blit(self.alpha_surface, (0, 0))
            self.hyper.run()
            self.planet.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

    @staticmethod
    def draw_ship(ship):
        ship.update()


if __name__ == '__main__':
    app = App()
    app.run()
    pygame.quit()
    sys.exit()
