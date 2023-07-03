import pygame
from scenes.scene import Scene
import settings.settings as settings

class TimeDown(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "timerDownScene"

        # Tracking time
        self.timer = pygame.time.get_ticks()
        self.seconds = 0

        self.start = True
    
    def restart(self):
        self.timer = pygame.time.get_ticks()
        self.seconds = 0

    def events(self):
        if self.seconds >= 3.2:
            return False
        return True
    
    def render(self):
        seconds_txt = settings.FONTS["extra"].render(
            "{0}".format(int(self.seconds)), True, settings.BLACK
        )
        self.game.display.blit(seconds_txt, (self.game.display.get_size()[0]/2-30, self.game.display.get_size()[1]*0.35))

    def update(self, _):
        if self.start:
            self.timer = pygame.time.get_ticks()
            self.seconds = 0
            self.start = False

        self.seconds = (
            pygame.time.get_ticks() - self.timer
        ) / 1000  # calculate how many seconds