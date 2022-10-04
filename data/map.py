import pygame as pg
from . import tools
from .entities import block, door, exits, tiles
from data.entities.traps import beartrap, firetrap, pittrap, pushtrap, spiketrap


class Map:
    def __init__(self, doors, tile_color, block_color, exit=0):
        self.tile_color = tile_color
        self.block_color = block_color
        self.top_door, self.left_door, self.bottom_door, self.right_door = doors
        maps = tools.Maps()
        self.map = maps.get_list(exit)
        self.parse_map()

    def parse_map(self):
        obstacles = []
        doors = []
        floor_exit = []
        tile = []
        fire_traps = []
        pit_traps = []
        spike_traps = []
        bear_traps = []
        push_traps_down = []
        push_traps_up = []
        push_traps_right = []
        push_traps_left = []
        for i in range(-1, len(self.map) - 1):
            for j in range(-1, len(self.map[0]) - 2):
                if self.map[i + 1][j + 1] == "O":
                    obstacles.append(block.Block((j * 50, i * 50), self.block_color))
                elif self.map[i + 1][j + 1] == "D":
                    if i == 0 and self.top_door:
                        doors.append(door.Door((j * 50, i * 50), "top", self.tile_color))
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
                elif self.map[i + 1][j + 1] == "S":
                    spike_traps.append(spiketrap.Spiketrap((j * 50, i * 50), self.tile_color))
                elif self.map[i + 1][j + 1] == "B":
                    bear_traps.append(beartrap.Beartrap((j * 50, i * 50), self.tile_color))
                elif self.map[i + 1][j + 1] == "P":
                    pit_traps.append(pittrap.Pittrap((j * 50, i * 50)))
                elif self.map[i + 1][j + 1] == "R":
                    push_traps_right.append(pushtrap.Pushtrap((j * 50, i * 50), "right", self.tile_color))
                elif self.map[i + 1][j + 1] == "L":
                    push_traps_left.append(pushtrap.Pushtrap((j * 50, i * 50), "left", self.tile_color))
                elif self.map[i + 1][j + 1] == "A":
                    push_traps_up.append(pushtrap.Pushtrap((j * 50, i * 50), "front", self.tile_color))
                elif self.map[i + 1][j + 1] == "Z":
                    push_traps_down.append(pushtrap.Pushtrap((j * 50, i * 50), "bottom", self.tile_color))
        return (pg.sprite.Group(obstacles),pg.sprite.Group(doors), pg.sprite.Group(floor_exit), pg.sprite.Group(tile), pg.sprite.Group(fire_traps), pg.sprite.Group(pit_traps), pg.sprite.Group(spike_traps), pg.sprite.Group(bear_traps), pg.sprite.Group(push_traps_up), pg.sprite.Group(push_traps_down), pg.sprite.Group(push_traps_right), pg.sprite.Group(push_traps_left))
