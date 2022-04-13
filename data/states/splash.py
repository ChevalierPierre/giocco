"""
The splash screen of the game. The first thing the user sees.
"""

import pygame as pg

from .. import prepare, tools


class Splash(tools._State):
    """This State is updated while our game shows the splash screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.next = "MENU"
        self.timeout = 5
        self.cover = pg.Surface((prepare.SCREEN_SIZE)).convert()
        self.cover.fill(0)
        self.cover_alpha = 256
        self.alpha_step  = 2
        self.image = prepare.GFX['background']
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)
        self.font = pg.font.Font(prepare.FONTS["Fixedsys500c"], 120)
        text = ["Attention", "",
                "aux", "", 
                "gnards."]
        self.rendered_text = self.make_text_list(self.font, text,
                                                 pg.Color("White"), 100, 60)

    def make_text_list(self, font, strings, color, start_y, y_space):
        """
        Takes a list of strings and returns a list of
        (rendered_surface, rect) tuples. The rects are centered on the screen
        and their y coordinates begin at starty, with y_space pixels between
        each line.
        """
        rendered_text = []
        for i,string in enumerate(strings):
            msg_center = (prepare.SCREEN_RECT.centerx, start_y+i*y_space)
            msg_data = self.render_font(font, string, color, msg_center)
            rendered_text.append(msg_data)
        return rendered_text
    
    def update(self, surface, keys, current_time, time_delta):
        """Updates the splash screen."""
        pg.mouse.set_visible(False)
        self.current_time = current_time
        surface.blit(self.image,self.rect)
        for msg in self.rendered_text:
            surface.blit(*msg)
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        surface.blit(self.cover,(0,0))
        if self.current_time-self.start_time > 1000.0*self.timeout:
            self.done = True

    def get_event(self, event):
        """Get events from Control. Currently changes to next state on any key
        press."""
        if event.type == pg.KEYDOWN:
            self.done = True
