import pygame
from pygame.sprite import Group
import statistics
import random

import settings.settings as settings
import settings.settings_1 as settings_1

from ui.source import Source
from ui.sticker import Sticker
from ui.gui import BackgroundText
from ui.animation import Animation

from broker import DataBroker
from tracking.tracker_utils import *
from utils import *

from scenes.auxiliaryScenes.timeDownScene import TimeDown
from scenes.exergames.game import Exergame
from scenes.activitiesScene import ActivitiesScene
from scenes.auxiliaryScenes.calibrationScene import CalibrationScene

class SquadScene(Exergame):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "SquadScene"
        
        # Sounds
        self.pip_sound = pygame.mixer.Sound(settings.PIP)
        self.pip_sound.set_volume(1)
        self.error_sound = pygame.mixer.Sound(settings.ERROR_SOUND)
        self.error_sound.set_volume(1)
        self.claps = pygame.mixer.Sound(settings.CLAPS)
        self.claps.set_volume(1)

        # Sources
        self.right_feet = Source(game.display, settings.BOLA_VERDE, (50,50))
        self.left_feet = Source(game.display, settings.BOLA_VERDE, (50, 50))
        self.right_knee = Source(game.display, settings.BOLA_VERDE, (50, 50))
        self.left_knee = Source(game.display, settings.BOLA_VERDE, (50, 50))
        self.left_hip = Source(game.display, settings.BOLA_VERDE, (50, 50))
        self.right_hip = Source(game.display, settings.BOLA_VERDE, (50, 50))

        # Game settings
        self.velocidad_squad = read(settings_1.EXER_1_CONFIG, "VELOCIDAD_SQUAD") 
        self.tiempo_juego = read(settings_1.EXER_1_CONFIG, "TIEMPO_JUEGO_SQUAD")

        self.aciertos = 0
        self.errores = 0
        self.media_angulo = []

        # Score total and partial to show
        self.angle = 0
        self.best_angle = 200
        self.correct_squad = False
        self.animation = Group()

        # Text
        self.txt_instr = BackgroundText(
            "Realiza sentadillas",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )


        # Tracking time during game
        self.time_squad = pygame.time.get_ticks()
        self.pitido = True

        # Animation
        self.init_gif = Animation(
            self.game.display,
            self.game.display.get_size()[0]*0.5,
            self.game.display.get_size()[1]-250,
            settings.SQUADGIF,
            settings_1.FPS_SQUAD, (400,500)
        )
        self.init_animation = Group(self.init_gif)
        self.min_angulo = 200

        self.coefficient = 500 / self.tiempo_juego
    
    def resized(self):
        # Text
        self.txt_instr = BackgroundText(
            "Realiza sentadillas",
            (self.game.display.get_size()[0]*0.11, 70),
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

    def events(self, events):
        if self.end:
            json_object = DataBroker()
            json_object.write_data_json(settings_1.EXER_1_JSON, settings_1.ID_SQUAD, self.tiempo_juego,
                                            self.errores, self.aciertos, round(statistics.mean(self.media_angulo), 2))
            return ActivitiesScene(self.game)
        if self.atras.get_clicked_state() or self.atras.on_click(events):
            self.music.stop()
            return ActivitiesScene(self.game)

        return None

    def render(self):
        if self.time_instr >= 3 and self.calibration and not self.visibility_checker:
            self.txt_visibility.draw(self.game.display)
        
        try:
            angle = settings.FONTS["medium"].render(
            "{0}º".format(
                int(self.angle)
            ),
            True,
            settings.BLACK)
        except:
            angle = settings.FONTS["medium"].render(
            "{0}º".format(
                200
            ),
            True,
            settings.BLACK)

        self.right_feet.draw(self.game.display)
        self.right_knee.draw(self.game.display)
        self.right_hip.draw(self.game.display)

        pygame.draw.lines(
                self.game.display, settings.COLOR_VERDE, True, [(self.right_hip.rect.centerx, self.right_hip.rect.centery), (self.right_knee.rect.centerx, self.right_knee.rect.centery), (self.right_feet.rect.centerx, self.right_feet.rect.centery)], 5)
        self.game.display.blit(angle, (self.right_knee.rect.centerx-50, self.right_knee.rect.centery))

        self.atras.draw(self.game.display)

    def calibration_success(self):
        self.time_squad = reset_pygame_timer()


    def logic(self):
        self.visibility_checker = check_visibility_squad(self.pose_tracker.landmark_process)
        if self.pitido:
            best_angle = 200
            self.pip_sound.play()
            self.pitido = False

        # Coger puntos pies
        left_current_foot, rigth_current_foot = get_feet_points(self.pose_tracker.landmark_process)
        self.left_feet.update_position(left_current_foot)
        self.right_feet.update_position(rigth_current_foot)

        # Coger puntos rodillas
        _, right_knee = get_knees_points(self.pose_tracker.landmark_process)
            
        self.right_knee.update_position(right_knee)

        # Coger caderas
        _, right_current_hip = get_hips_points(self.pose_tracker.landmark_process)

        self.right_hip.update_position(right_current_hip)

        self.angle = angle_calculate_by_points(right_current_hip, right_knee, rigth_current_foot)
            
        if self.angle <= 100.0:
            if self.best_angle > self.angle:
                self.best_angle = self.angle

            if (pygame.time.get_ticks() - self.time_squad) / 1000 < self.velocidad_squad and not self.correct_squad:
                self.aciertos += 1
                self.puntuacion += settings_1.ACIERTO_PTO
                self.correct_squad = True
                animation_right = Animation(
                    self.game.display,
                    self.right_feet.rect.centerx +50,
                    self.right_feet.rect.centery,
                    settings.GROUNDUP,
                    settings_1.FPS_ANIMATION, (300,300)
                )
                animation_left = Animation(
                    self.game.display,
                    self.left_feet.rect.centerx -50,
                    self.left_feet.rect.centery,
                    settings.GROUNDUP,
                    settings_1.FPS_ANIMATION, (300,300)
                )
                self.animation.add(animation_right)
                self.animation.add(animation_left)

        if (pygame.time.get_ticks() - self.time_squad) / 1000 >= self.velocidad_squad:
            if not self.correct_squad:
                self.errores += 1
                self.error_sound.play()
                
            self.correct_squad = False
            self.pitido = True
            self.time_squad = reset_pygame_timer()
            self.media_angulo.append(self.best_angle)
            self.best_angle = 200
                
        if self.current_time <= 0:
            self.end = True
            self.music.stop()
            self.claps.play()
        
        self.animation.draw(self.game.display)
        self.animation.update()

