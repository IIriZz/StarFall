# -*- coding: utf-8 -*-


import random
import sys

import pygame

from space_ships import *
from fx import *
from gui import *
from const import *

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("data/music/master/menu.mp3")
pygame.mixer.music.play(-1)

pygame.display.set_caption("StarFall")


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
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_()
            pygame.display.update()
            self.clock.tick(120)


if __name__ == '__main__':
    app = App()
