from scenes.scene import Scene
import pygame

import cv2
import settings.settings as settings
import settings.settings_2 as settings_2

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
from ui.moving_sprites import Moving_Sprite
from scenes.timeDownScene import TimeDown
from ui.gui import ImageButton
from scenes.timeDownScene import TimeDown
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
        self.error_sound = pygame.mixer.Sound(settings.ERROR_SOUND)
        self.error_sound.set_volume(1)
        self.explosion_sound = pygame.mixer.Sound(settings.EXPLOSION_SOUND)
        self.explosion_sound.set_volume(1)
        self.claps = pygame.mixer.Sound(settings.CLAPS)
        self.claps.set_volume(1)
        # Game settings
        self.tiempo_juego = read(settings_2.EXER_2_CONFIG, "TIEMPO_JUEGO_MOVILIDAD")
    
        self.errores = 0
        self.total_bolas = 0
        # Score total and partial to show
        self.puntuacion = 0

        # Text
        self.texto = BackgroundText(
            "Evita que te den las pelotas",
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

        # Manos con sprites vacios
        self.izq_mano = pygame.sprite.Sprite()
        self.drch_mano = pygame.sprite.Sprite()
        
        self.izq_mano.rect = pygame.Rect(0, 0, 5, 5)  # Tamaño del punto
        self.izq_mano.image = pygame.Surface(self.izq_mano.rect.size)

        self.drch_mano.rect = pygame.Rect(0, 0, 5, 5)  # Tamaño del punto
        self.drch_mano.image = pygame.Surface(self.drch_mano.rect.size)
                
        # Tracking time to show instruc.
        self.mostrar_instrucciones = True
        self.time_instr_balls = 0
        
        self.timedown_object = TimeDown(self.game)

        self.calibration = False if game.static_points == None else True
        # In case calibration is not done
        self.calibration_object = CalibrationScene(self.game)
        if self.calibration_object != None:
            self.ticks = pygame.time.get_ticks()
        else:
            self.ticks = 0

        if game.static_points != None:
            self.music.play()
            self.music.set_volume(0.6)
            self.music_playing = True

        # Tracking time during game
        self.time_balls = pygame.time.get_ticks()
        self.pitido = True
        self.correct = False
        self.wrong = False
        self.countdowns = True

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

        # Config
        self.probabilidad = read(settings_2.EXER_2_CONFIG, "PROBABILIDAD")
        self.speed = read(settings_2.EXER_2_CONFIG, "BALL_SPEED")
        self.footbal_image = pygame.image.load(settings.FOOTBALL)
        self.basket_image = pygame.image.load(settings.BASKETBALL)
        self.tennis_image = pygame.image.load(settings.TENISBALL)
        self.rugby_image = pygame.image.load(settings.RUGBYBALL)
        self.balls = Group()
        self.body = Group()
        self.explosiones = Group()

        # Time bar
        # Progress bar
        self.bar_rect = pygame.Rect(200, 25, 500, 10)
        self.width = 0
        self.coefficient = 500 / self.tiempo_juego

        # Animation
        self.balls_gif = Animation(
            self.game.display,
            620,
            500,
            settings.BALLGIF,
            settings_2.FPS_BALLS, (500, 500)
        )
        self.ballgif_animation = Group(self.balls_gif)

        # Go back
        self.img_atras = pygame.image.load(settings.ATRAS)
        self.atras = ImageButton(self.img_atras, (50,70), "modificar", (90, 90))
        self.countback = True
        self.timedown_back = TimeDown(self.game)

        # Atras
        self.img_atras = pygame.image.load(settings.ATRAS)
        self.atras = ImageButton(self.img_atras, (50,70), "modificar", (70, 70))


    def resized(self):
        self.texto = BackgroundText(
            "Evita que te den las pelotas",
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
            json_object.write_data_json(settings_2.EXER_2_JSON, settings_2.ID_BALLS, self.tiempo_juego,
                                        self.errores, self.total_bolas)
            return ActivitiesScene(self.game)
        
        if self.atras.get_clicked_state() or self.atras.on_click(events):
            self.music.stop()
            return ActivitiesScene(self.game)

        return None

    def draw(self):
        if self.mostrar_instrucciones and self.calibration and self.countdowns:
            self.boy.draw(self.game.display)
            self.texto.draw(self.game.display)
        elif self.time_instr_balls >= 3 and self.calibration and not self.visibility_checker:
            self.boy.draw(self.game.display)
            self.texto_partes.draw(self.game.display)

        self.balls.draw(self.game.display)
        self.atras.draw(self.game.display)

    def check_collide(self, left, right):
        if self.atras.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.atras.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Atras"
        return None

    def update_camera_utilities(self, image):
        self.image_camera = image

    def tracking(self, results):
        self.current_results = results
        self.visibility_checker = check_visibility_balls(self.current_results)
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
        
        if self.time_instr_balls < 3 and self.calibration and not self.end:
            self.time_instr_balls = count(self.ticks)
            self.seconds = 0
            self.time_balls = reset_pygame_timer()
            self.ballgif_animation.draw(self.game.display)
            self.ballgif_animation.update()
            
        elif (
            self.time_instr_balls >= 3
            and self.calibration
            and self.visibility_checker
            and not self.end
            and self.countdowns
        ):
            self.mostrar_instrucciones = False
            self.timedown_object.tracking(results)
            self.timedown_object.draw()
            self.countdowns = self.timedown_object.events()
            self.timer = reset_pygame_timer()
        elif (
            self.time_instr_balls >= 3
            and self.calibration
            and self.visibility_checker
            and not self.end
            and not self.countdowns
        ):
            # Cuando esta todo ok
            # Se usa la izquierda en la derecha y viceversa pq se invierte la imagen
            # Para checkeo de pies
            self.visibility_checker = check_visibility_balls(self.current_results)
            

            if self.pitido:
                self.pip_sound.play() 
                self.pitido = False

            self.body = update_pose_points(results, self.game.display.get_size())

            self.balls.update(self.speed)
            
            # Generate spheres randomly.
            if random.randrange(100) < self.probabilidad:
                self.total_bolas +=1
                self.balls.add(Moving_Sprite(self.game.display, self.footbal_image))
            
            if random.randrange(100) < self.probabilidad:
                self.total_bolas += 1
                self.balls.add(Moving_Sprite(self.game.display, self.basket_image))
            
            if random.randrange(100) < self.probabilidad:
                self.total_bolas += 1
                self.balls.add(Moving_Sprite(self.game.display, self.tennis_image))
            
            if random.randrange(100) < self.probabilidad:
                self.total_bolas += 1
                self.balls.add(Moving_Sprite(self.game.display, self.rugby_image))
            
            for ball in self.balls.sprites():
                # kill spheres when they leave the screen.
                if ball.rect.top > settings.HEIGHT:
                    self.puntuacion += settings_2.ACIERTO_BALLS
                    ball.kill()
            
            # This will find collisions between landmarks and spheres, killing the sprite of last group which collided.
            hit_list = pygame.sprite.groupcollide(self.body, self.balls, False, True)
            
            for sprite in hit_list:
                explosion = Animation(
                    self.game.display,
                    sprite.rect.centerx,
                    sprite.rect.centery,
                    settings.EXPLOSION,
                    settings_2.FPS_EXPLOSION,
                )
                self.explosiones.add(explosion)
                self.explosion_sound.play()
                self.errores += 1
                self.error_sound.play()

            # Mostrar en pantalla
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
            self.explosiones.draw(self.game.display)
            self.explosiones.update()

        if self.current_time <= 0:
            self.end = True

        if self.end:
            self.music.stop()
            self.claps.play()

