import pygame
from scenes.scene import Scene
import settings
from ui.gui import Button
from ui.source import Source
from utils import *

from scenes.menuScene import MenuScene

class TutorialScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = 'TutorialScene'

        # Text
        self.tutorial = settings.FONTS['header'].render(
            "Tutorial", True, settings.BLACK)

        # Images
        self.flecha_drch = pygame.image.load(settings.FLECHA_DERECHA)
        self.flecha_izq = pygame.image.load(settings.FLECHA_IZQUIERDA)
        self.pet = pygame.image.load(settings.MASCOTA_NORMAL)
        self.pet = pygame.transform.scale(self.pet, (500, 500))
        historial = pygame.image.load(settings.HISTORIAL)
        historial = pygame.transform.scale(historial, (1000, 500))
        opciones = pygame.image.load(settings.OPCIONES)
        opciones = pygame.transform.scale(opciones, (1000, 500))
        # Tutorial images
        self.images_group = [historial, opciones]

        # Needed variables
        self.current_image = 0

        # Buttons
        self.button_back = Button((170, 30), "Volver", settings.AMARILLO)
        self.button_arrow_left = Button(
            (45, settings.HEIGHT//2), "<", settings.GRANATE, 50)
        self.button_arrow_right = Button(
            (1178, settings.HEIGHT//2), ">", settings.GRANATE, 50)
        self.button_group = [self.button_back,
                             self.button_arrow_left, self.button_arrow_right]
        # Sources
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        # Tracking time
        self.time_hand = 0
        self.pressed_back = pygame.time.get_ticks()
        self.pressed_right = pygame.time.get_ticks()
        self.pressed_left = pygame.time.get_ticks()

        # Progress bar
        self.bar_rect = pygame.Rect(
            40, (game.display.get_size()[1])-50, 700, 30)
        self.width = 0

    def check_collide(self, left, right):
        if self.button_back.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_back.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Volver"
        elif self.button_arrow_left.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_arrow_left.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "<"
        elif self.button_arrow_right.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_arrow_right.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return ">"

        return ""

    def draw(self):
        # Backgrounds
        self.game.display.fill(settings.GRANATE)
        pygame.draw.rect(self.game.display, settings.AMARILLO,
                         pygame.Rect(40, 160, 1200, 560))

        # Text
        self.game.display.blit(self.tutorial, (settings.WIDTH//3+30, 10))

        # Buttons
        self.button_back.draw(self.game.display)
        self.button_arrow_left.draw(self.game.display)
        self.button_arrow_right.draw(self.game.display)

        # For show current image
        self.game.display.blit(
            self.images_group[self.current_image], (150, 200))

        # Sources
        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)

        # Draw progress bar
        pygame.draw.rect(self.game.display, settings.WHITE, (41,
                         (self.game.display.get_size()[1])-50, self.width, 30))
        pygame.draw.rect(self.game.display, settings.BLACK, self.bar_rect, 2)

    def events(self, events):
        if self.button_back.get_pressed() or self.button_back.on_click(events):
            return MenuScene(self.game)
        if self.button_arrow_left.get_pressed() or self.button_arrow_left.on_click(events):
            if self.current_image > 0:
                self.current_image -= 1
            self.reset_time()
            self.button_arrow_left.set_pressed(False)
        if self.button_arrow_right.get_pressed() or self.button_arrow_right.on_click(events):
            if self.current_image != len(self.images_group)-1:
                self.current_image += 1
            self.reset_time()
            self.button_arrow_right.set_pressed(False)

        return None
    
    def reset_time(self):
        self.time_hand = 0
        self.width = 0

    def count(self, start_ticks):
        seconds = (pygame.time.get_ticks()-start_ticks) / \
            1000  # calculate how many seconds
        if seconds >= settings.TIME_BUTTONS:
            return seconds
        return seconds

    def tracking(self, results):
        action = ""
        coefficient = settings.WIDTH_LOAD_BAR / settings.TIME_BUTTONS
        left_hand, right_hand = get_points(results)
        self.left_source.rect.centerx = left_hand[0] * settings.WIDTH
        self.left_source.rect.centery = left_hand[1] * settings.HEIGHT
        self.right_source.rect.centerx = right_hand[0] * settings.WIDTH
        self.right_source.rect.centery = right_hand[1] * settings.HEIGHT

        # Colisiones
        action = self.check_collide(self.left_source, self.right_source)
        # ------------------------------------------
        if action == "Volver":
            self.time_hand = self.count(self.pressed_back)
        else:
            self.pressed_back = pygame.time.get_ticks()
        # ------------------------------------------
        if action == ">":
            self.time_hand = self.count(self.pressed_right)
        else:
            self.pressed_right = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "<":
            self.time_hand = self.count(self.pressed_left)
        else:
            self.pressed_left = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if action == "":
            self.reset_time()
        if self.time_hand >= settings.TIME_BUTTONS:
            if action == "Volver":
                self.button_back.set_pressed(True)
            elif action == "<":
                self.button_arrow_left.set_pressed(True)
            elif action == ">":
                self.button_arrow_right.set_pressed(True)

    def update(self, dt):
        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
