import pygame
import windowgui, constants
from pile import Pile

class Game:
    def __init__(self, window):
        self.window = window
        self.player_deck = Pile(0, constants.HEIGHT-150)
        windowgui.root_rects(window.screen.get_size(),
        [self.player_deck.rect], center_x=True)
    
    def update(self):
        self.player_deck.render(self.window.screen)

