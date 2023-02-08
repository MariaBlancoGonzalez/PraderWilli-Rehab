#!/usr/bin/env python3

import sys
import pygame
import cv2
import mediapipe as mp

from gui import Button
from gui import Image
from settings import *
from source import Source
from game import Game_diagonals
from game import Game_calibration
from aux import *

class Scene:
    def __init__(self, options):
        self.options = options

    def events(self, events):
        raise NotImplementedError("events must be defined")

    def update(self, dt):
        raise NotImplementedError("update must be defined")

    def draw(self, display):
        raise NotImplementedError("draw must be defined")

class MenuScene(Scene):
    def __init__(self, options):
        super().__init__(options)
        self.button_play = Button(100, options.display.get_size()[1]/3,  "Empezar")
        self.button_calibrate = Button(500, options.display.get_size()[1]/3,  "Calibrar")
        self.button_historial = Button(900, options.display.get_size()[1]/3,  "Historial")
        self.button_exit = Button(900, options.display.get_size()[1]-100,  "Salir")
    
        self.pet = Image(MASCOTA, (options.display.get_size()[0]-100, options.display.get_size()[1]-100))
        
        pygame.font.init()
        self.font_header = pygame.font.Font(FONT, HEADER_FONT)
        self.font_message = pygame.font.Font(FONT, MEDIUM_FONT)
        self.bienvenido = self.font_header.render("BIENVENIDO", True, BLACK)
        self.message = self.font_message.render("Elige una de las posibles acciones", True, BLACK)

    def events(self, events):
        if self.button_play.clicked:
            game_calibrate = Game_calibration(self.options)
            game_calibrate.calibrate()

            game_diagonals = Game_diagonals(self.options)
            game_diagonals.information()
            game_diagonals.game()
            print(game_diagonals.aciertos, ', ', game_diagonals.errores)
        if self.button_calibrate.clicked:
            game_calibrate = Game_calibration(self.options)
            game_calibrate.calibrate()
        if self.button_exit.clicked:
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.button_play.update()
        self.button_calibrate.update()
        self.button_exit.update()

    def count(self, start_ticks):
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        if seconds>=2.5:
            return True

    def check_collide(self, left, right):

        if self.button_play.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_play.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Play"
        elif self.button_calibrate.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_calibrate.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Calibrate"
        if self.button_exit.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_exit.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Exit"
                
        return ""

    def draw(self, display):
        mp_pose = mp.solutions.pose
        
        pygame.display.flip()

        right_source = Source(self.options.display, PUNTERO_ROJO)
        left_source = Source(self.options.display, PUNTERO_ROJO)
        pressed_play = pygame.time.get_ticks()
        pressed_calibrate = pygame.time.get_ticks()
        pressed_history = pygame.time.get_ticks()
        pressed_exit= pygame.time.get_ticks()
        finish = False
        action = ""
        # For webcam input:
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                # Make sure game doesn't run at more than 60 frames per second.
                self.options.clock.tick(60)

                # Check for any Pygame events.
                for event in pygame.event.get():
                    # Exit game if user hits the quit button.
                    ## print(event)
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                        sys.exit()

                success, image = cap.read()
                resized = cv2.resize(image, (WIDTH, HEIGHT)) 
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # Para "pegar" las ventanas
                image = cv2.cvtColor(cv2.flip(resized, 2), cv2.COLOR_BGR2RGB)
                results = pose.process(image)

                # Get the point in the hand
                left_hand, right_hand = get_points(results)

                # For each hand
                left_source.rect.centerx =  left_hand[0] * WIDTH
                left_source.rect.centery = left_hand[1] * HEIGHT
                right_source.rect.centerx = right_hand[0] * WIDTH
                right_source.rect.centery = right_hand[1] * HEIGHT

                action = self.check_collide(left_source, right_source)
                # ------------------------------------------
                if action == "Play":
                    finish = self.count(pressed_play)
                else:
                    pressed_play = pygame.time.get_ticks()
                # ------------------------------------------
                if action == "Calibrate":
                    finish = self.count(pressed_calibrate)
                else:
                    pressed_calibrate = pygame.time.get_ticks()
                # ------------------------------------------
                # TODO quitar comments
                '''if action == "Record":
                    finish = self.count(pressed_calibrate)
                else:
                    pressed_calibrate = pygame.time.get_ticks()'''
                # ------------------------------------------
                if action == "Exit":
                    finish = self.count(pressed_exit)
                else:
                    pressed_exit = pygame.time.get_ticks()


                if finish:
                    cap.release()
                    continue

                pygame.surfarray.blit_array(self.options.display, image.swapaxes(0, 1))
                self.button_play.draw(self.options.display)
                self.button_calibrate.draw(self.options.display)
                self.button_historial.draw(self.options.display)
                self.button_exit.draw(self.options.display)
                self.pet.draw(self.options.display)
                
                self.options.display.blit(self.bienvenido, self.bienvenido.get_rect(
							center=(WIDTH // 2, HEIGHT // 8)))
                self.options.display.blit(self.message, self.message.get_rect(
							center=(WIDTH // 2, HEIGHT // 5)))

                # Draw point on the screen
                right_source.draw(self.options.display)
                left_source.draw(self.options.display)
                pygame.display.flip()

        if action == "Play":
            self.button_play.pressed = True
            self.button_play.clicked = True
        elif action == "Calibrate":
            self.button_calibrate.pressed = True
            self.button_calibrate.clicked = True
        elif action == "Exit":
            self.button_exit.pressed = True
            self.button_exit.clicked = True
        # TODO 
        '''elif action == "Record":
            self.button_record.pressed = True
            self.button_record.clicked = True'''
        
