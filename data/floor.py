from . import maze
from . import map
import random
from datetime import datetime

class Floor:
    def __init__(self):
        self.maps_array = maze.genMaze(4, 4)
        self.current_map = [None, None]
        self.parse_floor()
        self.get_existing_map()

    def parse_floor(self):
        for i in range(len(self.maps_array)):
            for j in range(len(self.maps_array[0]) - 1):
                if self.maps_array[i][j] == "c":
                    doors = self.check_doors(i,j)
                    self.maps_array[i][j] = map.Map(doors)

    def get_existing_map(self):
        random.seed(datetime.now())
        condition = True
        while True:
            x = random.randint(0, len(self.maps_array[0]) - 1)
            y = random.randint(0, len(self.maps_array) - 1)
            if self.maps_array[y][x] != "w" and condition:
                self.current_map = [y,x]
                self.entry_map = self.maps_array[y][x]
                condition = False
            elif self.maps_array[y][x] != "w" and [y,x] != self.current_map and self.maps_array[y][x] != self.entry_map:
                doors = self.check_doors(y, x)
                self.maps_array[y][x] = map.Map(doors, True)
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
