import pygame
import math

from const import *


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.delta_angle = 0
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.image_rotated = pygame.transform.rotate(self.image, self.delta_angle)
        self.rrect = self.image_rotated.get_rect(center=(self.x, self.y))

        self.cos = math.cos(math.radians(self.delta_angle + 90))
        self.sin = math.sin(math.radians(self.delta_angle + 90))

        self.head = (self.x - self.cos * self.width // 2,
                     self.y + self.sin * self.height // 2)


    def update(self, screen):
        screen.blit(self.image_rotated, self.rrect)

    def rotateLeft(self):
        self.delta_angle += 5
        self.image_rotated = pygame.transform.rotate(self.image, self.delta_angle)
        self.rrect = self.image_rotated.get_rect(center=(self.x, self.y))

        self.cos = math.cos(math.radians(self.delta_angle + 90))
        self.sin = math.sin(math.radians(self.delta_angle + 90))

        self.head = (self.x - self.cos * self.width // 2,
                     self.y + self.sin * self.height // 2)


    def rotateRight(self):
        self.delta_angle -= 5
        self.image_rotated = pygame.transform.rotate(self.image, self.delta_angle)
        self.rrect = self.image_rotated.get_rect(center=(self.x, self.y))

        self.cos = math.cos(math.radians(self.delta_angle + 90))
        self.sin = math.sin(math.radians(self.delta_angle + 90))

        self.head = (self.x - self.cos * self.width // 2,
                     self.y + self.sin * self.height // 2)


    def move(self):
        self.x += self.cos * self.speed
        self.y -= self.sin * self.speed

        self.image_rotated = pygame.transform.rotate(self.image, self.delta_angle)
        self.rrect = self.image_rotated.get_rect(center=(self.x, self.y))

        self.cos = math.cos(math.radians(self.delta_angle + 90))
        self.sin = math.sin(math.radians(self.delta_angle + 90))

        self.head = (self.x - self.cos * self.width // 2,
                     self.y + self.sin * self.height // 2)



class Player(SpaceShip): ...


class Enemy(SpaceShip): ...


class Laser(pygame.sprite.Sprite):
    def __init__(self, image, player):
        super().__init__()
        self.image = image

        self.sound = pygame.mixer.Sound("data/music/sfx/laser.mp3")
        self.sound.play()

        self.x, self.y = player.head
        self.rect = self.image.get_rect(center=(player.head))

        self.cos = player.cos * 20
        self.sin = player.sin * 20

        self.dx = self.cos
        self.dy = self.sin

    def move(self):
        self.x += self.dx
        self.y -= self.dy

    def update(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check(self):
        if self.x > WIDTH or self.y > HEIGHT:
            return True

class PlayerLaser(Laser): ...


class EnemyLaser(Laser): ...