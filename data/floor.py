from . import maze
from . import map

class Floor:
    def __init__(self):
        self.maps_array = maze.genMaze(12, 16)
        self.parse_floor()
        self.floor_number = None
        self.entry_map = None
        self.exit_map = None
        self.boss_map = None

    def parse_floor(self):
        for i in range(len(self.maps_array)):  # 12 rows
            for j in range(len(self.maps_array[0]) - 1):  # 16 columns
                if self.maps_array[i][j] == "c":
                    self.maps_array[i][j] = map.Map()
                else: # TMP
                     self.maps_array[i][j] = map.Map() # TMP