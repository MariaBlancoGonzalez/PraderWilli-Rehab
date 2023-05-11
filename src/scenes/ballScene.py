from scenes.scene import Scene
import pygame
import json

import settings
from ui.source import Source
from ui.sticker import Sticker
from pygame.sprite import Group
from ui.gui import BackgroundText
from broker import Broker
from pose_tracking.tracker_utils import *
import datetime
from ui.animation import Animation
import random
from utils import *
from scenes.activitiesScene import ActivitiesScene
from scenes.calibrationScene import CalibrationScene


class BallScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "ballScene"

        # Music
        self.music = pygame.mixer.Sound(settings.MUSIC_DIAGONALES)
        # self.music_playing = False

        # Sounds
        self.pip_sound = pygame.mixer.Sound(settings.PIP)

        # Sources
        self.hand_right = Source(game.display, settings.PUNTERO_ROJO, (50, 50))
        self.hand_left = Source(game.display, settings.PUNTERO_ROJO, (50, 50))
        self.hands = Group([self.right_source, self.left_source])

        # Game settings
        self.velocidad_squad = settings.VELOCIDAD_BALL
        self.tiempo_juego = settings.TIEMPO_JUEGO_BALL

        self.aciertos = 0
        self.errores = 0

        # Score total and partial to show
        self.puntuacion = 0

        self.correct_ball = False
        self.correct_score = settings.FONTS["medium"].render(
            str(settings.ACIERTO), True, settings.BLACK
        )
        self.error_score = settings.FONTS["medium"].render(
            str(settings.FALLO), True, settings.BLACK
        )
        # Text
        self.texto = BackgroundText(
            "Tira la pelota hacia arriba",
            (350, 150),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        self.texto_partes = BackgroundText(
            "Muestra todas las partes del cuerpo",
            (120, 300),
            settings.WHITE,
            settings.GRIS,
            30,
        )

        # Tracking time to show instruc.
        self.mostrar_instrucciones = True
        self.time_instr = 0
        self.ticks = 0

        self.calibration = False if game.static_points == None else True

        if game.static_points != None:
            self.music.play()
            self.music_playing = True

        # Tracking time during game
        self.time_squad = pygame.time.get_ticks()
        self.pitido = True

        self.draw_part = ''
        # In case calibration is not done
        self.calibration_object = CalibrationScene(self.game)

        # Some checkers and timer
        self.timer = 0
        self.current_results = None
        self.visibility_checker = True
        self.current_time = self.tiempo_juego

        # Game complete
        self.end = False
        self.data_introduced = False

        # Animation
        self.ball_gif = Animation(
            self.game.display,
            600,
            500,
            settings.BALLGIF,
            settings.FPS_BALL, (400, 500)
        )
        self.squadgif_animation = Group(self.squad_gif)

    def events(self, events):
        if self.end:
            if self.game.connection == 0:
                # self.introduced_data()
                return ActivitiesScene(self.game)
            else:
                # self.game.json_object.write_data_json(
                #    self.errores_izquierda, self.aciertos_derecha, self.errores_derecha, self.aciertos_derecha)
                return ActivitiesScene(self.game)

        return None

    def update(self, dt):
        pass

    def draw(self):
        if self.mostrar_instrucciones and self.calibration:
            self.texto.draw(self.game.display)
        elif self.time_instr >= 3 and self.calibration and not self.visibility_checker:
            self.texto_partes.draw(self.game.display)
        angle = settings.FONTS["medium"].render(
            "{0}º".format(
                int(self.angle)
            ),
            True,
            settings.BLACK)
        self.hands.draw(self.game.display)

    def tracking(self, results):
        self.current_results = results
        self.visibility_checker = check_visibility(self.current_results)
        if self.current_results == None:
            return None

        # Get initial points
        if not self.calibration:
            self.calibration_object.tracking(results)
            self.calibration_object.update(0)
            self.calibration_object.draw()
            self.calibration = self.calibration_object.calibrated
            self.ticks = pygame.time.get_ticks()
            if self.calibration:
                self.music.play()
                self.draw_part = get_part_forward(results)
        # Pantalla de 3,2,1...
        if self.time_instr < 3 and self.calibration and not self.end:
            self.time_instr = count(self.ticks)
            self.seconds = 0
            self.time_squad = reset_pygame_timer()
            self.timer = reset_pygame_timer()
            self.squadgif_animation.draw(self.game.display)
            self.squadgif_animation.update()

        elif (
            self.time_instr >= 3
            and self.calibration
            and not self.visibility_checker
            and not self.end
        ):
            # Para checkeo de pies
            pass
        elif (
            self.time_instr >= 3
            and self.calibration
            and self.visibility_checker
            and not self.end
        ):
            # Cuando esta todo ok
            # Se usa la izquierda en la derecha y viceversa pq se invierte la imagen
            # Para checkeo de pies
            self.visibility_checker = check_visibility(self.current_results)
            self.mostrar_instrucciones = False

            if self.pitido:
                self.pip_sound.play()
                self.pitido = False

            # Get the point in the hand
            left_hand, right_hand = get_points(results)

            # For each hand
            self.hand_left.rect.centerx = left_hand[0] * settings.WIDTH
            self.hand_left.rect.centery = left_hand[1] * settings.HEIGHT
            self.hand_right.rect.centerx = right_hand[0] * settings.WIDTH
            self.hand_right.rect.centery = right_hand[1] * settings.HEIGHT

            # TODO
            # COLLIDE PELOTA CON MANOS
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)

                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)


            if self.current_time <= 0:
                game_over_text = settings.FONTS["big"].render(
                    "Bien hecho", True, settings.BLACK
                )
                self.game.display.blit(
                    game_over_text,
                    game_over_text.get_rect(
                        center=(settings.WIDTH // 2, settings.HEIGHT // 2)
                    ),
                )

                mistakes_txt = settings.FONTS["medium"].render(
                    "Aciertos: {0}".format(
                        self.aciertos
                    ),
                    True,
                    settings.BLACK,
                )
                self.game.display.blit(mistakes_txt, (15, 15))

                self.end = True

            new_time = (pygame.time.get_ticks() - self.timer) / 1000

            self.current_time = self.tiempo_juego - int(new_time)

            min = int(self.current_time / 60)
            sec = int(self.current_time % 60)
            time_txt = settings.FONTS["medium"].render(
                "Tiempo: {0}".format(get_str_time(min, sec)),
                True,
                settings.BLACK,
            )
            self.game.display.blit(time_txt, (15, 15))

            puntuacion = settings.FONTS["medium"].render(
                "Puntuacion: ", True, settings.BLACK
            )
            self.game.display.blit(puntuacion, (900, 15))

            puntos = settings.FONTS["medium"].render(
                "{0}".format(self.puntuacion), True, settings.COLOR_ROJO
            )
            self.game.display.blit(puntos, (1065, 15))
            if (pygame.time.get_ticks() - self.time_squad) / 1000 >= self.velocidad_squad:
                self.pitido = True
                if not self.correct_squad:
                    self.errores += 1
                    self.puntuacion -= 50
                    print("Errores", self.errores)
                else:
                    self.correct_squad = False
                self.time_squad = reset_pygame_timer()

        if self.end:
            self.music.stop()