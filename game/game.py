import random, time
import pygame
import assets, constants, windowgui
import game.rules as rules
from game.pile import Pile

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
        self.animation_running = False
        self.animation_piles = [self.waste, self.stock] + self.tableau
        self.animation_timer = windowgui.Timer()
        self.animation_timer.start()
 
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
    
    
    def _step_animation(self):
        while True:
            pile = random.choice(self.animation_piles)
            while not pile.cards:
                self.animation_piles.remove(pile)
                pile = random.choice(self.animation_piles)
            card = pile.cards[-1]
            if pile.label == "waste" or pile.label == "stock":
                card = random.choice(pile.cards)

            for foundation in self.foundations:
                if card["suit"] == foundation.label[11:]:
                    if not foundation.cards:
                        if card["power"] == 1:
                            foundation.cards.append(card)
                            pile.cards.remove(card)
                            return 
                    elif foundation.cards[-1]["power"] == card["power"] - 1:
                        foundation.cards.append(card)
                        pile.cards.remove(card)
                        return
            
    def update(self):
        if self.animation_running:
            if len(self.foundations[0].cards) == len(self.foundations[1].cards) \
                == len(self.foundations[2].cards) == len(self.foundations[3].cards) == 13:
                time.sleep(2)
                self.window.end()

            if self.animation_timer.passed(.5):
                self.animation_timer.start()
                self._step_animation()

            for pile in self.piles:
                pile.render(self.window.screen)
                  
        else:
            for pile in self.piles:
                pile.render(self.window.screen)
                
            mouse_pos = pygame.mouse.get_pos()
            if self.hand.cards:
                self.hand.rect.center = mouse_pos
                self.hand.render(self.window.screen)

            for card in [card for tableau in self.tableau for card in tableau.cards]:
                if card["flipped"]:
                    break   
            else:
                self.animation_running = True

        
        
            
    def eventloop(self, event):
        if self.animation_running:
            return
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

            


