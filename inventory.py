import pygame


def print_text(surface, message, x, y, font_color=(0), font_size=30):
    font = pygame.font.Font('data/sprites_gui/font/Pixeltype.ttf', font_size)
    text = font.render(message, True, font_color)
    surface.blit(text, (x, y))


class Inventory:
    def __init__(self):
        self.resources = {
            'amethyst': Item('Amethyst', pygame.image.load('data/sprites/items/amethyst.png')),
            'emerald': Item('Emerald', pygame.image.load('data/sprites/items/emerald.png')),
            'garnet': Item('Garnet', pygame.image.load('data/sprites/items/garnet.png')),
            'opal': Item('Opal', pygame.image.load('data/sprites/items/opal.png')),
            'sapphire': Item('Sapphire', pygame.image.load('data/sprites/items/sapphire.png')),
            'gold': Item('Gold', pygame.image.load('data/sprites/items/gold.png')),
            'silver': Item('Silver', pygame.image.load('data/sprites/items/silver.png')),
            'iron': Item('Iron', pygame.image.load('data/sprites/items/iron.png')),
            'tin': Item('Tin', pygame.image.load('data/sprites/items/tin.png')),
            'copper': Item('Copper', pygame.image.load('data/sprites/items/copper.png')),
            'malachite': Item('Malachite', pygame.image.load('data/sprites/items/malachite.png')),
            'coal': Item('Coal', pygame.image.load('data/sprites/items/coal.png')),
            'cinnabar': Item('Cinnabar', pygame.image.load('data/sprites/items/cinnabar.png')),
            'pyromorphite': Item('Pyromorphite', pygame.image.load('data/sprites/items/pyromorphite.png')),
            'fieldstone': Item('Fieldstone', pygame.image.load('data/sprites/items/fieldstone.png')),
            'limestone': Item('Limestone', pygame.image.load('data/sprites/items/limestone.png')),
            'sandstone': Item('Sandstone', pygame.image.load('data/sprites/items/sandstone.png')),
            'marble': Item('Marble', pygame.image.load('data/sprites/items/marble.png')),
            'granite': Item('Granite', pygame.image.load('data/sprites/items/granite.png')),
            'wood': Item('Wood', pygame.image.load('data/sprites/items/wood.png'))
        }

        self.inventory_panel = [None] * 4
        self.whole_panel = [None] * 24

    def get_amount(self, name):
        try:
            return self.resources[name].amount
        except KeyError:
            return -1

    def increase(self, name):
        try:
            self.resources[name].amount += 1
        except KeyError:
            print('a')

    def update(self):
        for name, item in self.resources.items():
            if item.amount != 0 and item not in self.whole_panel:
                self.whole_panel.insert(self.whole_panel.index(None), item)
                self.whole_panel.remove(None)

    def draw(self, surface):
        x = y = 60
        side = 80
        step = 100

        for cell in self.whole_panel:
            pygame.draw.rect(surface, (200, 215, 227), (x, y, side, side))
            if cell is not None:
                surface.blit(cell.image, (x + 4, y))
                print_text(surface, str(cell.amount), x + 30, y + 60, (255, 0, 0), 50)
            x += step
            if x == 1260:
                x = 60
                y += step


class Item(pygame.sprite.Sprite):
    def __init__(self, name, sprite):
        super().__init__()

        self.name = name
        self.amount = 0
        self.image = sprite
        self.rect = self.image.get_rect()