import pygame
from pygame.sprite import Sprite
import random
from settings.settings import WIDTH, HEIGHT

class Moving_Sprite(Sprite):
    def __init__(self, screen, image, scale=(70, 70)):
        super(Moving_Sprite, self).__init__()
        self.screen = screen

        # Load the sphere image, scale it and set its rect attribute.
        self.image = pygame.transform.scale(image, scale)

        self.rect = self.image.get_rect()

        # Start each new sphere.
        bound_x = (WIDTH - 20)
        self.rect.centerx = random.randint(20, bound_x)
        bound_ya, bound_yb = (-(HEIGHT // 2), 0)
        self.rect.centery = random.randint(bound_ya, bound_yb)

    def update(self, speed):
        """Move the sphere down."""
        self.rect.centery += speed

    '''def update_right(self, speed):
        """Move the sphere down."""
        self.rect.centerx += speed

    def update_left(self, speed):
        """Move the sphere down."""
        self.rect.centerx -= speed'''
