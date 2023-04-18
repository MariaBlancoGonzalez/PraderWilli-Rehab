import pygame
import settings

from scenes.scene import Scene
from broker import Broker

from ui.gui import InputBox, Button, DropDown
from ui.source import Source

from utils import *
from pose_tracking.tracker_utils import *
from scenes.menuScene import MenuScene


class OptionsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "OptionsScene"

        # Text
        self.options = settings.FONTS["header"].render("Opciones", True, settings.BLACK)
        self.txt_camara = settings.FONTS["small"].render(
            "Cambiar de fuente", True, settings.BLACK
        )
        self.txt_include_user = settings.FONTS["small"].render(
            "Incluir usuario en base de datos (Nombre/Apellido)", True, settings.BLACK
        )
        self.txt_delete_user = settings.FONTS["small"].render(
            "Eliminar usuario de la base de datos (Nombre/Apellido)",
            True,
            settings.BLACK,
        )
        # Input text box
        self.input_create_user = InputBox(100, 330, 200, 35, text="")
        self.input_create_surname = InputBox(350, 330, 200, 35, text="")
        self.input_delete_user = InputBox(100, 430, 200, 35, text="")
        self.input_delete_surname = InputBox(350, 430, 200, 35, text="")

        # Images

        # Buttons
        self.button_back = Button((170, 30), "Volver", settings.AMARILLO)
        self.button_apply = Button(
            (960, self.game.display.get_size()[1] - 130), "Aplicar"
        )
        self.camDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            100,
            230,
            200,
            35,
            settings.FONTS["arial_small"],
            f"{game.current_camara}",
            [f"{i}" for i in game.device_list],
        )
        self.button_group = [self.button_apply, self.button_back, self.camDropDown]

        # Sources
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        # Tracking time
        self.time_hand = 0
        self.pressed_back = pygame.time.get_ticks()

        # Progress bar
        self.bar_rect = pygame.Rect(40, (self.game.display.get_size()[1]) - 50, 700, 30)
        self.width = 0

    def draw(self):
        # Background
        self.game.display.fill(settings.GRANATE)
        pygame.draw.rect(
            self.game.display, settings.AMARILLO, pygame.Rect(40, 160, 1200, 560)
        )

        # Text
        self.game.display.blit(self.txt_camara, (100, 200))
        self.game.display.blit(self.txt_include_user, (100, 300))
        self.game.display.blit(self.txt_delete_user, (100, 400))
        self.game.display.blit(self.options, (settings.WIDTH // 3 + 30, 10))

        # Buttons
        self.button_apply.draw(self.game.display)
        self.button_back.draw(self.game.display)

        # Sources
        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)

        # Input text
        self.input_create_user.draw(self.game.display)
        self.input_create_surname.draw(self.game.display)
        self.input_delete_user.draw(self.game.display)
        self.input_delete_surname.draw(self.game.display)

        # DropDown
        self.camDropDown.draw(self.game.display)

        # Draw progress bar
        pygame.draw.rect(
            self.game.display,
            settings.WHITE,
            (41, (self.game.display.get_size()[1]) - 50, self.width, 30),
        )
        pygame.draw.rect(self.game.display, settings.BLACK, self.bar_rect, 2)

    def include_user(self, name, surname):
        broker = Broker()
        broker.connect()
        broker.add_user(name, surname)
        broker.close()

    def delete_user(self, name, surname):
        broker = Broker()
        broker.connect()
        broker.delete_user(name, surname)
        broker.close()

    def events(self, events):
        self.input_create_user.handle_event(events)
        self.input_create_surname.handle_event(events)
        self.input_delete_user.handle_event(events)
        self.input_delete_surname.handle_event(events)
        self.camDropDown.update(events)
        if self.button_back.get_pressed() or self.button_back.on_click(events):
            return MenuScene(self.game)
        if self.button_apply.get_pressed() or self.button_apply.on_click(events):
            cam = int(self.camDropDown.getMain())
            if self.game.current_camara != cam:
                self.game.change_camara(cam)

            self.include_user(
                self.input_create_user.get_text(), self.input_create_surname.get_text()
            ) if self.input_create_user.get_text() != "" and self.input_create_surname.get_text() != "" else None
            self.input_create_user.reset()
            self.input_create_surname.reset()

            self.delete_user(
                self.input_delete_user.get_text(), self.input_delete_surname.get_text()
            ) if self.input_delete_user.get_text() != "" and self.input_delete_surname.get_text() != "" else None
            self.input_delete_user.reset()
            self.input_delete_surname.reset()

            self.game.get_users()
        return None

    def check_collide(self, left, right):
        if self.button_back.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_back.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Volver"

        return ""

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

        self.width = self.time_hand * coefficient

        if action == "":
            self.time_hand, self.width = reset_time()

        if self.time_hand > settings.TIME_BUTTONS:
            if action == "Volver":
                self.button_back.set_pressed(True)

    def update(self, dt):
        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
