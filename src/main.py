#!/usr/bin/env python3

import cv2
import mediapipe as mp
import os

import pygame
import sys
import json 
from utils import *
from settings import CAPTION, WIDTH, HEIGHT, JSON_FILE
from scenes.menuScene import (
    MenuScene,
)  # , RecordScene, CalibrationScene, DiagonalsScene, OptionsScene, TutorialScene
from broker import Broker
from broker import No_DB
from pose_tracking.cam_initialazer import check_availability

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
        self.exer_list = []
        self.connection = self.check_connection()
        self.json_object = None
        self.get_credentials() if self.connection == 0 else self.set_up_json()

        self.current_user = self.user_list[0]
        
        self.device_list = []
        self.current_camara = 0
        self.flag_cam = False
        self.__scene = MenuScene(self)

    def check_connection(self):
        br = Broker()
        status = br.connect()
        if status == 0:
            br.close()
        return status

    def set_up_json(self):
        if os.path.exists(JSON_FILE):
            pass
        else:
            json_obj = No_DB()
            json_obj.create_json_file(JSON_FILE)

        with open(JSON_FILE, 'r') as f:
            json_object = json.load(f)

        self.user_list = [
            f"{json_object['id']}-{json_object['credentials']['usuario']}_{json_object['credentials']['apellido']}"]
        self.exer_list = ['1-Diagonales']

        self.json_object = No_DB()

    def get_credentials(self):
        broker = Broker()
        _ = broker.connect()
        
        self.users = broker.get_users()
        self.user_list = create_list_users(self.users)
        self.current_user = self.user_list[0]
        self.exercises = broker.get_exercises()
        self.exer_list = create_list(self.exercises)
        broker.close()

    def set_up(self):
        self.device_list = check_availability()
        self.current_camara = self.device_list[0]

    def change_scene(self, scene):
        self.__scene = scene

    def get_scene(self):
        return self.__scene

    def change_camara(self, camara):
        self.current_camara = camara
        self.flag_cam = True

    def run(self):
        current_scene = self.get_scene()
        if self.device_list == []:
            # TODO cuando no hay camara disponible
            cap = cv2.VideoCapture(2)
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

                    if new_scene is not None:
                        self.change_scene(new_scene)
                        current_scene = new_scene

                    # Some necessary events for some specific scenes
                    if current_scene.get_name() == "MenuScene":
                        current_scene.tracking(results)
                        new_scene = current_scene.events(ev)
                        current_scene.update(dt)
                        current_scene.draw()
                    elif current_scene.get_name() == "RecordScene":
                        current_scene.tracking(results)
                        new_scene = current_scene.events(ev)
                        current_scene.update(dt)
                        current_scene.draw()
                    elif current_scene.get_name() == "TutorialScene":
                        current_scene.tracking(results)
                        new_scene = current_scene.events(ev)
                        current_scene.update(dt)
                        current_scene.draw()
                    elif current_scene.get_name() == "CalibrationScene":
                        current_scene.tracking(results)
                        current_scene.update(dt)
                        new_scene = current_scene.events(dt)
                        current_scene.draw()
                    elif current_scene.get_name() == "DiagonalsScene":
                        current_scene.tracking(results)
                        current_scene.update(dt)
                        new_scene = current_scene.events(ev)
                        current_scene.draw()
                    elif current_scene.get_name() == "SquadScene":
                        current_scene.tracking(results)
                        current_scene.update(dt)
                        new_scene = current_scene.events(ev)
                        current_scene.draw()
                    elif current_scene.get_name() == "ActivitiesScene":
                        current_scene.tracking(results)
                        new_scene = current_scene.events(ev)
                        current_scene.update(dt)
                        current_scene.draw()
                    elif current_scene.get_name() == "OptionsScene":
                        current_scene.tracking(results)
                        new_scene = current_scene.events(ev)
                        current_scene.update(dt)
                        current_scene.draw()

                    pygame.display.update()


if __name__ == "__main__":
    initiate = Initiator()
    initiate.set_up()
    initiate.run()
