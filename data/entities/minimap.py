import pygame as pg
from .. import tools
import os
import copy


class Minimap(pg.sprite.Sprite):
    def __init__(self):
        self.bsq_list = []
        self.render_list = []
        self.memo_raw_list = []

    def make_room_sprite(self,i,j,room_content, empty=False, entrance=False, active=False):
        sprite_list = []
        pos_x, pos_y = i * self.room_height, j * self.room_width
        pos_x_plus, pos_y_plus = (i + 1) * self.room_height, (j + 1) * self.room_width
        image = pg.Surface((self.actual_room_width, self.actual_room_height))
        if not empty:
            if entrance:
                if active:
                    image_sprite = tools.Image.load(os.path.join("minimap", "asfault_10.png")).convert()
                else:
                    image_sprite = tools.Image.load(os.path.join("minimap", "asfault_7.png")).convert()
            else:
                if active:
                    image_sprite = tools.Image.load(os.path.join("minimap", "asfault_11.png")).convert()
                else:
                    image_sprite = tools.Image.load(os.path.join("minimap", "asfault_8.png")).convert()
            image_sprite = pg.transform.smoothscale(image_sprite, (self.actual_room_width, self.actual_room_height))
            image.blit(image_sprite, (0, 0))
            door_sprite = tools.Image.load(os.path.join("minimap","dungeons_and_flagons5.jpg")).convert()
            door_sprite = pg.transform.smoothscale(door_sprite, (self.door_width,self.door_height))
            door_image = pg.Surface((self.door_width, self.door_height))
            door_image.blit(door_sprite,(0,0))
            sprite_list.append((image,(pos_y,pos_x)))
            if room_content["tile"]:
                if room_content["doors"][0]:
                    sprite_list.append((door_image,(pos_y + 2 * 4 * self.door_width, pos_x)))
                if room_content["doors"][1]:
                    sprite_list.append((door_image,(pos_y, pos_x + 2 * 4 * self.door_height)))
                if room_content["doors"][2]:
                    sprite_list.append((door_image,(pos_y + 2 * 4 * self.door_width, pos_x_plus - self.door_height)))
                if room_content["doors"][3]:
                    sprite_list.append((door_image,(pos_y_plus - self.door_width, pos_x + 2 * 4 * self.door_height)))
            return sprite_list
        else:
            image_sprite = tools.Image.load(os.path.join("minimap","asfault_4.jpg")).convert()
            image_sprite = pg.transform.smoothscale(image_sprite, (self.actual_room_width,self.actual_room_height))
            image.blit(image_sprite,(0,0))
            sprite_list.append((image, (pos_y, pos_x)))
            return sprite_list

    def make_render_list(self):
        self.render_list = []
        for i in range(0, len(self.bsq_list)):
            for j in range(0, len(self.bsq_list[i])):
                if self.bsq_list[i][j]["tile"] and self.bsq_list[i][j]["known"]:
                    if self.bsq_list[i][j]["entrance"]:
                        if self.bsq_list[i][j]["active"]:
                            self.render_list.append(self.make_room_sprite(i, j, self.bsq_list[i][j], False, True, True))
                        else:
                            self.render_list.append(self.make_room_sprite(i, j, self.bsq_list[i][j], False, True))
                    else:
                        if self.bsq_list[i][j]["active"]:
                            self.render_list.append(self.make_room_sprite(i, j, self.bsq_list[i][j], False, False, True))
                        else:
                            self.render_list.append(self.make_room_sprite(i,j,self.bsq_list[i][j]))
                else:
                    self.render_list.append(self.make_room_sprite(i,j,self.bsq_list[i][j], True))

    def update(self, now, raw_list=None):
        notequal = [x for x in raw_list + self.memo_raw_list if x not in raw_list or x not in self.memo_raw_list]
        if not notequal:
            return
        self.memo_raw_list = copy.deepcopy(raw_list)
        vertical_index = []
        horizontal_index = []
        for i in range(0, len(raw_list)):
            for j in range(0, len(raw_list[i])):
                if raw_list[i][j]["tile"] and raw_list[i][j]["known"]:
                    vertical_index.append(i)
                    horizontal_index.append(j)
        vertical_index.sort()
        horizontal_index.sort()
        start_vertical = vertical_index[0]
        end_vertical = vertical_index[-1]
        start_horizontal = horizontal_index[0]
        end_horizontal = horizontal_index[-1]
        new_list = []
        count = -1
        for i in range(start_vertical, end_vertical+1):
            new_list.append([])
            count += 1
            for j in range(start_horizontal, end_horizontal+1):
                new_list[count].append(raw_list[i][j].copy())

        self.bsq_list = new_list
        self.room_width = int(800/len(self.bsq_list[0]))
        self.actual_room_width = int(800/len(self.bsq_list[0]))
        self.room_height = int(600/len(self.bsq_list))
        self.actual_room_height = int(600/len(self.bsq_list))
        self.door_width = int(self.actual_room_width/17)
        self.door_height = int(self.actual_room_height/17)
        self.make_render_list()

    def render(self, screen):
        for i in range(0,len(self.render_list)):
            for j in range(0,len(self.render_list[i])):
                screen.blit(self.render_list[i][j][0], self.render_list[i][j][1])
