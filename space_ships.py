import pygame


class SpaceShip(pygame.sprite.Sprite):
    dist = 1
    image = pygame.image.load('data/sprites/space_ships/spaceship.png')

    def __init__(self, *args):
        super().__init__(*args)
        self.image = SpaceShip.image
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

    def return_image(self):
        return self.image

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.rect.top += self.dist
            self.image = pygame.transform.rotate(SpaceShip.image, 180)
        elif keys[pygame.K_w]:
            self.rect.top -= self.dist
            self.image = pygame.transform.rotate(SpaceShip.image, 360)
        if keys[pygame.K_d]:
            self.rect.left += self.dist
            self.image = pygame.transform.rotate(SpaceShip.image, -90)
        elif keys[pygame.K_a]:
            self.rect.left -= self.dist
            self.image = pygame.transform.rotate(SpaceShip.image, 90)



class Player(SpaceShip): ...


class Enemy(SpaceShip): ...


class Laser(pygame.sprite.Sprite): ...


class PlayerLaser(Laser): ...


class EnemyLaser(Laser): ...