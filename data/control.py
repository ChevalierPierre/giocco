
import os
import pygame as pg
from .states import menu, play, options, settings, controls, audio, splash, keybinding, getkey

class Control():
    def __init__(self, fullscreen, size):
        self.historic = []
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.init()
        pg.display.set_caption("Giocco")
        self.screensize = (int(size[0]), int(size[1]))
        if fullscreen:
            self.screen = pg.display.set_mode(self.screensize, pg.FULLSCREEN)
        else:
            os.environ["SDL_VIDEO_CENTERED"] = "True"
            self.screen = pg.display.set_mode(self.screensize)
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.keys = pg.key.get_pressed()
        self.done = False
        self.state_dict = {
            "MENU"     : menu.Menu(self.screen_rect),
            "PLAY"     : play.Play(self.screen_rect),
            "CONTROLS" : controls.Controls(self.screen_rect),
            "OPTIONS"  : options.Options(self.screen_rect),
            "SETTINGS" : settings.Settings(self.screen_rect),
            "AUDIO"    : audio.Audio(self.screen_rect),
            "SPLASH"   : splash.Splash(self.screen_rect),
            "KEYBINDING" : keybinding.KeyBinding(self.screen_rect),
            "GETKEY"   : getkey.GetKey(self.screen_rect)
        }
        self.state_name = "SPLASH"
        self.state = self.state_dict[self.state_name]

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            elif event.type in (pg.KEYDOWN,pg.KEYUP):
                self.keys = pg.key.get_pressed()
            self.state.get_event(event, self.keys)

    def change_state(self):
        if self.state.done:
            self.historic += [self.state.name]
            self.state.cleanup()
            self.state_name = self.state.next
            self.state.done = False
            self.state = self.state_dict[self.state_name]
            self.state.name = self.state_name
            self.state.previous_state = self.historic
            self.state.entry()

    def run(self):
        while not self.done:
            if self.state.quit:
                self.done = True
            now = pg.time.get_ticks()
            self.event_loop()
            self.change_state()
            self.state.update(now, self.keys)
            self.state.render(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)


