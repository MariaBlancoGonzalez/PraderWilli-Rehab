import pygame
import settings
from scenes.scene import Scene

from ui.gui import Button, ImageButton, InputNumberBox
from ui.source import Source

from utils import *

class ActivitiesScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = 'ActivitiesScene'

        # Text
        self.activities = settings.FONTS['header'].render(
            "Actividades", True, settings.BLACK)
        self.txt_modificadores = settings.FONTS['medium'].render(
            "Modificadores.", True, settings.BLACK)
        self.txt_time = settings.FONTS['small'].render(
            "Tiempo de juego (segundos)", True, settings.BLACK)
        self.txt_diagonales = settings.FONTS['small'].render(
            "Diagonales superiores", True, settings.BLACK)
        self.txt_time_appear = settings.FONTS['small'].render(
            "Tiempo en el que los elementos aparecen", True, settings.BLACK)
        self.txt_change_mano = settings.FONTS['small'].render(
            "Elegir miniatura de manos", True, settings.BLACK)
        self.txt_change_acierto = settings.FONTS['small'].render(
            "Elegir miniatura aciertos", True, settings.BLACK)
        self.txt_change_error = settings.FONTS['small'].render(
            "Elegir miniatura error", True, settings.BLACK)

        # Images
        img_diagonales = pygame.image.load(settings.MINIATURA_DIAGONALES)
        img_modify = pygame.image.load(settings.MODIFY)

        # Buttons
        self.diagonales = ImageButton(
            img_diagonales, (150, 150), 'diagonales', (200, 200))
        self.button_modify = ImageButton(
            img_modify, (230, 390), 'modificar', (30, 30))
        self.button_calibrate = Button(
            (970, 30), "Calibrar", settings.AMARILLO)
        self.button_back = Button((170, 30), "Volver", settings.AMARILLO)
        self.button_apply = Button(
            (900, self.game.display.get_size()[1]-180), 'Aplicar')
        self.button_group = [self.button_back, self.button_calibrate,
                             self.button_modify, self.diagonales, self.button_apply]

        # Sources
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        # About modifiers
        self.modify_components = False

        # Input text
        self.input_time = InputNumberBox(100, 520, 200, 35, text='')
        self.input_time_appear = InputNumberBox(100, 590, 200, 35, text='')

        # Tracking time
        self.time_hand = 0
        self.pressed_diagonales = pygame.time.get_ticks()
        self.pressed_calibrate = pygame.time.get_ticks()
        self.pressed_apply = pygame.time.get_ticks()
        self.pressed_back = pygame.time.get_ticks()

        # Progress bar
        self.bar_rect = pygame.Rect(
            100, (self.game.display.get_size()[1])-90, 700, 30)
        self.width = 0

    def draw(self):
        self.game.display.fill(settings.GRANATE)

        pygame.draw.rect(self.game.display, settings.AMARILLO,
                         pygame.Rect(50, 100, 1180, 650))
        self.button_calibrate.draw(self.game.display)
        self.button_back.draw(self.game.display)
        self.button_modify.draw(self.game.display)
        self.game.display.blit(self.activities, (settings.WIDTH//3, 10))

        self.game.display.blit(self.txt_diagonales, (150, 360))
        self.diagonales.draw(self.game.display)
        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)

        # Modificadores
        if self.modify_components:
            self.game.display.blit(self.txt_modificadores, (100, 450))
            self.game.display.blit(self.txt_time, (100, 490))
            self.input_time.draw(self.game.display)
            self.game.display.blit(self.txt_time_appear, (100, 560))
            self.input_time_appear.draw(self.game.display)
            self.button_apply.draw(self.game.display)
        # Draw progress bar
        pygame.draw.rect(self.game.display, settings.WHITE, (101,
                         (self.game.display.get_size()[1])-90, self.width, 30))
        pygame.draw.rect(self.game.display, settings.BLACK, self.bar_rect, 2)

    def events(self, events):

        if self.diagonales.on_click(events) or self.diagonales.get_clicked_state():
            self.diagonales.clicked = True
            from scenes.diagonalesScene import DiagonalsScene
            return DiagonalsScene(self.game)
        if self.button_back.get_pressed() or self.button_back.on_click(events):
            from scenes.menuScene import MenuScene
            return MenuScene(self.game)
        if self.button_modify.on_click(events):
            self.modify_components = True
        if self.button_calibrate.get_pressed() or self.button_calibrate.on_click(events):
            from scenes.calibrationScene import CalibrationScene
            return CalibrationScene(self.game)
        if self.button_apply.get_pressed() or self.button_apply.on_click(events):
            # TODO aplicar cambios de modify (si no hay nada no)
            settings.TIEMPO_JUEGO = int(self.input_time.get_text(
            )) if self.input_time.get_text() != "" else settings.TIEMPO_JUEGO
            settings.VELOCIDAD_ENTRE_BOLAS = int(self.input_time_appear.get_text(
            )) if self.input_time_appear.get_text() != "" else settings.VELOCIDAD_ENTRE_BOLAS
            self.input_time.reset()
            self.input_time_appear.reset()
            self.modify_components = False
            self.button_modify.update()
        if self.modify_components:
            self.input_time.handle_event(events)
            self.input_time_appear.handle_event(events)
        return None

    def check_collide(self, left, right):
        if self.diagonales.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.diagonales.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Diagonales"
        elif self.button_calibrate.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_calibrate.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Calibrate"
        elif self.button_back.top_rect.collidepoint(left.rect.centerx, left.rect.centery) or self.button_back.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
            return "Volver"

        return ""

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
        if action == "Diagonales":
            self.time_hand = self.count(self.pressed_diagonales)
        else:
           self.pressed_diagonales = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Calibrate":
            self.time_hand = self.count(self.pressed_calibrate)
        else:
            self.pressed_calibrate = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Aplicar":
            self.time_hand = self.count(self.pressed_apply)
        else:
            self.pressed_apply = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Volver":
            self.time_hand = self.count(self.pressed_back)
        else:
            self.pressed_back = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if action == "":
            self.reset_time()
        if self.time_hand >= settings.TIME_BUTTONS:
            if action == "Diagonales":
                self.diagonales.set_clicked_true()
            elif action == "Calibrate":
                self.button_calibrate.set_pressed(True)
            elif action == "Aplicar":
                self.button_apply.set_pressed(True)
            elif action == "Volver":
                self.button_back.set_pressed(True)

    def update(self, dt):
        self.diagonales.update()
        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
