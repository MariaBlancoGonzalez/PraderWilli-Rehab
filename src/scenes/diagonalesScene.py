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


class DiagonalsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "DiagonalsScene"
        self.right_feet = 0
        self.left_feet = 0

        # Music
        self.music = pygame.mixer.Sound(settings.MUSIC_DIAGONALES)
        # self.music_playing = False

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

        # Game settings
        self.trampas = settings.PORCENTAJE_TRAMPAS
        self.velocidad_bolas = settings.VELOCIDAD_ENTRE_BOLAS
        self.tiempo_juego = settings.TIEMPO_JUEGO

        self.aciertos_izquierda = 0
        self.aciertos_derecha = 0
        self.errores_izquierda = 0
        self.errores_derecha = 0

        # Score total and partial to show
        self.puntuacion = 0
        self.correct_score = settings.FONTS["medium"].render(
                str(settings.ACIERTO), True, settings.BLACK
                 )
        self.error_score = settings.FONTS["medium"].render(
                str(settings.FALLO), True, settings.BLACK
                 )
        # Text
        self.texto = BackgroundText(
            "Atrapa las estrellas con las manos",
            (120, 300),
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
        self.texto_pies = BackgroundText(
            "Coloca los pies en la casilla",
            (150, 300),
            settings.WHITE,
            settings.GRIS,
            30,
        )

        # Tracking time to show instruc.
        self.mostrar_instrucciones = True
        self.time_instr = 0
        self.ticks = 0

        # If calibration is done before start
        self.feet_right = (
            None
            if game.static_points == None
            else (
                self.game.static_points.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.LEFT_ANKLE
                ].x,
                self.game.static_points.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.LEFT_ANKLE
                ].y,
            )
        )
        self.feet_left = (
            None
            if game.static_points == None
            else (
                self.game.static_points.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.RIGHT_ANKLE
                ].x,
                self.game.static_points.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.RIGHT_ANKLE
                ].y,
            )
        )
        self.calibration = False if game.static_points == None else True
        self.box_feet = [] if game.static_points == None else self.create_box_feet()

        if game.static_points != None:
            self.music.play()
            self.music_playing = True
            left_hand_bound = create_diagonal_points_left(game.static_points)
            right_hand_bound = create_diagonal_points_right(game.static_points)
            top_margin = create_top_margin(game.static.points)
            self.shoulder_left, self.shoulder_right = get_shoulder_pos(
                game.static_points
            )
            self.margin = (top_margin[0], top_margin[1])
            self.bound_left_hand = (left_hand_bound[0], left_hand_bound[1])
            self.bound_right_hand = (right_hand_bound[0], right_hand_bound[1])

        else:
            self.bound_left_hand, self.bound_left_hand, self.margin = (0, 0), (0, 0), settings.MARGIN

        # Tracking time during game
        self.time_left = pygame.time.get_ticks()
        self.time_right = pygame.time.get_ticks()

        # In case calibration is not done
        self.calibration_object = CalibrationScene(self.game)

        # Some checkers and timer
        self.timer = 0
        self.current_results = None
        self.visibility_checker = True
        self.feet_checker = True
        self.current_time = self.tiempo_juego

        # Game complete
        self.end = False

    def events(self, events):
        if self.end:
            if self.game.connection == 0:
                self.introduced_data()
                return ActivitiesScene(self.game)
            else:
                self.write_data_json()
        return None

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
            pygame.draw.rect(self.game.display, settings.GRANATE, self.box_feet, 5, 0)

    def create_box_feet(self):
        point_left = escale_coor_pix(self.feet_left[0], self.feet_left[1])
        point_right = escale_coor_pix(self.feet_right[0], self.feet_right[1])
        width = distance_between_pixels(point_left, point_right)

        rect = pygame.Rect(
            point_left[0] - settings.FEET_MARGIN,
            point_left[1] - settings.FEET_MARGIN,
            width + settings.FEET_BOX,
            settings.FEET_BOX,
        )
        return rect

    def check_feet(self):
        left_current_foot, rigth_current_foot = get_feet_points(self.current_results)

        self.left_foot.rect.centerx = left_current_foot[0] * settings.WIDTH
        self.left_foot.rect.centery = left_current_foot[1] * settings.HEIGHT
        self.right_foot.rect.centerx = rigth_current_foot[0] * settings.WIDTH
        self.right_foot.rect.centery = rigth_current_foot[1] * settings.HEIGHT

        if self.left_foot.rect.colliderect(
            self.box_feet
        ) and self.right_foot.rect.colliderect(self.box_feet):
            self.feet_checker = True
        else:
            self.feet_checker = False

    def tracking(self, results):
        self.current_results = results
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
                self.feet_right = (
                    self.game.static_points.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_ANKLE
                    ].x,
                    self.game.static_points.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_ANKLE
                    ].y,
                )
                self.feet_left = (
                    self.game.static_points.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.RIGHT_ANKLE
                    ].x,
                    self.game.static_points.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.RIGHT_ANKLE
                    ].y,
                )
                self.box_feet = self.create_box_feet()

                left_hand_bound = create_diagonal_points_left(results)
                right_hand_bound = create_diagonal_points_right(results)
                top_margin = create_top_margin(results)
                self.shoulder_left, self.shoulder_right = get_shoulder_pos(results)
                self.margin = (top_margin[0], top_margin[1])
                self.bound_left_hand = (left_hand_bound[0], left_hand_bound[1])
                self.bound_right_hand = (right_hand_bound[0], right_hand_bound[1])
                self.music.play()
                print(self.margin)
                # self.music_playing = True
        # Pantalla de 3,2,1...
        if self.time_instr < 3 and self.calibration and not self.end:
            self.time_instr = count(self.ticks)
            self.seconds = 0
            self.time_right = reset_pygame_timer()
            self.time_left = reset_pygame_timer()
            self.timer = reset_pygame_timer()

        elif (
            self.time_instr >= 3
            and self.calibration
            and not self.feet_checker
            and not self.end
        ):
            # Cuando los pies no estan la posicion calibrada o falta algún punto en la pantalla
            # Para checkeo de pies
            self.check_feet()
        elif (
            self.time_instr >= 3
            and self.calibration
            and not self.visibility_checker
            and not self.end
        ):
            # Para checkeo de pies
            self.visibility = check_visibility(self.current_results)
        elif (
            self.time_instr >= 3
            and self.calibration
            and self.feet_checker
            and self.visibility_checker
            and not self.end
        ):
            # Cuando esta todo ok
            # Se usa la izquierda en la derecha y viceversa pq se invierte la imagen
            # Para checkeo de pies
            self.check_feet()
            self.visibility = check_visibility(self.current_results)
            self.mostrar_instrucciones = False
            left_tramp = random.random() < self.trampas
            right_tramp = random.random() < self.trampas

            # Si puedo poner bolas
            bola_permitida_drch = (
                True
                if (pygame.time.get_ticks() - self.time_right) / 1000
                >= settings.VELOCIDAD_ENTRE_BOLAS
                else False
            )
            bola_permitida_izq = (
                True
                if (pygame.time.get_ticks() - self.time_left) / 1000
                >= settings.VELOCIDAD_ENTRE_BOLAS
                else False
            )
            # Crear acierto y fallo
            if len(self.points_left) == 0 and not left_tramp and bola_permitida_izq:
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

            # Get the point in the hand
            left_hand, right_hand = get_points(results)

            # For each hand
            self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
            self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
            self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
            self.right_source.rect.centery = right_hand[1] * settings.HEIGHT

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
                    self.puntuacion -= settings.FALLO
                    explosion = Animation(
                        self.game.display,
                        self.right_point.rect.centerx,
                        self.right_point.rect.centery,
                        settings.EXPLOSION,
                        settings.FPS_EXPLOSION,
                    )
                    self.explosiones.add(explosion)
                    self.explosion.play()
                    self.game.display.blit(self.error_score, (self.right_source.rect.centerx, self.right_source.rect.centery))
                else:
                    self.aciertos_derecha += 1
                    self.puntuacion += settings.ACIERTO
                    firework = Animation(
                        self.game.display,
                        self.right_point.rect.centerx,
                        self.right_point.rect.centery,
                        settings.FIREWORKS,
                        settings.FPS_FIREWORKS,
                    )
                    self.fireworks.add(firework)
                    self.press_star.play()
                    self.game.display.blit(self.correct_score, (self.right_source.rect.centerx, self.right_source.rect.centery))
                self.time_right = pygame.time.get_ticks()

            for _ in hit_list_left:
                if self.left_point.get_trap():
                    self.errores_izquierda += 1
                    self.puntuacion -= settings.FALLO
                    explosion = Animation(
                        self.game.display,
                        self.left_point.rect.centerx,
                        self.left_point.rect.centery,
                        settings.EXPLOSION,
                        settings.FPS_EXPLOSION,
                    )
                    self.explosiones.add(explosion)
                    self.explosion.play()
                    
                    self.game.display.blit(self.error_score, (self.left_source.rect.centerx, self.left_source.rect.centery))
                else:
                    self.aciertos_izquierda += 1
                    self.puntuacion += settings.ACIERTO
                    firework = Animation(
                        self.game.display,
                        self.left_point.rect.centerx,
                        self.left_point.rect.centery,
                        settings.FIREWORKS,
                        settings.FPS_FIREWORKS,
                    )
                    self.fireworks.add(firework)
                    self.press_star.play()
                    self.game.display.blit(self.correct_score, (self.left_source.rect.centerx, self.left_source.rect.centery))
                self.time_left = pygame.time.get_ticks()

            if len(self.points_left) > 0:
                self.points_left.update()

            if len(self.points_right) > 0:
                self.points_right.update()

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
                        self.aciertos_izquierda + self.aciertos_derecha
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

            # Draw point on the screen
            self.hands.draw(self.game.display)
            self.points_left.draw(self.game.display)
            self.points_right.draw(self.game.display)
            self.explosiones.draw(self.game.display)
            self.explosiones.update()
            self.fireworks.draw(self.game.display)
            self.fireworks.update()

        if self.end:
            self.music.stop()
            self.claps.play()

    def introduced_data(self):
        broker = Broker()
        broker.connect()
        today = datetime.date.today()
        today = today.strftime("%Y-%m-%d")
        id = get_id(self.game.current_user)
        broker.add_score(
            id,
            settings.ID_DIAGONALES,
            today,
            settings.TIEMPO_JUEGO,
            self.errores_izquierda,
            self.aciertos_izquierda,
            self.errores_derecha,
            self.aciertos_derecha,
        )
        broker.close()

    def write_data_json(self):
        today = datetime.date.today()
        today = today.strftime("%Y-%m-%d")
        new_data = {
            "PT_id":1, "PT_A_id": id, "PT_E_id": settings.ID_DIAGONALES, "PT_fecha":today, "PT_tiempo": settings.TIEMPO_JUEGO,
            "PT_fallos_izquierda": self.errores_izquierda,
            "PT_aciertos_izquierda": self.aciertos_izquierda,
            "PT_fallos_derecha": self.errores_derecha,
            "PT_aciertos_derecha": self.aciertos_derecha
        }

        with open('default.json', 'r') as f:
            data = json.load(f)

        data['puntuaciones'].append(new_data)

        with open('default.json', 'w') as f:
            json.dump(data, f)

