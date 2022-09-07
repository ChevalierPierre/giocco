import pygame as pg
from . import tools
from . import block


class Parser:
    def __init__(self):
        maps = tools.Maps()
        self.map = maps.get_list()

    def parse(self):
        obstacles = []
        #enemies = []
        #items = []
        for i in range(len(self.map)):  # 12 rows
            for j in range(len(self.map[0]) - 1):  # 16 columns
                if self.map[i][j] == "O":
                    obstacles.append(block.Block((j*50,i*50)))
        return pg.sprite.Group(obstacles)
