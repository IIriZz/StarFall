import pygame


class Object:
    animation_step = 50
    animation_update = pygame.time.get_ticks()
    animation_cooldown = 50
    frame = 0

    def __init__(self, anim_list, pos):
        self.list = anim_list
        self.pos = pos
        self.rect = self.list[self.frame].get_rect()

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_update >= self.animation_cooldown:
            self.frame += 1
            self.animation_update = current_time
            if self.frame >= len(self.list):
                self.frame = 0
        screen.blit(self.list[self.frame], self.pos)


class Star(Object):
    def info(self): ...


class Asteroid(Object): ...


class Planet(Object): ...


class GasGiant(Planet): ...


class BlackHole(Object):
    def active_hyperspace(self, app):
        import fx


        self.hyperspace = fx.Hyperspace(app)
        self.hyperspace.run()
