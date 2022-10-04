import pygame as pg
from data import tools


class Heart(pg.sprite.Sprite):
    """Something to run head-first into."""
    def __init__(self, location):
        """The location argument is where I will be located."""
        self.pos_x = location[0]
        self.pos_y = location[1]
        self.sprite = tools.Image.load("heart.png").convert_alpha()
        self.image = self.make_image()
        self.rect = self.image.get_rect(topleft=location)

    def make_image(self):
        """Let's not forget aesthetics."""
        image = pg.Surface((36,36)).convert_alpha()
        image.blit(self.sprite, (0,0))
        image.set_colorkey((0, 0, 0))
        return image

    def render(self, screen):
        screen.blit(self.image, self.rect)
