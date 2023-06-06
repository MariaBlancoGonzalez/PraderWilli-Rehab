import pygame
from pygame.sprite import Sprite

import os
from settings import BLACK


class Animation(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, animacion, fps,dim = (90,90)):
        super(Animation, self).__init__()
        self.screen = screen

        self.dim = dim
        self.animaciones = self.cargar_animacion(animacion)
        # Current image
        self.index = 0
        self.image = self.animaciones[self.index]

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.fps = fps
        self.fotograma = 0
        

    def cargar_animacion(self, carpeta):
        animacion = []
        files = sorted([file for file in os.listdir(carpeta)])
        for i in files:
            image = pygame.image.load(f"{carpeta}/{i}")
            image.set_colorkey(BLACK)
            scaled_image = pygame.transform.scale(image, (self.dim[0],self.dim[1]))
            animacion.append(scaled_image)

        return animacion

    def update(self):
        # update explosion animation
        self.fotograma += 1

        if self.fotograma >= self.fps and self.index < len(self.animaciones) - 1:
            self.fotograma = 0
            self.index += 1
            self.image = self.animaciones[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.animaciones) - 1 and self.fotograma >= self.fps:
            self.kill()
