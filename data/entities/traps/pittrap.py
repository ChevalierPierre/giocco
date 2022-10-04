import pygame as pg
from data import tools
import os


class Pittrap(pg.sprite.Sprite):
    """Trap filled with spikes."""

    def __init__(self, location):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.firetrap_mask = tools.Image.load(os.path.join("traps", "Pit_Trap_Spikes.png")).convert_alpha()
        self.image = self.make_image()
        self.rect = self.image.get_rect(topleft=location)
        self.mask = self.make_mask()

    def make_image(self):
        """Let's not forget aesthetics."""
        image = pg.Surface((50,50)).convert_alpha()
        image.blit(self.firetrap_mask, (0,0))
        return image

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill(pg.Color("white"), (5, 5, 40, 40))
        mask = pg.mask.from_surface(mask_surface)
        return mask

    def render(self, screen):
        screen.blit(self.image, self.rect)


