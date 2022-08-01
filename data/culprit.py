import pygame as pg
import itertools

from . import tools

DIRECT_DICT = {tools.CONTROLLER_DICT['left']: (-1, 0),
               tools.CONTROLLER_DICT['right']: (1, 0),
               tools.CONTROLLER_DICT['up']: (0, -1),
               tools.CONTROLLER_DICT['down']: (0, 1)}

class Culprit:
    def __init__(self, x, y, width, height, facing=tools.CONTROLLER_DICT['up']):
        self.width = width
        self.height = height
        self.surface = pg.Surface([width, height])
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.animate_timer = 0.0
        self.animate_fps = 7
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
        self.rect = self.image.get_rect(center=(x,y))

    def sound_init(self):
        self.collide = tools.Sound('boing.wav')
        self.collide.sound.set_volume(.5)
        self.hit = tools.Sound('whoosh.wav')
        self.hit.sound.set_volume(.1)

    def interact(self):
        print("interact")

    def get_event(self, event):
        """
        Handle events pertaining to player control.
        """
        if event.type == pg.KEYDOWN:
            self.add_direction(event.key)
        elif event.type == pg.KEYUP:
            self.pop_direction(event.key)

    def update(self, now, screen_rect):
        """
        Updates our player appropriately every frame.
        """
        self.adjust_images(now)
        if self.direction_stack:
            direction_vector = DIRECT_DICT[self.direction]
            self.rect.x += self.speed*direction_vector[0]
            self.rect.y += self.speed*direction_vector[1]
            self.rect.clamp_ip(screen_rect)

    def render(self, screen):
        screen.blit(self.image, self.rect)

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
            self.walkframes = self.walkframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image(now)


    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frame cycles. We can use
        transform functions to reduce the size of the sprite sheet needed.
        """
        frames = split_sheet(self.sprite, (self.width, self.height), 4, 1)[0]
        flips = [pg.transform.flip(frame, True, False) for frame in frames]
        walk_cycles = {tools.CONTROLLER_DICT['left']: itertools.cycle(frames[0:2]),
                       tools.CONTROLLER_DICT['right']: itertools.cycle(flips[0:2]),
                       tools.CONTROLLER_DICT['down']: itertools.cycle([frames[3], flips[3]]),
                       tools.CONTROLLER_DICT['up']: itertools.cycle([frames[2], flips[2]])}
        return walk_cycles


def split_sheet(sheet, size, columns, rows):
    """
    Divide a loaded sprite sheet into subsurfaces.

    The argument size is the width and height of each frame (w,h)
    columns and rows are the integer number of cells horizontally and
    vertically.
    """
    subsurfaces = []
    for y in range(rows):
        row = []
        for x in range(columns):
            rect = pg.Rect((x * size[0], y * size[1]), size)
            row.append(sheet.subsurface(rect))
        subsurfaces.append(row)
    return subsurfaces