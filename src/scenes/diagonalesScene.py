from scenes.scene import Scene
import pygame

import settings.settings as settings
import settings.settings_0 as settings_0
from ui.source import Source
from ui.sticker import Sticker
from pygame.sprite import Group
from ui.gui import BackgroundText

from broker import DataBroker
from pose_tracking.tracker_utils import *
import datetime
from ui.animation import Animation
import random
from utils import *
from scenes.activitiesScene import ActivitiesScene
from scenes.calibrationScene import CalibrationScene
from scenes.timeDownScene import TimeDown
from ui.gui import ImageButton

class DiagonalsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "DiagonalsScene"

        self.boy = Sticker(
            self.game.display,
            settings.NIÑO,
            settings.WIDTH*0.11,
            250,
            200,
            160,
        )

        self.right_feet = 0
        self.left_feet = 0

        # Music
        self.pip_sound = pygame.mixer.Sound(settings.PIP)
        self.pip_sound.set_volume(1)
        song = random.randint(0, 5)
        self.music = pygame.mixer.Sound(settings.MUSIC[song])
        self.music.set_volume(0.5)
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

        # Animation
        self.diag_gif = Animation(
            self.game.display,
            self.game.display.get_size()[0]*0.45,
            self.game.display.get_size()[1]*0.7,
            settings.DIAGGIF,
            settings_0.FPS_DIAG, (500, 500)
        )
        self.diaggif_animation = Group(self.diag_gif)
        # Game settings
        self.trampas = read(settings_0.EXER_0_CONFIG, "PORCENTAJE_TRAMPAS")
        self.velocidad_bolas = read(settings_0.EXER_0_CONFIG, "VELOCIDAD_ENTRE_BOLAS")
        self.tiempo_juego = read(settings_0.EXER_0_CONFIG, "TIEMPO_JUEGO")

        self.aciertos_izquierda = 0
        self.aciertos_derecha = 0
        self.errores_izquierda = 0
        self.errores_derecha = 0

        # Score total and partial to show
        self.puntuacion = 0

        # Text
        self.texto = BackgroundText(
            "Atrapa las estrellas con las manos",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        self.texto_partes = BackgroundText(
            "Muestra todas las partes del cuerpo",
            (self.game.display.get_size()[0]*0.11, self.game.display.get_size()[1]*0.45),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        self.texto_pies = BackgroundText(
            "Coloca los pies en la casilla",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )

        # Tracking time to show instruc.
        self.mostrar_instrucciones = True
        self.time_instr = 0
        self.ticks = pygame.time.get_ticks()

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
        self.timedown_object = TimeDown(self.game)
        self.calibration = False if game.static_points == None else True
        self.box_feet = [] if game.static_points == None else self.create_box_feet()

        if game.static_points != None:
            self.music.play()
            self.music_playing = True
            left_hand_bound = create_diagonal_points_left(game.static_points, self.game.display.get_size())
            right_hand_bound = create_diagonal_points_right(game.static_points, self.game.display.get_size())
            top_margin = create_top_margin(game.static_points, self.game.display.get_size())
            self.shoulder_left, self.shoulder_right = get_shoulder_pos(
                game.static_points, self.game.display.get_size()
            )
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
        # In case calibration is not done
        self.calibration_object = CalibrationScene(self.game)

        # Some checkers and timer
        self.timer = pygame.time.get_ticks()
        self.current_results = None
        self.visibility_checker = True
        self.feet_checker = True
        self.current_time = self.tiempo_juego

        self.countdowns = True
        self.pitido = True
        # Game complete
        self.end = False
        self.data_introduced = False

        # Time bar
        self.bar_rect = pygame.Rect(
            200, 25, 500, 10)
        self.width = 0
        self.coefficient = 500 / self.tiempo_juego

        # Go back
        self.img_atras = pygame.image.load(settings.ATRAS)
        self.atras = ImageButton(self.img_atras, (50,70), "modificar", (70, 70))
        self.countback = True
        self.timedown_back = TimeDown(self.game)

    def resized(self):
        # Text
        self.texto = BackgroundText(
            "Atrapa las estrellas con las manos",
            (self.game.display.get_size()[0]*0.11,
            70),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        self.texto_partes = BackgroundText(
            "Muestra todas las partes del cuerpo",
            (self.game.display.get_size()[0]*0.11, self.game.display.get_size()[1]*0.45),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        self.texto_pies = BackgroundText(
            "Coloca los pies en la casilla",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )
        self.boy = Sticker(
            self.game.display,
            settings.NIÑO,
            settings.WIDTH*0.11,
            250,
            200,
            160,
        )

    def events(self, events):
        if self.end:
            json_object = DataBroker()
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

    def draw(self):
        if self.time_instr >= 3 and self.calibration and not self.feet_checker:
            self.boy.draw(self.game.display)
            self.texto_pies.draw(self.game.display)
        elif self.time_instr >= 3 and self.calibration and not self.visibility_checker:
            self.boy.draw(self.game.display)
            self.texto_partes.draw(self.game.display)
        if self.calibration and self.time_instr >=3 and not self.countdowns:
            pygame.draw.rect(self.game.display, settings.AZUL_CLARO, self.box_feet, 7, 0)
        
        self.atras.draw(self.game.display)
    
    def check_collide(self, left, right):
        if self.atras.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.atras.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Atras"

    def create_box_feet(self):
        point_left = escale_coor_pix(self.feet_left[0], self.feet_left[1], self.game.display.get_size())
        point_right = escale_coor_pix(self.feet_right[0], self.feet_right[1], self.game.display.get_size())
        width = distance_between_pixels(point_left, point_right)

        rect = pygame.Rect(
            point_left[0] - settings_0.FEET_MARGIN,
            point_left[1] - settings_0.FEET_MARGIN,
            width + settings_0.FEET_BOX,
            settings_0.FEET_BOX,
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

        left_hand, right_hand = get_points(results)
        self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
        self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
        self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
        self.right_source.rect.centery = right_hand[1] * settings.HEIGHT
        
        action = self.check_collide(self.left_source, self.right_source)
        if action == "Atras":
            self.timedown_back.tracking(results)
            self.countback = self.timedown_back.events()
            self.timedown_back.draw()
            if not self.countback:
                self.atras.set_clicked_true()
        else:
            self.timedown_back.restart()  
        
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

                left_hand_bound = create_diagonal_points_left(results, self.game.display.get_size())
                right_hand_bound = create_diagonal_points_right(results, self.game.display.get_size())
                top_margin = create_top_margin(results, self.game.display.get_size())
                self.shoulder_left, self.shoulder_right = get_shoulder_pos(results, self.game.display.get_size())
                self.margin = (top_margin[0], top_margin[1])
                self.bound_left_hand = (left_hand_bound[0], left_hand_bound[1])
                self.bound_right_hand = (right_hand_bound[0], right_hand_bound[1])
                self.music.play()
                # self.music_playing = True
                self.ticks = pygame.time.get_ticks()
                self.time_instr = 0

        elif self.time_instr < 3 and self.calibration and not self.end:
            self.time_instr = count(self.ticks)
            self.time_right = reset_pygame_timer()
            self.time_left = reset_pygame_timer()
            self.reaction_timeLeft = reset_pygame_timer()
            self.reaction_timeRight = reset_pygame_timer()
            self.timer = reset_pygame_timer()
            self.diaggif_animation.draw(self.game.display)
            self.diaggif_animation.update()
            self.texto.draw(self.game.display)
        elif (
            self.time_instr >= 3
            and self.calibration
            and not self.feet_checker
            and not self.end
            and not self.countdowns
        ):
            # Cuando los pies no estan la posicion calibrada o falta algún punto en la pantalla
            # Para checkeo de pies
            self.check_feet()
        elif (
            self.time_instr >= 3
            and self.calibration
            and not self.visibility_checker
            and not self.end
            and not self.countdowns
        ):
            # para checkeo visibilidad
            self.visibility = check_visibility(self.current_results)
        elif (
            self.time_instr >= 3
            and self.calibration
            and self.visibility_checker
            and not self.end
            and self.countdowns
        ):
            self.timedown_object.tracking(results)
            self.timedown_object.draw()
            self.countdowns = self.timedown_object.events()
            self.timer = reset_pygame_timer()
        elif (
            self.time_instr >= 3
            and self.calibration
            and self.feet_checker
            and self.visibility_checker
            and not self.end
            and not self.countdowns
        ):
            # Cuando esta todo ok
            # Se usa la izquierda en la derecha y viceversa pq se invierte la imagen
            # Para checkeo de pies
            self.check_feet()
            self.visibility = check_visibility(self.current_results)
            self.mostrar_instrucciones = False
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

            self.width = self.current_time * self.coefficient
            
            rect_stats = pygame.Surface(
                (settings.WIDTH, 50))  # the size of your rect
            rect_stats.set_alpha(128)  # alpha level
            # this fills the entire surface
            rect_stats.fill((255, 255, 255))
            self.game.display.blit(rect_stats, (0, 0))

            # Time bar
            pygame.draw.rect(
                self.game.display,
                settings.RED,
                (201, 25, self.width, 10),
            )
            pygame.draw.rect(self.game.display,
                             settings.BLACK, self.bar_rect, 2)

            # Time
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
            self.game.display.blit(puntuacion, (self.game.display.get_size()[0]-300, 15))

            puntos = settings.FONTS["medium"].render(
                "{0}".format(self.puntuacion), True, settings.COLOR_ROJO
            )
            self.game.display.blit(puntos, (self.game.display.get_size()[0]-100, 15))
            
            # Draw point on the screen
            self.hands.draw(self.game.display)
            self.points_left.draw(self.game.display)
            self.points_right.draw(self.game.display)
            self.explosiones.draw(self.game.display)
            self.explosiones.update()
            self.fireworks.draw(self.game.display)
            self.fireworks.update()

        if self.end:
            self.time_instr = 0
            self.music.stop()
            self.claps.play()
