import pygame
from scenes.scene import Scene
import settings.settings as settings
from ui.gui import Button
from ui.source import Source
from tracking.tracker_utils import *
from utils import *

from scenes.menuScene import MenuScene

class TutorialScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "TutorialScene"

        # Text
        self.tutorial = settings.FONTS["header"].render("Tutorial", True, settings.BLACK)

        # Imágenes
        self.historial = cargar_archivos_folder(settings.HISTORIAL, (self.game.display.get_size()[0]*0.7,self.game.display.get_size()[0]*0.4))
        self.actividades = cargar_archivos_folder(settings.ACTIVIDADES, (self.game.display.get_size()[0]*0.7,self.game.display.get_size()[0]*0.4))
        self.menu = cargar_archivos_folder(settings.MENU, (self.game.display.get_size()[0]*0.7,self.game.display.get_size()[0]*0.4))
        # Tutorial images
        self.images_group = self.menu
        self.current_image_name = 'Menu'
        # Needed variables
        self.current_image = 0

        # Buttons
        self.button_back = Button((170, 30), "Volver", settings.AMARILLO, 200, settings.BLACK)
        self.button_arrow_left = Button(
            (45, self.game.display.get_size()[1]*0.55), "<", settings.GRANATE, 50
        )
        self.button_arrow_right = Button(
            (self.game.display.get_size()[0]-100, self.game.display.get_size()[1]*0.55), ">", settings.GRANATE, 50
        )

        self.button_act = Button((self.game.display.get_size()[0]*0.45, 100), "Actividades", settings.AMARILLO,200,settings.BLACK)
        self.button_hist = Button((self.game.display.get_size()[0]*0.75, 100), "Historial", settings.AMARILLO,200,settings.BLACK)
        self.button_menu = Button((self.game.display.get_size()[0]*0.15, 100), "Menú", settings.AMARILLO,200,settings.BLACK)

        self.button_group = [
            self.button_back,
            self.button_arrow_left,
            self.button_arrow_right,
            self.button_hist,
            self.button_act,
            self.button_menu,
        ]
        # Sources
        self.right_source = Source(self.game.display, settings.MANO_DERECHA)
        self.left_source = Source(self.game.display, settings.MANO_IZQUIERDA)
        self.hands = pygame.sprite.Group([self.right_source, self.left_source])
        self.action = ""

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

    def resized(self):
        self.bar_rect = pygame.Rect(40, (self.game.display.get_size()[1]) - 50, 700, 30)

        self.button_arrow_left.change_pos((45, self.game.display.get_size()[1]*0.55),50)
        self.button_arrow_right.change_pos((self.game.display.get_size()[0]-100, self.game.display.get_size()[1]*0.55),50)

        self.button_act.change_pos((self.game.display.get_size()[0]*0.45,100))
        self.button_hist.change_pos((self.game.display.get_size()[0]*0.75,100))
        self.button_menu.change_pos((self.game.display.get_size()[0]*0.15,100))

        self.historial = cargar_archivos_folder(settings.HISTORIAL, (self.game.display.get_size()[0]*0.7,self.game.display.get_size()[0]*0.4))
        self.actividades = cargar_archivos_folder(settings.ACTIVIDADES, (self.game.display.get_size()[0]*0.7,self.game.display.get_size()[0]*0.4))
        self.menu = cargar_archivos_folder(settings.MENU, (self.game.display.get_size()[0]*0.7,self.game.display.get_size()[0]*0.4))
       
        if self.current_image_name == 'Menu':
            self.images_group = self.menu
        elif self.current_image_name == 'Actividades':
            self.images_group = self.actividades
        elif self.current_image_name == 'Historial':
            self.images_group = self.historial

    def render(self):
        # Backgrounds
        self.game.display.fill(settings.GRANATE)
        pygame.draw.rect(self.game.display, settings.AMARILLO, pygame.Rect(40, 160, self.game.display.get_size()[0]-80, self.game.display.get_size()[1]-220))
        for i in range(4):
            # Rectangulo grande
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (40, 160, self.game.display.get_size()[0]-80, self.game.display.get_size()[1]-220), 2)

        # Text
        self.game.display.blit(self.tutorial, (self.game.display.get_size()[0]*0.4, 10))

        # Buttons
        self.button_back.draw(self.game.display)
        self.button_arrow_left.draw(self.game.display)
        self.button_arrow_right.draw(self.game.display)
        self.button_act.draw(self.game.display)
        self.button_hist.draw(self.game.display)
        self.button_menu.draw(self.game.display)

        # For show current video
        self.game.display.blit(self.images_group[self.current_image], (self.game.display.get_size()[0]*0.15, 180))

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
            self.current_image_name = 'Actividades'
        if self.button_hist.get_pressed() or self.button_hist.on_click(events):
            self.images_group = self.historial
            self.current_image = 0
            self.current_image_name = 'Historial'
        if self.button_menu.get_pressed() or self.button_menu.on_click(events):
            self.images_group = self.menu
            self.current_image = 0
            self.current_image_name = 'Menu'
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
        if pygame.sprite.spritecollideany(self.button_back, self.hands) != None:
            self.time_hand = count(self.pressed_back)
            self.action = "Volver"
        else:
            self.pressed_back = pygame.time.get_ticks()
        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_arrow_right, self.hands) != None:
            self.time_hand = count(self.pressed_right)
            self.action = ">"
        else:
            self.pressed_right = pygame.time.get_ticks()
        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_arrow_left, self.hands) != None:
            self.time_hand = count(self.pressed_left)
            self.action = "<"
        else:
            self.pressed_left = pygame.time.get_ticks()
        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_act, self.hands) != None:
            self.time_hand = count(self.pressed_act)
            self.action = "Act"
        else:
            self.pressed_act = pygame.time.get_ticks()
        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_hist, self.hands) != None:
            self.time_hand = count(self.pressed_hist)
            self.action = "Hist"
        else:
            self.pressed_hist = pygame.time.get_ticks()
        # ------------------------------------------
        if pygame.sprite.spritecollideany(self.button_menu, self.hands) != None:
            self.time_hand = count(self.pressed_menu)
            self.action = "Menu"
        else:
            self.pressed_menu = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if self.time_hand >= settings.TIME_BUTTONS:
            if self.action == "Volver":
                self.button_back.set_pressed(True)
            elif self.action == "<":
                self.button_arrow_left.set_pressed(True)
            elif self.action == ">":
                self.button_arrow_right.set_pressed(True)
            elif self.action == "Act":
                self.button_act.set_pressed(True)
            elif self.action == "Hist":
                self.button_hist.set_pressed(True)
            elif self.action == "Menu":
                self.button_menu.set_pressed(True)
            self.time_hand, self.width = reset_time()
            self.reset_timer_after()
        
        if self.action == "":
            self.time_hand, self.width = reset_time()

        self.action=""

    def reset_timer_after(self):
        self.pressed_back = pygame.time.get_ticks()
        self.pressed_right = pygame.time.get_ticks()
        self.pressed_left = pygame.time.get_ticks()
        self.pressed_act = pygame.time.get_ticks()
        self.pressed_hist = pygame.time.get_ticks()
        self.pressed_menu = pygame.time.get_ticks()