import pygame


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image



class Player(SpaceShip): ...


class Enemy(SpaceShip): ...


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


class PlayerLaser(Laser): ...


class EnemyLaser(Laser): ...