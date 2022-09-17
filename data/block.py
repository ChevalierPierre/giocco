import pygame as pg
from . import tools

import random


class Block(pg.sprite.Sprite):
    """Something to run head-first into."""
    def __init__(self, location):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.shade_mask = tools.Image.load("shader.png").convert()
        self.image = self.make_image()
        self.rect = self.image.get_rect(topleft=location)
        self.mask = pg.mask.from_surface(self.image)

    def make_image(self):
        """Let's not forget aesthetics."""
        image = pg.Surface((50,50)).convert_alpha()
        #image.fill([random.randint(0, 255) for _ in range(3)])
        image.blit(self.shade_mask, (0,0))
        return image

    def render(self, screen):
        screen.blit(self.image, self.rect)
