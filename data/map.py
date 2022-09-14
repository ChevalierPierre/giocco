import pygame as pg
from . import tools
from . import block

class Map:
    def __init__(self) -> None:
        maps = tools.Maps()
        self.map = maps.get_list()
        self.parse_map()
        # self.obstacles = 
        # porte
        # vide
        # enemy
        # power ups
        #self.floor_instance = floor_instance

    def parse_map(self):
        obstacles = []
        #enemies = []
        #items = []
        for i in range(len(self.map)):  # 12 rows
            for j in range(len(self.map[0]) - 1):  # 16 columns
                if self.map[i][j] == "O":
                    obstacles.append(block.Block((j*50,i*50)))
        return pg.sprite.Group(obstacles)