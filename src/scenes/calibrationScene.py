import pygame
from scenes.scene import Scene
from ui.sticker import Sticker
import settings.settings as settings
from ui.gui import ImageButton
from ui.source import Source
from ui.gui import BackgroundText
from mediapipe.python.solutions import pose as mp_pose
from pose_tracking.tracker_utils import *
from math import sqrt
from scenes.timeDownScene import TimeDown

from scenes.activitiesScene import ActivitiesScene

class CalibrationScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "CalibrationScene"

        # Images
        self.body = Sticker(
            self.game.display,
            settings.BODY,
            settings.WIDTH*0.2,
            self.game.display.get_size()[1]-250,
            400,
            350,
        )
        self.boy = Sticker(
            self.game.display,
            settings.NIÑO,
            settings.WIDTH*0.11,
            250,
            200,
            160,
        )

        # Timer
        self.timedown_object = TimeDown(self.game)
        
        # Atras
        self.img_atras = pygame.image.load(settings.ATRAS)
        self.atras = ImageButton(self.img_atras, (50,70), "modificar", (70, 70))

        # Puntos de la cabeza
        self.cabeza = Source(self.game.display, settings.VERDE, (70,70))

        # Puntos de las manos
        self.izq_mano = Source(self.game.display, settings.VERDE, (70,70))
        self.drch_mano = Source(self.game.display, settings.VERDE, (70,70))

        # Puntos de los pies
        self.drch_pie = Source(self.game.display, settings.VERDE, (70,70))
        self.izq_pie = Source(self.game.display, settings.VERDE, (70,70))

        self.mostrar_instrucciones = True
        self.texto = BackgroundText(
            "Muestra todas las partes del cuerpo",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )

        # Tracking time
        self.timer = pygame.time.get_ticks()
        self.ticks = pygame.time.get_ticks()
        self.seconds = 0
        self.time_instr = 0

        # About calibration
        self.points = []
        self.checker = [False, False, False, False, False]
        self.current_results = None
        self.calibrated = False
        self.end = False
        self.countdowns = True

    def resized(self):
        self.body = Sticker(
            self.game.display,
            settings.BODY,
            settings.WIDTH*0.17,
            self.game.display.get_size()[1]-200,
            400,
            350,
        )
        self.boy = Sticker(
            self.game.display,
            settings.NIÑO,
            settings.WIDTH*0.11,
            250,
            200,
            160,
        )
        self.texto = BackgroundText("Muestra todas las partes del cuerpo",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )

    def events(self, ev):
        if self.end:
            self.end = False
            return ActivitiesScene(self.game)
        
        if self.atras.get_clicked_state() or self.atras.on_click(ev):
            self.game.static_points = None
            return ActivitiesScene(self.game)
        
        return None

    def update(self, dt):
        if self.calibrated and dt != 0:
            self.game.static_points = self.current_results
            self.end = True

        if self.time_instr < 3:
            self.mostrar_instrucciones = True
        else:
            self.mostrar_instrucciones = False

    def draw(self):
        self.atras.draw(self.game.display)
        
        if self.mostrar_instrucciones:
            self.texto.draw(self.game.display)
            self.boy.draw(self.game.display)
        else:
            self.body.draw(self.game.display)

        if not all(item is True for item in self.checker):
            self.texto.draw(self.game.display)
            self.boy.draw(self.game.display)

    def count_seconds(self):
        self.seconds = (
            pygame.time.get_ticks() - self.timer
        ) / 1000  # calculate how many seconds
        seconds_txt = settings.FONTS["extra"].render(
            "{0}".format(int(self.seconds)), True, settings.BLACK
        )
        self.game.display.blit(seconds_txt, (self.game.display.get_size()[0]/2-30, self.game.display.get_size()[1]*0.35))

        if self.seconds >= 3.2:
            self.calibrated = True

    def check_collide(self, left, right):
        if self.atras.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.atras.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Atras"

    def tracking(self, results):
        self.current_results = results
        
        left_hand, right_hand = get_points(results)
        self.izq_mano.rect.centerx = left_hand[0] * settings.WIDTH
        self.izq_mano.rect.centery = left_hand[1] * settings.HEIGHT
        self.drch_mano.rect.centerx = right_hand[0] * settings.WIDTH
        self.drch_mano.rect.centery = right_hand[1] * settings.HEIGHT

        head = get_head_points(results)
        self.cabeza.rect.centerx = head[0] * settings.WIDTH
        self.cabeza.rect.centery = head[1] * settings.HEIGHT
        
        left_feet, right_feet = get_feet_points(results)
        self.drch_pie.rect.centerx = left_feet[0] * settings.WIDTH
        self.drch_pie.rect.centery = left_feet[1] * settings.HEIGHT
        self.izq_pie.rect.centerx = right_feet[0] * settings.WIDTH
        self.izq_pie.rect.centery = right_feet[1] * settings.HEIGHT
        
        action = self.check_collide(self.izq_mano, self.drch_mano)
        if action == "Atras":
            self.timedown_object.tracking(results)
            self.timedown_object.draw()
            self.countdowns = self.timedown_object.events()
            if not self.countdowns:
                self.atras.set_clicked_true()
        else:
            self.timedown_object.restart()      

        if self.time_instr < 3:
            self.time_instr = count(self.ticks)
            self.timer = reset_pygame_timer()
            self.seconds = 0
        elif self.time_instr >= 3:
            try:
                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].visibility > 0.6:
                    self.cabeza.draw(self.game.display)
                    self.checker[0] = True
                else:
                    self.checker[0] = False
                # Manos
                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.6:
                    self.drch_mano.draw(self.game.display)
                    self.checker[1] = True
                else:
                    self.checker[1] = False

                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.6:
                    self.izq_mano.draw(self.game.display)
                    self.checker[2] = True
                else:
                    self.checker[2] = False

                # Pies
                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].visibility > 0.6:
                    self.drch_pie.draw(self.game.display)
                    self.checker[3] = True
                else:
                    self.checker[3] = False

                if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].visibility > 0.6:
                    self.izq_pie.draw(self.game.display)
                    self.checker[4] = True
                else:
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
                
                self.timer = reset_pygame_timer()
                self.seconds = 0
