import pygame

from const import *


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('data/sprites/space_ships/spaceship.png')
        self.rect = self.image.get_rect()

    def update(self, screen, pos):
        screen.blit(self.image, pos)


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()

        self.action = False
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)

        return self.action


def camera_func(camera, target):
    x = -target.x + WIDTH / 2
    y = -target.y + HEIGHT / 2
    width, height = camera.width, camera.height
    x = min(0, x)
    x = max(-(camera.width - WIDTH), x)
    y = max(-(camera.height - HEIGHT), y)
    y = min(0, y)
    return pygame.Rect(x, y, width, height)


class Camera:
    def __init__(self, func, width, height):
        self.func = func
        self.camera = pygame.Rect(0, 0, width, height)

    def update(self, target):
        self.camera = self.func(self.camera, target.rect)

    def apply(self, target):
        return target.rect.move(self.camera.topleft)