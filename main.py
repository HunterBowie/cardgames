import assets
import windowgui

window = windowgui.Window((500, 500))

class Manager:
    def __init__(self, window):
        pass
    def update(self):
        x = 0
        for card in assets.cards:
            window.screen.blit(card["image"], (x, 100))
            x += 30
        print("updating")
window.set_manager(Manager)
window.start(auto_cycle=True)