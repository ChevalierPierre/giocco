import pygame as pg


class Minimap(pg.sprite.Sprite):
    def __init__(self):
        self.bsq_list = []
        self.render_list = []
    
    def make_room_sprite(self,i,j,room_content):
        #first make room textures
        
        #then door textures
        if room.doors[0]:
        if room.doors[1]:
        if room.doors[2]:
        if room.doors[3]:

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
        self.room_width = 800/len(self.bsq_list)-4
        self.room_height = 600/len(self.bsq_list[0])-4

    def render(self, screen):
        for i in range(len(self.render_list) - 1):
            for j in range(len(self.render_list[0])):
                screen.blit(self.render_list[i][j].image, self.render_list[i][j].rect)
