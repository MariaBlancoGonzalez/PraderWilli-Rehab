import pygame
from pygame.sprite import Sprite

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Point(pygame.sprite.Sprite):
    """A class to represent a single landmark."""
    def __init__(self, screen, image, width, height):
        super(Point, self).__init__()
        self.screen = screen

        self.image = pygame.image.load(image)

        self.image = pygame.transform.scale(
            self.image, (25, 25))
        self.rect = self.image.get_rect()

        self.rect.centerx = width
        self.rect.centery = height

    def draw(self, surface):
        surface.blit(self.image, self.rect)
