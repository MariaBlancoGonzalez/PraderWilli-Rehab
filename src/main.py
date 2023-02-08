#!/usr/bin/env python3

import cv2
import mediapipe as mp

import pygame
import sys

from settings import *
from scene import MenuScene

class Initiator:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))

        self.clock = pygame.time.Clock()
        self.scene = MenuScene(self)

    def run(self):
        while 1:
            dt = self.clock.tick(60)
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    sys.exit()
            # Scene events
            self.scene.events(ev)
            self.scene.update(dt)
            self.scene.draw(self.display)
            pygame.display.update()

    def change_scene(self, scene):
        self.scene = scene

if __name__ == '__main__':
    initiate = Initiator()
    initiate.run()
