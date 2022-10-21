import pygame as pg
import itertools
from data import tools
import os
import random


class Cobra(pg.sprite.Sprite):
    """Traps erecting fire."""

    def __init__(self, location, color):
        """The location argument is where I will be located."""
        # GRAPHICS
        pg.sprite.Sprite.__init__(self)
        self.animate_timer = 0.0
        self.animate_fps = 5
        tile = tools.Image.loaddir(os.path.join("tiles", color)).convert()
        self.pre_image = pg.Surface((50, 50)).convert_alpha()
        self.pre_image.blit(tile, (0, 0))
        self.enemy_mask = tools.Image.load(os.path.join("enemies", "king_cobra-blue.png")).convert_alpha()
        self.image = pg.Surface((50, 50)).convert_alpha()
        self.location = location
        self.rect = self.image.get_rect(topleft=location)
        self.pre_rect = self.pre_image.get_rect(topleft=location)
        self.walkframes = None
        self.frame_count = 0
        self.direction = "down"
        self.old_direction = None
        self.direction_stack = []
        self.redraw = True
        self.walkframe_dict = self.make_frame_dict()
        self.last_hurt = 0
        self.hurt_show = False
        self.mask = self.make_mask()

        # DATA
        self.life = 16
        self.speed = 1

    def make_frame_dict(self):
        frames = tools.split_sheet(self.enemy_mask, (50, 50), 3, 4)
        walk_cycles = {'left': itertools.cycle(frames[3][0:2]),
                       'right': itertools.cycle(frames[1][0:2]),
                       'down': itertools.cycle(frames[2][0:2]),
                       'up': itertools.cycle(frames[0][0:2])}
        return walk_cycles

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill((0, 0, 0, 0))
        mask_surface.fill(pg.Color("white"), (5,30,40,20))
        mask = pg.mask.from_surface(mask_surface)
        return mask

    def render(self, screen):
        screen.blit(self.pre_image, self.pre_rect)
        if self.life > 0:
            if not self.hurt_show:
                screen.blit(self.image, self.rect)
            else:
                cpy = self.image.copy()
                cpy.blit(pg.Surface(self.image.get_size()).convert_alpha(), (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    def update(self, now, obstacles, culprit, fire_traps, pit_traps, spike_traps, bear_traps, push_traps_up, push_traps_down, push_traps_right, push_traps_left):
        """
        Updates our player appropriately every frame.
        """
        if self.life > 0:
            self.ai(now, obstacles, culprit)
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

    def ai(self, now, obstacles, culprit):
        distance_x = culprit.rect.x - self.rect.x
        distance_y = culprit.rect.y - self.rect.y
        if abs(distance_x) >= abs(distance_y):
            if distance_x > 0:
                dirr = 2
            else:
                dirr = 3
        else:
            if distance_y > 0:
                dirr = 1
            else:
                dirr = 0
        if dirr == 0:
            if "up" in self.direction_stack:
                self.direction_stack.remove("up")
            self.direction_stack.append("up")
            self.direction = self.direction_stack[-1]
        if dirr == 1:
            if "down" in self.direction_stack:
                self.direction_stack.remove("down")
            self.direction_stack.append("down")
            self.direction = self.direction_stack[-1]
        if dirr == 2:
            if "right" in self.direction_stack:
                self.direction_stack.remove("right")
            self.direction_stack.append("right")
            self.direction = self.direction_stack[-1]
        if dirr == 3:
            if "left" in self.direction_stack:
                self.direction_stack.remove("left")
            self.direction_stack.append("left")
            self.direction = self.direction_stack[-1]

    def adjust_images(self, now=0):
        """
        Update the sprite's walkframes as the sprite's direction changes.
        """
        if self.direction != self.old_direction:
            self.walkframes = self.walkframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image(now)

    def make_image(self, now):
        """
        Update the sprite's animation as needed.
        """
        elapsed = now-self.animate_timer > 1000.0/self.animate_fps
        if self.redraw or (self.direction_stack and elapsed):
            self.image = next(self.walkframes)
            self.animate_timer = now
        self.redraw = False

    def movement(self, obstacles, i):
        """Move player and then check for collisions; adjust as necessary."""
        direct_dict = {'left': (-1, 0),
                       'right': (1, 0),
                       'up': (0, -1),
                       'down': (0, 1)}
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
            return self.direction

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

    def hurt(self, now, fire_traps, pit_traps, spike_traps, bear_traps, push_traps_up, push_traps_down, push_traps_right, push_traps_left):
        collisions_fire = pg.sprite.spritecollide(self, fire_traps, False)
        collisions_pit = pg.sprite.spritecollide(self, pit_traps, False)
        collisions_spike = pg.sprite.spritecollide(self, spike_traps, False)
        collisions_bear = pg.sprite.spritecollide(self, bear_traps, False)
        collisions_push_up = pg.sprite.spritecollide(self, push_traps_up, False)
        collisions_push_down = pg.sprite.spritecollide(self, push_traps_down, False)
        collisions_push_right = pg.sprite.spritecollide(self, push_traps_right, False)
        collisions_push_left = pg.sprite.spritecollide(self, push_traps_left, False)

        callback = pg.sprite.collide_mask

        self.collide_fire = pg.sprite.spritecollideany(self, collisions_fire, callback)
        self.collide_pit = pg.sprite.spritecollideany(self, collisions_pit, callback)
        self.collide_spike = pg.sprite.spritecollideany(self, collisions_spike, callback)
        self.collide_bear = pg.sprite.spritecollideany(self, collisions_bear, callback)
        self.collide_push_up = pg.sprite.spritecollideany(self, collisions_push_up, callback)
        self.collide_push_down = pg.sprite.spritecollideany(self, collisions_push_down, callback)
        self.collide_push_right = pg.sprite.spritecollideany(self, collisions_push_right, callback)
        self.collide_push_left = pg.sprite.spritecollideany(self, collisions_push_left, callback)

        if self.collide_fire or self.collide_pit or self.collide_spike or self.collide_bear or self.collide_push_up or self.collide_push_down or self.collide_push_left or self.collide_push_right:
            self.life -= 1
            self.last_hurt = now