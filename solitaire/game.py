import random
import pygame
import assets, constants, windowgui
import solitaire.rules as rules
from pile import Pile

class Game:
    def __init__(self, window):
        self.window = window
        self.stock = Pile(632, 30, label="stock")
        self.waste = Pile(532, 30, label="waste")
        self.tableau = [Pile(i*100+32, 215, label="tableau", renders_vertically=True) for i in range(7)]        
        self.foundations = [
            Pile(32, 30, label="foundation clubs", top_image=assets.CLUBS_SYMBOL),
            Pile(132, 30, label="foundation diamonds", top_image=assets.DIAMONDS_SYMBOL),
            Pile(100*2+32, 30, label="foundation hearts", top_image=assets.HEARTS_SYMBOL),
            Pile(100*3+32, 30, label="foundation spades", top_image=assets.SPADES_SYMBOL)
        ]
        self.piles = [self.stock, self.waste] + self.tableau + self.foundations
        self.hand = Pile(0, 0, renders_vertically=True)
        self.picked_pile = None
        self._init_cards()
 
    def _init_cards(self):
        cards = assets.cards.copy()
        random.shuffle(cards)
        for count,tableau in enumerate(self.tableau, 1):
            for i in range(count):
                card = cards.pop(0)
                if i != count-1:
                    card["flipped"] = True
                tableau.cards.append(card)
        self.stock.cards = cards
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for pile in self.piles:
            pile.render(self.window.screen)
        
        if self.hand.cards:
            self.hand.rect.center = mouse_pos
            self.hand.render(self.window.screen)

        for card in [card for tableau in self.tableau for card in tableau.cards]:
            if card["flipped"]:
                break   
        else:
            pass # player has won
        
        for foundation in self.foundations:
            if len(foundation.cards) < 13:
                break
        else:
            self.window.end()
            
    def eventloop(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for pile in self.piles:
                if pile.renders_vertically:
                    clicked_card_index = None
                    for index,rect in enumerate(pile.get_card_rects()):
                        if rect.collidepoint(mouse_pos) and not pile.cards[index]["flipped"]:
                            clicked_card_index = index
                    if clicked_card_index != None:
                        self.hand.cards = pile.cards[clicked_card_index:]
                        pile.cards = pile.cards[:clicked_card_index]
                        self.picked_pile = pile
                        break
                        
                elif pile.rect.collidepoint(mouse_pos) and pile.cards:
                    self.hand.cards = [pile.cards.pop()]
                    self.picked_pile = pile
                    break
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.hand.cards:
                card_moved = True
                for pile in self.piles:
                    if pile.renders_vertically:
                        on_card = False
                        for rect in pile.get_card_rects():
                            if rect.collidepoint(mouse_pos):
                                on_card = True
                        if pile.rect.collidepoint(mouse_pos) or on_card:
                            if rules.check(self.picked_pile, pile, self.hand.cards):
                                pile.cards.extend(self.hand.cards)
                                break

                    elif pile.rect.collidepoint(mouse_pos) and len(self.hand.cards) == 1:
                        move_valid = True       
                        if pile.label == "stock" and self.picked_pile.label != "waste":
                            move_valid = False

                        if pile.label == "waste" and self.picked_pile.label != "stock":
                            move_valid = False

                        if move_valid and rules.check(self.picked_pile, pile, self.hand.cards):
                            pile.cards.extend(self.hand.cards)
                            break
                            
                else:
                    card_moved = False
                    self.picked_pile.cards.extend(self.hand.cards)
                
                if card_moved:
                    if self.picked_pile.cards:
                        self.picked_pile.cards[-1]["flipped"] = False

                self.hand.cards.clear()
                self.picked_pile = None
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.stock.cards:
                    self.waste.cards.append(self.stock.cards.pop())
                else:
                    self.stock.cards = self.waste.cards.copy()
                    self.waste.cards.clear()

            


