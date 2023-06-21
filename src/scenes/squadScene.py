from scenes.scene import Scene
import pygame

import settings.settings as settings
import settings.settings_1 as settings_1
from ui.source import Source
from ui.sticker import Sticker
from pygame.sprite import Group
from ui.gui import BackgroundText
from broker import DataBroker
from pose_tracking.tracker_utils import *

from ui.animation import Animation
import random
from utils import *
from scenes.activitiesScene import ActivitiesScene
from scenes.calibrationScene import CalibrationScene
import statistics

class SquadScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "SquadScene"
        
        pygame.mixer.init()
        # Music
        song = random.randint(0, 5)
        self.music = pygame.mixer.Sound(settings.MUSIC[song])
        self.music.set_volume(0.5)
        # self.music_playing = False

        # Sounds
        self.pip_sound = pygame.mixer.Sound(settings.PIP)
        self.pip_sound.set_volume(1)
        self.error_sound = pygame.mixer.Sound(settings.ERROR_SOUND)
        self.error_sound.set_volume(1)
        self.claps = pygame.mixer.Sound(settings.CLAPS)
        self.claps.set_volume(1)


        # Manos con sprites vacios
        self.izq_mano = pygame.sprite.Sprite()
        self.drch_mano = pygame.sprite.Sprite()
        
        self.izq_mano.rect = pygame.Rect(0, 0, 5, 5)  # Tamaño del punto
        self.izq_mano.image = pygame.Surface(self.izq_mano.rect.size)

        self.drch_mano.rect = pygame.Rect(0, 0, 5, 5)  # Tamaño del punto
        self.drch_mano.image = pygame.Surface(self.drch_mano.rect.size)

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
        self.puntuacion = 0
        self.angle = 0
        self.best_angle = 200
        self.correct_squad = False

        # Text
        self.texto = BackgroundText(
            "Realiza sentadillas",
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
        self.boy = Sticker(
            self.game.display,
            settings.NIÑO,
            settings.WIDTH*0.11,
            250,
            200,
            160,
        )

        # Tracking time to show instruc.
        self.mostrar_instrucciones = True
        self.time_instr_squad = 0

        self.calibration = False if game.static_points == None else True

        if game.static_points != None:
            self.music.play()
            self.music.set_volume(0.6)
            self.music_playing = True

        # Tracking time during game
        self.time_squad = pygame.time.get_ticks()
        self.pitido = True

        self.draw_part = 'right'
        # In case calibration is not done
        self.calibration_object = CalibrationScene(self.game)
        if self.calibration_object != None:
            self.ticks = pygame.time.get_ticks()
        else:
            self.ticks = 0

        # Some checkers and timer
        self.timer = 0
        self.current_results = None
        self.visibility_checker = True
        self.current_time = self.tiempo_juego

        # Game complete
        self.end = False
        self.data_introduced = False

        # Animation
        self.squad_gif = Animation(
            self.game.display,
            self.game.display.get_size()[0]*0.5,
            self.game.display.get_size()[1]-350,
            settings.SQUADGIF,
            settings_1.FPS_SQUAD, (400,500)
        )
        self.squadgif_animation = Group(self.squad_gif)
        self.min_angulo = 200
        # Time bar
        # Progress bar
        self.bar_rect = pygame.Rect(
            200, 25, 500, 10)
        self.width = 0
        self.coefficient = 500 / self.tiempo_juego
        self.angle = read(settings_1.EXER_1_CONFIG, "ANGLE") 
    
    def resized(self):
        # Text
        self.texto = BackgroundText(
            "Realiza sentadillas",
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
            json_object.write_data_json(settings_1.EXER_1_JSON, settings_1.ID_SQUAD, self.tiempo_juego,
                                            self.errores, self.aciertos, round(statistics.mean(self.media_angulo), 2))
            return ActivitiesScene(self.game)
        if self.atras.get_clicked_state() or self.atras.on_click(events):
            self.music.stop()
            return ActivitiesScene(self.game)

        return None

    def draw(self):
        if self.mostrar_instrucciones and self.calibration:
            self.boy.draw(self.game.display)
            self.texto.draw(self.game.display)
        elif self.time_instr_squad >= 3 and self.calibration and not self.visibility_checker:
            self.boy.draw(self.game.display)
            self.texto_partes.draw(self.game.display)
        
        angle = settings.FONTS["medium"].render(
            "{0}º".format(
                int(self.angle)
            ),
            True,
            settings.BLACK)

        if self.draw_part == 'right':
            self.right_feet.draw(self.game.display)
            self.right_knee.draw(self.game.display)
            self.right_hip.draw(self.game.display)

            pygame.draw.lines(
                self.game.display, settings.COLOR_VERDE, True, [(self.right_hip.rect.centerx, self.right_hip.rect.centery), (self.right_knee.rect.centerx, self.right_knee.rect.centery), (self.right_feet.rect.centerx, self.right_feet.rect.centery)], 5)

            self.game.display.blit(angle, (self.right_knee.rect.centerx-50, self.right_knee.rect.centery))

        self.atras.draw(self.game.display)

    def check_collide(self, left, right):
        if self.atras.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.atras.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Atras"

    def tracking(self, results):
        self.current_results = results
        self.visibility_checker = check_visibility_squad(self.current_results)

        if self.current_results == None:
            return None

        left_hand, right_hand = get_points(results)
        self.izq_mano.rect.centerx = left_hand[0] * settings.WIDTH
        self.izq_mano.rect.centery = left_hand[1] * settings.HEIGHT
        self.drch_mano.rect.centerx = right_hand[0] * settings.WIDTH
        self.drch_mano.rect.centery = right_hand[1] * settings.HEIGHT
        action = self.check_collide(self.izq_mano, self.drch_mano)
            
        if action == "Atras":
            self.timedown_object.tracking(results)
            self.timedown_object.draw()
            self.countdowns = self.timedown_object.events()
            if not self.countdowns:
                self.atras.set_clicked_true()
        else:
            self.timedown_object.restart()  

        # Get initial points
        if not self.calibration:
            self.calibration_object.tracking(results)
            self.calibration_object.update(0)
            self.calibration_object.draw()
            self.calibration = self.calibration_object.calibrated
            self.ticks = pygame.time.get_ticks()
            if self.calibration:
                self.music.play()

        #if self.calibration and self.time_instr_squad <= 0 and not self.end:
        #    self.ticks = pygame.time.get_ticks()
        
        if self.time_instr_squad < 3 and self.calibration and not self.end:
            self.time_instr_squad = count(self.ticks)
            self.time_squad = reset_pygame_timer()
            self.timer = reset_pygame_timer()
            self.squadgif_animation.draw(self.game.display)
            self.squadgif_animation.update()
        elif (
            self.time_instr_squad >= 3
            and self.calibration
            and self.visibility_checker
            and not self.end
        ):
            # Cuando esta todo ok
            # Se usa la izquierda en la derecha y viceversa pq se invierte la imagen
            # Para checkeo de pies
            self.mostrar_instrucciones = False
            self.visibility_checker = check_visibility(self.current_results)
            if self.pitido:
                best_angle = 200
                self.pip_sound.play()
                self.pitido = False

            # Coger puntos pies
            left_current_foot, rigth_current_foot = get_feet_points(
                self.current_results)

            self.left_feet.rect.centerx = left_current_foot[0] * settings.WIDTH
            self.left_feet.rect.centery = left_current_foot[1] * settings.HEIGHT
            self.right_feet.rect.centerx = rigth_current_foot[0] * settings.WIDTH
            self.right_feet.rect.centery = rigth_current_foot[1] * settings.HEIGHT

            # Coger puntos rodillas
            _, right_knee = get_knees_points(self.current_results)
            
            self.right_knee.rect.centerx = right_knee[0] * settings.WIDTH
            self.right_knee.rect.centery = right_knee[1] * settings.HEIGHT

            # Coger caderas
            _, right_current_hip = get_hips_points(self.current_results)

            self.right_hip.rect.centerx = right_current_hip[0] * settings.WIDTH
            self.right_hip.rect.centery = right_current_hip[1] * settings.HEIGHT

            if self.draw_part == "right":
                self.angle = angle_calculate_by_points(right_current_hip, right_knee, rigth_current_foot)
            
            if self.angle <= 100.0:
                if self.best_angle > self.angle:
                    self.best_angle = self.angle

                if (pygame.time.get_ticks() - self.time_squad) / 1000 < self.velocidad_squad and not self.correct_squad:
                    self.aciertos += 1
                    self.puntuacion += settings_2.ACIERTO_PTO
                    self.correct_squad = True


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

        if self.end:
            self.music.stop()
            self.claps.play()
