"""
The menu screen of the game. The hub of the game.
"""

import pygame as pg

from .. import prepare, tools

import random

class Menu(tools._State):
    """This State is updated while our game shows the splash screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.screen_rect = pg.Surface((prepare.SCREEN_SIZE)).convert()
        self.image = prepare.GFX['menu']
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)
        self.options = ['Play', 'Options', 'Quit']
        self.next_list = ["GAME", "OPTIONS"]
        self.title, self.title_rect = self.make_text('Gnons de Gnards', (75,75,75), (prepare.SCREEN_RECT.centerx, 75), 150)
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = 75
            
    def draw(self, surface):
        """Blit all elements to surface."""
        surface.blit(self.image, self.rect)
        surface.blit(self.title, self.title_rect)
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (self.screen_rect.centerx, self.from_bottom+i*self.spacer)
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                surface.blit(rend_img,rend_rect)
            else:
                surface.blit(opt[0],opt[1])

    
    def update(self, surface, keys, current_time, time_delta):
        """Updates the menu screen."""
        self.mouse_hover_sound()
        self.change_selected_option()
        self.draw(surface)

    def get_event(self, event):
        """Get events from Control. Currently changes to next state on any key
        press."""
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        self.mouse_menu_click(event)
