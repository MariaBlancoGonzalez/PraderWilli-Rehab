#!/usr/bin/env python3

import cv2
import mediapipe as mp

import pygame
import sys
from utils import *
from settings import CAPTION, WIDTH, HEIGHT
from scenes import MenuScene #, RecordScene, CalibrationScene, DiagonalsScene, OptionsScene, TutorialScene

from broker import Broker

class Initiator:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))

        self.clock = pygame.time.Clock()
        
        self.static_points = None

        self.users = []
        self.user_list = []
        self.exercises = []
        self.get_users()
        self.get_exer()
        self.current_user = self.user_list[0]
        self.exer_list = create_list(self.exercises)

        self.device_list = []
        self.current_camara = 0
        self.flag_cam = False
        self._scene = MenuScene(self)
    
    def get_users(self):
        broker = Broker()
        broker.connect()
        self.users = broker.get_users()
        self.user_list = create_list(self.users)
        self.current_user = self.user_list[0]
        broker.close()

    def get_exer(self):
        broker = Broker()
        broker.connect()
        self.exercises = broker.get_exercises()
        broker.close()

    def set_up(self):
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                self.device_list.append(i)
            cap.release()
        if self.device_list != []:
            self.current_camara = self.device_list[0]
        
    def change_scene(self, scene):
        self._scene = scene

    def change_camara(self, camara):
        self.current_camara = camara
        self.flag_cam = True

    def run(self):
        if self.device_list == []:
            # TODO cuando no hay camara disponible
            cap = cv2.VideoCapture(2)
        else:
            cap = cv2.VideoCapture(self.current_camara)
            mp_pose = mp.solutions.pose
            with mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as pose:
                while cap.isOpened():
                    # Make sure game doesn't run at more than 60 frames per second.
                    self.clock.tick(60)

                    dt = self.clock.tick(60)
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.QUIT:
                            sys.exit()
                    if self.flag_cam:
                        cap = cv2.VideoCapture(self.current_camara)
                        self.flag_cam = False
                    success, image = cap.read()
                    resized = cv2.resize(image, (WIDTH, HEIGHT)) 
                    if not success:
                        # If loading a video, use 'break' instead of 'continue'.
                        continue

                    image = cv2.cvtColor(cv2.flip(resized, 2), cv2.COLOR_BGR2RGB)
                    results = pose.process(image)
                    pygame.surfarray.blit_array(self.display, image.swapaxes(0, 1))
                        
                    # Some necessary events for some specific scenes
                    if self._scene.get_name() == 'MenuScene':
                        self._scene.tracking(results)
                        self._scene.events(ev)
                        self._scene.update(dt)
                        self._scene.draw()
                    elif self._scene.get_name() == 'RecordScene':
                        self._scene.events(ev)
                        self._scene.update(dt)
                        self._scene.draw()
                    elif self._scene.get_name() == 'TutorialScene':
                        self._scene.events(ev)
                        self._scene.update(dt)
                        self._scene.draw()
                    elif self._scene.get_name() == 'Calibration':
                        self._scene.body_controller(results)
                        self._scene.update(dt)
                        self._scene.draw()
                    elif self._scene.get_name() == 'DiagonalesSuperiores':
                        self._scene.body_controller(results)
                        self._scene.update(dt)
                        self._scene.events(ev)
                        self._scene.draw()
                    elif self._scene.get_name() == 'ActivitiesScene':
                        self._scene.tracking(results)
                        self._scene.update(dt)
                        self._scene.events(ev)
                        self._scene.draw()
                    elif self._scene.get_name() == 'OptionsScene':
                        self._scene.update(dt)
                        self._scene.events(ev)
                        self._scene.draw()
                        
                    pygame.display.update()
                
                
if __name__ == '__main__':
    initiate = Initiator()
    initiate.set_up()
    initiate.run()
