import pygame as pg
import itertools
from . import floor as f
from data import tools
from .. import astar
from math import floor
import os
import random


class Bat(pg.sprite.Sprite):
    """Traps erecting fire."""

    def __init__(self, location, color):
        """The location argument is where I will be located."""
        # GRAPHICS
        pg.sprite.Sprite.__init__(self)
        self.width, self.height = 50, 50
        self.animate_timer = 0.0
        self.animate_fps = 7
        self.color = color
        tile = tools.Image.loaddir(os.path.join("tiles", color)).convert()
        self.pre_image = pg.Surface((self.width, self.height)).convert_alpha()
        self.pre_image.blit(tile, (0, 0))
        self.enemy_mask = tools.Image.load(os.path.join("enemies", "bat", "flight.png")).convert_alpha()
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
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
        self.parsed_map = False
        self.removed = False

        # DATA
        self.life = 1
        self.speed = 1  # Must divide 50 without rest

    def make_frame_dict(self):
        frames = tools.split_sheet(self.enemy_mask, (self.width, self.height), 8, 1)[0]
        flips = [pg.transform.flip(frame, True, False) for frame in frames]
        walk_cycles = {'left': itertools.cycle(flips[0:7]),
                       'right': itertools.cycle(frames[0:7]),
                       'down': itertools.cycle(frames[0:7]),
                       'up': itertools.cycle(flips[0:7]),
                       }
        return walk_cycles

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill((0, 0, 0, 0))
        mask_surface.fill(pg.Color("white"), (10,10,30,34))  # left, top, width, height. Yet to define for the bat
        mask = pg.mask.from_surface(mask_surface)
        return mask

    def render(self, screen, bat_time=False):
        if bat_time is False:
            screen.blit(self.pre_image, self.pre_rect)
        if self.life > 0 and bat_time:
            if not self.hurt_show:
                screen.blit(self.image, self.rect)
            else:
                cpy = self.image.copy()
                cpy.blit(pg.Surface(self.image.get_size()).convert_alpha(), (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    def update(self, now, mapfile, obstacles, culprit, push_traps_up, push_traps_down, push_traps_right, push_traps_left):
        """
        Updates our player appropriately every frame.
        """
        if self.life > 0:
            if not self.direction_stack:
                self.astar_ai(mapfile)
            self.adjust_images(now)
            self.collision_direction = None
            if self.direction_stack:
                self.direction = self.direction_stack[0]
                self.movement(obstacles, 0)
                self.movement(obstacles, 1)
                self.direction_stack = self.direction_stack[1:]
            if now - 1260 > self.last_hurt:
                self.hurt(now, push_traps_up, push_traps_down, push_traps_right, push_traps_left)
            if self.last_hurt < now < self.last_hurt + 160 or self.last_hurt + 220 < now < self.last_hurt + 380 or self.last_hurt + 440 < now < self.last_hurt + 600 or self.last_hurt + 660 < now < self.last_hurt + 820 or self.last_hurt + 880 < now < self.last_hurt + 1040 or self.last_hurt + 1100 < now < self.last_hurt + 1260:
                self.hurt_show = True
            else:
                self.hurt_show = False

    def astar_ai(self, realmap):
        if not self.parsed_map:
            self.ai_doors = []
            self.map = realmap.copy()
            for i in range(0,len(self.map)):
                self.map[i] = list(self.map[i])
            for i in range(0, len(self.map)):
                for j in range(0, len(self.map[0])):
                    if self.map[i][j] == "D":
                        self.ai_doors.append((j,i))
                    pass
                    if self.map[i][j] == "O":
                        self.map[i][j] = 1
                    else:
                        self.map[i][j] = 0
            self.parsed_map = True
        ai_door = random.choice(self.ai_doors)
        rest_y = (self.rect.y + 25) % 50
        rest_x = (self.rect.x + 25) % 50
        go_up, go_down, go_right, go_left = 0, 0, 0, 0
        if rest_y > 25:
            go_up = rest_y - 25
            # go up
            pass
        elif rest_y < 25:
            go_down = 25 - rest_y
            # go down
            pass
        elif rest_y == 25:
            # intended location
            pass
        if rest_x > 25:
            go_left = rest_x - 25
            # go left
            pass
        elif rest_x < 25:
            go_right = 25 - rest_x
            # go right
            pass
        elif rest_x == 25:
            # intended location
            pass
        end_y = ai_door[1]
        end_x = ai_door[0]
        start_y = floor((self.rect.y + 25) / 50)
        start_x = floor((self.rect.x + 25) / 50)
        if end_y < 0:
            end_y = 0
        if end_y > 11:
            end_y = 11
        if end_x < 0:
            end_x = 0
        if end_x > 15:
            end_x = 15
        if start_y < 0:
            start_y = 0
        if start_y > 11:
            start_y = 11
        if start_x < 0:
            start_x = 0
        if start_x > 15:
            start_x = 15
        end = (end_y,end_x)
        start = (start_y,start_x)
        dirr = astar.astar(self.map, start, end)
        if not dirr:
            odds = random.randint(1, 4)
            if odds == 1:
                dirr = [start, (start_y, start_x + 1)]
            if odds == 2:
                dirr = [start, (start_y, start_x - 1)]
            if odds == 3:
                dirr = [start, (start_y + 1, start_x)]
            if odds == 4:
                dirr = [start, (start_y - 1, start_x)]
        count = 0
        if go_up > 0:
            for step in range(0, int(go_up / self.speed)):
                self.direction_stack.append("up")
                count += 1
        if go_down > 0:
            for step in range(0, int(go_down / self.speed)):
                self.direction_stack.append("down")
                count += 1
        if go_right > 0:
            for step in range(0, int(go_right / self.speed)):
                self.direction_stack.append("right")
                count += 1
        if go_left > 0:
            for step in range(0, int(go_left / self.speed)):
                self.direction_stack.append("left")
                count += 1
        for i in range(0, len(dirr) - 1):
            if dirr[i+1][0] > dirr[i][0]:
                for step in range(0,int(50/self.speed)):
                    self.direction_stack.append("down")
            elif dirr[i+1][0] < dirr[i][0]:
                for step in range(0, int(50 / self.speed)):
                    self.direction_stack.append("up")
            elif dirr[i+1][1] > dirr[i][1]:
                for step in range(0, int(50 / self.speed)):
                    self.direction_stack.append("right")
            elif dirr[i+1][1] < dirr[i][1]:
                for step in range(0, int(50 / self.speed)):
                    self.direction_stack.append("left")
        if f.Floor.size < 5:
            return
        elif f.Floor.size < 7:
            if len(self.direction_stack) > (int(50/self.speed) * 12) + count:
                self.direction_stack = self.direction_stack[:(int(50/self.speed) * 12) + count]
        else:
            if len(self.direction_stack) > int(50/self.speed) * 6 + count:
                self.direction_stack = self.direction_stack[:int(50/self.speed) * 6 + count]

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

    def hurt(self, now, push_traps_up, push_traps_down, push_traps_right, push_traps_left):
        callback = pg.sprite.collide_mask

        self.collide_push_up = pg.sprite.spritecollideany(self, push_traps_up, callback)
        self.collide_push_down = pg.sprite.spritecollideany(self, push_traps_down, callback)
        self.collide_push_right = pg.sprite.spritecollideany(self, push_traps_right, callback)
        self.collide_push_left = pg.sprite.spritecollideany(self, push_traps_left, callback)

        if self.collide_push_up or self.collide_push_down or self.collide_push_left or self.collide_push_right:
            self.life -= 1
            self.last_hurt = now