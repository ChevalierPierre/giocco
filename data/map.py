import pygame as pg
from . import tools
from . import block
from . import door

class Map:
    def __init__(self, doors):
        self.left_door, self.right_door, self.top_door, self.bottom_door = doors
        maps = tools.Maps()
        self.map = maps.get_list()
        self.parse_map()
        # porte
        # vide
        # enemy
        # power ups

    def parse_map(self):
        obstacles = []
        doors = []
        #enemies = []
        #items = []
        for i in range(-1, len(self.map) -1):  # 12 rows
            for j in range(-1, len(self.map[0]) - 2):  # 16 columns
                if self.map[i + 1][j + 1] == "O":
                    obstacles.append(block.Block((j*50,i*50)))
                if self.map[i + 1][j + 1] == "D":
                    doors.append(door.Door((j*50,i*50)))
        return (pg.sprite.Group(obstacles),pg.sprite.Group(doors))
