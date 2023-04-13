#!/usr/bin/env python3

import sys
import pygame
from pygame.sprite import Group

from gui import Button
from gui import ImageButton
from gui import DropDown
from gui import BackgroundText
from gui import InputNumberBox
from gui import InputBox

from sticker import Sticker
import settings

from source import Source
from math import sqrt
import plots as plt
import datetime
import random
from animation import Animation
from utils import *

from pdfReport import MyDocTemplate

from broker import Broker

class Scene:
    def __init__(self, game):
        self.game = game
        self._name_scene = ''

    def get_name(self):
        return self._name_scene

    def events(self, events):
        raise NotImplementedError("events must be defined")

    def update(self, dt):
        raise NotImplementedError("update must be defined")

    def draw(self):
        raise NotImplementedError("draw must be defined")

class RecordScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = 'RecordScene'
        self.current_user = game.current_user
        self.historial = settings.FONTS['header'].render(
            "Historial", True, settings.BLACK)
        
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        
        self.button_back = Button((100, 20),  "Volver", settings.AMARILLO)
        self.userDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            100, 100, 200, 35,
            settings.FONTS['arial_small'],
            f'{game.current_user}', game.user_list)
        
        self.exerDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            530, 100, 200, 35, 
            settings.FONTS['arial_small'],
            f'{game.exer_list[0]}', game.exer_list)
        
        self.current_exer = self.exerDropDown.main
        self.tiempo=[]
        self.izq_errores = []
        self.izq_aciertos = []
        self.drcha_errores = []
        self.drcha_aciertos = []

        self.id_exer = get_id(self.exerDropDown.main)
        self.id_user = get_id(self.game.current_user)
        self.get_data()

        self.color = (238, 205, 134, 150)

        self.fontUnderline = settings.FONTS['arial_small']
        self.fontUnderline.set_underline(True)

        self.best_score, self.best_day = 0,0
        self.media_total_fallos, self.media_total_aciertos = 0,0
        self.media_errores_d, self.media_errores_i = 0,0

        self.no_data = self.fontUnderline.render(
            f"No hay datos disponibles", True, settings.BLACK)
        if self.data != []:
            self.tiempo, self.izq_errores, self.izq_aciertos, self.drcha_errores, self.drcha_aciertos = distribute_data(self.data)

            self.estadisticas = self.fontUnderline.render(
                f"Estadisticas", True, settings.BLACK)

            self.best_score, self.best_day = get_best_score(self.data)
            self.media_total_aciertos = calculate_media_total(self.izq_aciertos, self.drcha_aciertos)
            self.media_total_fallos = calculate_media_total(self.izq_errores, self.drcha_errores)

            self.media_aciertos_d = calculate_media_parte(self.drcha_aciertos)
            self.media_aciertos_i = calculate_media_parte(self.izq_aciertos)

            self.media_errores_d = calculate_media_parte(self.drcha_errores)
            self.media_errores_i = calculate_media_parte(self.izq_errores)

            self.canvas_izq, self.raw_data_izq = plt.create_right_hand_two_lines(
                self.izq_errores, self.izq_aciertos, self.tiempo, 'izquierda')
            self.size_izq = self.canvas_izq.get_width_height()

            self.surf_izq = pygame.image.fromstring(
                self.raw_data_izq, self.size_izq, "RGB")

            self.canvas_drcha, self.raw_data_drcha = plt.create_right_hand_two_lines(
                self.drcha_errores, self.drcha_aciertos, self.tiempo, 'derecha')
            self.size_drcha = self.canvas_drcha.get_width_height()

            self.surf_drcha = pygame.image.fromstring(
                self.raw_data_drcha, self.size_drcha, "RGB")

        self.bar_rect = pygame.Rect(300, (game.display.get_size()[1])-50, 700, 30)
        self.width = 0
        self.time_hand = 0
        self.pressed_back = pygame.time.get_ticks()
        # button pdf
        self.imagePDF = pygame.image.load(settings.PDF)
        self.pdfDownload = ImageButton(self.imagePDF, (1170, 100), 'pdf', (45,45))

    def get_data(self):
        broker = Broker()
        broker.connect()
        self.data = broker.get_score(self.id_exer, self.id_user,  10)
        broker.close()

    def events(self, events):
        self.userDropDown.update(events)
        self.game.current_user = self.userDropDown.main
        self.exerDropDown.update(events)
        if self.button_back.on_click(events) or self.button_back.get_clicked_state():
            self.game.change_scene(MenuScene(self.game))
        if self.pdfDownload.on_click(events):
            user = self.current_user.split('-')[1]
            filename = f'{user}_{datetime.datetime.now().strftime("%d-%m")}.pdf'
            if not os.path.exists(os.path.isfile(filename)):
                with open(filename, 'wb') as file:
                    file.write("")

            doc = MyDocTemplate(filename, self.id_user, self.id_exer)
            doc.create_doc(doc)
            
    def update(self, dt):
        self.button_back.update()
        if self.current_user != self.game.current_user:
            self.current_user = self.game.current_user
            self.id_exer = get_id(self.exerDropDown.main)
            self.id_user = get_id(self.current_user)
            self.get_data()
        
            if self.data != []:
                self.best_score, self.best_day = get_best_score(self.data)

                self.media_total_aciertos = calculate_media_total(self.izq_aciertos, self.drcha_aciertos)
                self.media_total_fallos = calculate_media_total(self.izq_errores, self.drcha_errores)

                self.media_aciertos_d = calculate_media_parte(self.drcha_aciertos)
                self.media_aciertos_i = calculate_media_parte(self.izq_aciertos)

                self.media_errores_d = calculate_media_parte(self.drcha_errores)
                self.media_errores_i = calculate_media_parte(self.izq_errores)

                self.canvas_izq, self.raw_data_izq = plt.create_right_hand_two_lines(self.izq_errores, self.izq_aciertos, self.tiempo, 'izquierda')
                self.size_izq = self.canvas_izq.get_width_height()

                self.surf_izq = pygame.image.fromstring(self.raw_data_izq, self.size_izq, "RGB")

                self.canvas_drcha, self.raw_data_drcha = plt.create_right_hand_two_lines(self.drcha_errores, self.drcha_aciertos, self.tiempo, 'derecha')
                self.size_drcha = self.canvas_drcha.get_width_height()

                self.surf_drcha = pygame.image.fromstring(self.raw_data_drcha, self.size_drcha, "RGB")
                
            else:
                self.best_score, self.best_day = 0, 0

    def reset_time(self):
        self.time_hand = 0
        self.width = 0

    def draw(self):
        self.game.display.fill(settings.GRANATE)

        pygame.draw.rect(self.game.display, self.color,
                         pygame.Rect(40, 160, 1200, 560))
        self.button_back.draw(self.game.display)
        self.pdfDownload.draw(self.game.display)
        self.game.display.blit(self.historial, (settings.WIDTH//3+30, 10))
        
        self.userDropDown.draw(self.game.display)
        self.exerDropDown.draw(self.game.display)

        if self.data != [] and self.game.current_user == self.current_user:
            self.mejor = settings.FONTS['arial_small'].render(
                f"-Mejor marca: {self.best_score}", True, settings.BLACK)
            self.dia = settings.FONTS['arial_small'].render(
                f"-Fecha: {self.best_day}", True, settings.BLACK)

            self.media_fallos = settings.FONTS['arial_small'].render(
                f"-Aciertos medios: {round(self.media_total_fallos,2)}", True, settings.BLACK)
            self.media_aciertos = settings.FONTS['arial_small'].render(
                f"-Errores medios: {round(self.media_total_aciertos,2)}", True, settings.BLACK)

            self.media_aciertos_dr = settings.FONTS['arial_small'].render(
                f"-Aciertos medios derecha: {round(self.media_aciertos_d,2)}", True, settings.BLACK)
            self.media_aciertos_iz = settings.FONTS['arial_small'].render(
                f"-Aciertos medios izquierda: {round(self.media_aciertos_i,2)}", True, settings.BLACK)

            self.media_err_dr = settings.FONTS['arial_small'].render(
                f"-Errores medios derecha: {round(self.media_errores_d,2)}", True, settings.BLACK)
            self.media_err_iz = settings.FONTS['arial_small'].render(
                f"-Errores medios izquierda: {round(self.media_errores_i,2)}", True, settings.BLACK)

            self.rect_stats = pygame.Surface(
                (370, 525))  # the size of your rect
            self.rect_stats.set_alpha(128)                # alpha level
            # this fills the entire surface
            self.rect_stats.fill((255, 255, 255))

            self.game.display.blit(self.rect_stats, (840,170))    # (0,0) are the top-left coordinates
            self.game.display.blit(self.surf_izq, (40,160))
            self.game.display.blit(self.surf_drcha, (40,430))
            self.game.display.blit(self.mejor, (870, 230))
            self.game.display.blit(self.estadisticas, (860, 180))
            self.game.display.blit(self.dia, (870, 280))
            self.game.display.blit(self.media_fallos, (870, 330))
            self.game.display.blit(self.media_aciertos, (870, 380))
            self.game.display.blit(self.media_aciertos_dr, (870, 430))
            self.game.display.blit(self.media_aciertos_iz, (870, 480))
            self.game.display.blit(self.media_err_dr, (870, 530))
            self.game.display.blit(self.media_err_iz, (870, 580))
            
        else:
            self.game.display.blit(self.no_data, (100, 200))

        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)
        # Draw progress bar
        pygame.draw.rect(self.game.display, settings.WHITE,
                         (300, (self.game.display.get_size()[1])-50, self.width, 30))
        pygame.draw.rect(self.game.display, settings.BLACK, self.bar_rect, 2)

    def check_collide(self, left, right):
        if self.button_back.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_back.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Volver"

        return ""

    def count(self, start_ticks):
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        if seconds >= settings.TIME_BUTTONS:
            return seconds
        return seconds
    
    def tracking(self, results):
        action = ""
        coefficient = settings.WIDTH_LOAD_BAR / settings.TIME_BUTTONS
        left_hand, right_hand = get_points(results)
        self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
        self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
        self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
        self.right_source.rect.centery = right_hand[1] * settings.HEIGHT

        # Colisiones
        action = self.check_collide(self.left_source, self.right_source)
        # ------------------------------------------
        if action == "Volver":
            self.time_hand = self.count(self.pressed_back)
        else:
           self.pressed_back = pygame.time.get_ticks()
        # ------------------------------------------

        self.width = self.time_hand * coefficient

        if action == "":
            self.reset_time()
        
        if self.time_hand > settings.TIME_BUTTONS:
            if action == "Volver":
                self.button_back.set_clicked_true()

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = 'MenuScene'
        self.screen = game.display

        self.button_activities = Button((100, self.screen.get_size()[1]/3),  "Activities")
        self.button_options = Button((1000, self.screen.get_size()[1]/3),  "Opciones")
        self.button_historial = Button((400, self.screen.get_size()[1]/3),  "Historial")
        self.button_tutorial = Button((700, self.screen.get_size()[1]/3), "Tutorial")
        self.button_exit = Button((1000, 80),  "Salir")

        self.bienvenido = settings.FONTS['header'].render("BIENVENIDO", True, settings.BLACK)
        self.message = settings.FONTS['medium'].render("Elige una de las posibles acciones", True, settings.BLACK)
        self.text_user = settings.FONTS['medium'].render("Usuario", True, settings.BLACK)
        
        self.bar_rect = pygame.Rect(100, (self.screen.get_size()[1])-90, 700, 30)
        self.userDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            100, 80, 200, 35, 
            settings.FONTS['arial_small'],
            f'{game.current_user}', game.user_list)

        self.right_source = Source(self.screen, settings.PUNTERO_ROJO)
        self.left_source = Source(self.screen, settings.PUNTERO_ROJO)
        self.width = 0
        self.time_hand = 0
        self.pressed_activities = pygame.time.get_ticks()
        self.pressed_options = pygame.time.get_ticks()
        self.pressed_tutorial = pygame.time.get_ticks()
        self.pressed_history = pygame.time.get_ticks()
        self.pressed_exit = pygame.time.get_ticks()

    def draw(self):
        # Buttons
        self.button_activities.draw(self.screen)
        self.button_options.draw(self.screen)
        self.button_historial.draw(self.screen)
        self.button_exit.draw(self.screen)
        self.button_tutorial.draw(self.screen)
        self.right_source.draw(self.screen)
        self.left_source.draw(self.screen)
        # Text
        self.screen.blit(self.bienvenido, self.bienvenido.get_rect(
            center=(settings.WIDTH // 2, settings.HEIGHT // 8)))
        self.screen.blit(self.message, self.message.get_rect(
            center=(settings.WIDTH // 2, settings.HEIGHT // 5)))
        self.screen.blit(self.text_user, self.text_user.get_rect(
							center=(150, 60)))

        self.userDropDown.draw(self.screen)
        # Draw progress bar
        pygame.draw.rect(self.screen, settings.WHITE,
                         (101, (self.screen.get_size()[1])-90, self.width, 30))
        pygame.draw.rect(self.screen, settings.BLACK, self.bar_rect, 2)

    def events(self, event):
        self.userDropDown.update(event)

        self.game.current_user = self.userDropDown.main
        if self.button_activities.on_click(event) or self.button_activities.get_clicked_state():
            self.game.change_scene(ActivitiesScene(self.game))
            self.button_activities.set_clicked_false()
        if self.button_options.on_click(event) or self.button_options.get_clicked_state():
            self.game.change_scene(OptionsScene(self.game))
            self.button_options.set_clicked_false()
        if self.button_historial.on_click(event) or self.button_historial.get_clicked_state():
            self.game.change_scene(RecordScene(self.game))
            self.button_historial.set_clicked_false()
        if self.button_tutorial.on_click(event) or self.button_tutorial.get_clicked_state():
            self.game.change_scene(TutorialScene(self.game))
            self.button_tutorial.set_clicked_false()
        if self.button_exit.on_click(event) or self.button_exit.get_clicked_state():
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.button_options.update()
        self.button_activities.update()
        self.button_tutorial.update()
        self.button_exit.update()
        self.button_historial.update()

    def count(self, start_ticks):
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        if seconds >= settings.TIME_BUTTONS:
            return seconds
        return seconds

    def check_collide(self, left, right):
        if self.button_activities.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_activities.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Activities"
        elif self.button_options.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_options.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Options"
        elif self.button_historial.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_historial.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Record"
        elif self.button_tutorial.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_tutorial.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Tutorial"
        if self.button_exit.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_exit.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Exit"
                
        return ""
    
    def reset_time(self):
        self.time_hand = 0
        self.width = 0

    def tracking(self, results):
        action = ""

        coefficient = settings.WIDTH_LOAD_BAR / settings.TIME_BUTTONS
        # Get the point in the hand
        left_hand, right_hand = get_points(results)

        # For each hand
        self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
        self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
        self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
        self.right_source.rect.centery = right_hand[1] * settings.HEIGHT

        # Colisiones
        action = self.check_collide(self.left_source, self.right_source)
        # ------------------------------------------
        if action == "Activities":
            self.time_hand = self.count(self.pressed_activities)
        else:
            self.pressed_activities = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Options":
            self.time_hand = self.count(self.pressed_options)
        else:
            self.pressed_options = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Record":
            self.time_hand = self.count(self.pressed_history)
        else:
            self.pressed_history = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Tutorial":
            self.time_hand = self.count(self.pressed_tutorial)
        else:
            self.pressed_tutorial = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Exit":
            self.time_hand = self.count(self.pressed_exit)
        else:
           self.pressed_exit = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if action == "":
            self.reset_time()

        if self.time_hand > settings.TIME_BUTTONS:
            if action == "Activities":
                self.button_activities.set_clicked_true()
            elif action == "Options":
                self.button_options.set_clicked_true()
            elif action == "Tutorial":
                self.button_tutorial.set_clicked_true()
            elif action == "Exit":
                self.button_exit.set_clicked_true()
            elif action == "Record":
                self.button_historial.set_clicked_true()

class CalibrationScene(Scene):
    def __init__(self, options):
        super().__init__(options)
        self._name_scene ='Calibration'
        self.screen = options.display
        self.body = Sticker(self.screen, settings.BODY, settings.WIDTH/2, settings.HEIGHT/2, 1000, 760)

		# Count, extrabig, mess, medium
        self.instructions = settings.FONTS['medium'].render("Haz visibles los siguientes puntos en la pantalla", True, settings.BLACK)
        self.mostrar_instrucciones = True

		# Puntos de la cabeza
        self.verde_cabeza = Sticker(self.screen, settings.VERDE, 640, 80, 60,60)
        self.rojo_cabeza = Sticker(self.screen, settings.ROJO, 640, 80, 60, 60)

		# Puntos de las manos
        self.verde_izq_mano = Sticker(self.screen, settings.VERDE, 870, 400, 60,60)
        self.rojo_izq_mano=  Sticker(self.screen, settings.ROJO, 870, 400, 60,60)

        self.verde_drch_mano = Sticker(self.screen, settings.VERDE, 410, 400, 60,60)
        self.rojo_drch_mano =  Sticker(self.screen, settings.ROJO, 410, 400, 60,60)

		# Puntos de los pies
        self.verde_drch_pie = Sticker(self.screen, settings.VERDE, 600, 700, 60,60)
        self.rojo_drch_pie =  Sticker(self.screen, settings.ROJO, 600, 700, 60,60)

        self.verde_izq_pie = Sticker(self.screen, settings.VERDE, 680, 700, 60,60)
        self.rojo_izq_pie  =  Sticker(self.screen, settings.ROJO, 680, 700, 60,60)

        # Tiempos
        self.timer = pygame.time.get_ticks()
        self.seconds = 0
        self.points = []
        self.checker = [False, False, False, False, False]

        self.current_results = None
        self.calibrated = False

        self.texto = BackgroundText(
            'Haz visibles los puntos en la pantalla', (100, 300), settings.WHITE, settings.GRIS, 30)
        
        self.time_instr =0
        self.ticks = pygame.time.get_ticks()
    
    def events(self, ev):
        pass

    def update(self, dt):
        if self.calibrated and dt != 0:
            self.game.static_points = self.current_results
            self.game.change_scene(MenuScene(self.game))

        if self.time_instr<3:
            self.mostrar_instrucciones =True
        else:
            self.mostrar_instrucciones=False

    def draw(self):
        if self.mostrar_instrucciones:
            self.texto.draw(self.screen)

    def reset_timer(self):
        self.timer = pygame.time.get_ticks()
        self.seconds = 0

    def count_seconds(self):
        self.seconds = (pygame.time.get_ticks()-self.timer) / \
            1000  # calculate how many seconds
        seconds_txt = settings.FONTS['extra'].render(
            '{0}'.format(int(self.seconds)), True, settings.BLACK)
        self.screen.blit(seconds_txt, (settings.WIDTH/2, settings.HEIGHT/2))

        pygame.display.flip()
        if self.seconds >= 3.2:
            self.calibrated = True

    def count(self, start_ticks):
        seconds = (pygame.time.get_ticks()-start_ticks) / 1000  # calculate how many seconds
        return seconds

    def calculate_distances(self, results):
        def distance_calculator(a, b):
            return sqrt(((results.pose_landmarks.landmark[b].x-results.pose_landmarks.landmark[a].x)**2) \
						+ ((results.pose_landmarks.landmark[b].y-results.pose_landmarks.landmark[a].y)**2) \
						+ ((results.pose_landmarks.landmark[b].z-results.pose_landmarks.landmark[a].z)**2))
		
        distance_ab_right = distance_calculator(12,14)
        distance_bc_right = distance_calculator(14,16)
        distance_right_total = distance_ab_right+distance_bc_right

        distance_ab_left = distance_calculator(11,13)
        distance_bc_left = distance_calculator(13,15)
        distance_left_total = distance_ab_left+distance_bc_left

        return distance_right_total, distance_left_total

    def calculate_final_point(self, results, right, left):
        final_right = (results.pose_landmarks.landmark[12].x+right,results.pose_landmarks.landmark[12].y)
        final_left = (results.pose_landmarks.landmark[11].x+right,results.pose_landmarks.landmark[11].y)
        return final_right, final_left

    def body_controller(self, results):
        self.current_results = results
        if self.time_instr < 3:
            self.time_instr = self.count(self.ticks)
            self.reset_timer()
        elif self.time_instr >= 3:
            try:
                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].visibility > 0.6:
                    if not all(item is True for item in self.checker):
                        self.verde_cabeza.draw(self.screen)
                    self.checker[0] = True
                else:
                    self.rojo_cabeza.draw(self.screen)
                    self.checker[0] = False
                # Manos
                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.6:
                    if not all(item is True for item in self.checker):
                        self.verde_drch_mano.draw(self.screen)
                    self.checker[1] = True
                else:
                    self.rojo_drch_mano.draw(self.screen)
                    self.checker[1] = False

                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.6:
                    if not all(item is True for item in self.checker):
                        self.verde_izq_mano.draw(self.screen)
                    self.checker[2] = True
                else:
                    self.rojo_izq_mano.draw(self.screen)
                    self.checker[2] = False

                # Pies
                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].visibility > 0.6:
                    if not all(item is True for item in self.checker):
                        self.verde_drch_pie.draw(self.screen)
                    self.checker[3] = True
                else:
                    self.rojo_drch_pie.draw(self.screen)
                    self.checker[3] = False

                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].visibility > 0.6:
                    if not all(item is True for item in self.checker):
                        self.verde_izq_pie.draw(self.screen)
                    self.checker[4] = True
                else:
                    self.rojo_izq_pie.draw(self.screen)
                    self.checker[4] = False
            except:
                self.checker = [False, False, False, False, False]


            # All points availables
            if all(item is True for item in self.checker):
                self.count_seconds()
                self.game.static_points = results

            # Not all points available
            elif not all(item is True for item in self.checker):
                self.show_seconds = False
                self.body.draw(self.screen)
                self.reset_timer()
                self.screen.blit(self.instructions, self.instructions.get_rect(center=(settings.WIDTH/2, 750)))
                pygame.display.flip()

class DiagonalsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = 'DiagonalesSuperiores'
        self.right_feet = 0
        self.left_feet = 0

        # Sounds
        self.press_star = pygame.mixer.Sound(settings.CLICKS)
        self.claps = pygame.mixer.Sound(settings.CLAPS)
        self.explosion = pygame.mixer.Sound(settings.EXPLOSION_SOUND)

        self.right_source = Source(game.display, settings.ROCKET)
        self.left_source = Source(game.display, settings.ROCKET)
        self.hands = Group([self.right_source, self.left_source])

        self.right_foot = Source(self.game.display, settings.LINEA_HORIZONTAL)
        self.left_foot = Source(self.game.display, settings.LINEA_HORIZONTAL)
        self.feet_group = Group([self.right_foot, self.left_foot])
     
        self.right_point = None
        self.left_point = None
        self.points_left = Group()
        self.points_right = Group()
        self.explosiones = Group()
        self.fireworks = Group()

        # Game settings
        self.trampas = settings.PORCENTAJE_TRAMPAS
        self.velocidad_bolas = settings.VELOCIDAD_ENTRE_BOLAS
        self.tiempo_juego = settings.TIEMPO_JUEGO

        self.aciertos_izquierda = 0
        self.aciertos_derecha = 0
        self.errores_izquierda = 0
        self.errores_derecha = 0

        self.puntuacion = 0

        self.texto = BackgroundText(
            'Atrapa las estrellas con las manos', (120, 300), settings.WHITE, settings.GRIS, 30)
        self.texto_partes = BackgroundText(
            'Muestra todas las partes del cuerpo', (120, 300), settings.WHITE, settings.GRIS, 30)
        self.texto_pies = BackgroundText(
            'Coloca los pies en la casilla', (150, 300), settings.WHITE, settings.GRIS, 30)
        self.mostrar_instrucciones = True
        self.time_instr = 0
        self.ticks = 0

        self.feet_right = None if game.static_points == None else (self.game.static_points.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x, self.game.static_points.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y)
        self.feet_left = None if game.static_points == None else (self.game.static_points.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x, self.game.static_points.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y)
        self.calibration = False if game.static_points == None else True
        self.box_feet = [] if game.static_points == None else self.create_box_feet()

        if game.static_points != None:
            left_hand_bound = create_diagonal_points_left(game.static_points)
            right_hand_bound = create_diagonal_points_right(game.static_points)
            self.shoulder_left, self.shoulder_right = get_shoulder_pos(game.static_points)

            self.bound_left_hand = (left_hand_bound[0], left_hand_bound[1])
            self.bound_right_hand = (right_hand_bound[0], right_hand_bound[1])

        else:  
            self.bound_left_hand, self.bound_left_hand = (0, 0), (0, 0)

        self.time_left = pygame.time.get_ticks()
        self.time_right = pygame.time.get_ticks()

        self.calibration_object = CalibrationScene(self.game)

        self.timer = 0
        self.current_results = None
        self.visibility_checker = True
        self.feet_checker = True
        self.current_time = self.tiempo_juego
        self.end = False
    def reset_sticker_timer(self):
        self.time_right = pygame.time.get_ticks()
        self.time_left = pygame.time.get_ticks()
        
    def reset_timer(self):
        self.timer = pygame.time.get_ticks()
        self.seconds = 0

    def count(self, start_ticks):
        seconds = (pygame.time.get_ticks()-start_ticks) / 1000  # calculate how many seconds
        return seconds
    
    def check_visibility(self):
        try:
            visibility = [i.visibility for i in self.current_results.pose_landmarks.landmark]
            self.visibility_checker = all(i >= 0.65 for i in visibility)
        except:
            self.visibility_checker = False

    def events(self, events):
        if self.end:
            self.introduced_data()
            self.game.change_scene(ActivitiesScene(self.game))
    
    def update(self, dt):
        pass

    def draw(self):
        if self.mostrar_instrucciones and self.calibration:
            self.texto.draw(self.game.display)
        elif self.time_instr >= 3 and self.calibration and not self.feet_checker:
            self.texto_pies.draw(self.game.display)
        elif self.time_instr >= 3 and self.calibration and not self.visibility_checker:
            self.texto_partes.draw(self.game.display)
        if self.calibration:
            pygame.draw.rect(self.game.display, settings.GRANATE, self.box_feet,  5, 0)
        
    def create_box_feet(self):
        point_left = escale_coor_pix(self.feet_left[0], self.feet_left[1])
        point_right = escale_coor_pix(self.feet_right[0], self.feet_right[1])
        width = distance_between_pixels(point_left, point_right)
        
        rect = pygame.Rect(point_left[0]-settings.FEET_MARGIN, point_left[1]-settings.FEET_MARGIN, width + settings.FEET_BOX, settings.FEET_BOX)
        return rect
    
    def check_feet(self):
        left_current_foot, rigth_current_foot = get_feet_points(self.current_results)

        self.left_foot.rect.centerx = left_current_foot[0] * settings.WIDTH
        self.left_foot.rect.centery = left_current_foot[1] * settings.HEIGHT
        self.right_foot.rect.centerx = rigth_current_foot[0] * settings.WIDTH
        self.right_foot.rect.centery = rigth_current_foot[1] * settings.HEIGHT

        if self.left_foot.rect.colliderect(self.box_feet) and self.right_foot.rect.colliderect(self.box_feet):
            self.feet_checker = True
        else:
            self.feet_checker = False

    def body_controller(self, results):
        self.current_results = results
        if self.current_results == None:
            return None

        # Get initial points
        if not self.calibration:
            self.calibration_object.body_controller(results)
            self.calibration_object.update(0)
            self.calibration_object.draw()
            self.calibration = self.calibration_object.calibrated
            self.ticks = pygame.time.get_ticks()
            if self.calibration:
                self.feet_right = (self.game.static_points.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x,
                                   self.game.static_points.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y)
                self.feet_left = (self.game.static_points.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
                              self.game.static_points.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y)
                self.box_feet = self.create_box_feet()

                left_hand_bound = create_diagonal_points_left(results)
                right_hand_bound = create_diagonal_points_right(results)
                self.shoulder_left, self.shoulder_right = get_shoulder_pos(results)
                self.bound_left_hand = (left_hand_bound[0], left_hand_bound[1])
                self.bound_right_hand = (right_hand_bound[0],right_hand_bound[1])
        # Pantalla de 3,2,1...
        if self.time_instr < 3 and self.calibration and not self.end:
            
            self.time_instr = self.count(self.ticks)
            self.reset_timer()
            self.reset_sticker_timer()
            self.timer = pygame.time.get_ticks()
        elif self.time_instr >= 3 and self.calibration and not self.feet_checker and not self.end:
            # Cuando los pies no estan la posicion calibrada o falta algún punto en la pantalla
            # Para checkeo de pies
            self.check_feet()
        elif self.time_instr >= 3 and self.calibration and not self.visibility_checker and not self.end:
            # Para checkeo de pies
            self.check_visibility()
        elif self.time_instr >= 3 and self.calibration and self.feet_checker and self.visibility_checker and not self.end:
            # Cuando esta todo ok
            # Se usa la izquierda en la derecha y viceversa pq se invierte la imagen
            # Para checkeo de pies
            self.check_feet()
            self.check_visibility()
            self.mostrar_instrucciones = False
            left_tramp = random.random() < self.trampas
            right_tramp = random.random() < self.trampas

            # Si puedo poner bolas
            bola_permitida_drch = True if (pygame.time.get_ticks()-self.time_right)/1000 >= settings.VELOCIDAD_ENTRE_BOLAS else False
            bola_permitida_izq = True if (pygame.time.get_ticks()-self.time_left)/1000 >= settings.VELOCIDAD_ENTRE_BOLAS else False
            # Crear acierto y fallo
            if len(self.points_left) == 0 and not left_tramp and bola_permitida_izq:
                
                left_x = random.uniform(self.bound_left_hand[0], self.shoulder_right[0])
                left_y = random.uniform(self.shoulder_right[1], settings.MARGIN)

                if left_x > settings.WIDTH:
                    left_x = settings.WIDTH - settings.MARGIN

                if left_y > settings.HEIGHT:
                    left_y = settings.HEIGHT - settings.MARGIN
                
                # Crear acierto o trampa
                if not left_tramp:
                    self.left_point = Sticker(self.game.display, settings.ESTRELLA, left_x, left_y, 75, 75)
                else:
                    self.left_point = Sticker(self.game.display, settings.BOMBA, left_x, left_y, 75, 75, True)
                self.left_point.time = pygame.time.get_ticks()
                self.points_left.add(self.left_point)

            if len(self.points_right) == 0 and bola_permitida_drch:

                right_x = random.uniform(self.shoulder_left[0], self.bound_right_hand[0])
                right_y = random.uniform(self.shoulder_left[1], settings.MARGIN)

                if right_x > settings.WIDTH:
                    right_x = settings.WIDTH - settings.MARGIN

                if right_y > settings.HEIGHT:
                    right_y = settings.HEIGHT - settings.MARGIN

                if not right_tramp:
                    self.right_point = Sticker(self.game.display, settings.ESTRELLA, right_x, right_y, 75, 75)
                else:
                    self.right_point = Sticker(self.game.display, settings.BOMBA, right_x, right_y, 75, 75, True)

                self.right_point.time = pygame.time.get_ticks()
                self.points_right.add(self.right_point)

            # Get the point in the hand
            left_hand, right_hand = get_points(results)

		    # For each hand
            self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
            self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
            self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
            self.right_source.rect.centery = right_hand[1] * settings.HEIGHT

            hit_list_left = pygame.sprite.groupcollide(self.hands, self.points_left, False, True)
            hit_list_right = pygame.sprite.groupcollide(self.hands, self.points_right, False, True)
            
            # Check the list of colliding sprites, and add one to the score for each one.
            for _ in hit_list_right:
                if self.right_point.get_trap():
                    self.errores_derecha += 1
                    self.puntuacion -= settings.FALLO
                    explosion = Animation(self.game.display, self.right_point.rect.centerx,
                                          self.right_point.rect.centery, settings.EXPLOSION, settings.FPS_EXPLOSION)
                    self.explosiones.add(explosion)
                    self.explosion.play()
                else:
                    self.aciertos_derecha += 1
                    self.puntuacion += settings.ACIERTO
                    firework = Animation(self.game.display, self.right_point.rect.centerx,
                                         self.right_point.rect.centery, settings.FIREWORKS, settings.FPS_FIREWORKS)
                    self.fireworks.add(firework)
                    self.press_star.play()
                self.time_right = pygame.time.get_ticks()

            for _ in hit_list_left:
                if self.left_point.get_trap():
                    self.errores_izquierda += 1
                    self.puntuacion -= settings.FALLO
                    explosion = Animation(self.game.display, self.left_point.rect.centerx,
                                          self.left_point.rect.centery, settings.EXPLOSION, settings.FPS_EXPLOSION)
                    self.explosiones.add(explosion)
                    self.explosion.play()
                else:
                    self.aciertos_izquierda += 1
                    self.puntuacion += settings.ACIERTO
                    firework = Animation(self.game.display, self.left_point.rect.centerx,
                                         self.left_point.rect.centery, settings.FIREWORKS, settings.FPS_FIREWORKS)
                    self.fireworks.add(firework)
                    self.press_star.play()
                self.time_left = pygame.time.get_ticks()

            if len(self.points_left) > 0:
                self.points_left.update()

            if len(self.points_right) > 0:
                self.points_right.update()

            if self.current_time <= 0:
                game_over_text = settings.FONTS['big'].render("Bien hecho", True, settings.BLACK)
                self.game.display.blit(game_over_text, game_over_text.get_rect(
                    center=(settings.WIDTH // 2, settings.HEIGHT // 2)))

                mistakes_txt = settings.FONTS['medium'].render(
                    "Aciertos: {0}".format(self.aciertos_izquierda+self.aciertos_derecha), True, settings.BLACK)
                self.game.display.blit(mistakes_txt, (15, 15))

                self.end = True

            new_time = (pygame.time.get_ticks() - self.timer)/1000

            self.current_time = self.tiempo_juego-int(new_time)

            min = int(self.current_time/60)
            sec = int(self.current_time % 60)
            time_txt = settings.FONTS['medium'].render("Tiempo: {0}".format(
                f'{min}:{sec}' if sec != 0 else f'{min}:00'), True, settings.BLACK)
            self.game.display.blit(time_txt, (15, 15))

            puntuacion = settings.FONTS['medium'].render("Puntuacion: ", True, settings.BLACK)
            self.game.display.blit(puntuacion, (900, 15))

            puntos = settings.FONTS['medium'].render(
                "{0}".format(self.puntuacion), True, settings.COLOR_ROJO)
            self.game.display.blit(puntos, (1065, 15))

	        # Draw point on the screen
            self.hands.draw(self.game.display)
            self.points_left.draw(self.game.display)
            self.points_right.draw(self.game.display)
            self.explosiones.draw(self.game.display)
            self.explosiones.update()
            self.fireworks.draw(self.game.display)
            self.fireworks.update()

        if self.end:
            self.claps.play()
				
    def introduced_data(self):
        broker = Broker()
        broker.connect()
        today = datetime.date.today()
        today = today.strftime("%Y-%m-%d")
        id = broker.get_user_id(self.game.current_user)
        broker.add_score(id, settings.ID_DIAGONALES, today, settings.TIEMPO_JUEGO, self.errores_izquierda, self.aciertos_izquierda,
                         self.errores_derecha, self.aciertos_derecha)
        broker.close()

class TutorialScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = 'TutorialScene'
        self.tutorial = settings.FONTS['header'].render(
            "Tutorial", True, settings.BLACK)

        self.flecha_drch = pygame.image.load(settings.FLECHA_DERECHA)
        self.flecha_izq = pygame.image.load(settings.FLECHA_IZQUIERDA)
        self.flecha_drch_button = ImageButton(self.flecha_drch, (450, 400), 'drch', (50,50))
        self.flecha_izq_button = ImageButton(self.flecha_izq, (450, 100), 'izq', (50,50))
        
        self.pet = pygame.image.load(settings.MASCOTA_NORMAL)
        self.pet = pygame.transform.scale(self.pet, (500,500))
        self.image = pygame.image.load(settings.ATRAS)
        self.home_btn = ImageButton(self.image, (15, 735), 'atras')
    
    def draw(self):
        self.game.display.fill(settings.GRANATE)

        pygame.draw.rect(self.game.display, settings.AMARILLO,
                         pygame.Rect(350, 100, 900, 650))
        
        self.home_btn.draw(self.game.display)
        self.flecha_drch_button.draw(self.game.display)
        self.flecha_izq_button.draw(self.game.display)
        self.game.display.blit(self.pet, (30, 300))
        self.game.display.blit(self.tutorial, (settings.WIDTH//3+30, 10))

    def events(self, events):
        if self.home_btn.on_click(events):
            self.game.change_scene(MenuScene(self.game))

    def update(self, dt):
        pass

class ActivitiesScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = 'ActivitiesScene'
        self.activities = settings.FONTS['header'].render("Actividades", True, settings.BLACK)

        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)
        
        self.button_calibrate = Button((970, 30), "Calibrar", settings.AMARILLO)
        self.button_back = Button((170, 30), "Volver", settings.AMARILLO)
        img_diagonales = pygame.image.load(settings.MINIATURA_DIAGONALES)
        img_modify = pygame.image.load(settings.MODIFY)

        self.diagonales = ImageButton(img_diagonales, (150, 150), 'diagonales', (200, 200))
        self.txt_diagonales = settings.FONTS['small'].render("Diagonales superiores", True, settings.BLACK)
        self.button_modify = ImageButton(img_modify, (230,390), 'modificar', (30,30))

        ''' Modify components '''
        self.modify_components = False
        self.txt_modificadores = settings.FONTS['medium'].render("Modificadores.", True, settings.BLACK)
        self.txt_time = settings.FONTS['small'].render("Tiempo de juego (segundos)", True, settings.BLACK)
        self.input_time = InputNumberBox(100, 520, 200, 35, text='')
        self.txt_time_appear = settings.FONTS['small'].render("Tiempo en el que los elementos aparecen", True, settings.BLACK)
        self.input_time_appear = InputNumberBox(100, 590, 200, 35, text='')
        self.txt_change_mano = settings.FONTS['small'].render("Elegir miniatura de manos", True, settings.BLACK)
        self.txt_change_acierto = settings.FONTS['small'].render("Elegir miniatura aciertos", True, settings.BLACK)
        self.txt_change_error = settings.FONTS['small'].render("Elegir miniatura error", True, settings.BLACK)

        self.button_apply = Button((900, self.game.display.get_size()[1]-180), 'Aplicar')

        self.bar_rect = pygame.Rect(100, (self.game.display.get_size()[1])-90, 700, 30)

        self.width = 0
        self.time_hand = 0
        self.pressed_diagonales = pygame.time.get_ticks()
        self.pressed_calibrate = pygame.time.get_ticks()
        self.pressed_apply = pygame.time.get_ticks()
        self.pressed_back = pygame.time.get_ticks()

    def draw(self):
        self.game.display.fill(settings.GRANATE)

        pygame.draw.rect(self.game.display, settings.AMARILLO,
                 pygame.Rect(50, 100, 1180, 650))
        self.button_calibrate.draw(self.game.display)
        self.button_back.draw(self.game.display)
        self.button_modify.draw(self.game.display)
        self.game.display.blit(self.activities, (settings.WIDTH//3, 10))

        self.game.display.blit(self.txt_diagonales, (150, 360))
        self.diagonales.draw(self.game.display)
        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)

        # Modificadores
        if self.modify_components:
            self.game.display.blit(self.txt_modificadores, (100, 450))
            self.game.display.blit(self.txt_time, (100,490))
            self.input_time.draw(self.game.display)
            self.game.display.blit(self.txt_time_appear, (100, 560))
            self.input_time_appear.draw(self.game.display)
            self.button_apply.draw(self.game.display)
        # Draw progress bar
        pygame.draw.rect(self.game.display, settings.WHITE,
                         (101, (self.game.display.get_size()[1])-90, self.width, 30))
        pygame.draw.rect(self.game.display, settings.BLACK, self.bar_rect, 2)

    def events(self, events):

        if self.diagonales.on_click(events) or self.diagonales.get_clicked_state():
            self.game.change_scene(DiagonalsScene(self.game))
            self.diagonales.clicked = True
        if self.button_back.on_click(events) or self.button_back.get_clicked_state():
            self.game.change_scene(MenuScene(self.game))
        if self.button_modify.on_click(events):
            self.modify_components = True
        if self.button_calibrate.on_click(events) or self.button_calibrate.get_clicked_state():
            self.game.change_scene(CalibrationScene(self.game))
            self.button_calibrate.set_clicked_false()
        if self.button_apply.on_click(events) or self.button_apply.get_clicked_state():
            # TODO aplicar cambios de modify (si no hay nada no)
            settings.TIEMPO_JUEGO = int(self.input_time.get_text()) if self.input_time.get_text() != "" else settings.TIEMPO_JUEGO
            settings.VELOCIDAD_ENTRE_BOLAS = int(self.input_time_appear.get_text()) if self.input_time_appear.get_text() != "" else settings.VELOCIDAD_ENTRE_BOLAS
            self.input_time.reset()
            self.input_time_appear.reset()
            self.modify_components = False
            self.button_modify.update()
        if self.modify_components:
            self.input_time.handle_event(events)
            self.input_time_appear.handle_event(events)
        
    def check_collide(self, left, right):
        if self.diagonales.rect.collidepoint(left.rect.centerx, left.rect.centery) or self.diagonales.rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Diagonales"
        elif self.button_calibrate.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_calibrate.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Calibrate"
        elif self.button_back.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_back.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Volver"
        
        return ""
    
    def reset_time(self):
        self.time_hand = 0
        self.width = 0

    def count(self, start_ticks):
        seconds = (pygame.time.get_ticks()-start_ticks) / 1000  # calculate how many seconds
        if seconds >= settings.TIME_BUTTONS:
            return seconds
        return seconds
    
    def tracking(self, results):
        action = ""
        coefficient = settings.WIDTH_LOAD_BAR / settings.TIME_BUTTONS
        left_hand, right_hand = get_points(results)
        self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
        self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
        self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
        self.right_source.rect.centery = right_hand[1] * settings.HEIGHT

        # Colisiones
        action = self.check_collide(self.left_source, self.right_source)
        # ------------------------------------------
        if action == "Diagonales":
            self.time_hand = self.count(self.pressed_diagonales)
        else:
           self.pressed_diagonales = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Calibrate":
            self.time_hand = self.count(self.pressed_calibrate)
        else:
            self.pressed_calibrate = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Aplicar":
            self.time_hand = self.count(self.pressed_apply)
        else:
            self.pressed_apply = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Volver":
            self.time_hand = self.count(self.pressed_back)
        else:
            self.pressed_back = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if action == "":
            self.reset_time()
        if self.time_hand >= settings.TIME_BUTTONS:
            if action == "Diagonales":
                self.diagonales.set_clicked_true()
            elif action == "Calibrate":
                self.button_calibrate.set_clicked_true()
            elif action == "Aplicar":
                self.button_apply.set_clicked_true()
            elif action == "Volver":
                self.button_back.set_clicked_true()

    def update(self, dt):
        self.diagonales.update()
        self.button_calibrate.update()
        self.button_apply.update()
        self.button_back.update()

class OptionsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "OptionsScene"
        self.options = settings.FONTS['header'].render(
            "Opciones", True, settings.BLACK)
        self.button_back = Button((170, 30),  "Volver", settings.AMARILLO)
        self.txt_camara = settings.FONTS['small'].render("Cambiar de fuente", True, settings.BLACK)
        self.camDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            100, 250, 200, 35,
            settings.FONTS['arial_small'],
            f'{game.current_camara}', [f'{i}' for i in game.device_list])

        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        self.txt_include_user = settings.FONTS['small'].render("Incluir usuario en base de datos (Nombre/Apellido)", True, settings.BLACK)
        self.input_create_user = InputBox(100, 330, 200, 35, text='')
        self.input_create_surname = InputBox(350, 330, 200, 35, text='')

        self.txt_delete_user = settings.FONTS['small'].render("Eliminar usuario de la base de datos (Nombre/Apellido)", True, settings.BLACK)
        self.input_delete_user = InputBox(100, 430, 200, 35, text='')
        self.input_delete_surname = InputBox(350, 430, 200, 35, text='')

        self.button_apply = Button((960, self.game.display.get_size()[1]-130), 'Aplicar')

        self.width = 0
        self.time_hand = 0
        self.pressed_back = pygame.time.get_ticks()
    def draw(self):
        self.game.display.fill(settings.GRANATE)

        pygame.draw.rect(self.game.display, settings.AMARILLO,
                         pygame.Rect(40, 160, 1200, 560))

        self.game.display.blit(self.txt_camara, (100, 200))
        self.camDropDown.draw(self.game.display)
        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)
        self.game.display.blit(self.txt_include_user, (100, 300))
        self.input_create_user.draw(self.game.display)
        self.input_create_surname.draw(self.game.display)

        self.game.display.blit(self.txt_delete_user, (100, 400))
        self.input_delete_user.draw(self.game.display)
        self.input_delete_surname.draw(self.game.display)

        self.button_apply.draw(self.game.display)
        self.button_back.draw(self.game.display)
        self.game.display.blit(self.options, (settings.WIDTH//3+30, 10))

    def include_user(self, name, surname):
        broker = Broker()
        broker.connect()
        broker.add_user(name, surname)
        broker.close()

    def delete_user(self, name, surname):
        broker = Broker()
        broker.connect()
        broker.delete_user(name, surname)
        broker.close()

    def events(self, events):
        self.input_create_user.handle_event(events)
        self.input_create_surname.handle_event(events)
        self.input_delete_user.handle_event(events)
        self.input_delete_surname.handle_event(events)
        self.camDropDown.update(events)
        if self.button_back.on_click(events) or self.button_back.get_clicked_state():
            self.game.change_scene(MenuScene(self.game))
        if self.button_apply.on_click(events) or self.button_apply.get_clicked_state():
            cam = int(self.camDropDown.getMain())
            if self.game.current_camara != cam:
                self.game.change_camara(cam)

            self.include_user(self.input_create_user.get_text(), self.input_create_surname.get_text()) if self.input_create_user.get_text() != "" and self.input_create_surname.get_text() != "" else None
            self.input_create_user.reset()
            self.input_create_surname.reset()

            self.delete_user(self.input_delete_user.get_text(), self.input_delete_surname.get_text()) if self.input_delete_user.get_text() != "" and self.input_delete_surname.get_text() != "" else None
            self.input_delete_user.reset()
            self.input_delete_surname.reset()

            self.game.get_users()

    def check_collide(self, left, right):
        if self.button_back.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_back.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Volver"

        return ""
    def reset_time(self):
        self.time_hand = 0
        self.width = 0

    def tracking(self, results):
        action = ""
        coefficient = settings.WIDTH_LOAD_BAR / settings.TIME_BUTTONS
        left_hand, right_hand = get_points(results)
        self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
        self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
        self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
        self.right_source.rect.centery = right_hand[1] * settings.HEIGHT

        # Colisiones
        action = self.check_collide(self.left_source, self.right_source)
        # ------------------------------------------
        if action == "Volver":
            self.time_hand = self.count(self.pressed_back)
        else:
           self.pressed_back = pygame.time.get_ticks()
        # ------------------------------------------

        self.width = self.time_hand * coefficient

        if action == "":
            self.reset_time()

        if self.time_hand > settings.TIME_BUTTONS:
            if action == "Volver":
                self.button_back.set_clicked_true()

    def count(self, start_ticks):
        seconds = (pygame.time.get_ticks()-start_ticks) / \
            1000  # calculate how many seconds
        if seconds >= settings.TIME_BUTTONS:
            return seconds
        return seconds

    def update(self, dt):
        self.button_apply.update()
        self.button_back.update()
