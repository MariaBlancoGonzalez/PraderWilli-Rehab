import pygame
from pygame.sprite import Group
import statistics
import random
import datetime

import settings.settings as settings
import settings.settings_0 as settings_0

from ui.source import Source
from ui.sticker import Sticker
from ui.animation import Animation
from ui.gui import BackgroundText, ImageButton

from broker import DataBroker
from tracking.tracker_utils import *
from utils import *

from scenes.exergames.game import Exergame
from scenes.activitiesScene import ActivitiesScene
from scenes.auxiliaryScenes.calibrationScene import CalibrationScene
from scenes.auxiliaryScenes.timeDownScene import TimeDown

class DiagonalsScene(Exergame):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "DiagonalsScene"

        self.right_feet = 0
        self.left_feet = 0

        # Music
        self.pip_sound = pygame.mixer.Sound(settings.PIP)
        self.pip_sound.set_volume(1)

        # Sounds
        self.press_star = pygame.mixer.Sound(settings.CLICKS)
        self.claps = pygame.mixer.Sound(settings.CLAPS)
        self.explosion = pygame.mixer.Sound(settings.EXPLOSION_SOUND)

        # Sources
        self.right_source = Source(game.display, settings.ROCKET)
        self.left_source = Source(game.display, settings.ROCKET)
        self.hands = Group([self.right_source, self.left_source])
        self.right_hand = Group([self.right_source])
        self.left_hand = Group([self.left_source])

        # No se dibujan, simplemente sirven como un Sprite checker para que los pies no se salgan
        self.right_foot = Source(self.game.display, settings.LINEA_HORIZONTAL)
        self.left_foot = Source(self.game.display, settings.LINEA_HORIZONTAL)
        self.feet_group = Group([self.right_foot, self.left_foot])

        # Points and animations
        self.right_point = None
        self.left_point = None
        self.points_left = Group()
        self.points_right = Group()
        self.explosiones = Group()
        self.fireworks = Group()

        # Animation
        self.init_gif = Animation(
            self.game.display,
            self.game.display.get_size()[0]*0.5,
            self.game.display.get_size()[1]-350,
            settings.DIAGGIF,
            settings_0.FPS_DIAG, (700, 700)
        )
        self.init_animation = Group(self.init_gif)

        # Game settings
        self.trampas = read(settings_0.EXER_0_CONFIG, "PORCENTAJE_TRAMPAS")
        self.velocidad_bolas = read(settings_0.EXER_0_CONFIG, "VELOCIDAD_ENTRE_BOLAS")
        self.tiempo_juego = read(settings_0.EXER_0_CONFIG, "TIEMPO_JUEGO")

        self.coefficient = 500 / self.tiempo_juego
        
        self.aciertos_izquierda = 0
        self.aciertos_derecha = 0
        self.errores_izquierda = 0
        self.errores_derecha = 0

        # Text
        self.txt_instr = BackgroundText(
            "Atrapa las estrellas con las manos",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        
        self.txt_feet = BackgroundText(
            "Coloca los pies en la casilla",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )

        # If calibration is done before start
        self.feet_right = (
            None
            if game.static_points == None
            else (
                self.game.static_points[27]['x'],
                self.game.static_points[27]['y']
        ))
        self.feet_left = (
            None
            if game.static_points == None
            else (
                self.game.static_points[28]['x'],
                self.game.static_points[28]['y'],
            )
        )
        self.box_feet = [] if game.static_points == None else self.create_box_feet()

        if game.static_points != None:
            left_hand_bound = create_diagonal_points_left(game.static_points)
            right_hand_bound = create_diagonal_points_right(game.static_points)
            top_margin = create_top_margin(game.static_points)
            self.shoulder_left, self.shoulder_right = get_shoulder_pos(game.static_points)
            self.margin = (top_margin[0], top_margin[1])
            self.bound_left_hand = (left_hand_bound[0], left_hand_bound[1])
            self.bound_right_hand = (right_hand_bound[0], right_hand_bound[1])

        else:
            self.bound_left_hand, self.bound_left_hand, self.margin = (0, 0), (0, 0), settings.MARGIN

        # Tracking time during game
        self.time_left = pygame.time.get_ticks()
        self.time_right = pygame.time.get_ticks()
        self.reaction_timeLeft = pygame.time.get_ticks()
        self.reaction_timeRight = pygame.time.get_ticks()


        self.reaction_timeLeft_list_good = []
        self.reaction_timeLeft_list_bad = []
        self.reaction_timeRight_list_good = []
        self.reaction_timeRight_list_bad = []

        self.feet_checker = True

        self.pitido = True

    def resized(self):
        # Text
        self.txt_instr = BackgroundText(
            "Atrapa las estrellas con las manos",
            (self.game.display.get_size()[0]*0.11,70),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        self.txt_visibility = BackgroundText(
            "Muestra todas las partes del cuerpo",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        self.txt_feet = BackgroundText(
            "Coloca los pies en la casilla",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )


    def events(self, events):
        if self.end:
            json_object = DataBroker()
            print(self.reaction_timeLeft_list_bad, self.reaction_timeLeft_list_good)
            json_object.write_data_json(settings_0.EXER_0_JSON, settings_0.ID_DIAGONALES, self.tiempo_juego, 
                                self.errores_izquierda, self.aciertos_derecha, self.errores_derecha, self.aciertos_derecha, 
                                round(statistics.mean(self.reaction_timeLeft_list_bad), 2) if len(self.reaction_timeLeft_list_bad) >1 else self.velocidad_bolas, 
                                round(statistics.mean(self.reaction_timeLeft_list_good),2) if len(self.reaction_timeLeft_list_good) >1 else self.velocidad_bolas,
                                round(statistics.mean(self.reaction_timeRight_list_bad), 2) if len(self.reaction_timeRight_list_bad) >1 else self.velocidad_bolas, 
                                round(statistics.mean(self.reaction_timeRight_list_good),2) if len(self.reaction_timeRight_list_good) >1 else self.velocidad_bolas)
            return ActivitiesScene(self.game)

        if self.atras.get_clicked_state() or self.atras.on_click(events):
            self.music.stop()
            return ActivitiesScene(self.game)

        return None

    def render(self):
        if self.time_instr >= 3 and self.calibration and not self.feet_checker:
            self.txt_feet.draw(self.game.display)
        elif self.time_instr >= 3 and self.calibration and not self.visibility_checker:
            self.txt_visibility.draw(self.game.display)
        if self.calibration and self.time_instr >=3 and not self.countdowns:
            pygame.draw.rect(self.game.display, settings.AZUL_CLARO, self.box_feet, 7, 0)
        
        self.atras.draw(self.game.display)

    def create_box_feet(self):
        point_left = self.feet_left[0], self.feet_left[1]
        point_right = self.feet_right[0], self.feet_right[1]
        width = distance_between_pixels(point_left, point_right)

        rect = pygame.Rect(
            point_left[0] - settings_0.FEET_MARGIN,
            point_left[1] - settings_0.FEET_MARGIN,
            width + settings_0.FEET_BOX,
            settings_0.FEET_BOX,
        )

        return rect

    def check_feet(self):
        left_current_foot, rigth_current_foot = get_feet_points(self.pose_tracker.landmark_process)

        self.left_foot.update_position(left_current_foot)
        self.right_foot.update_position(rigth_current_foot)

        if self.left_foot.rect.colliderect(self.box_feet) and self.right_foot.rect.colliderect(self.box_feet):
            self.feet_checker = True
        else:
            self.feet_checker = False
    
    def calibration_success(self):
        self.feet_right = (self.pose_tracker.landmark_process[27]['x'],self.pose_tracker.landmark_process[27]['y'])
        self.feet_left = (self.pose_tracker.landmark_process[28]['x'],self.pose_tracker.landmark_process[28]['y'])
                
        self.box_feet = self.create_box_feet()

        left_hand_bound = create_diagonal_points_left(self.pose_tracker.landmark_process)
        right_hand_bound = create_diagonal_points_right(self.pose_tracker.landmark_process)
        top_margin = create_top_margin(self.pose_tracker.landmark_process)
        self.shoulder_left, self.shoulder_right = get_shoulder_pos(self.pose_tracker.landmark_process)
        self.margin = (top_margin[0], top_margin[1])
        self.bound_left_hand = (left_hand_bound[0], left_hand_bound[1])
        self.bound_right_hand = (right_hand_bound[0], right_hand_bound[1])
        self.music.play()

        self.ticks = pygame.time.get_ticks()
        self.time_instr = 0

    def reset_timers(self):
        self.time_left = pygame.time.get_ticks()
        self.time_right = pygame.time.get_ticks()
        self.reaction_timeLeft = pygame.time.get_ticks()
        self.reaction_timeRight = pygame.time.get_ticks()

    def logic(self):
        self.check_feet()
        self.visibility = check_visibility(self.pose_tracker.landmark_process)
        if self.feet_checker:
            left_tramp = random.random() < self.trampas
            right_tramp = random.random() < self.trampas

            if self.pitido:    
                self.pip_sound.play()
                self.pitido = False

            # Si puedo poner bolas
            bola_permitida_drch = (
                True
                if (pygame.time.get_ticks() - self.time_right) / 1000
                >= self.velocidad_bolas
                else False
            )
            bola_permitida_izq = (
                True
                if (pygame.time.get_ticks() - self.time_left) / 1000
                >= self.velocidad_bolas
                else False
            )
            # Crear acierto y fallo
            if len(self.points_left) == 0 and bola_permitida_izq:
                left_x = random.uniform(self.bound_left_hand[0], self.shoulder_right[0])
                left_y = random.uniform(self.shoulder_right[1], settings.MARGIN if self.margin[1] <= 0 else self.margin[1]) # En vez de margin

                if left_x > settings.WIDTH:
                    left_x = settings.WIDTH - settings.MARGIN

                if left_y > settings.HEIGHT:
                    left_y = settings.HEIGHT - settings.MARGIN

                # Crear acierto o trampa
                if not left_tramp:
                    self.left_point = Sticker(
                        self.game.display, settings.ESTRELLA, left_x, left_y, 75, 75
                    )
                else:
                    self.left_point = Sticker(
                        self.game.display, settings.BOMBA, left_x, left_y, 75, 75, True
                    )
                self.left_point.time = pygame.time.get_ticks()
                self.points_left.add(self.left_point)

            if len(self.points_right) == 0 and bola_permitida_drch:
                right_x = random.uniform(
                    self.shoulder_left[0], self.bound_right_hand[0]
                )
                right_y = random.uniform(self.shoulder_left[1], settings.MARGIN if self.margin[1] <= 0 else self.margin[1])

                if right_x > settings.WIDTH:
                    right_x = settings.WIDTH - settings.MARGIN

                if right_y > settings.HEIGHT:
                    right_y = settings.HEIGHT - settings.MARGIN

                if not right_tramp:
                    self.right_point = Sticker(
                        self.game.display, settings.ESTRELLA, right_x, right_y, 75, 75
                    )
                else:

                    self.right_point = Sticker(
                        self.game.display,
                        settings.BOMBA,
                        right_x,
                        right_y,
                        75,
                        75,
                        True,
                    )

                self.right_point.time = pygame.time.get_ticks()
                self.points_right.add(self.right_point)

            hit_list_left = pygame.sprite.groupcollide(
                self.left_hand, self.points_left, False, True
            )
            hit_list_right = pygame.sprite.groupcollide(
                self.right_hand, self.points_right, False, True
            )

            # Check the list of colliding sprites, and add one to the score for each one.
            for _ in hit_list_right:
                if self.right_point.get_trap():
                    self.errores_derecha += 1
                    self.puntuacion -= settings_0.FALLO_PTO
                    explosion = Animation(
                    self.game.display,
                        self.right_point.rect.centerx,
                        self.right_point.rect.centery,
                        settings.EXPLOSION,
                        settings_0.FPS_EXPLOSION,
                    )
                    self.explosiones.add(explosion)
                    self.explosion.play()
                    self.reaction_timeRight_list_good.append((pygame.time.get_ticks() - self.reaction_timeRight) / 1000)
                    
                else:
                    self.aciertos_derecha += 1
                    self.puntuacion += settings_0.ACIERTO_PTO
                    firework = Animation(
                        self.game.display,
                        self.right_point.rect.centerx,
                        self.right_point.rect.centery,
                        settings.FIREWORKS,
                        settings_0.FPS_FIREWORKS,
                    )
                    self.fireworks.add(firework)
                    self.press_star.play()
                    self.reaction_timeRight_list_good.append((pygame.time.get_ticks() - self.reaction_timeRight) / 1000)
                self.reaction_timeRight = reset_pygame_timer()
                self.time_right = pygame.time.get_ticks()

            for _ in hit_list_left:
                if self.left_point.get_trap():
                    self.errores_izquierda += 1
                    self.puntuacion -= settings_0.FALLO_PTO
                    explosion = Animation(
                        self.game.display,
                        self.left_point.rect.centerx,
                        self.left_point.rect.centery,
                        settings.EXPLOSION,
                        settings_0.FPS_EXPLOSION,
                    )
                    self.explosiones.add(explosion)
                    self.explosion.play()
                    self.reaction_timeLeft_list_good.append((pygame.time.get_ticks() - self.reaction_timeLeft) / 1000)
                else:
                    self.aciertos_izquierda += 1
                    self.puntuacion += settings_0.ACIERTO_PTO
                    firework = Animation(
                        self.game.display,
                        self.left_point.rect.centerx,
                        self.left_point.rect.centery,
                        settings.FIREWORKS,
                        settings_0.FPS_FIREWORKS,
                    )
                    self.fireworks.add(firework)
                    self.press_star.play()
                    self.reaction_timeLeft_list_good.append((pygame.time.get_ticks() - self.reaction_timeLeft) / 1000)
                self.time_left = pygame.time.get_ticks()
                self.reaction_timeLeft = pygame.time.get_ticks()

            if len(self.points_left) > 0:
                kill = self.points_left.update()
                if kill:
                    self.reaction_timeLeft_list_bad.append(self.velocidad_bolas)
                    self.time_left = pygame.time.get_ticks()
                    self.reaction_timeLeft = pygame.time.get_ticks()

            if len(self.points_right) > 0:
                kill = self.points_right.update()
                if kill:
                    self.reaction_timeRight_list_bad.append(self.velocidad_bolas)
                    self.reaction_timeRight = reset_pygame_timer()
                    self.time_right = pygame.time.get_ticks()
            self.points_left.draw(self.game.display)
            self.points_right.draw(self.game.display)
            self.explosiones.draw(self.game.display)
            self.explosiones.update()
            self.fireworks.draw(self.game.display)
            self.fireworks.update()

        if self.current_time <= 0:
            self.end = True

        # Draw point on the screen
        self.hands.draw(self.game.display)
            

        if self.end:
            self.time_instr = 0
            self.music.stop()
            self.claps.play()
