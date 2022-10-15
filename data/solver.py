from colorama import Fore
from . import maze as m


class Solver:
    def __init__(self, height, width):
        self.maze = m.genMaze(height, width, True)
        self.maze_list = [value_copy(self.maze)]
        start, self.finish = self.get_starting_finishing_points()
        self.maze[start[0]][start[1]] = 'p'
        self.maze_list.append(value_copy(self.maze))
        self.rat_path = [start]
        self.end = False
        self.escape()

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

        if self.maze[current_cell[0] + 1][current_cell[1]] == 'c':
            self.maze[current_cell[0] + 1][current_cell[1]] = 'p'
            self.rat_path.append([current_cell[0] + 1, current_cell[1]])
            if not self.end:
                self.maze_list.append(value_copy(self.maze))
            self.escape()

        if self.maze[current_cell[0]][current_cell[1] + 1] == 'c':
            self.maze[current_cell[0]][current_cell[1] + 1] = 'p'
            self.rat_path.append([current_cell[0], current_cell[1] + 1])
            if not self.end:
                self.maze_list.append(value_copy(self.maze))
            self.escape()

        if self.maze[current_cell[0] - 1][current_cell[1]] == 'c':
            self.maze[current_cell[0] - 1][current_cell[1]] = 'p'
            self.rat_path.append([current_cell[0] - 1, current_cell[1]])
            if not self.end:
                self.maze_list.append(value_copy(self.maze))
            self.escape()

        if self.maze[current_cell[0]][current_cell[1] - 1] == 'c':
            self.maze[current_cell[0]][current_cell[1] - 1] = 'p'
            self.rat_path.append([current_cell[0], current_cell[1] - 1])
            if not self.end:
                self.maze_list.append(value_copy(self.maze))
            self.escape()

        # If we get here, this means that we made a wrong decision, so we need to
        # backtrack
        current_cell = self.rat_path[len(self.rat_path) - 1]
        if current_cell != self.finish:
            cell_to_remove = self.rat_path[len(self.rat_path) - 1]
            self.rat_path.remove(cell_to_remove)
            self.maze[cell_to_remove[0]][cell_to_remove[1]] = 'c'
            if not self.end:
                self.maze_list.append(value_copy(self.maze))

    def map_historic(self):
        return self.maze_list


def value_copy(a):
    b = [[a[x][y] for y in range(len(a[0]))] for x in range(len(a))]
    return b


def maze_solver(selfmaze):
    for i in range(0, len(selfmaze)):
        for j in range(0, len(selfmaze[0])):
            if selfmaze[i][j] == 'u':
                print(Fore.WHITE, f'{selfmaze[i][j]}', end=" ")
            elif selfmaze[i][j] == 'c':
                print(Fore.GREEN, f'{selfmaze[i][j]}', end=" ")
            elif selfmaze[i][j] == 'p':
                print(Fore.BLUE, f'{selfmaze[i][j]}', end=" ")
            else:
                print(Fore.RED, f'{selfmaze[i][j]}', end=" ")
        print('\n')


"""insta = Solver(15,15)
ins = insta.map_historic()
for i in ins:
    maze_solver(i)
    print("\n")"""
