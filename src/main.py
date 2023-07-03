#!/usr/bin/env python3
import sys
import cv2
import mediapipe as mp

import pygame

import settings.settings as settings
from utils import *
from ui.gui import BackgroundText
from scenes.menuScene import MenuScene
from tracking.cam_initialazer import check_availability

class Initiator:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.CAPTION)
        self.display = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
        
        self.device_list = []
        self.current_camara = 0
        self.flag_cam = False
        
        self.set_up()

        self.clock = pygame.time.Clock()

        self.static_points = None

        self.users = []
        self.user_list = []
        self.exercises = []
        self.exer_list = []

        self.get_credentials()
        self.current_user = self.user_list[0]

        self.__scene = MenuScene(self)

    def get_credentials(self):
        self.users = ['Usuario_Default']
        self.user_list = self.users
        self.current_user = self.users[0]
        self.exer_list = ['0-Diagonales superiores', '1-Squad', '2-Balls']

    def set_up(self):
        self.device_list = check_availability()
        try:
            self.current_camara = self.device_list[0]
        except IndexError:
            pass

    def change_scene(self, scene):
        self.__scene = scene

    def get_scene(self):
        return self.__scene

    def change_camara(self, camara):
        self.current_camara = camara
        self.flag_cam = True

    def run(self):
        if self.device_list == []:
            new_scene = None
            while True:
                self.clock.tick(60)
                dt = self.clock.tick(60)
                ev = pygame.event.get()
                self.display.fill(settings.WHITE)
                for event in ev:
                    if event.type == pygame.QUIT:
                        sys.exit()

                if new_scene is not self.get_scene() and new_scene is not None and new_scene.get_name() != "ActivitiesScene":
                    self.change_scene(new_scene)
                    self.change_scene(new_scene)
                    
                if self.get_scene().get_name() == "MenuScene":
                    new_scene = self.get_scene().events(ev)
                    self.get_scene().draw()
                elif self.get_scene().get_name() == "RecordScene":
                    new_scene = self.get_scene().events(ev)
                    self.get_scene().update(dt)
                    self.get_scene().draw()
                elif self.get_scene().get_name() == "TutorialScene":
                    new_scene = self.get_scene().events(ev)
                    self.get_scene().update(dt)
                    self.get_scene().draw()
                
                if self.get_scene().get_name() == "MenuScene":
                    texto_partes = BackgroundText(
                        "No hay dispositivos disponibles",
                        (self.display.get_size()[0]*0.3 , 400),
                        settings.WHITE,
                        settings.GRIS,
                        20,
                    )
                    texto_partes.draw(self.display)
                pygame.display.update()

        else:
            new_scene = None
            cap = cv2.VideoCapture(self.current_camara)
            mp_pose = mp.solutions.pose
            with mp_pose.Pose(
                min_detection_confidence=0.5, min_tracking_confidence=0.5
            ) as pose:
                while cap.isOpened():
                    # Make sure game doesn't run at more than 60 frames per second.
                    self.clock.tick(60)

                    dt = self.clock.tick(60)
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.VIDEORESIZE:
                            # Redimensionar la ventana
                            settings.WIDTH = event.w
                            settings.HEIGHT = event.h
                            self.display = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
                            self.get_scene().resized()

                    if self.flag_cam:
                        cap = cv2.VideoCapture(self.current_camara)
                        self.flag_cam = False
                    success, frame = cap.read()
                    try:
                        resized = cv2.resize(frame, (settings.WIDTH, settings.HEIGHT))
                    except:
                        pass

                    if not success:
                        # If loading a video, use 'break' instead of 'continue'.
                        continue
                    try:
                        frame = cv2.cvtColor(cv2.flip(resized, 2), cv2.COLOR_BGR2RGB)
                        pygame.surfarray.blit_array(self.display, frame.swapaxes(0, 1))
                    except:
                        pass

                    if new_scene is not self.get_scene() and new_scene is not None:
                        self.change_scene(new_scene)
                    # Some necessary events for some specific scenes
                    if self.get_scene().get_name() == "MenuScene":
                        self.get_scene().update(frame)
                        new_scene = self.get_scene().events(ev)
                        self.get_scene().render()
                    elif self.get_scene().get_name() == "ActivitiesScene":
                        self.get_scene().update(frame)
                        new_scene = self.get_scene().events(ev)
                        self.get_scene().render()
                    elif self.get_scene().get_name() == "RecordScene":
                        self.get_scene().update(frame)
                        new_scene = self.get_scene().events(ev)
                        self.get_scene().render()
                    elif self.get_scene().get_name() == "TutorialScene":
                        self.get_scene().update(frame)
                        new_scene = self.get_scene().events(ev)
                        self.get_scene().render()
                    elif self.get_scene().get_name() == "CalibrationScene":
                        self.get_scene().update(frame)
                        self.get_scene().time_control(dt)
                        self.get_scene().render()
                        new_scene = self.get_scene().events(dt)
                        self.get_scene().render()
                    elif self.get_scene().get_name() == "DiagonalsScene":
                        self.get_scene().update(frame)
                        new_scene = self.get_scene().events(ev)
                        self.get_scene().render()
                    elif self.get_scene().get_name() == "SquadScene":
                        self.get_scene().update(frame)
                        new_scene = self.get_scene().events(ev)
                        self.get_scene().render()
                    elif self.get_scene().get_name() == "BallScene":
                        self.get_scene().update(frame)
                        new_scene = self.get_scene().events(ev)
                        self.get_scene().render()

                    pygame.display.update()
                    pygame.display.flip()
if __name__ == "__main__":
    initiate = Initiator()
    initiate.run()
