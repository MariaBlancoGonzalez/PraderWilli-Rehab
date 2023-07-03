import pygame
import sys

from scenes.scene import Scene
from tracking.tracker_utils import *
import settings.settings as settings
from ui.gui import Button, DropDown
from ui.source import Source
from utils import *

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "MenuScene"

        # Buttons
        pos = self.game.display.get_size()[0]
        self.button_activities = Button((pos*0.05, self.game.display.get_size()[1] / 3), "Actividades")
        self.button_historial = Button((pos*0.3, self.game.display.get_size()[1] / 3), "Historial")
        self.button_tutorial = Button((pos*0.55, self.game.display.get_size()[1] / 3), "Tutorial")
        self.button_exit = Button((pos*0.8, self.game.display.get_size()[1] / 3), "Salir")

        self.userDropDown = DropDown([settings.GRISCLARO, settings.WHITE],[settings.WHITE, settings.GRISCLARO],
            pos*0.05,80,
            200,35,
            settings.FONTS["arial_small"],f"{game.current_user}",game.user_list,
        )

        self.camDropDown = DropDown([settings.GRISCLARO, settings.WHITE],[settings.WHITE, settings.GRISCLARO],
            pos*0.8,80,
            200,35,
            settings.FONTS["arial_small"],f"{game.current_camara}",[f"{i}" for i in game.device_list],
        )

        self.button_group = [
            self.button_activities, self.button_exit, self.button_historial,
            self.button_tutorial, self.userDropDown, self.camDropDown,
            ]

        # Text
        self.bienvenido = settings.FONTS["header"].render("BIENVENIDO", True, settings.BLACK)
        self.message = settings.FONTS["medium"].render("Elige una de las posibles acciones", True, settings.BLACK)
        self.text_user = settings.FONTS["medium"].render("Usuario", True, settings.BLACK)
        self.txt_camara = settings.FONTS["medium"].render("Cambiar de fuente", True, settings.BLACK)

        # Sources
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.hands = pygame.sprite.Group([self.right_source,self.left_source])

        # Tracking time
        self.time_hand = 0
        self.pressed_activities = pygame.time.get_ticks()
        self.pressed_tutorial = pygame.time.get_ticks()
        self.pressed_history = pygame.time.get_ticks()
        self.pressed_exit = pygame.time.get_ticks()

        # Bar progress
        self.bar_rect = pygame.Rect(100, (self.game.display.get_size()[1]) - 90, 700, 30)
        self.width = 0

        self.action = ""

    def resized(self):
        self.bar_rect = pygame.Rect(100, (self.game.display.get_size()[1]) - 90, 700, 30)
        
        # Buttons
        pos = self.game.display.get_size()[0]
        self.button_activities = Button((pos*0.05, self.game.display.get_size()[1] / 3), "Actividades")
        self.button_historial = Button((pos*0.3, self.game.display.get_size()[1] / 3), "Historial")
        self.button_tutorial = Button((pos*0.55, self.game.display.get_size()[1] / 3), "Tutorial")
        self.button_exit = Button((pos*0.8, self.game.display.get_size()[1] / 3), "Salir")

        self.userDropDown.resized(pos*0.05, 80, 200,35)
        self.camDropDown.resized(pos*0.8, 80, 200,35)

    def render(self):
        # Buttons
        self.button_activities.draw(self.game.display)
        self.button_historial.draw(self.game.display)
        self.button_exit.draw(self.game.display)
        self.button_tutorial.draw(self.game.display)
        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)
        # Text
        self.game.display.blit(self.bienvenido,self.bienvenido.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 8)))
        self.game.display.blit(self.message,self.message.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 5)))
        self.game.display.blit(self.text_user, self.text_user.get_rect(center=(self.game.display.get_size()[0]*0.05+50, 60)))
        self.game.display.blit(self.txt_camara, self.txt_camara.get_rect(center=(self.game.display.get_size()[0]*0.8+100, 60)))

        self.userDropDown.draw(self.game.display)
        self.camDropDown.draw(self.game.display)
        # Draw progress bar
        pygame.draw.rect(self.game.display,settings.WHITE,(101, (self.game.display.get_size()[1]) - 90, self.width, 30),)
        pygame.draw.rect(self.game.display, settings.BLACK, self.bar_rect, 2)

    def events(self, event):
        self.userDropDown.update(event)
        self.camDropDown.update(event)
        self.game.current_user = self.userDropDown.main

        cam = int(self.camDropDown.getMain())
        if self.game.current_camara != cam:
            self.game.change_camara(cam)
        if self.button_activities.get_pressed() or self.button_activities.on_click(event):
            from scenes.activitiesScene import ActivitiesScene

            return ActivitiesScene(self.game)

        if self.button_historial.get_pressed() or self.button_historial.on_click(event):
            from scenes.recordScene import RecordScene

            return RecordScene(self.game)
        if self.button_tutorial.get_pressed() or self.button_tutorial.on_click(event):
            from scenes.tutorialScene import TutorialScene

            return TutorialScene(self.game)
        if self.button_exit.get_pressed() or self.button_exit.on_click(event):
            pygame.quit()
            sys.exit()

        pos = pygame.mouse.get_pos()
        if any(button.rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return None

    def update(self, frame):
        self.pose_tracker.pose_tracking(frame)

        coefficient = settings.WIDTH_LOAD_BAR / settings.TIME_BUTTONS
        left_hand, right_hand = get_hands_points(self.pose_tracker.landmark_process)

        self.left_source.update_position(left_hand)
        self.right_source.update_position(right_hand)

        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_activities, self.hands) != None:
            self.time_hand = count(self.pressed_activities)
            self.action = "Actividades"
        else:
            self.pressed_activities = pygame.time.get_ticks()
        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_historial, self.hands) != None:
            self.time_hand = count(self.pressed_history)
            self.action = "Record"
        else:
            self.pressed_history = pygame.time.get_ticks()
        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_tutorial, self.hands) != None:
            self.time_hand = count(self.pressed_tutorial)
            self.action = "Tutorial"
        else:
            self.pressed_tutorial = pygame.time.get_ticks()
        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_exit, self.hands) != None:
            self.time_hand = count(self.pressed_exit)
            self.action = "Exit"
        else:
            self.pressed_exit = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if self.action == "":
            self.time_hand, self.width = reset_time()
            
        if self.time_hand > settings.TIME_BUTTONS:
            if self.action == "Actividades":
                self.button_activities.set_pressed(True)
            elif self.action == "Tutorial":
                self.button_tutorial.set_pressed(True)
            elif self.action == "Exit":
                self.button_exit.set_pressed(True)
            elif self.action == "Record":
                self.button_historial.set_pressed(True)
            self.time_hand, self.width = reset_time()
            self.reset_timer_after()
        
        self.action = ""
            
    def reset_timer_after(self):
        self.pressed_exit = pygame.time.get_ticks()
        self.pressed_tutorial = pygame.time.get_ticks()
        self.pressed_history = pygame.time.get_ticks()
        self.pressed_activities = pygame.time.get_ticks()