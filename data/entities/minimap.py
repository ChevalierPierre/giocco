import pygame as pg


class Minimap(pg.sprite.Sprite):
    def __init__(self):
        self.bsq_list = []
        self.render_list = []
    
    def make_room_sprite(self,i,j,room_content):
        sprite_list = []
        pos_x, pos_y = i * self.room_width, y * self.room_height
        image = pg.Surface(self.actual_room_width,self.actual_room_height)
        image.fill(self.room_color)#pick a color
        sprite_list.append((image,(pos_y,pos_x))
        if room.doors[0]:
            door_image = pg.Surface(self.door_width, self.door_height)
            image.fill(self.door_color)
            sprite_list.append((door_image,(pos_y, pos_x + 2 * self.door_width)))
        if room.doors[1]:
            door_image = pg.Surface(self.door_width, self.door_height)
            image.fill(self.door_color)#pick a color
            sprite_list.append((door_image,(pos_y + 2 * self.door_height, pos_x)))
        if room.doors[2]:
            door_image = pg.Surface(self.door_width, self.door_height)
            image.fill(self.door_color)#pick a color
            sprite_list.append((door_image,(pos_y + 4 * self.door_height, pos_x + 2 * self.door_width))
        if room.doors[3]:
            door_image = pg.Surface(self.door_width, self.door_height)
            image.fill(self.door_color)#pick a color
            sprite_list.append((door_image,(pos_y + 2 * self.door_height, pos_x + 4 * self.door_width))

        return sprite_list

    def make_render_list(self):

        #x*room_weight
        # make the list of rect (position where I display the picture) and image (actual color or image to display)
        # based on bsq list, 800 / number of colomns and 600/ number of rows.
        # round these values to the lower integer and pick a room picture based of the offset of the doors in this room
        for i in range(0, len(self.bsq_list)-1):
            for j in range(0, len(self.bsq_list[i]) -1):
                self.render_list.append(make_room_sprite(i,j,self.bsq_list[i][j]))

    def update(self, now, raw_list=None):
        vertical_index = []
        horizontal_index = []
        for i in range(0, len(raw_list) - 1):
            for j in range(0, len(raw_list[0]) - 1):
                if raw_list[i][j].tile and raw_list[i][j].known:
                    vertical_index.append(i)
                    horizontal_index.append(j)
        vertical_index.sort()
        horizontal_index.sort()
        start_vertical = vertical_index[0]
        end_vertical = vertical_index[-1]
        start_horizontal = horizontal_index[0]
        end_horizontal = horizontal_index[-1]
        new_list = []
        for i in range(start_vertical, end_vertical):
            new_list.append([])
            for j in range(start_horizontal, end_horizontal):
                new_list[i].append(raw_list[i][j].copy())
        self.bsq_list = new_list
        self.room_width = 800/len(self.bsq_list)
        self.actual_room_width = 800/len(self.bsq_list)-40                    
        self.room_height = 600/len(self.bsq_list[0])
        self.actual_room_height = 600/len(self.bsq_list[0])-30
        self.door_width = int(self.actual_room_width/5)
        self.door_height = int(self.actual_room_height/5)          

    def render(self, screen):
        for i in range(len(self.render_list) - 1):
            for j in range(len(self.render_list[0])):
                for sprite, pos in self.render_list[i][j]:
                    screen.blit(sprite, pos)
