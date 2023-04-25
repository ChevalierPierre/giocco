import pygame as pg
from data import maze as m
from .. import tools
import random

class Solver:
    def __init__(self):
        self.sizes = generate_size()
        self.maze = m.genMaze(self.sizes[1], self.sizes[0], True)
        self.maze_list = [tools.value_copy(self.maze)]
        start, self.finish = self.get_starting_finishing_points()
        self.maze[start[0]][start[1]] = 'p'
        self.maze_list.append(tools.value_copy(self.maze))
        self.rat_path = [start]
        self.end = False
        self.escape()

        # MAZE ANIMATION
        self.maze_counter = 0
        self.next_maze = 1000
        self.next_maze_step = 1000
        self.maze_c = random.randint(35,45),random.randint(35,45),random.randint(35,45)
        self.maze_w = random.randint(20,30),random.randint(20,30),random.randint(20,30)
        self.maze_p = random.randint(145,155),random.randint(145,155),random.randint(70,110)

    def get_starting_finishing_points(self):
        _start = [i for i in range(len(self.maze[0])) if self.maze[0][i] == 'c']
        _end = [i for i in range(len(self.maze[0])) if self.maze[len(self.maze)-1][i] == 'c']
        return [0, _start[0]], [len(self.maze) - 1, _end[0]]

    def escape(self):
        if self.end:
            return

        current_cell = self.rat_path[len(self.rat_path) - 1]

        if current_cell == self.finish:
            self.end = True
            return
        alea = [[1,0],[0,1],[-1,0],[0,-1]]
        random.shuffle(alea)
        for i in range(4):
            if self.maze[current_cell[0] + alea[i][0]][current_cell[1]+alea[i][1]] == 'c':
                self.maze[current_cell[0] + alea[i][0]][current_cell[1]+alea[i][1]] = 'p'
                self.rat_path.append([current_cell[0] + alea[i][0], current_cell[1]+alea[i][1]])
                if not self.end:
                    self.maze_list.append(tools.value_copy(self.maze))
                self.escape()



        # If we get here, this means that we made a wrong decision, so we need to
        # backtrack
        current_cell = self.rat_path[len(self.rat_path) - 1]
        if current_cell != self.finish:
            cell_to_remove = self.rat_path[len(self.rat_path) - 1]
            self.rat_path.remove(cell_to_remove)
            self.maze[cell_to_remove[0]][cell_to_remove[1]] = 'c'
            if not self.end:
                self.maze_list.append(tools.value_copy(self.maze))

    def update(self, now):

        if now - 5 > self.next_maze:
            self.next_maze = now
            self.maze_counter += 1
            if len(self.maze_list) == self.maze_counter:
                self.maze_counter = 0
                self.sizes = generate_size()
                self.maze = m.genMaze(self.sizes[1], self.sizes[0], True)
                self.maze_list = [tools.value_copy(self.maze)]
                start, self.finish = self.get_starting_finishing_points()
                self.maze[start[0]][start[1]] = 'p'
                self.maze_list.append(tools.value_copy(self.maze))
                self.rat_path = [start]
                self.end = False
                self.escape()
                self.maze_c = random.randint(35, 45), random.randint(35, 45), random.randint(35, 45)
                self.maze_w = random.randint(20, 30), random.randint(20, 30), random.randint(20, 30)
                self.maze_p = random.randint(145, 155), random.randint(145, 155), random.randint(70, 110)

    def render(self, screen):
        size = (800 / self.sizes[0], 600 / self.sizes[1])
        maze = self.maze_list[self.maze_counter]
        for i in range(0, len(maze)):
            for j in range(0, len(maze[0])):
                if maze[i][j] == 'w':
                    image = pg.Surface(size)
                    image.fill(self.maze_w)
                    screen.blit(image, (j * size[1], i * size[0]))
                if maze[i][j] == 'c':
                    image = pg.Surface(size)
                    image.fill(self.maze_c)
                    screen.blit(image, (j * size[1], i * size[0]))
                if maze[i][j] == 'p':
                    image = pg.Surface(size)
                    image.fill(self.maze_p)
                    screen.blit(image, (j * size[1], i * size[0]))


def generate_size():
    while True:
        y = random.randint(20, 60)
        if (y * 8 / 6).is_integer():
            return int(y * 8 / 6), y
