import pygame as pg
from .. import tools
from ..entities import culprit as culprit_, floor
from ..entities import hud, tiles, minimap


class Play(tools.States):
    def __init__(self, screen_rect): 
        tools.States.__init__(self)
        self.name = "PLAY"
        self.screen_rect = screen_rect
        self.game_over_text, self.game_over_rect = self.make_text("GAME OVER",
            (255,255,255), screen_rect.center, 50)

        self.cover = pg.Surface((screen_rect.width, screen_rect.height))
        self.death_cover = pg.Surface((screen_rect.width, screen_rect.height))
        self.death_cover.fill(0)
        self.alpha_step = 1
        self.death_alpha = 0
        self.death_cover.set_alpha(self.death_alpha)
        self.cover.fill(0)
        self.cover.set_alpha(200)
        self.score = 0
        culprit_width = 50
        culprit_height = 50
        culprit_y = self.screen_rect.height // 2 - culprit_height // 2
        culprit_x = self.screen_rect.width // 2 - culprit_width // 2
        self.culprit = culprit_.Culprit(culprit_x, culprit_y, culprit_width, culprit_height)
        self.hud = hud.Hud(self.culprit, self.score, self.screen_rect)

    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == tools.CONTROLLER_DICT['back'] and self.culprit.life > 0:
                # self.button_sound.sound.play()
                self.done = True
                self.next = 'SETTINGS'
            elif event.key == tools.CONTROLLER_DICT['map']:
                self.mini_map = not self.mini_map
                if self.mini_map:
                    pg.mixer.music.pause()
                if not self.mini_map:
                    pg.mixer.music.unpause()
        elif event.type == self.background_music.track_end:
            self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
            pg.mixer.music.load(self.background_music.tracks[self.background_music.track])
            pg.mixer.music.play()
        if self.culprit.life > 0:
            self.culprit.get_event(event)

    def interact(self, keys, now):
        if keys[tools.CONTROLLER_DICT['action']]:
            if now - 500 > self.last_action:
                for art in self.artifacts:
                    if pg.sprite.collide_mask(self.culprit, art):
                        if art.artifact_name == "life" and self.culprit.life < 6:
                            self.pickup_sound.sound.play()
                            art.used = True
                            self.culprit.life += 1
                        else:
                            self.error_sound.sound.play()
                loop_doors = self.doors
                for do in loop_doors:
                    if pg.sprite.collide_mask(self.culprit, do):
                        self.whoosh_sound.sound.play()
                        leads_to = do.leads_to
                        self.floor_instance.mini_map[self.floor_instance.current_map[0]][self.floor_instance.current_map[1]]["active"] = False
                        instance = self.floor_instance.change_map(leads_to)
                        self.mapfile, self.obstacles, self.doors, self.floor_exit, self.floor_tiles, self.fire_traps, self.pit_traps, self.spike_traps, self.bear_traps, self.push_traps_up, self.push_traps_down, self.push_traps_right, self.push_traps_left, self.cobras, self.bats, self.artifacts = instance.parse_map()
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
                        break
                for ex in self.floor_exit:
                    if pg.sprite.collide_mask(self.culprit, ex):
                        self.low_whoosh_sound.sound.play()
                        self.adjust_score(1)
                        self.floor_instance = floor.Floor()
                        self.mapfile, self.obstacles, self.doors, self.floor_exit, self.floor_tiles, self.fire_traps, self.pit_traps, self.spike_traps, self.bear_traps, self.push_traps_up, self.push_traps_down, self.push_traps_right, self.push_traps_left, self.cobras, self.bats, self.artifacts = self.floor_instance.entry_map.parse_map()
                self.last_action = now
            else:
                self.error_sound.sound.play()

    def update(self, now, keys):
        if not self.mini_map:
            if self.culprit.life <= 0:
                self.next = "MENU"
                self.culprit.direction_stack = []
                pg.mixer.music.stop()
                self.background_music.setup(self.background_music_volume)
                current_time = pg.time.get_ticks()
                if not self.died_sound:
                    self.die_sound.sound.play()
                    self.start_time = current_time
                    self.died_sound = True
                self.death_cover.set_alpha(self.death_alpha)
                self.death_alpha = self.death_alpha + self.alpha_step
                if current_time - self.start_time > 4000.0:
                    self.done = True
            elif self.culprit.last_hurt != self.check_hurt:
                self.hurt_sound.sound.play()
                self.check_hurt = self.culprit.last_hurt
            self.culprit.update(now, self.screen_rect, self.obstacles, self.fire_traps, self.pit_traps, self.spike_traps, self.bear_traps, self.push_traps_up, self.push_traps_down, self.push_traps_right, self.push_traps_left, self.cobras, self.bats)
            for do in self.doors:
                do.update(now)
            for ft in self.fire_traps:
                ft.update(now)
            for ex in self.floor_exit:
                ex.update(now)
            for st in self.spike_traps:
                st.update(now)
            for bt in self.bear_traps:
                if self.culprit.collide_bear and bt.id == self.culprit.collide_bear.id:
                    bt.update(now, self.culprit.collide_bear)
                else:
                    bt.update(now)
            for ptd in self.push_traps_down:
                ptd.update(now)
            for ptu in self.push_traps_up:
                ptu.update(now)
            for ptr in self.push_traps_right:
                ptr.update(now)
            for ptl in self.push_traps_left:
                ptl.update(now)
            for art in self.artifacts:
                art.update(now)
                if art.used is True and not art.removed:
                    self.updatemap(art.location)
                    art.removed = True
            for cob in self.cobras:
                cob.update(now, self.mapfile, self.obstacles, self.culprit, self.fire_traps, self.pit_traps, self.spike_traps, self.bear_traps, self.push_traps_up, self.push_traps_down, self.push_traps_right, self.push_traps_left)
                if cob.life <= 0 and not cob.removed:
                    self.updatemap(cob.location)
                    cob.removed = True
            for bat in self.bats:
                bat.update(now, self.mapfile, self.obstacles, self.culprit, self.push_traps_up, self.push_traps_down,
                           self.push_traps_right, self.push_traps_left)
                if bat.life <= 0 and not bat.removed:
                    self.updatemap(bat.location)
                    bat.removed = True
            self.hud.update(self.culprit, self.score)
            self.interact(keys, now)
        else:
            self.mini_map_instance.update(now, self.floor_instance.mini_map)

        pg.mouse.set_visible(False)

    def updatemap(self, targetlocation):
        map_tmp = self.floor_instance.maps_array[self.floor_instance.current_map[0]][self.floor_instance.current_map[1]].map[int((targetlocation[1] + 50) / 50)]  # vertical
        self.floor_instance.maps_array[self.floor_instance.current_map[0]][self.floor_instance.current_map[1]].map[int((targetlocation[1] + 50) / 50)] = str(map_tmp[:int((targetlocation[0] + 50) / 50)] + "F" + map_tmp[int((targetlocation[0] + 100) / 50):])  # horizontal

    def render(self, screen):
        if not self.mini_map:
            # Display Traps
            for ti in self.floor_tiles:
                ti.render(screen)
            for ob in self.obstacles:
                ob.render(screen)
            for do in self.doors:
                do.render(screen)
            for ex in self.floor_exit:
                ex.render(screen)
            for ft in self.fire_traps:
                ft.render(screen)
            for pt in self.pit_traps:
                pt.render(screen)
            for st in self.spike_traps:
                st.render(screen)
            for bt in self.bear_traps:
                bt.render(screen)
            for ptd in self.push_traps_down:
                ptd.render(screen)
            for ptu in self.push_traps_up:
                ptu.render(screen)
            for ptr in self.push_traps_right:
                ptr.render(screen)
            for ptl in self.push_traps_left:
                ptl.render(screen)
            for art in self.artifacts:
                art.render(screen)
            for cob in self.cobras:
                cob.render(screen)
            for cob in self.cobras:
                cob.render(screen, True)
            for bat in self.bats:
                bat.render(screen)
            for bat in self.bats:
                bat.render(screen, True)
            # Display HUD
            self.hud.render(screen)
            # Display Culprit
            self.culprit.render(screen)
            if self.culprit.life <= 0:
                screen.blit(self.death_cover, (0,0))
                screen.blit(self.game_over_text, self.game_over_rect)
        else:
            screen.blit(self.cover,(0,0))
            self.mini_map_instance.render(screen)
        
    def adjust_score(self, point):
        self.score += point

    def cleanup(self):
        pg.mixer.music.stop()
        self.background_music.setup(self.background_music_volume)

    def entry(self):
        pg.mixer.music.play()
        for item in reversed(self.previous_state):
            if item == "MENU":
                self.next_list = ["MENU"]
                self.mini_map = False
                self.culprit.reset(self.screen_rect)
                floor.Floor.size = 4
                self.floor_instance = floor.Floor()
                self.mini_map_instance = minimap.Minimap()
                self.mapfile, self.obstacles, self.doors, self.floor_exit, self.floor_tiles, self.fire_traps, self.pit_traps, self.spike_traps, self.bear_traps, self.push_traps_up, self.push_traps_down, self.push_traps_right, self.push_traps_left, self.cobras, self.bats, self.artifacts = self.floor_instance.entry_map.parse_map()
                self.last_action = 0
                self.check_hurt = self.culprit.last_hurt
                self.score = 0
                self.died_sound = False
                self.death_alpha = 0
                return
            elif item == "SETTINGS":
                self.next_list = ["SETTINGS"]
                return