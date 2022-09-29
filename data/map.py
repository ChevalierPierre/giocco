import pygame as pg
from . import tools
from . import block
from . import door
from . import exits
from . import tiles
from . import firetrap


class Map:
    def __init__(self, doors, tile_color, block_color, exit=False):
        self.tile_color = tile_color
        self.block_color = block_color
        self.top_door, self.left_door, self.bottom_door, self.right_door = doors
        maps = tools.Maps()
        if exit:
            self.map = maps.get_list(True)
        else:
            self.map = maps.get_list()
        self.parse_map()

    def parse_map(self):
        obstacles = []
        doors = []
        floor_exit = []
        tile = []
        fire_traps = []
        for i in range(-1, len(self.map) - 1):
            for j in range(-1, len(self.map[0]) - 2):
                if self.map[i + 1][j + 1] == "O":
                    obstacles.append(block.Block((j*50,i*50), self.block_color))
                elif self.map[i + 1][j + 1] == "D":
                    if i == 0 and self.top_door:
                        doors.append(door.Door((j*50,i*50), "top", self.tile_color))
                    elif i == len(self.map) - 3 and self.bottom_door:
                        doors.append(door.Door((j * 50, i * 50), "bottom", self.tile_color))
                    elif j == 0 and self.left_door:
                        doors.append(door.Door((j * 50, i * 50), "left", self.tile_color))
                    elif j == len(self.map[0]) - 4 and self.right_door:
                        doors.append(door.Door((j * 50, i * 50), "right", self.tile_color))
                    else:
                        obstacles.append(block.Block((j * 50, i * 50), self.block_color))
                elif self.map[i + 1][j + 1] == "E":
                    floor_exit.append(exits.Exits((j * 50, i * 50), self.tile_color))
                elif self.map[i + 1][j + 1] == "F":
                    tile.append(tiles.Tiles((j * 50, i * 50), self.tile_color))
                elif self.map[i + 1][j + 1] == "T":
                    fire_traps.append(firetrap.Firetrap((j * 50, i * 50), self.tile_color))
        return (pg.sprite.Group(obstacles),pg.sprite.Group(doors), pg.sprite.Group(floor_exit), pg.sprite.Group(tile), pg.sprite.Group(fire_traps))
