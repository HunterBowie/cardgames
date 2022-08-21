import pygame
from os import path
import windowgui


CURRENT_DIR = path.dirname(__file__)
CARDS_DIR = path.join(CURRENT_DIR, "images/cards")

cards = []
for suit in ["clubs", "diamonds", "hearts", "spades"]:
    for power in range(1, 13):
        power_string = str(power)
        if power < 10:
            power_string = "0" + power_string
        if power == 1:
            power_string = "A"
        elif power == 11:
            power_string = "J"
        elif power == 12:
            power_string = "Q"
        elif power == 13:
            power_string = "K"
        
        cards.append({
        "suit": suit,
        "power": power, 
        "image": windowgui.load_image(f"card_{suit}_{power_string}", CARDS_DIR)
        })



