import pygame as pg
from . import tools
from . import block
from . import door
from . import exits

class Map:
    def __init__(self, doors, exit=False):
        self.top_door, self.left_door, self.bottom_door, self.right_door = doors
        maps = tools.Maps()
        if exit:
            self.map = maps.get_list(True)
        else:
            self.map = maps.get_list()
        self.parse_map()
        # porte
        # vide
        # enemy
        # power ups

    def parse_map(self):
        obstacles = []
        doors = []
        floor_exit = []
        #enemies = []
        #items = []
        for i in range(-1, len(self.map) - 1):
            for j in range(-1, len(self.map[0]) - 2):
                if self.map[i + 1][j + 1] == "O":
                    obstacles.append(block.Block((j*50,i*50)))
                elif self.map[i + 1][j + 1] == "D":
                    if i == 0 and self.top_door:
                        doors.append(door.Door((j*50,i*50), "top"))
                    elif i == len(self.map) - 3 and self.bottom_door:
                        doors.append(door.Door((j * 50, i * 50), "bottom"))
                    elif j == 0 and self.left_door:
                        doors.append(door.Door((j * 50, i * 50), "left"))
                    elif j == len(self.map[0]) - 4 and self.right_door:
                        doors.append(door.Door((j * 50, i * 50), "right"))
                    else:
                        obstacles.append(block.Block((j * 50, i * 50)))
                elif self.map[i + 1][j + 1] == "E":
                    floor_exit.append(exits.Exits((j * 50, i * 50)))
        return (pg.sprite.Group(obstacles),pg.sprite.Group(doors), pg.sprite.Group(floor_exit))
