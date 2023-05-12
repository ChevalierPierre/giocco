import pygame as pg


class Minimap(pg.sprite.Sprite):
    def __init__(self):
        self.bsq_list = []
        self.render_list = []
        self.room_color = (50, 50, 50)
        self.door_color = (150, 150, 50)
        self.memo_raw_list = []

    def make_room_sprite(self,i,j,room_content):
        print("f      make room sprite")
        print(room_content)
        sprite_list = []
        pos_x, pos_y = i * self.room_width, j * self.room_height
        image = pg.Surface((self.actual_room_width,self.actual_room_height))
        image.fill(self.room_color)
        sprite_list.append((image,(pos_y,pos_x)))
        if room_content["doors"][0]:
            door_image = pg.Surface((self.door_width, self.door_height))
            image.fill(self.door_color)
            sprite_list.append((door_image,(pos_y, pos_x + 2 * self.door_width)))
        if room_content["doors"][1]:
            door_image = pg.Surface((self.door_width, self.door_height))
            image.fill(self.door_color)
            sprite_list.append((door_image,(pos_y + 2 * self.door_height, pos_x)))
        if room_content["doors"][2]:
            door_image = pg.Surface((self.door_width, self.door_height))
            image.fill(self.door_color)
            sprite_list.append((door_image,(pos_y + 4 * self.door_height, pos_x + 2 * self.door_width)))
        if room_content["doors"][3]:
            door_image = pg.Surface((self.door_width, self.door_height))
            image.fill(self.door_color)
            sprite_list.append((door_image,(pos_y + 2 * self.door_height, pos_x + 4 * self.door_width)))

        return sprite_list

    def make_render_list(self):
        print("makerenderlist")
        for i in range(0, len(self.bsq_list)):
            for j in range(0, len(self.bsq_list[i])):
                self.render_list.append(self.make_room_sprite(i,j,self.bsq_list[i][j]))

    def update(self, now, raw_list=None):
        print("update")
        #equal = [x for x in raw_list + self.memo_raw_list if x not in raw_list or x not in self.memo_raw_list]
        #if equal:
        #    return
        #self.memo_raw_list = raw_list
        vertical_index = []
        horizontal_index = []
        for i in range(0, len(raw_list)):
            for j in range(0, len(raw_list[0])):
                if raw_list[i][j]["tile"] and raw_list[i][j]["known"]:
                    vertical_index.append(i)
                    horizontal_index.append(j)
        vertical_index.sort()
        horizontal_index.sort()
        start_vertical = vertical_index[0]
        end_vertical = vertical_index[-1]
        start_horizontal = horizontal_index[0]
        end_horizontal = horizontal_index[-1]
        print(start_vertical, end_vertical, start_horizontal, end_horizontal)
        new_list = []
        count = -1
        for i in range(start_vertical, end_vertical+1):
            new_list.append([])
            count += 1
            for j in range(start_horizontal, end_horizontal+1):
                new_list[count].append(raw_list[i][j].copy())


        self.bsq_list = new_list
        self.room_width = int(800/len(self.bsq_list))
        self.actual_room_width = int(800/len(self.bsq_list))
        self.room_height = int(600/len(self.bsq_list[0]))
        self.actual_room_height = int(600/len(self.bsq_list[0]))
        self.door_width = int(self.actual_room_width/5)
        self.door_height = int(self.actual_room_height/5)
        self.make_render_list()

    def render(self, screen):
        print("render")
        print(self.render_list)
        for i in range(len(self.render_list) - 1):
            for j in range(len(self.render_list[0])):
                screen.blit(self.render_list[i][j][0], self.render_list[i][j][1])

