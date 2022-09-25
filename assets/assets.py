import pygame
from os import path
import windowgui, constants


CURRENT_DIR = path.dirname(__file__)
IMAGES_DIR = path.join(CURRENT_DIR, "images")
CARDS_DIR = path.join(CURRENT_DIR, "images/cards")

CARD_BACK = windowgui.load_image("card_back", CARDS_DIR, scale=constants.CARD_SCALE)
CARD_EMPTY = windowgui.load_image("card_empty", CARDS_DIR, scale=constants.CARD_SCALE)
CLUBS_SYMBOL = windowgui.load_image("clubs", IMAGES_DIR, scale=constants.CARD_SCALE)
DIAMONDS_SYMBOL = windowgui.load_image("diamonds", IMAGES_DIR, scale=constants.CARD_SCALE)
HEARTS_SYMBOL = windowgui.load_image("hearts", IMAGES_DIR, scale=constants.CARD_SCALE)
SPADES_SYMBOL = windowgui.load_image("spades", IMAGES_DIR, scale=constants.CARD_SCALE)

cards = []
for suit in ["clubs", "diamonds", "hearts", "spades"]:
    for power in range(1, 14):
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
        
        color = "red"
        if suit in ["clubs", "spades"]:
            color = "black"
        
        cards.append({
        "flipped": False,
        "suit": suit,
        "power": power,
        "color": color,
        "image": windowgui.load_image(f"card_{suit}_{power_string}", CARDS_DIR, scale=constants.CARD_SCALE)
        })


