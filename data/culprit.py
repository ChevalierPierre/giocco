import pygame as pg
from . import tools

class Culprit:
    def __init__(self):
        self.sound_init()

    def collide_walls(self):
        if self.rect.x < 0 or self.rect.x > self.screen_rect.right or self.rect.y < 0 or self.rect.y > self.screen_rect.bottom - self.height or self.rect.x < 0 or self.rect.x > self.screen_rect.right - self.height:
            if not self.menu:
                self.walls.sound.play()
                return 1
        return 0

    def sound_init(self):
        self.collide = tools.Sound('boing.wav')
        self.collide.sound.set_volume(.5)
        self.hit = tools.Sound('whoosh.wav')
        self.hit.sound.set_volume(.1)
        self.action = tools.Sound('action.wav')
        self.action.sound.set_volume(.5)
        self.walls = tools.Sound('action.wav')
        self.walls.sound.set_volume(.5)

    def move(self, x, y):
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed

    def update(self, now, keys):
        if keys[pg.K_UP]:
            collide_case = (self.rect.x, self.rect.y)
            self.move(0,-1)
            if self.collide_walls() == 1:
                self.rect.x, self.rect.y = collide_case
        if keys[pg.K_DOWN]:
            collide_case = (self.rect.x, self.rect.y)
            self.move(0,1)
            if self.collide_walls() == 1:
                self.rect.x, self.rect.y = collide_case
        if keys[pg.K_LEFT]:
            collide_case = (self.rect.x, self.rect.y)
            self.move(-1,0)
            if self.collide_walls() == 1:
                self.rect.x, self.rect.y = collide_case
        if keys[pg.K_RIGHT]:
            collide_case = (self.rect.x, self.rect.y)
            self.move(1,0)
            if self.collide_walls() == 1:
                self.rect.x, self.rect.y = collide_case
