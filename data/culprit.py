import pygame as pg
import itertools

from . import tools

DIRECT_DICT = {tools.CONTROLLER_DICT['left']: (-1, 0),
                       tools.CONTROLLER_DICT['right']: (1, 0),
                       tools.CONTROLLER_DICT['up']: (0, -1),
                       tools.CONTROLLER_DICT['down']: (0, 1)}
OPPOSITE_DICT = {tools.CONTROLLER_DICT['left']: "right",
                              tools.CONTROLLER_DICT['right']: "left",
                              tools.CONTROLLER_DICT['up']: "bottom",
                              tools.CONTROLLER_DICT['down']: "top"}
KEY_CHANGE = False

class Culprit:
    def __init__(self, x, y, width, height, facing=tools.CONTROLLER_DICT['up']):
        self.width = width
        self.height = height
        self.surface = pg.Surface([width, height])
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.animate_timer = 0.0
        self.animate_fps = 7
        self.mask = self.make_mask()
        self.collision_direction = None
        self.first_collision_per_frame = None
        self.direction = facing
        self.old_direction = None
        self.direction_stack = []
        self.redraw = True
        self.image = None
        self.walkframes = None
        self.sprite = tools.Image.load("skelly.png").convert()
        self.sprite.set_colorkey(pg.Color("magenta"))
        self.walkframe_dict = self.make_frame_dict()
        self.adjust_images()
        #self.rect = self.image.get_rect(center=(x,y))

    def get_event(self, event):
        """
        Handle events pertaining to player control.
        """
        if event.type == pg.KEYDOWN:
            self.add_direction(event.key)
        elif event.type == pg.KEYUP:
            self.pop_direction(event.key)

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, now, screen_rect, obstacles):
        """
        Updates our player appropriately every frame.
        """
        self.adjust_images(now)
        self.collision_direction = None
        if self.direction_stack:
            self.movement(obstacles, 0)
            self.movement(obstacles, 1)

    def movement(self, obstacles, i):
        """Move player and then check for collisions; adjust as necessary."""
        change = self.speed*DIRECT_DICT[self.direction][i]
        self.rect[i] += change
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        callback = pg.sprite.collide_mask
        collide = pg.sprite.spritecollideany(self, collisions, callback)
        if collide and not self.collision_direction:
            self.collision_direction = self.get_collision_direction(collide)
        while collide:
            self.rect[i] += (1 if change<0 else -1)
            collide = pg.sprite.spritecollideany(self, collisions, callback)

    def add_direction(self, key):
        """
        Add a pressed direction key on the direction stack.
        """
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """
        Pop a released key from the direction stack.
        """
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]

    def make_image(self, now):
        """
        Update the sprite's animation as needed.
        """
        elapsed = now-self.animate_timer > 1000.0/self.animate_fps
        if self.redraw or (self.direction_stack and elapsed):
            self.image = next(self.walkframes)
            self.animate_timer = now
        self.redraw = False

    def adjust_images(self, now=0):
        """
        Update the sprite's walkframes as the sprite's direction changes.
        """
        if self.direction != self.old_direction:
            global KEY_CHANGE
            if KEY_CHANGE:
                self.walkframe_dict = self.make_frame_dict()
                KEY_CHANGE = False
            self.walkframes = self.walkframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image(now)

    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frame cycles. We can use
        transform functions to reduce the size of the sprite sheet needed.
        """
        frames = tools.split_sheet(self.sprite, (self.width, self.height), 4, 1)[0]
        flips = [pg.transform.flip(frame, True, False) for frame in frames]
        walk_cycles = {tools.CONTROLLER_DICT['left']: itertools.cycle(frames[0:2]),
                       tools.CONTROLLER_DICT['right']: itertools.cycle(flips[0:2]),
                       tools.CONTROLLER_DICT['down']: itertools.cycle([frames[3], flips[3]]),
                       tools.CONTROLLER_DICT['up']: itertools.cycle([frames[2], flips[2]])}
        return walk_cycles

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill((0,0,0,0))
        mask_surface.fill(pg.Color("white"), (10,20,30,30))
        mask = pg.mask.from_surface(mask_surface)
        return mask

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


def set_bindings():
    global OPPOSITE_DICT
    global DIRECT_DICT
    global KEY_CHANGE
    OPPOSITE_DICT = {   tools.CONTROLLER_DICT['left']: "right",
                        tools.CONTROLLER_DICT['right']: "left",
                        tools.CONTROLLER_DICT['up']: "bottom",
                        tools.CONTROLLER_DICT['down']: "top"}
    DIRECT_DICT = { tools.CONTROLLER_DICT['left']: (-1, 0),
                    tools.CONTROLLER_DICT['right']: (1, 0),
                    tools.CONTROLLER_DICT['up']: (0, -1),
                    tools.CONTROLLER_DICT['down']: (0, 1)}
    KEY_CHANGE = True

