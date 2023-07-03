import pygame
from scenes.scene import Scene
from ui.sticker import Sticker
import settings.settings as settings
from ui.gui import ImageButton
from ui.source import Source
from ui.gui import BackgroundText
from tracking.tracker_utils import *

from math import sqrt
from scenes.auxiliaryScenes.timeDownScene import TimeDown

from scenes.activitiesScene import ActivitiesScene

class CalibrationScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "CalibrationScene"

        # Images
        self.body = Sticker(self.game.display,settings.BODY,settings.WIDTH*0.2,self.game.display.get_size()[1]-250,400,350)

        # Timer
        self.timedown_object = TimeDown(self.game)
        
        # Atras
        self.img_atras = pygame.image.load(settings.ATRAS)
        self.atras = ImageButton(self.img_atras, (50,70), "modificar", (70, 70))

        # Puntos de la cabeza
        self.cabeza = Source(self.game.display, settings.VERDE, (70,70))

        # Puntos de las manos
        self.izq_mano = Source(self.game.display, settings.VERDE, (70,70))
        self.drch_mano = Source(self.game.display, settings.VERDE, (70,70))
        self.hands = pygame.sprite.Group([self.izq_mano, self.drch_mano])

        # Puntos de los pies
        self.drch_pie = Source(self.game.display, settings.VERDE, (70,70))
        self.izq_pie = Source(self.game.display, settings.VERDE, (70,70))

        self.mostrar_instrucciones = True
        self.texto = BackgroundText("Muestra todas las partes del cuerpo",(self.game.display.get_size()[0]*0.11, 70),settings.WHITE,settings.GRIS,30)

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
        self.countdowns = True

    def resized(self):
        self.body = Sticker(self.game.display,settings.BODY,settings.WIDTH*0.17,
            self.game.display.get_size()[1]-200,
            400,350)
        self.texto = BackgroundText("Muestra todas las partes del cuerpo",(self.game.display.get_size()[0]*0.11, 70),
            settings.WHITE,
            settings.GRIS,
            30,
        )

    def events(self, ev):
        if self.end:
            self.end = False
            return ActivitiesScene(self.game)
        
        if self.atras.get_clicked_state() or self.atras.on_click(ev):
            self.game.static_points = None
            return ActivitiesScene(self.game)
        
        return None

    def time_control(self, dt):
        if self.calibrated and dt != 0:
            self.game.static_points = self.pose_tracker.landmark_process
            self.end = True


    def render(self):
        self.atras.draw(self.game.display)
        
        self.texto.draw(self.game.display)
        self.body.draw(self.game.display)

        if not all(item is True for item in self.checker):
            self.texto.draw(self.game.display)

    def count_seconds(self):
        self.seconds = (
            pygame.time.get_ticks() - self.timer
        ) / 1000  # calculate how many seconds
        seconds_txt = settings.FONTS["extra"].render(
            "{0}".format(int(self.seconds)), True, settings.BLACK
        )
        self.game.display.blit(seconds_txt, (self.game.display.get_size()[0]/2-30, self.game.display.get_size()[1]*0.35))

        if self.seconds >= 3.2:
            self.calibrated = True

    def update(self, frame):
        self.pose_tracker.pose_tracking(frame)

        left_hand, right_hand = get_hands_points(self.pose_tracker.landmark_process)
        self.izq_mano.update_position(left_hand)
        self.drch_mano.update_position(right_hand)

        head = get_head_points(self.pose_tracker.landmark_process)
        self.cabeza.update_position(head)
        
        left_feet, right_feet = get_feet_points(self.pose_tracker.landmark_process)
        self.drch_pie.update_position(right_feet)
        self.izq_pie.update_position(left_feet)
        
        if pygame.sprite.spritecollideany(self.atras, self.hands) != None:
            self.timedown_object.tracking(self.pose_tracker.landmark_process)
            self.timedown_object.draw()
            self.countdowns = self.timedown_object.events()
            if not self.countdowns:
                self.atras.set_clicked_true()
        else:
            self.timedown_object.restart()      
        
        if self.time_instr < 3:
            self.time_instr = count(self.ticks)
            self.timer = reset_pygame_timer()
            self.seconds = 0
        elif self.time_instr >= 3:
            try:
                if self.pose_tracker.landmark_process[0]['visibility'] > 0.6:
                    self.cabeza.draw(self.game.display)
                    self.checker[0] = True
                else:
                    self.checker[0] = False
                # Manos
                if self.pose_tracker.landmark_process[16]['visibility'] > 0.6:
                    self.drch_mano.draw(self.game.display)
                    self.checker[1] = True
                else:
                    self.checker[1] = False

                if self.pose_tracker.landmark_process[15]['visibility'] > 0.6:
                    self.izq_mano.draw(self.game.display)
                    self.checker[2] = True
                else:
                    self.checker[2] = False

                # Pies
                if self.pose_tracker.landmark_process[28]['visibility'] > 0.6:
                    self.drch_pie.draw(self.game.display)
                    self.checker[3] = True
                else:
                    self.checker[3] = False

                if self.pose_tracker.landmark_process[27]['visibility'] > 0.6:
                    self.izq_pie.draw(self.game.display)
                    self.checker[4] = True
                else:
                    self.checker[4] = False
            except:
                self.checker = [False, False, False, False, False]

            # All points availables
            if all(item is True for item in self.checker):
                self.count_seconds()
                self.game.static_points = self.pose_tracker.landmark_process

            # Not all points available
            elif not all(item is True for item in self.checker):
                self.show_seconds = False
                
                self.timer = reset_pygame_timer()
                self.seconds = 0
        self.action =""