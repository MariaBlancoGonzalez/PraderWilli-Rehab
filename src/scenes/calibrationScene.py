import pygame
from scenes.scene import Scene
from ui.sticker import Sticker
import settings
from ui.gui import BackgroundText
from mediapipe.python.solutions import pose as mp_pose
from pose_tracking.tracker_utils import *
from math import sqrt

from scenes.activitiesScene import ActivitiesScene


class CalibrationScene(Scene):
    def __init__(self, options):
        super().__init__(options)
        self._name_scene = "CalibrationScene"
        self.screen = options.display

        # Images
        self.body = Sticker(
            self.screen,
            settings.BODY,
            settings.WIDTH / 2,
            settings.HEIGHT / 2,
            1000,
            760,
        )

        # Puntos de la cabeza
        self.verde_cabeza = Sticker(self.screen, settings.VERDE, 640, 80, 60, 60)
        self.rojo_cabeza = Sticker(self.screen, settings.ROJO, 640, 80, 60, 60)

        # Puntos de las manos
        self.verde_izq_mano = Sticker(self.screen, settings.VERDE, 870, 400, 60, 60)
        self.rojo_izq_mano = Sticker(self.screen, settings.ROJO, 870, 400, 60, 60)

        self.verde_drch_mano = Sticker(self.screen, settings.VERDE, 410, 400, 60, 60)
        self.rojo_drch_mano = Sticker(self.screen, settings.ROJO, 410, 400, 60, 60)

        # Puntos de los pies
        self.verde_drch_pie = Sticker(self.screen, settings.VERDE, 600, 700, 60, 60)
        self.rojo_drch_pie = Sticker(self.screen, settings.ROJO, 600, 700, 60, 60)

        self.verde_izq_pie = Sticker(self.screen, settings.VERDE, 680, 700, 60, 60)
        self.rojo_izq_pie = Sticker(self.screen, settings.ROJO, 680, 700, 60, 60)

        # Text
        self.instructions = settings.FONTS["medium"].render(
            "Haz visibles los siguientes puntos en la pantalla", True, settings.BLACK
        )
        self.mostrar_instrucciones = True
        self.texto = BackgroundText(
            "Haz visibles los puntos en la pantalla",
            (100, 300),
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

    def events(self, ev):
        if self.end:
            self.end = False
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
        if self.mostrar_instrucciones:
            self.texto.draw(self.screen)

    def count_seconds(self):
        self.seconds = (
            pygame.time.get_ticks() - self.timer
        ) / 1000  # calculate how many seconds
        seconds_txt = settings.FONTS["extra"].render(
            "{0}".format(int(self.seconds)), True, settings.BLACK
        )
        self.screen.blit(seconds_txt, (settings.WIDTH / 2, settings.HEIGHT / 2))

        pygame.display.flip()
        if self.seconds >= 3.2:
            self.calibrated = True

    def calculate_distances(self, results):
        def distance_calculator(a, b):
            return sqrt(
                (
                    (
                        results.pose_landmarks.landmark[b].x
                        - results.pose_landmarks.landmark[a].x
                    )
                    ** 2
                )
                + (
                    (
                        results.pose_landmarks.landmark[b].y
                        - results.pose_landmarks.landmark[a].y
                    )
                    ** 2
                )
                + (
                    (
                        results.pose_landmarks.landmark[b].z
                        - results.pose_landmarks.landmark[a].z
                    )
                    ** 2
                )
            )

        distance_ab_right = distance_calculator(12, 14)
        distance_bc_right = distance_calculator(14, 16)
        distance_right_total = distance_ab_right + distance_bc_right

        distance_ab_left = distance_calculator(11, 13)
        distance_bc_left = distance_calculator(13, 15)
        distance_left_total = distance_ab_left + distance_bc_left

        return distance_right_total, distance_left_total

    def calculate_final_point(self, results, right, left):
        final_right = (
            results.pose_landmarks.landmark[12].x + right,
            results.pose_landmarks.landmark[12].y,
        )
        final_left = (
            results.pose_landmarks.landmark[11].x + right,
            results.pose_landmarks.landmark[11].y,
        )
        return final_right, final_left

    def tracking(self, results):
        self.current_results = results
        if self.time_instr < 3:
            self.time_instr = count(self.ticks)
            self.timer = reset_pygame_timer()
            self.seconds = 0
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
                self.timer = reset_pygame_timer()
                self.seconds = 0
                self.screen.blit(
                    self.instructions,
                    self.instructions.get_rect(center=(settings.WIDTH / 2, 750)),
                )
                pygame.display.flip()
