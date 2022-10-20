import pygame as pg
from .. import tools
from ..entities import solver
import random


class Menu(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.name = "MENU"
        self.screen_rect = screen_rect
        self.options = ['Play', 'Options', 'Quit']
        self.next_list = ['PLAY', 'OPTIONS']
        self.title, self.title_rect = self.make_text('Giocco', (75,75,75), (self.screen_rect.centerx, 75), 150)
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = 75

        self.maze_instance = solver.Solver()

    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_z]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
                
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        self.mouse_menu_click(event)

    def update(self, now, keys):
        #pg.mouse.set_visible(True)
        self.mouse_hover_sound()
        self.change_selected_option()
        self.maze_instance.update(now)

    def render(self, screen):
        screen.fill(self.bg_color)
        self.maze_instance.render(screen)
        screen.blit(self.title,self.title_rect)

        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (self.screen_rect.centerx, self.from_bottom+i*self.spacer)
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                screen.blit(opt[0],opt[1])
        
    def cleanup(self):
        pass
        
    def entry(self):
        pass

    def render_maze(self, screen):
        size = (800 / self.sizes[0], 600 / self.sizes[1])
        maze = self.maze_list[self.maze_counter]
        for i in range(0, len(maze)):
            for j in range(0, len(maze[0])):
                if maze[i][j] == 'w':
                    image = pg.Surface(size)
                    image.fill(self.maze_w)
                    screen.blit(image, (j*size[1],i*size[0]))
                if maze[i][j] == 'c':
                    image = pg.Surface(size)
                    image.fill(self.maze_c)
                    screen.blit(image, (j*size[1],i*size[0]))
                if maze[i][j] == 'p':
                    image = pg.Surface(size)
                    image.fill(self.maze_p)
                    screen.blit(image, (j*size[1],i*size[0]))


def generate_size():
    while True:
        y = random.randint(20, 60)
        if (y * 8 / 6).is_integer():
            return int(y * 8 / 6), y

