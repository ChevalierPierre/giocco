from . import maze
from . import map
import random
from datetime import datetime

class Floor:
    def __init__(self):
        self.maps_array = maze.genMaze(12, 16)
        self.parse_floor()
        self.floor_number = None
        self.entry_map = self.get_existing_map()
        self.exit_map = None
        self.boss_map = None

    def parse_floor(self):
        for i in range(len(self.maps_array)):  # 12 rows
            for j in range(len(self.maps_array[0]) - 1):  # 16 columns
                if self.maps_array[i][j] == "c":
                    self.maps_array[i][j] = map.Map()

    def get_existing_map(self):
        random.seed(datetime.now())
        while True:
            x = random.randint(0, 15)
            y = random.randint(0, 11)
            if self.maps_array[y][x] != "w":
                return self.maps_array[y][x]