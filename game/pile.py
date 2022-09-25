import pygame
import constants, windowgui, assets

class Pile:
    def __init__(self, x, y, label="", cards=None, top_image=None, renders_vertically=False):
        self.cards = cards
        if cards is None:
            self.cards = []
        self.top_image = top_image
        self.label = label
        self.renders_vertically = renders_vertically
        self.rect = pygame.Rect(x, y, constants.CARD_WIDTH, constants.CARD_WIDTH)
    
    
    def get_card_rects(self):
        card_rects = []
        y_offset = 0
        for i in range(len(self.cards)):
            card_rects.append(pygame.Rect(self.rect.x, self.rect.y+y_offset,
             constants.CARD_WIDTH, constants.CARD_WIDTH))
            y_offset += constants.CARD_VERTICAL_OFFSET
        return card_rects
    
    def render(self, screen):
        if self.cards:
            if self.renders_vertically:
                for index,rect in enumerate(self.get_card_rects()):
                    image = self.cards[index]["image"] 
                    if self.cards[index]["flipped"]:
                        image = assets.CARD_BACK                       
                    
                    screen.blit(image, rect.topleft)
            else:    
                image = self.cards[-1]["image"]
                if self.cards[-1]["flipped"]:
                    image = assets.CARD_BACK
                    
                screen.blit(image, self.rect.topleft)
        else:
            screen.blit(assets.CARD_EMPTY, self.rect.topleft)
            if self.top_image:
                screen.blit(self.top_image, self.rect.topleft)
            
    
    def __repr__(self):
        return str(self.cards)

        
