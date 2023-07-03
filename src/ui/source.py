import pygame
from pygame.sprite import Sprite


class Source(pygame.sprite.Sprite):
    """A class to represent a single landmark."""

    def __init__(self, screen, image, scale=(70,70)):
        super(Source, self).__init__()
        self.screen = screen
        self.scale= scale
        self.image = pygame.image.load(image)

        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()

        # Start each new landmark.
        self.rect.centerx = 0
        self.rect.centery = 0
    
    def update_position(self, pos):
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_image(self, image):
        self.image=image
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()

        # Start each new landmark.
        self.rect.centerx = 0
        self.rect.centery = 0