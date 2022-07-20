import pygame as pg
from .. import tools
from .. import culprit as culprit_


class Play(tools.States):
    def __init__(self, screen_rect): 
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.score_text, self.score_rect = self.make_text("SCOREBOARD_PLACEHOLDER",
            (255,255,255), (screen_rect.centerx,100), 50)
        self.pause_text, self.pause_rect = self.make_text("PAUSED",
            (255,255,255), screen_rect.center, 50)
            
        self.cover = pg.Surface((screen_rect.width, screen_rect.height))
        self.cover.fill(0)
        self.cover.set_alpha(200)
        
        #game specific content
        self.bg_color = (0,0,0)
        self.pause = False
        self.score = [0,0]

        culprit_width = 10
        culprit_height = 10
        culprit_y = self.screen_rect.centery - (culprit_height // 2)
        padding = 25 #padding from wall
        culprit_right = screen_rect.width - culprit_width - padding

        self.culprit = culprit_.Culprit(culprit_right, culprit_y, culprit_width, culprit_height, (150, 150, 150))

    def reset(self):
        self.pause = False
        self.score = [0,0]
    
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == tools.CONTROLLER_DICT['back']:
                #self.button_sound.sound.play()
                self.done = True
                self.next = 'MENU'
                self.reset()
            elif event.key == tools.CONTROLLER_DICT['pause']:
                self.pause = not self.pause
            elif event.key == tools.CONTROLLER_DICT['action']:
                print("tony")
        elif event.type == self.background_music.track_end:
            self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
            pg.mixer.music.load(self.background_music.tracks[self.background_music.track]) 
            pg.mixer.music.play()
                    
    def movement(self, keys):           
        if keys[tools.CONTROLLER_DICT['up']]:
            self.culprit.move(0, -1)
        if keys[tools.CONTROLLER_DICT['down']]:
            self.culprit.move(0, 1)
        if keys[tools.CONTROLLER_DICT['left']]:
            self.culprit.move(-1, 0)
        if keys[tools.CONTROLLER_DICT['right']]:
            self.culprit.move(1, 0)

    def update(self, now, keys):
        if not self.pause:
            self.score_text, self.score_rect = self.make_text('{}:{}'.format(self.score[0], self.score[1]),
                                                              (255, 255, 255), (self.screen_rect.centerx, 25), 50)
            self.culprit.update((self.screen_rect))
            self.movement(keys)
        else:
            self.pause_text, self.pause_rect = self.make_text("PAUSED",
                (255,255,255), self.screen_rect.center, 50)
        pg.mouse.set_visible(False)

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.score_text, self.score_rect)
        self.culprit.render(screen)
        if self.pause:
            screen.blit(self.cover,(0,0))
            screen.blit(self.pause_text, self.pause_rect)
        
    def adjust_score(self, hit_side):
        if hit_side == -1:
            self.score[1] += 1
        elif hit_side == 1:
            self.score[0] += 1
            
    def cleanup(self):
        pg.mixer.music.stop()
        self.background_music.setup(self.background_music_volume)
        
    def entry(self):
        pg.mixer.music.play()