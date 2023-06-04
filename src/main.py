#!/usr/bin/env python3

import cv2
import mediapipe as mp
import os

import pygame
import sys
import json 
from utils import *
from settings import CAPTION, WIDTH, HEIGHT, EXER_0_JSON, EXER_1_JSON, EXER_2_JSON
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
        # If connection = 0 good connection = 1 no internet
        self.connection = self.check_connection()

        # Si se han estado almacenando datos del niño sin conexión
        if self.connection == 0:
            # checkea si hay algún json que no sea {}, si lo hay almacena los datos
            self.check_json_files(EXER_0_JSON)
            self.check_json_files(EXER_1_JSON)
            self.check_json_files(EXER_2_JSON)

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

    def get_credentials(self):
        broker = Broker()
        _ = broker.connect()
        
        self.users = broker.get_users()
        self.user_list = create_list_users(self.users)
        self.current_user = self.user_list[0]
        self.exercises = broker.get_exercises()
        self.exer_list = create_list(self.exercises)
        broker.close()

    def check_json_files(self, file):
        data = []
        with open(file, 'r') as f:
            json_object = json.load(f)
            if json_object != []:
                # Introduce into db
                broker = Broker()
                broker.connect()
                for i in json_object:
                    broker.add_score(i['PT_A_id'], i['PT_E_id'], i['PT_fecha'], i['PT_tiempo'],
                                    i['PT_fallos_izquierda'], i['PT_aciertos_izquierda'], i['PT_fallos_derecha'], i['PT_aciertos_derecha'])
        with open(file, 'w') as f:
            json.dump(data, f)

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
                    elif current_scene.get_name() == "BallScene":
                        current_scene.update_camera_utilities(image)
                        current_scene.tracking(results)
                        new_scene = current_scene.events(ev)
                        current_scene.update(dt)
                        current_scene.draw()

                    pygame.display.update()

if __name__ == "__main__":
    initiate = Initiator()
    initiate.set_up()
    initiate.run()
