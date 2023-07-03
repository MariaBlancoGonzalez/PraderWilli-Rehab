import pygame
from pygame.sprite import Sprite

class Sticker(Sprite):
    """A class to represent a single landmark."""

    def __init__(self, screen, image, width, height, x=45, y=45, trap=False):
        super(Sticker, self).__init__()
        self.screen = screen

        self.image = pygame.image.load(image)

        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()

        # Insider clock
        self.time = None
        self.trap = trap
        self.rect.centerx = width
        self.rect.centery = height

    def get_trap(self):
        return self.trap

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        if self.time is not None:  # If the timer has been started...
            # and 500 ms have elapsed, kill the sprite.
            if pygame.time.get_ticks() - self.time >= 3000:
                self.kill()
                return True
        return False
