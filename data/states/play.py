import pygame as pg
from .. import tools
from .. import culprit as culprit_
from .. import block as block_
from .. import floor
from .. import map

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
        self.bg_color = (50,50,50)
        self.pause = False
        self.score = 0
        #game specific content
        culprit_width = 50
        culprit_height = 50
        culprit_y = self.screen_rect.height // 2 - culprit_height // 2
        culprit_x = self.screen_rect.width // 2 - culprit_width // 2
        self.culprit = culprit_.Culprit(culprit_x, culprit_y, culprit_width, culprit_height)
        self.floor_instance = floor.Floor()
        self.obstacles, self.doors, self.floor_exit = self.floor_instance.entry_map.parse_map()
        self.last_action = 0

    def reset(self):
        self.pause = False
        self.score = 0
        culprit_width = 50
        culprit_height = 50
        culprit_y = self.screen_rect.height // 2 - culprit_height // 2
        culprit_x = self.screen_rect.width // 2 - culprit_width // 2
        self.culprit = culprit_.Culprit(culprit_x, culprit_y, culprit_width, culprit_height)
        self.floor_instance = floor.Floor()
        self.obstacles, self.doors, self.floor_exit = self.floor_instance.entry_map.parse_map()
        self.last_action = 0
    
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == tools.CONTROLLER_DICT['back']:
                # self.button_sound.sound.play()
                self.done = True
                self.next = 'MENU'
                self.reset()
            elif event.key == tools.CONTROLLER_DICT['pause']:
                self.pause = not self.pause
                if self.pause:
                    pg.mixer.music.pause()
                if not self.pause:
                    pg.mixer.music.unpause()
        elif event.type == self.background_music.track_end:
            self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
            pg.mixer.music.load(self.background_music.tracks[self.background_music.track])
            pg.mixer.music.play()
        self.culprit.get_event(event)

    def interact(self, keys, now):
        if keys[tools.CONTROLLER_DICT['action']]:
            if now - 500 > self.last_action:
                loop_doors = self.doors
                for do in loop_doors:
                    if pg.sprite.collide_mask(self.culprit, do):
                        leads_to = do.leads_to
                        instance = self.floor_instance.change_map(leads_to)
                        self.obstacles, self.doors, self.floor_exit = instance.parse_map()
                        if leads_to == "top":
                            for doo in self.doors:
                                if doo.location[1] == self.screen_rect.height - 50:
                                    self.culprit.rect.x = doo.location[0]
                                    self.culprit.rect.y = doo.location[1]
                                    break
                            self.culprit.direction = tools.CONTROLLER_DICT['up']
                        elif leads_to == "bottom":
                            for doo in self.doors:
                                if doo.location[1] == 0:
                                    self.culprit.rect.x = doo.location[0]
                                    self.culprit.rect.y = doo.location[1]
                                    break
                            self.culprit.direction = tools.CONTROLLER_DICT['down']
                        elif leads_to == "right":
                            for doo in self.doors:
                                if doo.location[0] == 0:
                                    self.culprit.rect.x = doo.location[0]
                                    self.culprit.rect.y = doo.location[1]
                                    break
                            self.culprit.direction = tools.CONTROLLER_DICT['right']
                        elif leads_to == "left":
                            for doo in self.doors:
                                if doo.location[0] == self.screen_rect.width - 50:
                                    self.culprit.rect.x = doo.location[0]
                                    self.culprit.rect.y = doo.location[1]
                                    break
                            self.culprit.direction = tools.CONTROLLER_DICT['left']
                        self.adjust_score(1)
                        break
                for ex in self.floor_exit:
                    if pg.sprite.collide_mask(self.culprit, ex):
                        self.reset()
                self.last_action = now

    def update(self, now, keys):
        if not self.pause:
            self.score_text, self.score_rect = self.make_text('{}'.format(self.score),
                                                              (255, 255, 255), (25, 25), 50)
            self.culprit.update(now, self.screen_rect, self.obstacles)
            for do in self.doors:
                do.update(now)
            for ex in self.floor_exit:
                ex.update(now)
            self.interact(keys, now)
        else:
            self.pause_text, self.pause_rect = self.make_text("PAUSED",
                (255,255,255), self.screen_rect.center, 50)
        pg.mouse.set_visible(False)

    def render(self, screen):
        screen.fill(self.bg_color)
        for ob in self.obstacles:
            ob.render(screen)
        for do in self.doors:
            do.render(screen)
        for ex in self.floor_exit:
            ex.render(screen)
        screen.blit(self.score_text, self.score_rect)
        self.culprit.render(screen)
        if self.pause:
            screen.blit(self.cover,(0,0))
            screen.blit(self.pause_text, self.pause_rect)
        
    def adjust_score(self, point):
        self.score += point
            
    def cleanup(self):
        pg.mixer.music.stop()
        self.background_music.setup(self.background_music_volume)
        
    def entry(self):
        pg.mixer.music.play()
