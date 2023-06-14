import pygame
from scenes.scene import Scene
import settings
from ui.gui import Button
from ui.source import Source
from pose_tracking.tracker_utils import *
from utils import *

from scenes.menuScene import MenuScene

class TutorialScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "TutorialScene"

        # Text
        self.tutorial = settings.FONTS["header"].render(
            "Tutorial", True, settings.BLACK
        )

        # Imágenes
        self.historial = cargar_archivos_folder(settings.HISTORIAL, (1000,500))
        self.actividades = cargar_archivos_folder(settings.ACTIVIDADES, (1000,500))
        self.menu = cargar_archivos_folder(settings.MENU, (1000,500))
        # Tutorial images
        self.images_group = self.menu

        # Needed variables
        self.current_image = 0

        # Buttons
        self.button_back = Button((170, 30), "Volver", settings.AMARILLO)
        self.button_arrow_left = Button(
            (45, settings.HEIGHT // 2), "<", settings.GRANATE, 50
        )
        self.button_arrow_right = Button(
            (1178, settings.HEIGHT // 2), ">", settings.GRANATE, 50
        )

        self.button_act = Button((530, 100), "Actividades", settings.AMARILLO)
        self.button_hist = Button((880, 100), "Historial", settings.AMARILLO)
        self.button_menu = Button((170, 100), "Menú", settings.AMARILLO)

        self.button_group = [
            self.button_back,
            self.button_arrow_left,
            self.button_arrow_right,
            self.button_hist,
            self.button_act,
            self.button_menu,
        ]
        # Sources
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        # Tracking time
        self.time_hand = 0
        self.pressed_back = pygame.time.get_ticks()
        self.pressed_right = pygame.time.get_ticks()
        self.pressed_left = pygame.time.get_ticks()
        self.pressed_act = pygame.time.get_ticks()
        self.pressed_hist = pygame.time.get_ticks()
        self.pressed_menu = pygame.time.get_ticks()

        # Progress bar
        self.bar_rect = pygame.Rect(40, (game.display.get_size()[1]) - 50, 700, 30)
        self.width = 0

    def check_collide(self, left, right):
        if self.button_back.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_back.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Volver"
        elif self.button_arrow_left.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_arrow_left.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "<"
        elif self.button_arrow_right.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_arrow_right.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return ">"

        elif self.button_hist.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_hist.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Act"
        elif self.button_act.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_act.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Hist"
        elif self.button_menu.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_menu.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Menu"
        return ""

    def draw(self):
        # Backgrounds
        self.game.display.fill(settings.GRANATE)
        pygame.draw.rect(
            self.game.display, settings.AMARILLO, pygame.Rect(40, 160, 1200, 560)
        )
        for i in range(4):
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (40, 160, 1200, 560), 2)

        # Text
        self.game.display.blit(self.tutorial, (settings.WIDTH // 3 + 30, 10))

        # Buttons
        self.button_back.draw(self.game.display)
        self.button_arrow_left.draw(self.game.display)
        self.button_arrow_right.draw(self.game.display)
        self.button_act.draw(self.game.display)
        self.button_hist.draw(self.game.display)
        self.button_menu.draw(self.game.display)

        # For show current video
        self.game.display.blit(self.images_group[self.current_image], (135, 200))

        # Sources
        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)

        # Draw progress bar
        pygame.draw.rect(
            self.game.display,
            settings.WHITE,
            (41, (self.game.display.get_size()[1]) - 50, self.width, 30),
        )
        pygame.draw.rect(self.game.display, settings.BLACK, self.bar_rect, 2)

    def events(self, events):
        if self.button_act.get_pressed() or self.button_act.on_click(events):
            self.images_group = self.actividades
            self.current_image = 0
        if self.button_hist.get_pressed() or self.button_hist.on_click(events):
            self.images_group = self.historial
            self.current_image = 0
        if self.button_menu.get_pressed() or self.button_menu.on_click(events):
            self.images_group = self.menu
            self.current_image = 0
        if self.button_back.get_pressed() or self.button_back.on_click(events):
            
            return MenuScene(self.game)
        if self.button_arrow_left.get_pressed() or self.button_arrow_left.on_click(
            events
        ):
            if self.current_image > 0:
                self.current_image -= 1
            self.time_hand, self.width = reset_time()
            self.button_arrow_left.set_pressed(False)
        if self.button_arrow_right.get_pressed() or self.button_arrow_right.on_click(
            events
        ):
            if self.current_image != len(self.images_group) - 1:
                self.current_image += 1
            self.time_hand, self.width = reset_time()
            self.button_arrow_right.set_pressed(False)

        return None

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
            self.time_hand = count(self.pressed_back)
        else:
            self.pressed_back = pygame.time.get_ticks()
        # ------------------------------------------
        if action == ">":
            self.time_hand = count(self.pressed_right)
        else:
            self.pressed_right = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "<":
            self.time_hand = count(self.pressed_left)
        else:
            self.pressed_left = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Act":
            self.time_hand = count(self.pressed_act)
        else:
            self.pressed_act = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Hist":
            self.time_hand = count(self.pressed_hist)
        else:
            self.pressed_hist = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Menu":
            self.time_hand = count(self.pressed_menu)
        else:
            self.pressed_menu = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if action == "":
            self.time_hand, self.width = reset_time()
        if self.time_hand >= settings.TIME_BUTTONS:
            if action == "Volver":
                self.button_back.set_pressed(True)
            elif action == "<":
                self.button_arrow_left.set_pressed(True)
            elif action == ">":
                self.button_arrow_right.set_pressed(True)
            elif action == "Act":
                self.button_act.set_pressed(True)
            elif action == "Hist":
                self.button_hist.set_pressed(True)
            elif action == "Menu":
                self.button_menu.set_pressed(True)

    def update(self, dt):
        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
