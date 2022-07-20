import pygame as pg
from . import tools

class Culprit:
    def __init__(self, x, y, width, height, color=(255,255,255)):
        self.surface = pg.Surface([width, height])
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.surface.fill(self.color)
        self.speed = 1

    def sound_init(self):
        self.collide = tools.Sound('boing.wav')
        self.collide.sound.set_volume(.5)
        self.hit = tools.Sound('whoosh.wav')
        self.hit.sound.set_volume(.1)

    def move(self, x, y):
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed

    def update(self, screen_rect):
        self.rect.clamp_ip(screen_rect)

    def render(self, screen):
        screen.blit(self.surface, self.rect)