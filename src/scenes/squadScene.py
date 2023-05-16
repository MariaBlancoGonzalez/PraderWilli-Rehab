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

class SquadScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "SquadScene"
        
        # Music
        self.music = pygame.mixer.Sound(settings.MUSIC_DIAGONALES)
        # self.music_playing = False

        # Sounds
        self.pip_sound = pygame.mixer.Sound(settings.PIP)

        # Sources
        self.right_feet = Source(game.display, settings.PUNTERO_ROJO, (50,50))
        self.left_feet = Source(game.display, settings.PUNTERO_ROJO, (50, 50))
        self.right_knee = Source(game.display, settings.PUNTERO_ROJO, (50, 50))
        self.left_knee = Source(game.display, settings.PUNTERO_ROJO, (50, 50))
        self.left_hip = Source(game.display, settings.PUNTERO_ROJO, (50, 50))
        self.right_hip = Source(game.display, settings.PUNTERO_ROJO, (50, 50))

        # Game settings
        self.velocidad_squad = settings.VELOCIDAD_SQUAD 
        self.tiempo_juego = settings.TIEMPO_JUEGO_SQUAD

        self.aciertos = 0
        self.errores = 0

        # Score total and partial to show
        self.puntuacion = 0
        self.angle = 0
        self.correct_squad = False
        self.correct_score = settings.FONTS["medium"].render(
            str(settings.ACIERTO_PTO), True, settings.BLACK
        )
        self.error_score = settings.FONTS["medium"].render(
            str(settings.FALLO), True, settings.BLACK
        )
        # Text
        self.texto = BackgroundText(
            "Realiza sentadillas",
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
        self.squad_gif = Animation(
            self.game.display,
            600,
            500,
            settings.SQUADGIF,
            settings.FPS_SQUAD, (400,500)
        )
        self.squadgif_animation = Group(self.squad_gif)

    def events(self, events):
        if self.end:
            if self.game.connection == 0:
                #self.introduced_data()
                return ActivitiesScene(self.game)
            else:
                #self.game.json_object.write_data_json(
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
        # Draw point on the screen
        if self.draw_part == 'left':
            self.left_feet.draw(self.game.display)
            self.left_knee.draw(self.game.display)
            self.left_hip.draw(self.game.display)

            pygame.draw.lines(
                self.game.display, settings.COLOR_ROJO, True, [(self.left_hip.rect.centerx, self.left_hip.rect.centery), (self.left_knee.rect.centerx, self.left_knee.rect.centery), (self.left_feet.rect.centerx, self.left_feet.rect.centery)], 5)
            self.game.display.blit(angle, (self.left_knee.rect.centerx+50, self.left_knee.rect.centery))
        
        elif self.draw_part == 'right':
            self.right_feet.draw(self.game.display)
            self.right_knee.draw(self.game.display)
            self.right_hip.draw(self.game.display)

            pygame.draw.lines(
                self.game.display, settings.COLOR_ROJO, True, [(self.right_hip.rect.centerx, self.right_hip.rect.centery), (self.right_knee.rect.centerx, self.right_knee.rect.centery), (self.right_feet.rect.centerx, self.right_feet.rect.centery)], 5)

            self.game.display.blit(angle, (self.right_knee.rect.centerx-50, self.right_knee.rect.centery))
        


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

            # Coger puntos pies
            left_current_foot, rigth_current_foot = get_feet_points(
                self.current_results)

            self.left_feet.rect.centerx = left_current_foot[0] * settings.WIDTH
            self.left_feet.rect.centery = left_current_foot[1] * settings.HEIGHT
            self.right_feet.rect.centerx = rigth_current_foot[0] * settings.WIDTH
            self.right_feet.rect.centery = rigth_current_foot[1] * settings.HEIGHT

            # Coger puntos rodillas
            left_knee, right_knee = get_knees_points(self.current_results)
            self.left_knee.rect.centerx = left_knee[0] * settings.WIDTH
            self.left_knee.rect.centery = left_knee[1] * settings.HEIGHT
            self.right_knee.rect.centerx = right_knee[0] * settings.WIDTH
            self.right_knee.rect.centery = right_knee[1] * settings.HEIGHT

            # Coger caderas
            left_current_hip, right_current_hip = get_hips_points(self.current_results)
            self.left_hip.rect.centerx = left_current_hip[0] * settings.WIDTH
            self.left_hip.rect.centery = left_current_hip[1] * settings.HEIGHT
            self.right_hip.rect.centerx = right_current_hip[0] * settings.WIDTH
            self.right_hip.rect.centery = right_current_hip[1] * settings.HEIGHT

            if self.draw_part == "right":
                self.angle = angle_calculate_by_points(right_current_hip, right_knee, rigth_current_foot)
            else:
                self.angle = angle_calculate_by_points(left_current_hip, left_knee, left_current_foot)

            if self.angle <= 90.0:
                if (pygame.time.get_ticks() - self.time_squad) / 1000 < self.velocidad_squad and not self.correct_squad:
                    self.aciertos += 1
                    self.puntuacion += settings.ACIERTO_PTO
                    self.correct_squad = True
                    print("Aciertos", self.aciertos)
                
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
                    print("Errores",self.errores)
                else:
                    self.correct_squad = False
                self.time_squad = reset_pygame_timer()

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
            settings.ID_DIAGONALES,
            today,
            settings.TIEMPO_JUEGO,
            self.errores_izquierda,
            self.aciertos_izquierda,
            self.errores_derecha,
            self.aciertos_derecha,
        )
        broker.close()
