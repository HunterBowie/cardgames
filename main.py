import pygame
import constants
import windowgui, solitaire, blackjack

window = windowgui.Window(constants.SCREEN_SIZE)
pygame.display.set_caption("Card Games")

window.set_manager(blackjack.Game)
window.start(auto_cycle=True)