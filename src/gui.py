import pygame

from settings import *

class Button():
    def __init__(self, x=0, y=0, text="", width=200, height=50, elev=6):
        self.font = pygame.font.Font(FONT, 24)
        self.text = self.font.render(text, True, BLACK)
        self.text_rect = self.text.get_rect()

        self.bottom_rect = pygame.Rect((x+elev, y+elev), (width, height))
        self.top_rect = pygame.Rect((x, y), (width, height))
        self.text_rect.center = self.top_rect.center

        self.time_pressed = 0.0
        self.hover = False
        self.pressed = False
        self.clicked = False

    def update(self):
        # Si esta click activar gif
        pass

    def draw(self, screen):
        top_rect_color = AZUL_MARINO if self.hover else AZUL_CLARO
        if not self.clicked:
            # Si no pulsamos dibujamos todo en su posición original
            pygame.draw.rect(screen, GRIS, self.bottom_rect)
            pygame.draw.rect(screen, top_rect_color, self.top_rect)
            self.text_rect.center = self.top_rect.center
        else:
            # Si pulsamos cambiamos la posición de dibujado abajo
            pygame.draw.rect(screen, top_rect_color, self.bottom_rect)
            self.text_rect.center = self.bottom_rect.center
        screen.blit(self.text, self.text_rect)

class Image:
    def __init__(self, image="", pos = (0,0)):
        self.image = pygame.image.load(image)
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.image, self.pos)