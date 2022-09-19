from . import maze
from . import map
import random
from datetime import datetime

class Floor:
    def __init__(self):
        self.maps_array = maze.genMaze(12, 16)
        self.parse_floor()
        self.floor_number = None
        self.current_map = [None, None]
        self.entry_map = self.get_existing_map()
        self.exit_map = None
        self.boss_map = None

    def parse_floor(self):
        for i in range(len(self.maps_array)):
            for j in range(len(self.maps_array[0]) - 1):
                if self.maps_array[i][j] != "w":
                    doors = self.check_doors(i,j)
                    self.maps_array[i][j] = map.Map(doors)

    def get_existing_map(self):
        random.seed(datetime.now())
        while True:
            x = random.randint(0, len(self.maps_array[0]) - 1)
            y = random.randint(0, len(self.maps_array) - 1)
            if self.maps_array[y][x] != "w":
                self.current_map = [y,x]
                return self.maps_array[y][x]

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
            elif j == len(self.maps_array[0] - 1):
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
            elif j == len(self.maps_array[0] - 1):
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
