import pygame
from pygame.sprite import Sprite


class Source(pygame.sprite.Sprite):
    """A class to represent a single landmark."""

    def __init__(self, screen, image):
        super(Source, self).__init__()
        self.screen = screen

        self.image = pygame.image.load(image)

        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        # Start each new landmark.
        self.rect.centerx = 0
        self.rect.centery = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
