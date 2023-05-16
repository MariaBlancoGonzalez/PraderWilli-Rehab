import pygame

class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface(
            (2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
