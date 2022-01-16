import pygame
import const


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/sprites_gui/cursor.png")
        self.rect = self.image.get_rect(topleft=(0, 0))

    def update(self, pos):
        self.rect.topleft = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()

        self.sound = pygame.mixer.Sound('data/music/gui/zoom.wav')

        self.action = False
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.action = True
                self.sound.play()
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)

        return self.action


class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(const.ALL_SPRITES)

        self.image = image
        self.rect = self.image.get_rect()


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, obj):
        return obj.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + (const.WIDTH / 2)
        y = -target.rect.y + (const.HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
