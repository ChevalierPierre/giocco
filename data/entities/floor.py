from data import maze
from data.entities import map
import random
from datetime import datetime


class Floor:
    size = 3

    def __init__(self):
        Floor.size += 1
        random.seed(datetime.now())
        brick_list = ["black", "dark", "light", "red", "red_4"]
        tile_list = ["blue", "green", "grey", "light", "grey_4"]

        self.floor_brick = random.choice(brick_list)
        if self.floor_brick == "light":
            self.floor_tile = random.choice(tile_list[:-1])
        else:
            self.floor_tile = random.choice(tile_list)
        self.maps_array = maze.genMaze(Floor.size, Floor.size)
        self.current_map = [None, None]
        self.parse_floor()
        self.get_existing_map()

    def parse_floor(self):
        for i in range(len(self.maps_array)):
            for j in range(len(self.maps_array[0]) - 1):
                if self.maps_array[i][j] == "c":
                    doors = self.check_doors(i,j)
                    self.maps_array[i][j] = map.Map(doors, self.floor_tile, self.floor_brick, 0)

    def get_existing_map(self):
        condition = True
        while True:
            x = random.randint(0, len(self.maps_array[0]) - 1)
            y = random.randint(0, len(self.maps_array) - 1)
            if self.maps_array[y][x] != "w" and condition:
                self.current_map = [y,x]
                doors = self.check_doors(y, x)
                self.maps_array[y][x] = map.Map(doors, self.floor_tile, self.floor_brick, 2)
                self.entry_map = self.maps_array[y][x]
                condition = False
            elif self.maps_array[y][x] != "w" and [y,x] != self.current_map and self.maps_array[y][x] != self.entry_map:
                doors = self.check_doors(y, x)
                self.maps_array[y][x] = map.Map(doors, self.floor_tile, self.floor_brick, 1)
                return

    def change_map(self, leads_to):
        if leads_to == "top":
            self.current_map[0] = self.current_map[0] - 1
            return self.maps_array[self.current_map[0]][self.current_map[1]]
        elif leads_to == "bottom":
            self.current_map[0] = self.current_map[0] + 1
            return self.maps_array[self.current_map[0]][self.current_map[1]]
        elif leads_to == "left":
            self.current_map[1] = self.current_map[1] - 1
            return self.maps_array[self.current_map[0]][self.current_map[1]]
        elif leads_to == "right":
            self.current_map[1] = self.current_map[1] + 1
            return self.maps_array[self.current_map[0]][self.current_map[1]]

    def check_doors(self, i, j):
        doors = [False, False, False, False]
        if i == 0:
            if j == 0:
                if self.maps_array[i + 1][j] != "w":
                    doors[2] = True
                if self.maps_array[i][j + 1] != "w":
                    doors[3] = True
            elif j == len(self.maps_array[0]) - 1:
                if self.maps_array[i + 1][j] != "w":
                    doors[2] = True
                if self.maps_array[i][j - 1] != "w":
                    doors[1] = True
            else:
                if self.maps_array[i + 1][j] != "w":
                    doors[2] = True
                if self.maps_array[i][j - 1] != "w":
                    doors[1] = True
                if self.maps_array[i][j + 1] != "w":
                    doors[3] = True
        elif i == len(self.maps_array):
            if j == 0:
                if self.maps_array[i - 1][j] != "w":
                    doors[0] = True
                if self.maps_array[i][j + 1] != "w":
                    doors[3] = True
            elif j == len(self.maps_array[0]) - 1:
                if self.maps_array[i - 1][j] != "w":
                    doors[0] = True
                if self.maps_array[i][j - 1] != "w":
                    doors[1] = True
            else:
                if self.maps_array[i - 1][j] != "w":
                    doors[0] = True
                if self.maps_array[i][j - 1] != "w":
                    doors[1] = True
                if self.maps_array[i][j + 1] != "w":
                    doors[3] = True
        else:
            if j == 0:
                if self.maps_array[i - 1][j] != "w":
                    doors[0] = True
                if self.maps_array[i][j + 1] != "w":
                    doors[3] = True
                if self.maps_array[i + 1][j] != "w":
                    doors[2] = True
            elif j == len(self.maps_array[0]) - 1:
                if self.maps_array[i + 1][j] != "w":
                    doors[2] = True
                if self.maps_array[i - 1][j] != "w":
                    doors[0] = True
                if self.maps_array[i][j - 1] != "w":
                    doors[1] = True
            else:
                if self.maps_array[i + 1][j] != "w":
                    doors[2] = True
                if self.maps_array[i - 1][j] != "w":
                    doors[0] = True
                if self.maps_array[i][j - 1] != "w":
                    doors[1] = True
                if self.maps_array[i][j + 1] != "w":
                    doors[3] = True
        return doors
