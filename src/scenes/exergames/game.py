import pygame
from pygame.sprite import Group
from abc import ABCMeta, abstractmethod
import random

import settings.settings as settings
import settings.settings_0 as settings_0

from ui.source import Source
from ui.gui import BackgroundText, ImageButton
from ui.animation import Animation

from tracking.tracker_utils import *
from utils import *

from scenes.scene import Scene
from scenes.auxiliaryScenes.calibrationScene import CalibrationScene
from scenes.auxiliaryScenes.timeDownScene import TimeDown

class Exergame(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        pygame.mixer.init()
        song = random.randint(0, 5)
        self.music = pygame.mixer.Sound(settings.MUSIC[song])
        self.music.set_volume(0.5)

        self.right_source = Source(game.display, settings.VOID)
        self.left_source = Source(game.display, settings.VOID)
        self.hands = Group([self.right_source, self.left_source])
        
        # Init animation
        self.init_gif = Animation(
            self.game.display,
            self.game.display.get_size()[0]*0.45,
            self.game.display.get_size()[1]-250,
            settings.DIAGGIF,
            settings_0.FPS_DIAG, (500, 500)
        )
        self.init_animation = Group(self.init_gif)

        # Score total to show
        self.puntuacion = 0

        # Visibility text
        self.txt_visibility = BackgroundText(
            "Muestra todas las partes del cuerpo",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )

        self.txt_instr = BackgroundText(
            "Instrucciones",
            (self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )

        if game.static_points != None:
            self.music.play()
            self.music.set_volume(0.6)
            self.music_playing = True

        self.tiempo_juego = 1
        self.current_time = self.tiempo_juego

        # Tracking time to show instruc.
        self.time_instr = 0
        self.ticks = pygame.time.get_ticks()

        # Progressive count
        self.timedown_object = TimeDown(self.game)
        self.timedown_back = TimeDown(self.game)

        # Calibration before or after start
        self.calibration = False if game.static_points == None else True
        self.calibration_object = CalibrationScene(self.game) # In case calibration is not done

        # Timers
        self.timer = pygame.time.get_ticks()
        self.visibility_checker = True
        self.current_time = self.tiempo_juego
        self.countdowns = True
        self.countdowns_back = True

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
        

    @abstractmethod
    def events(self, events):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def calibration_success(self):
        pass

    @abstractmethod
    def reset_timers(self):
        pass

    def update(self, frame):
        self.pose_tracker.pose_tracking(frame)
        self.visibility_checker = check_visibility_balls(self.pose_tracker.landmark_process)

        left_hand, right_hand = get_hands_points(self.pose_tracker.landmark_process)
        
        self.left_source.update_position(left_hand)
        self.right_source.update_position(right_hand)

        if pygame.sprite.spritecollideany(self.atras, self.hands) != None:
            self.timedown_back.update(self.pose_tracker.landmark_process)
            self.timedown_back.render()
            self.countdowns_back = self.timedown_back.events()

            if not self.countdowns_back:
                self.atras.set_clicked_true()
        else:
            self.timedown_back.restart()   

        # Get initial points
        if not self.calibration:
            self.calibration_object.update(frame)
            self.calibration_object.time_control(0)
            self.calibration_object.render()
            self.calibration = self.calibration_object.calibrated
            self.ticks = pygame.time.get_ticks()
            if self.calibration:
                self.calibration_success()
        
        if self.time_instr < 3 and self.calibration and not self.end:
            self.time_instr = count(self.ticks)
            self.seconds = 0
            self.timer = reset_pygame_timer()
            self.init_animation.draw(self.game.display)
            self.init_animation.update()
            self.txt_instr.draw(self.game.display)
            self.reset_timers()
        elif (
            self.time_instr >= 3
            and self.calibration
            and self.visibility_checker
            and not self.end
            and self.countdowns
        ):
            self.timedown_object.update(self.pose_tracker.landmark_process)
            self.timedown_object.render()
            self.countdowns = self.timedown_object.events()
            self.timer = reset_pygame_timer()
        elif (
            self.time_instr >= 3
            and self.calibration
            and self.visibility_checker
            and not self.end
            and not self.countdowns
        ):
            self.logic()

            # Common elements
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


    def logic(self):
        pass