import random
import sys
import threading

import pygame

from space_ships import *
from fx import *
from gui import *
from const import *
from spritesheet import *
from object import *
from inventory import *


pygame.init()

pygame.mixer.init()

pygame.mixer.music.load("data/music/master/menu.mp3")
pygame.mixer.music.play(-1)

pygame.display.set_caption("StarFall")
pygame.display.set_icon(pygame.image.load('data/sprites_gui/icon.png'))

bh = BlackHole(AnimatedSprite(pygame.image.load('data/sprites/objects/black_holes/black_hole (4).png'), 50, 1, 200, 200))

asteroids = [Asteroid(pygame.image.load(f'data/sprites/objects/asteroids/normal/asteroid ({random.randint(1, 7)}).png')) for _ in range(20)]
for asteroid in asteroids:
    asteroid.rect.center = (random.randint(10, 1500), random.randint(10, 1500))

def exit_():
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.camera = Camera(WIDTH, HEIGHT)
        self.cursor = Cursor()

        self.inventory = Inventory()

        # --- КНОПКИ В МЕНЮ ---
        self.play_button = Button(WIDTH / 2 - 200, HEIGHT / 2, pygame.image.load('data/sprites_gui/buttons/play.png'), 1)
        self.exit_button = Button(WIDTH / 2 - 200, HEIGHT / 2 + 200, pygame.image.load('data/sprites_gui/buttons/exit.png'), 1)
        self.settings_button = Button(WIDTH / 2 - 200, HEIGHT / 2 + 100, pygame.image.load('data/sprites_gui/buttons/settings.png'), 1)
        # --- КНОПКИ В ИГРЕ ---
        self.map_button = Button(WIDTH - 150, HEIGHT - 100, pygame.image.load('data/sprites_gui/other/map_icon.png'), 1)
        self.shop_button = Button(WIDTH - 150, HEIGHT - 200, pygame.image.load('data/sprites_gui/other/shop_icon.png'), 1)
        # ---------------------

        self.logo = pygame.image.load('data/sprites_gui/logo.png')

        self.player = Player((WIDTH // 2, HEIGHT // 2), 2, 1,
                                pygame.image.load('data/sprites/space_ships/spaceship.png'),
                                pygame.image.load(f'data/sprites/lasers/laser ({random.randint(1, 8)}).png'))
        self.player_laser_group = pygame.sprite.Group()

        self.enemy_manager = EnemyManagerPass(self.player)

        self.clicked = False
        self.action = False

        self.run()

    def run(self):
        self.starfield = Starfield(self)
        self.alpha_surface = pygame.Surface(SIZE)
        self.alpha_surface.set_alpha(ALPHA_STARS)

        pygame.mouse.set_visible(False)
        while True:
            pos = pygame.mouse.get_pos()

            self.screen.blit(self.alpha_surface, (0, 0))
            self.starfield.run()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_()
                if pygame.mouse.get_focused():
                    self.cursor.update(pygame.mouse.get_pos())

            if self.play_button.rect.collidepoint(pos):
                self.play_button.image = pygame.image.load('data/sprites_gui/buttons/play_glow.png')
            else:
                self.play_button.image = pygame.image.load('data/sprites_gui/buttons/play.png')

            if self.exit_button.rect.collidepoint(pos):
                self.exit_button.image = pygame.image.load('data/sprites_gui/buttons/exit_glow.png')
            else:
                self.exit_button.image = pygame.image.load('data/sprites_gui/buttons/exit.png')

            if self.settings_button.rect.collidepoint(pos):
                self.settings_button.image = pygame.image.load('data/sprites_gui/buttons/settings_glow.png')
            else:
                self.settings_button.image = pygame.image.load('data/sprites_gui/buttons/settings.png')

            if self.play_button.draw(self.screen):
                self.start()
            if self.settings_button.draw(self.screen):
                ...
            if self.exit_button.draw(self.screen):
                exit_()

            self.screen.blit(self.logo, (WIDTH / 2 - 400, HEIGHT / 2 - 380))
            self.cursor.draw(self.screen)
            pygame.display.update()
            self.clock.tick(120)

    def start(self):
        pygame.mixer.music.load("data/music/master/master.wav")
        pygame.mixer.music.play(-1)

        self.starfield = None
        self.alpha_surface = None
        self.play_button = None
        self.exit_button = None
        self.settings_button = None

        while True:
            self.screen.fill((0, 0, 0))
            [self.screen.blit(sprite.image, self.camera.apply(sprite)) for sprite in ALL_SPRITES]
            [self.screen.blit(sprite.image, self.camera.apply(sprite)) for sprite in ASTEROIDS_GROUP]
            self.screen.blit(self.player.image, self.player.rect)

            self.player_laser_group.draw(self.screen)

            self.enemy_manager.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        laser = self.player.shoot()
                        if laser:
                            self.player_laser_group.add(laser)
                    if event.key == pygame.K_e:
                        self.player.get_health(100000)
                    if event.key == pygame.K_q:
                        self.player.get_damage(200)

                if pygame.mouse.get_focused():
                    self.cursor.update(pygame.mouse.get_pos())

            if self.map_button.draw(self.screen):
                pass
            if self.shop_button.draw(self.screen):
                self.open_shop()

            self.cursor.draw(self.screen)

            # --- ДВИЖЕНИЕ ИГРОКА ---
            vector = [0, 0]
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                vector[0] -= 1
            if keys[pygame.K_RIGHT]:
                vector[0] += 1
            if keys[pygame.K_UP]:
                vector[1] -= 1
            if keys[pygame.K_DOWN]:
                vector[1] += 1

            self.player.move(vector[0], vector[1])
            # ------------------------

            self.update()

    def open_map(self): ...

    def manage_enemy_collision(self):
        for enemy in self.enemy_manager.sprite_group.sprites():
            for laser in pygame.sprite.spritecollide(enemy, self.player_laser_group, False):
                enemy.kill()
                laser.kill()
                del enemy
                del laser
        for laser in pygame.sprite.spritecollide(self.player, self.enemy_manager.laser_group, False):
            laser.kill()
            del laser
            self.player.get_damage(200)

    def manage_asteroid_collision(self):
        for asteroid in ASTEROIDS_GROUP.sprites():
            for laser in pygame.sprite.spritecollide(asteroid, self.player_laser_group, False):
                asteroid.kill()
                self.inventory.increase('fieldstone')
                laser.kill()
                del asteroid
                del laser

    def open_shop(self):
        pygame.mixer.music.load("data/music/master/loading.wav")
        pygame.mixer.music.play(-1)

        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.inventory.increase('opal')
                    if event.key == pygame.K_2:
                        self.inventory.increase('cinnabar')
                        self.inventory.increase('pyromorphite')
                    if event.key == pygame.K_3:
                        self.inventory.increase('marble')
                    if event.key == pygame.K_4:
                        self.inventory.increase('wood')

                if pygame.mouse.get_focused():
                    self.cursor.update(pygame.mouse.get_pos())
            self.inventory.draw(self.screen)
            self.cursor.draw(self.screen)
            self.inventory.update()
            pygame.display.update()
            self.clock.tick(60)

    def clear_lasers(self):
        for laser in self.player_laser_group.sprites():
            if laser.rect.centerx > SIZE[0]:
                self.player_laser_group.remove(laser)
            if laser.rect.centery > SIZE[1]:
                self.player_laser_group.remove(laser)
            if laser not in self.player_laser_group:
                del laser

    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_()
            if pygame.mouse.get_focused():
                self.cursor.update(pygame.mouse.get_pos())
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                paused = False
        pygame.display.update()
        self.clock.tick(15)

    # --- МЕТОД, ДЛЯ ОБНОВЛЕНИЯ ОБЪЕКТОВ ---
    def update(self):
        if self.player.current_health == 0:
            exit_()
        if self.enemy_manager:
            if self.enemy_manager.level > 4:
                self.enemy_manager = EnemyManagerPass(self.player)
                pygame.mixer.music.load("data/music/master/master.wav")
                pygame.mixer.music.play(-1)
        if len(asteroids) < 10:
            self.enemy_manager = EnemyManager(self.player)
        self.clear_lasers()
        self.player.update(self.screen)
        if self.enemy_manager:
            self.enemy_manager.update()
        self.player_laser_group.update()

        [sprite.update() for sprite in ALL_SPRITES]

        self.manage_enemy_collision()
        self.manage_asteroid_collision()

        self.camera.update(self.player)
        pygame.display.update()

        self.clock.tick(120)
    # ---------------------------------------
