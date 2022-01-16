import random

import pygame
import math
import time

from const import *


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, pos, speed, scale, image, laser_image):
        super().__init__()

        self.pos = pos

        self.speed = speed
        self.angle_speed = 5
        self.scale = scale

        self.laser_image = laser_image

        self.laser_sound = pygame.mixer.Sound('data/music/sfx/laser.mp3')
        self.hurt_sound = pygame.mixer.Sound('data/music/sfx/hurt.mp3')

        self.laser_timer = 0.2
        self.start_time = 0
        self.can_shoot = True

        self.image = image
        self.image_clear = image

        self.mask = pygame.mask.from_surface(self.laser_image)

        self.rotation = 0
        self.direction = pygame.math.Vector2(0, 1)

        self.rect = self.image.get_rect()

    def update(self):
        self.image = pygame.transform.rotozoom(self.image_clear, self.rotation, self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        if time.time() - self.start_time >= self.laser_timer:
            self.can_shoot = True

    def move(self, dx, dy):
        delta_rotation = dx * self.angle_speed
        self.rotation -= delta_rotation

        vec = pygame.math.Vector2(0, 1)
        vec.y = dy * self.speed
        vec.rotate_ip(-self.rotation)

        self.direction.rotate_ip(delta_rotation)
        self.direction.normalize_ip()

        self.pos = (self.pos[0] + vec.x, self.pos[1] + vec.y)

    def shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            self.start_time = time.time()
            self.laser_sound.play()
            return Laser(self.pos, (self.direction.x, self.direction.y), 15, self.laser_image)


class Player(SpaceShip):
    def __init__(self, pos, speed, scale, image, laser_image):
        super().__init__(pos, speed, scale, image, laser_image)

        self.current_health = 200
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length

        self.regeneration_timer = 5
        self.regeneration_time_start = time.time()

    def update(self, surface):
        self.health_bar_active(surface)

        self.image = pygame.transform.rotozoom(self.image_clear, self.rotation, self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        if time.time() - self.start_time >= self.laser_timer:
            self.can_shoot = True
        if time.time() - self.regeneration_time_start >= self.regeneration_timer:
            self.get_health(0.5)

    def get_damage(self, amount):
        if self.current_health > 0:
            self.hurt_sound.play()
            self.current_health -= amount
        if self.current_health <= 0:
            self.hurt_sound.play()
            self.current_health = 0

    def get_health(self, amount):
        if self.current_health < self.max_health:
            self.current_health += amount
        if self.current_health >= self.max_health:
            self.current_health = self.max_health

    def health_bar_active(self, surface):
        if self.current_health <= self.max_health // 4:
            pygame.draw.rect(surface, (255, 0, 0), (125, 50, self.current_health / self.health_ratio, 25))
            pygame.draw.rect(surface, (100, 100, 100), (125, 50, self.health_bar_length, 25), 4)
        else:
            pygame.draw.rect(surface, (62, 180, 137), (125, 50, self.current_health / self.health_ratio, 25))
            pygame.draw.rect(surface, (100, 100, 100), (125, 50, self.health_bar_length, 25), 4)


class EnemyManager:
    def __init__(self, target):
        self.target = target

        self.sprite_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()

        self.laser_image = pygame.image.load(f'data/sprites/lasers/laser ({random.randint(1, 8)}).png')
        self.enemies = [pygame.image.load('data/sprites/space_ships/spaceship2.png'),
                        pygame.image.load('data/sprites/space_ships/spaceship3.png')]

        self.trajectory = (WIDTH // 2 - 100, HEIGHT // 2 - 50)

        self.level = 1
        self.spawn(self.level)

    def update(self):
        if len(self.sprite_group.sprites()) == 0:
            self.level += 1
            self.spawn(self.level)
        for enemy in self.sprite_group.sprites():
            laser = enemy.pre_update(self.target)
            if laser:
                self.laser_group.add(laser)
        self.sprite_group.update()
        self.laser_group.update()

    def draw(self, surface):
        self.sprite_group.draw(surface)
        self.laser_group.draw(surface)

    def spawn(self, n):
        for i in range(n):
            enemy_image = random.choice(self.enemies)
            enemy = Enemy((400, 100 * i), self.target.speed, 1.5, enemy_image, self.laser_image, self.trajectory)

            self.sprite_group.add(enemy)


class EnemyManagerPass(EnemyManager):
    def __init__(self, target):
        super().__init__(target)

    def update(self): pass

    def draw(self, surface): pass

    def spawn(self, n): pass


class Enemy(SpaceShip):
    def __init__(self, pos, speed, scale, image, laser_image, trajectory):
        super().__init__(pos, speed, scale, image, laser_image)

        self.trajectory_origin = trajectory
        self.trajectory = self.trajectory_origin
        self.trajectory_speed = 0.005

        self.time = random.random() * 100
        self.clockwise = False

        # --- СИСТЕМА СТРЕЛЬБЫ ---
        self.shoot_timer_range = [0.8, 5]
        self.shoot_timer_start = time.time()
        self.shoot_timer = self.calculate_timer(self.shoot_timer_range)
        # ------------------------

        # --- ОБРАТНАЯ СИСТЕМА ---
        self.reverse_timer_range = [2.5, 6]
        self.reverse_timer_start = time.time()
        self.reverse_timer = self.calculate_timer(self.reverse_timer_range)
        # ------------------------

    def increase_time(self):
        if self.clockwise:
            self.time += self.trajectory_speed
        else:
            self.time -= self.trajectory_speed

    @staticmethod
    def calculate_trajectory(a, b, t):
        return (WIDTH // 2 + a * math.cos(t), HEIGHT // 2 + b * math.sin(t))

    def pre_update(self, target):
        direction = pygame.math.Vector2(self.pos[0] - target.pos[0], self.pos[1] - target.pos[1]).normalize()
        self.rotation = direction.angle_to(pygame.math.Vector2(0, 1))

        self.direction = pygame.math.Vector2(float(direction.x), float(direction.y))

        self.increase_time()
        self.pos = self.calculate_trajectory(self.trajectory[0], self.trajectory[1], self.time)

        if time.time() - self.reverse_timer_start >= self.reverse_timer:
            self.reverse_timer_start = time.time()
            self.reverse_timer = self.calculate_timer(self.reverse_timer_range)
            self.clockwise = not self.clockwise

        if time.time() - self.shoot_timer_start >= self.shoot_timer:
            self.shoot_timer_start = time.time()
            self.shoot_timer = self.calculate_timer(self.shoot_timer_range)
            return self.shoot()
        else:
            return None

    @staticmethod
    def calculate_timer(range_):
        return random.random() * (range_[1] - range_[0]) + range_[0]


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, image):
        super().__init__()

        self.pos = pos
        self.direction = pygame.math.Vector2(direction[0], direction[1])
        self.speed = speed
        self.image_clear = image

        self.rotation = self.direction.angle_to(pygame.math.Vector2(0, 1))
        self.image = pygame.transform.rotate(self.image_clear, self.rotation)
        self.rect = self.image.get_rect()

    def update(self):
        self.pos = (self.pos[0] - self.speed * self.direction[0],
                    self.pos[1] - self.speed * self.direction[1])
        self.rect.center = self.pos
