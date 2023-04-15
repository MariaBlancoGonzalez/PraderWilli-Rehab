import pygame
import sys

from scenes.scene import Scene
import settings
from ui.gui import Button, DropDown
from ui.source import Source
from utils import *

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = 'MenuScene'
        self.screen = game.display

        # Buttons
        self.button_activities = Button(
            (100, self.screen.get_size()[1]/3),  "Activities")
        self.button_options = Button(
            (1000, self.screen.get_size()[1]/3),  "Opciones")
        self.button_historial = Button(
            (400, self.screen.get_size()[1]/3),  "Historial")
        self.button_tutorial = Button(
            (700, self.screen.get_size()[1]/3), "Tutorial")
        self.button_exit = Button((1000, 80),  "Salir")

        self.userDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            100, 80, 200, 35,
            settings.FONTS['arial_small'],
            f'{game.current_user}', game.user_list)

        self.button_group = [self.button_activities, self.button_exit, self.button_historial,
                             self.button_options, self.button_tutorial, self.userDropDown]

        # Text
        self.bienvenido = settings.FONTS['header'].render(
            "BIENVENIDO", True, settings.BLACK)
        self.message = settings.FONTS['medium'].render(
            "Elige una de las posibles acciones", True, settings.BLACK)
        self.text_user = settings.FONTS['medium'].render(
            "Usuario", True, settings.BLACK)

        # Sources
        self.right_source = Source(self.screen, settings.PUNTERO_ROJO)
        self.left_source = Source(self.screen, settings.PUNTERO_ROJO)

        # Tracking time
        self.time_hand = 0
        self.pressed_activities = pygame.time.get_ticks()
        self.pressed_options = pygame.time.get_ticks()
        self.pressed_tutorial = pygame.time.get_ticks()
        self.pressed_history = pygame.time.get_ticks()
        self.pressed_exit = pygame.time.get_ticks()

        # Bar progress
        self.bar_rect = pygame.Rect(
            100, (self.screen.get_size()[1])-90, 700, 30)
        self.width = 0

    def draw(self):
        # Buttons
        self.button_activities.draw(self.screen)
        self.button_options.draw(self.screen)
        self.button_historial.draw(self.screen)
        self.button_exit.draw(self.screen)
        self.button_tutorial.draw(self.screen)
        self.right_source.draw(self.screen)
        self.left_source.draw(self.screen)
        # Text
        self.screen.blit(self.bienvenido, self.bienvenido.get_rect(
            center=(settings.WIDTH // 2, settings.HEIGHT // 8)))
        self.screen.blit(self.message, self.message.get_rect(
            center=(settings.WIDTH // 2, settings.HEIGHT // 5)))
        self.screen.blit(self.text_user, self.text_user.get_rect(
            center=(150, 60)))

        self.userDropDown.draw(self.screen)
        # Draw progress bar
        pygame.draw.rect(self.screen, settings.WHITE,
                         (101, (self.screen.get_size()[1])-90, self.width, 30))
        pygame.draw.rect(self.screen, settings.BLACK, self.bar_rect, 2)

    def events(self, event):
        self.userDropDown.update(event)

        self.game.current_user = self.userDropDown.main
        if self.button_activities.get_pressed() or self.button_activities.on_click(event):
            from scenes.activitiesScene import ActivitiesScene
            return ActivitiesScene(self.game)
        if self.button_options.get_pressed() or self.button_options.on_click(event):
            from scenes.optionScene import OptionsScene
            return OptionsScene(self.game)
        if self.button_historial.get_pressed() or self.button_historial.on_click(event):
            from scenes.recordScene import RecordScene
            return RecordScene(self.game)
        if self.button_tutorial.get_pressed() or self.button_tutorial.on_click(event):
            from scenes.tutorialScene import TutorialScene
            return TutorialScene(self.game)
        if self.button_exit.get_pressed() or self.button_exit.on_click(event):
            pygame.quit()
            sys.exit()

        return None
    def update(self, dt):
        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def count(self, start_ticks):
        seconds = (pygame.time.get_ticks()-start_ticks) / \
            1000  # calculate how many seconds
        if seconds >= settings.TIME_BUTTONS:
            return seconds
        return seconds

    def check_collide(self, left, right):
        if self.button_activities.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_activities.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Activities"
        elif self.button_options.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_options.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Options"
        elif self.button_historial.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_historial.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Record"
        elif self.button_tutorial.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_tutorial.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Tutorial"
        if self.button_exit.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_exit.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Exit"

        return ""

    def reset_time(self):
        self.time_hand = 0
        self.width = 0

    def tracking(self, results):
        action = ""

        coefficient = settings.WIDTH_LOAD_BAR / settings.TIME_BUTTONS
        # Get the point in the hand
        left_hand, right_hand = get_points(results)

        # For each hand
        self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
        self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
        self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
        self.right_source.rect.centery = right_hand[1] * settings.HEIGHT

        # Colisiones
        action = self.check_collide(self.left_source, self.right_source)
        # ------------------------------------------
        if action == "Activities":
            self.time_hand = self.count(self.pressed_activities)
        else:
            self.pressed_activities = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Options":
            self.time_hand = self.count(self.pressed_options)
        else:
            self.pressed_options = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Record":
            self.time_hand = self.count(self.pressed_history)
        else:
            self.pressed_history = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Tutorial":
            self.time_hand = self.count(self.pressed_tutorial)
        else:
            self.pressed_tutorial = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Exit":
            self.time_hand = self.count(self.pressed_exit)
        else:
           self.pressed_exit = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if action == "":
            self.reset_time()

        if self.time_hand > settings.TIME_BUTTONS:
            if action == "Activities":
                self.button_activities.set_pressed(True)
            elif action == "Options":
                self.button_options.set_pressed(True)
            elif action == "Tutorial":
                self.button_tutorial.set_pressed(True)
            elif action == "Exit":
                self.button_exit.set_pressed(True)
            elif action == "Record":
                self.button_historial.set_pressed(True)
