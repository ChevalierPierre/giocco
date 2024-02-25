import pygame as pg
import itertools
from data import tools
import os
import random
import time


class Beartrap(pg.sprite.Sprite):
    """Traps erecting fire."""

    def __init__(self, location, color):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        # DATA
        random.seed(time.time())
        self.id = random.randint(1,100)
        self.animate_timer = 0.0
        self.animate_fps = 7
        self.animate_counter = 1
        self.animate_touched = False
        # GRAPHICS
        tile = tools.Image.loaddir(os.path.join("tiles", color)).convert()
        self.pre_image = pg.Surface((50, 50)).convert_alpha()
        self.pre_image.blit(tile, (0, 0))
        self.beartrap_image = tools.Image.load(os.path.join("traps", "Bear_Trap.png")).convert_alpha()
        self.image = pg.Surface((50, 50)).convert_alpha()
        self.location = location
        self.rect = self.image.get_rect(topleft=location)
        self.beartrap_frames = self.make_frame_dict()
        self.frame_count = 0
        self.mask = self.make_mask()
        self.image = self.beartrap_frames[self.frame_count]

    def make_frame_dict(self):
        frames = tools.split_sheet(self.beartrap_image, (50, 50), 4, 1)[0]
        return frames

    def adjust_images(self, now=0, touched=False):
        if touched:
            self.animate_touched = True
        elapsed = now - self.animate_timer > 1000.0 / self.animate_fps
        if elapsed and self.animate_touched:
            if self.animate_counter != 0:
                self.animate_timer = now
                self.frame_count += 1
                if self.frame_count == 4:
                    self.frame_count = 0
                self.image = self.beartrap_frames[self.frame_count]
                self.animate_timer = now
                self.animate_counter -= 1
            else:
                self.animate_touched = False
                self.animate_counter = 1

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask = pg.mask.from_surface(self.beartrap_frames[self.frame_count])
        return mask

    def render(self, screen):
        screen.blit(self.pre_image, self.rect)
        screen.blit(self.image, self.rect)

    def update(self, now, touched=None):
        self.adjust_images(now, touched)


