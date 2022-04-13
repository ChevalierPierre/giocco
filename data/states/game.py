"""
The class for our Game scene is found here.
"""

import pygame as pg

from .. import prepare, tools


class Game(tools._State):
    """This state could represent the actual gameplay phase."""
    def __init__(self):
        tools._State.__init__(self)
        self.next = None
        self.image = prepare.GFX['background']
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)
        self.bgm = prepare.MUSIC["Quintessence"]
        self.font = pg.font.Font(prepare.FONTS["Fixedsys500c"], 50)
        text = ["Les gros gnards ont", "pris possession de la", "forêt des bois lardés.",
                "Sortez vivant du sous-bois", "avant que vos amis",
                "ne reçoivent un e-gnard", "de votre disparition.", ""]
        self.rendered_text = self.make_text_list(self.font, text,
                                                 pg.Color("white"), 50, 50)
        self.escape = self.render_font(self.font, "Appuie sur Entrer",
                                       pg.Color("yellow"),
                                       (prepare.SCREEN_RECT.centerx, 550))
        self.blink = False
        self.timer = 0.0

    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""
        pg.mixer.music.load(self.bgm)
        pg.mixer.music.play(-1)
        return tools._State.startup(self, current_time, persistant)

    def cleanup(self):
        """Stop the music when scene is done."""
        pg.mixer.music.stop()
        return tools._State.cleanup(self)

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

    def end_game(self):
        self.quit = True

    def get_event(self, event):
        """Go back on escape key."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.quit = True

    def draw(self, surface):
        """Blit all elements to surface."""
        surface.blit(self.image,self.rect)
        for msg in self.rendered_text:
            surface.blit(*msg)
        if self.blink:
            surface.blit(*self.escape)

    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        self.current_time = current_time
        if self.current_time-self.timer > 1000.0/5.0:
            self.blink = not self.blink
            self.timer = self.current_time
        self.draw(surface)
