import pygame as pg
import itertools
from data import tools
import os
import random


class Enemy(pg.sprite.Sprite):
    """Traps erecting fire."""

    def __init__(self, location, name, color):
        """The location argument is where I will be located."""
        # GRAPHICS
        pg.sprite.Sprite.__init__(self)
        self.animate_timer = 0.0
        self.animate_fps = 5
        tile = tools.Image.loaddir(os.path.join("tiles", color)).convert()
        self.pre_image = pg.Surface((50, 50)).convert_alpha()
        self.pre_image.blit(tile, (0, 0))
        if name:
            self.enemy_mask = tools.Image.load(os.path.join("enemies", name)).convert_alpha()
        self.image = pg.Surface((50, 50)).convert_alpha()
        self.location = location
        self.rect = self.image.get_rect(topleft=location)
        self.enemy_frames = self.make_frame_dict()
        self.frame_count = 0
        self.mask = self.make_mask()

        # DATA
        self.speed = 1
        self.direction = "down"
        self.old_direction = None


    def make_frame_dict(self):
        frames = tools.split_sheet(self.enemy_mask, (50, 50), 3, 4)[0]
        walk_cycles = {'left': itertools.cycle(frames[9:12]),
                       'right': itertools.cycle(frames[3:6]),
                       'down': itertools.cycle(frames[6:9]),
                       'up': itertools.cycle(frames[0:3])}
        return walk_cycles

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask = pg.mask.from_surface(self.enemy_frames[self.frame_count])
        return mask

    def render(self, screen):
        screen.blit(self.pre_image, self.rect)
        screen.blit(self.image, self.rect)

    def update(self, now, obstacles, fire_traps, pit_traps, spike_traps, bear_traps, push_traps_up, push_traps_down, push_traps_right, push_traps_left):
        """
        Updates our player appropriately every frame.
        """
        self.adjust_images(now)
        self.collision_direction = None
        if self.direction_stack:
            self.movement(obstacles, 0)
            self.movement(obstacles, 1)
        if now - 1260 > self.last_hurt:
            self.hurt(now, fire_traps, pit_traps, spike_traps, bear_traps, push_traps_up, push_traps_down, push_traps_right, push_traps_left)
        if self.last_hurt < now < self.last_hurt + 160 or self.last_hurt + 220 < now < self.last_hurt + 380 or self.last_hurt + 440 < now < self.last_hurt + 600 or self.last_hurt + 660 < now < self.last_hurt + 820 or self.last_hurt + 880 < now < self.last_hurt + 1040 or self.last_hurt + 1100 < now < self.last_hurt + 1260:
            self.hurt_show = True
        else:
            self.hurt_show = False

    def adjust_images(self, now=0):
        """
        Update the sprite's walkframes as the sprite's direction changes.
        """
        if self.direction != self.old_direction:
            self.walkframes = self.walkframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image(now)

    def movement(self, obstacles, i):
        """Move player and then check for collisions; adjust as necessary."""
        direct_dict = {tools.CONTROLLER_DICT['left']: (-1, 0),
                       tools.CONTROLLER_DICT['right']: (1, 0),
                       tools.CONTROLLER_DICT['up']: (0, -1),
                       tools.CONTROLLER_DICT['down']: (0, 1)}
        change = self.speed*direct_dict[self.direction][i]
        self.rect[i] += change
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        callback = pg.sprite.collide_mask
        collide = pg.sprite.spritecollideany(self, collisions, callback)
        if collide and not self.collision_direction:
            self.collision_direction = self.get_collision_direction(collide)
        while collide:
            self.rect[i] += (1 if change<0 else -1)
            collide = pg.sprite.spritecollideany(self, collisions, callback)

    def get_collision_direction(self, other_sprite):
        """Find what side of an object the player is running into."""
        dx = self.get_finite_difference(other_sprite, 0, self.speed)
        dy = self.get_finite_difference(other_sprite, 1, self.speed)
        abs_x, abs_y = abs(dx), abs(dy)
        if abs_x > abs_y:
            return ("right" if dx>0 else "left")
        elif abs_x < abs_y:
            return ("bottom" if dy>0 else "top")
        else:
            OPPOSITE_DICT = {tools.CONTROLLER_DICT['left']: "right",
                                  tools.CONTROLLER_DICT['right']: "left",
                                  tools.CONTROLLER_DICT['up']: "bottom",
                                  tools.CONTROLLER_DICT['down']: "top"}
            return OPPOSITE_DICT[self.direction]

    def get_finite_difference(self, other_sprite, index, delta=1):
        """
        Find the finite difference in area of mask collision with the
        rects position incremented and decremented in axis index.
        """
        base_offset = [other_sprite.rect.x-self.rect.x,
                       other_sprite.rect.y-self.rect.y]
        offset_high = base_offset[:]
        offset_low = base_offset[:]
        offset_high[index] += delta
        offset_low[index] -= delta
        first_term = self.mask.overlap_area(other_sprite.mask, offset_high)
        second_term = self.mask.overlap_area(other_sprite.mask, offset_low)
        return first_term - second_term