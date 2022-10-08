from json import tool
from ..entities import heart
from .. import tools

class Hud(tools.States):
    def __init__(self, culprit, score, screen):
        self.screen = screen

        # Score management
        self.score = score
        self.score_text, self.score_rect = self.make_text('{}'.format(self.score), (255, 255, 255), (25, 25), 50)

        # Heart management
        self.heart = culprit.life
        self.heart_image = self.display_heart()
    
    def display_heart(self):
        heart_list = []
        heart_pos_x = 100
        for i in range(self.heart):
            heart_list.append(heart.Heart((heart_pos_x, 7)))
            heart_pos_x += 50
        return heart_list

    def render(self, screen):
        # RENDER SCORE
        screen.blit(self.score_text, self.score_rect)
        # RENDER HEART
        for lp in self.heart_image:
            lp.render(screen)

    def update(self, culprit, score):
        self.heart = culprit.life
        self.heart_image = self.display_heart()
        self.score = score
        self.score_text, self.score_rect = self.make_text('{}'.format(self.score), (255, 255, 255), (25, 25), 50)