import pygame


class SpriteSheet:
    def __init__(self, image: pygame.Surface):
        self.sheet = image

    def get_image(self, frame, width, height, key_color, scale=1) -> pygame.Surface:
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(key_color)

        return image