from scenes.scene import Scene
import pygame
import json
import cv2
import settings
import numpy as np
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
from ui.circle_point import Circle

class BallScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "BallScene"

        # Music
        song = random.randint(0, 5)
        self.music = pygame.mixer.Sound(settings.MUSIC[song])
        self.music.set_volume(0.5)
        # self.music_playing = False

        # Sounds
        self.pip_sound = pygame.mixer.Sound(settings.PIP)
        self.pip_sound.set_volume(1)

        # Sources
        self.hand_right = Source(game.display, settings.PUNTERO_ROJO, (50, 50))
        self.hand_left = Source(game.display, settings.PUNTERO_ROJO, (50, 50))
        
        self.hands = Group([self.hand_right, self.hand_left])
        self.line = Sticker(game.display, settings.LINEA_HORIZONTAL, settings.WIDTH//2, 50,800,50)

        # Game settings
        self.tiempo_juego = settings.TIEMPO_JUEGO_BALL

        self.aciertos = 0
        self.errores = 0

        # Score total and partial to show
        self.puntuacion = 0

        self.correct_ball = False
        self.correct_score = settings.FONTS["medium"].render(
            str(settings.ACIERTO_PTO), True, settings.BLACK
        )
        self.error_score = settings.FONTS["medium"].render(
            str(settings.FALLO_PTO), True, settings.BLACK
        )
        # Text
        self.texto = BackgroundText(
            "Tira la pelota hacia arriba",
            (330, 150),
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
        self.time_instr_balls = 0
        self.ticks = 0

        self.calibration = False if game.static_points == None else True
        # In case calibration is not done
        self.calibration_object = CalibrationScene(self.game)

        if game.static_points != None:
            self.music.play()
            self.music.set_volume(0.6)
            self.music_playing = True

        # Tracking time during game
        self.velocidad_balls = settings.VELOCIDAD_BALL
        self.time_balls = pygame.time.get_ticks()
        self.pitido = True
        self.correct = False
        self.wrong = False

        # Some checkers and timer
        self.timer = 0
        self.current_results = None
        self.visibility_checker = True
        self.current_time = self.tiempo_juego

        # Game complete
        self.end = False
        self.data_introduced = False

        # Camera from the main
        self.image_camera = None

        # Ball color
        self.ballColorUpper = np.array(settings.BALL_COLOR_UPPER)
        self.ballColorLower = np.array(settings.BALL_COLOR_LOWER)
        # Animation
        self.ball_gif = Animation(
            self.game.display,
            620,
            500,
            settings.BALLGIF,
            settings.FPS_BALL, (500, 500)
        )
        self.ballgif_animation = Group(self.ball_gif)

        # Para la pelota
        self.circle_ball = Circle(0,0,0)
        self.hit = 0
        self.state = [0,0,0] # Up, on hands, down

    def events(self, events):
        if self.end:
            if self.game.connection == 0:
                self.introduced_data()
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
        elif self.time_instr_balls >= 3 and self.calibration and not self.visibility_checker:
            self.texto_partes.draw(self.game.display)
        
        self.hands.draw(self.game.display)
        

    def update_camera_utilities(self, image):
        self.image_camera = image

    def tracking(self, results):
        self.current_results = results
        self.visibility_checker = check_visibility_balls(self.current_results)
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
        elif self.calibration and self.time_instr_balls <= 0 and not self.end:
            self.ticks = pygame.time.get_ticks()
        # Pantalla de 3,2,1...
        
        if self.time_instr_balls < 3 and self.calibration and not self.end:
            self.time_instr_balls = count(self.ticks)
            self.seconds = 0
            self.time_balls = reset_pygame_timer()
            self.timer = reset_pygame_timer()
            self.ballgif_animation.draw(self.game.display)
            self.ballgif_animation.update()

        elif (
            self.time_instr_balls >= 3
            and self.calibration
            and not self.visibility_checker
            and not self.end
        ):
            # Para checkeo de pies
            pass
        elif (
            self.time_instr_balls >= 3
            and self.calibration
            and self.visibility_checker
            and not self.end
        ):
            # Cuando esta todo ok
            # Se usa la izquierda en la derecha y viceversa pq se invierte la imagen
            # Para checkeo de pies
            self.visibility_checker = check_visibility_balls(self.current_results)
            self.mostrar_instrucciones = False

            if self.pitido:
                self.pip_sound.play() 
                self.pitido = False

            # Get the point in the hand
            left_hand, right_hand = get_points(results)
            left_knee, right_knee = get_hips_points(results)
            # For each hand
            self.hand_left.rect.centerx = left_hand[0] * settings.WIDTH
            self.hand_left.rect.centery = left_hand[1] * settings.HEIGHT
            self.hand_right.rect.centerx = right_hand[0] * settings.WIDTH
            self.hand_right.rect.centery = right_hand[1] * settings.HEIGHT
           
            hsv = cv2.cvtColor(self.image_camera, cv2.COLOR_RGB2HSV)

            mask = cv2.inRange(hsv, self.ballColorLower, self.ballColorUpper)
            mask = cv2.erode(mask, None, iterations=1)
            mask = cv2.dilate(mask, None, iterations=1)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)

                if radius > 25:
                    self.circle_ball = Circle(x, y, radius)
            
            if self.wrong is not True:
                hit_list = pygame.sprite.groupcollide(
                    self.hands, Group(self.circle_ball), False, True)
                # Check the list of colliding sprites, and add one to the score for each one.
                for _ in hit_list:
                    # estado incial pelota en mano
                    if self.state[1] == 0:
                        self.state[1] = 1
                    # cuando ha pasado del estado inicial y ha subido
                    if self.state[0] == 1 and self.state[1] == 1 and self.state[2] != 1:
                        self.state[2] = 1

                if self.state[1] == 1 and self.state[0] != 1:
                    hit_list_ball_down = pygame.sprite.groupcollide(
                        Group(self.circle_ball), Group(self.line), False, True)
                    for _ in hit_list_ball_down:
                        # cuando da la bola en la linea
                        if self.state[0] == 0:
                            self.state[0] = 1

            if self.circle_ball.rect.y > 0 and left_knee[1]*settings.HEIGHT < self.circle_ball.rect.y and right_knee[1]*settings.HEIGHT < self.circle_ball.rect.y and (pygame.time.get_ticks() - self.time_balls) / 1000 < self.velocidad_balls and self.correct == False and self.wrong == False:
                self.errores += 1
                self.puntuacion -= settings.FALLO_PTO
                self.wrong = True
            elif all(element == 1 for element in self.state) and (pygame.time.get_ticks() - self.time_balls) / 1000 < self.velocidad_balls and self.correct == False and self.wrong == False:
                self.aciertos += 1
                self.puntuacion += settings.ACIERTO_PTO
                self.correct = True
            if (pygame.time.get_ticks() - self.time_balls) / 1000 >= self.velocidad_balls:
                if self.correct == False and self.wrong == False:
                    self.errores += 1
                    self.puntuacion -= settings.FALLO_PTO
                self.correct = False
                self.wrong = False
                self.state = [0,0,0]
                self.time_balls = reset_pygame_timer()
                self.pitido = True

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
            self.line.draw(self.game.display)

        if self.end:
            self.music.stop()

    def introduced_data(self):
        broker = Broker()
        broker.connect()
        today = datetime.date.today()
        today = today.strftime("%Y-%m-%d")
        id = get_id(self.game.current_user)
        broker.add_score(
            id,
            settings.ID_BALLS,
            today,
            settings.TIEMPO_JUEGO_BALL,
            self.errores,
            self.aciertos,
            0,
            0,
        )
        broker.close()
