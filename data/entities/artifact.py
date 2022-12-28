import pygame as pg
import itertools
from data import tools
import os
import random

class Artifact(pg.sprite.Sprite):
    """Traps erecting fire."""

    def __init__(self, location, color):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.animate_timer = 0.0
        self.animate_fps = 2
        tile = tools.Image.loaddir(os.path.join("tiles", color)).convert()
        self.pre_image = pg.Surface((50, 50)).convert_alpha()
        self.pre_image.blit(tile, (0, 0))
        artifact_list = ["life"]
        self.artifact_name = random.choice(artifact_list)
        self.artifact_mask = tools.Image.load(os.path.join("artifacts", self.artifact_name + ".png")).convert_alpha()
        self.image = pg.Surface((50, 50)).convert_alpha()
        self.location = location
        self.rect = self.image.get_rect(topleft=location)
        self.artifact_frames = self.make_frame_dict()
        self.mask = self.make_mask()
        self.removed = False
        self.used = False

    def make_frame_dict(self):
        if self.artifact_name == "life":
            frames = tools.split_sheet(self.artifact_mask, (50, 50), 6, 1)[0]
        cycles = itertools.cycle(frames)
        return cycles

    def adjust_images(self, now=0):
        elapsed = now - self.animate_timer > 1000.0 / self.animate_fps
        if elapsed:
            self.image = next(self.artifact_frames)
            self.animate_timer = now

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill((0, 0, 0, 0))
        mask_surface.fill(pg.Color("white"), (10, 25, 20, 20))
        mask = pg.mask.from_surface(mask_surface)
        return mask

    def render(self, screen):
        screen.blit(self.pre_image, self.rect)
        if not self.used:
            screen.blit(self.image, self.rect)

    def update(self, now):
        if random.randint(0,2) == 0:
            return
        self.adjust_images(now)


