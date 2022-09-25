import pygame
import constants
import windowgui, game

window = windowgui.Window(constants.SCREEN_SIZE)
pygame.display.set_caption("Solitaire")

window.set_manager(game.Game)
window.start(auto_cycle=True)