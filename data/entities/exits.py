import pygame as pg
from data import tools
import itertools
import os
class Exits(pg.sprite.Sprite):
    """Something to run head-first into."""
    def __init__(self, location, color):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.animate_timer = 0.0
        self.animate_fps = 7
        tile = tools.Image.loaddir(os.path.join("tiles", color)).convert()
        self.pre_image = pg.Surface((50,50)).convert_alpha()
        self.pre_image.blit(tile, (0,0))
        self.door_mask = tools.Image.load("exits.png").convert_alpha()
        self.image = pg.Surface((50,50)).convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
        self.doorframes = self.make_frame_dict()
        self.mask = self.make_mask()

    def make_frame_dict(self):
        frames = tools.split_sheet(self.door_mask, (50, 50), 3, 2)[0]
        door_cycles = itertools.cycle(frames)
        return door_cycles

    def adjust_images(self, now=0):
        elapsed = now - self.animate_timer > 1000.0 / self.animate_fps
        if elapsed:
            self.image = next(self.doorframes)
            self.animate_timer = now

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill((0, 0, 0, 0))
        mask_surface.fill(pg.Color("white"), (5, 5, 40, 40))
        mask = pg.mask.from_surface(mask_surface)
        return mask

    def render(self, screen):
        screen.blit(self.pre_image, self.rect)
        screen.blit(self.image, self.rect)

    def update(self, now):
        self.adjust_images(now)


