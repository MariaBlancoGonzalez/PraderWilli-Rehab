import pygame
from pygame.sprite import Group
import cv2
import random

import settings.settings as settings
import settings.settings_2 as settings_2

from ui.source import Source
from ui.sticker import Sticker
from ui.moving_sprites import Moving_Sprite
from ui.animation import Animation
from ui.gui import BackgroundText, ImageButton

from broker import DataBroker
from tracking.tracker_utils import *
from utils import *

from scenes.exergames.game import Exergame
from scenes.activitiesScene import ActivitiesScene
from scenes.auxiliaryScenes.calibrationScene import CalibrationScene

class BallScene(Exergame):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "BallScene"

        # Sounds
        self.pip_sound = pygame.mixer.Sound(settings.PIP)
        self.pip_sound.set_volume(1)
        self.error_sound = pygame.mixer.Sound(settings.ERROR_SOUND)
        self.error_sound.set_volume(1)
        self.explosion_sound = pygame.mixer.Sound(settings.EXPLOSION_SOUND)
        self.explosion_sound.set_volume(1)
        self.claps = pygame.mixer.Sound(settings.CLAPS)
        self.claps.set_volume(1)

        # Text
        self.txt_instr = BackgroundText(
            "Evita que te den los balones",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )

        # Game settings
        self.tiempo_juego = read(settings_2.EXER_2_CONFIG, "TIEMPO_JUEGO_MOVILIDAD")
        self.coefficient = 500 / self.tiempo_juego
        self.errores = 0
        self.total_bolas = 0


        # Tracking time during game
        self.time_balls = pygame.time.get_ticks()
        self.pitido = True
        self.correct = False
        self.wrong = False

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

        # Animation
        self.init_gif = Animation(
            self.game.display,
            self.game.display.get_size()[0]*0.5,
            self.game.display.get_size()[1]-250,
            settings.BALLGIF,
            settings_2.FPS_BALLS, (500, 500)
        )
        self.init_animation = Group(self.init_gif)

    def resized(self):
        self.txt_instr = BackgroundText(
            "Evita que te den los balones",
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
            json_object.write_data_json(settings_2.EXER_2_JSON, settings_2.ID_BALLS, self.tiempo_juego,
                                        self.errores, self.total_bolas)
            return ActivitiesScene(self.game)
        
        if self.atras.get_clicked_state() or self.atras.on_click(events):
            self.music.stop()
            return ActivitiesScene(self.game)

        return None

    def render(self):
        if self.time_instr >= 3 and self.calibration and not self.visibility_checker:
            self.txt_visibility.draw(self.game.display)

        self.balls.draw(self.game.display)
        self.atras.draw(self.game.display)

    def calibration_success(self):
        self.music.play()

    def reset_timers(self):
        self.time_balls = reset_pygame_timer()

    def logic(self):
        self.visibility_checker = check_visibility_balls(self.pose_tracker.landmark_process)
        if self.pitido:
            self.pip_sound.play() 
            self.pitido = False

        self.body = update_pose_points(self.pose_tracker.landmark_process)

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
        
        if self.current_time <= 0:
            self.music.stop()
            self.claps.play()
            self.end = True
        
        self.explosiones.draw(self.game.display)
        self.explosiones.update()