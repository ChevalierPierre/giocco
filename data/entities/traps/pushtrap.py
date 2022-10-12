import pygame as pg
import itertools
from data import tools
import os
import random

class Pushtrap(pg.sprite.Sprite):
    """Traps erecting fire."""

    def __init__(self, location, direction, color):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.animate_timer = 0.0
        self.animate_fps = 5
        tile = tools.Image.loaddir(os.path.join("tiles", color)).convert()
        self.pre_image = pg.Surface((50, 50)).convert_alpha()
        self.pre_image.blit(tile, (0, 0))
        if direction == "bottom" or direction == "front":
            self.pushtrap_mask = tools.Image.load(os.path.join("traps", "Push_Trap_Bottom.png")).convert_alpha()
        elif direction == "right" or direction == "left":
            self.pushtrap_mask = tools.Image.load(os.path.join("traps", "Push_Trap_Right.png")).convert_alpha()
        self.image = pg.Surface((50, 50)).convert_alpha()
        self.location = location
        self.rect = self.image.get_rect(topleft=location)
        self.pushtrap_frames = self.make_frame_dict(direction)
        self.frame_count = 0
        self.mask = self.make_mask()

    def make_frame_dict(self, direction):
        frames = tools.split_sheet(self.pushtrap_mask, (50, 50), 4, 1)[0]
        if direction == "front":
            frames = [pg.transform.flip(frame, False, True) for frame in frames]
        elif direction == "left":
            frames = [pg.transform.flip(frame, True, False) for frame in frames]
        return frames

    def adjust_images(self, now=0):
        elapsed = now - self.animate_timer > 1000.0 / self.animate_fps
        if elapsed:
            self.image = self.pushtrap_frames[self.frame_count]
            self.animate_timer = now
            self.frame_count += 1
            if self.frame_count == 4:
                self.frame_count = 0

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask = pg.mask.from_surface(self.pushtrap_frames[self.frame_count])
        return mask

    def render(self, screen):
        screen.blit(self.pre_image, self.rect)
        screen.blit(self.image, self.rect)

    def update(self, now):
        if random.randint(0,2) == 0:
            return
        self.mask = self.make_mask()
        self.adjust_images(now)


