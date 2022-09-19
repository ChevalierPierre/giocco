import pygame as pg
import itertools
from . import tools
import random

class Door(pg.sprite.Sprite):
    """Something to change maps."""
    def __init__(self, location, leads_to):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.leads_to = leads_to
        self.animate_timer = 0.0
        self.animate_fps = 7
        self.door_mask = tools.Image.load("portal.png").convert()
        self.image = pg.Surface((50,50)).convert_alpha()
        self.interact_image = pg.Surface((2,2)).convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
        self.interact_rect = self.interact_image.get_rect(topleft=location)
        self.doorframes = self.make_frame_dict()
        self.mask = self.make_mask()

    def make_frame_dict(self):
        frames = tools.split_sheet(self.door_mask, (50, 50), 4, 4)[0]
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
        mask_surface.fill((0,0,0,0))
        mask_surface.fill(pg.Color("white"), (23,23,4,4))
        mask = pg.mask.from_surface(mask_surface)
        return mask

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, now):
        self.adjust_images(now)
        

