# -*- coding: utf-8 -*-


import random
import sys

import pygame

from space_ships import *
from fx import *
from gui import *
from const import *
from spritesheet import *
from object import *


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("data/music/master/menu.mp3")
pygame.mixer.music.play(-1)

pygame.display.set_caption("StarFall")

player_image = pygame.image.load("data/sprites/space_ships/spaceship.png")


def exit_():
    pygame.quit()
    sys.exit()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('data/bg.jpg')

        self.play_button = Button(300, 250, pygame.image.load('play.png'), 1)
        self.exit_button = Button(300, 350, pygame.image.load('exit.png'), 1)

        self.player = SpaceShip(100, 100, player_image, 2)
        self.player_lasers = []

        anim_list = []
        star = SpriteSheet(pygame.image.load("data/sprites/objects/stars/star_sheet_4.png"))
        for x in range(50):
            anim_list.append(star.get_image(x, 200, 200, (0, 0, 0)))
        self.star = Star(anim_list, (100, 100))

        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_()
            if self.play_button.draw(self.screen) == True:
                self.start()
            if self.exit_button.draw(self.screen) == True:
                exit_()
            pygame.display.update()
            self.clock.tick(120)

    def start(self):
        pygame.mixer.music.load("data/music/master/master.wav")
        pygame.mixer.music.play(-1)

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            self.player.update(self.screen)
            self.star.draw(self.screen)

            for laser in self.player_lasers:
                laser.move()
                if laser.check():
                    self.player_lasers.pop(self.player_lasers.index(laser))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.rotateLeft()
            if keys[pygame.K_RIGHT]:
                self.player.rotateRight()
            if keys[pygame.K_UP]:
                self.player.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.star.check((100, 100))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player_lasers.append(Laser(pygame.image.load("data/sprites/lasers/01.png"), self.player))
            for laser in self.player_lasers:
                laser.update(self.screen)
            pygame.display.update()
            self.clock.tick(120)


if __name__ == '__main__':
    app = App()
