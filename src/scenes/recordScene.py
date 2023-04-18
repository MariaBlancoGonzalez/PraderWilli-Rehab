import pygame
import datetime
import os
from broker import Broker
from scenes.scene import Scene
import settings

from ui.gui import Button, DropDown, ImageButton
from ui.source import Source

from stats.pdfReport import MyDocTemplate
from pose_tracking.tracker_utils import *
from utils import *
from stats.calc import *
import stats.plots as plt


class RecordScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "RecordScene"
        self.current_user = game.current_user

        # Text
        self.historial = settings.FONTS["header"].render(
            "Historial", True, settings.BLACK
        )
        self.fontUnderline = settings.FONTS["arial_small"]
        self.fontUnderline.set_underline(True)
        self.no_data = self.fontUnderline.render(
            f"No hay datos disponibles", True, settings.BLACK
        )

        # Images
        self.imagePDF = pygame.image.load(settings.PDF)

        # Buttons
        self.button_back = Button((100, 20), "Volver", settings.AMARILLO)
        self.userDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            100,
            100,
            200,
            35,
            settings.FONTS["arial_small"],
            f"{game.current_user}",
            game.user_list,
        )

        self.exerDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            530,
            100,
            200,
            35,
            settings.FONTS["arial_small"],
            f"{game.exer_list[0]}",
            game.exer_list,
        )

        self.pdfDownload = ImageButton(self.imagePDF, (1170, 100), "pdf", (45, 45))
        self.button_group = [
            self.button_back,
            self.pdfDownload,
            self.exerDropDown,
            self.userDropDown,
        ]

        # Sources
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        # Initiate dropdown
        self.current_exer = self.exerDropDown.main
        self.id_exer = get_id(self.exerDropDown.main)
        self.id_user = get_id(self.game.current_user)

        # Get data
        self.tiempo = []
        self.izq_errores = []
        self.izq_aciertos = []
        self.drcha_errores = []
        self.drcha_aciertos = []
        self.get_data()

        # Variables to compute
        self.best_score, self.best_day = 0, 0
        self.media_total_fallos, self.media_total_aciertos = 0, 0
        self.media_errores_d, self.media_errores_i = 0, 0

        # This shouldnt be done here TODO
        if self.data != []:
            (
                self.tiempo,
                self.izq_errores,
                self.izq_aciertos,
                self.drcha_errores,
                self.drcha_aciertos,
            ) = distribute_data(self.data)

            self.estadisticas = self.fontUnderline.render(
                f"Estadisticas", True, settings.BLACK
            )

            self.best_score, self.best_day = get_best_score(self.data)
            self.media_total_aciertos = calculate_media_total(
                self.izq_aciertos, self.drcha_aciertos
            )
            self.media_total_fallos = calculate_media_total(
                self.izq_errores, self.drcha_errores
            )

            self.media_aciertos_d = calculate_media_parte(self.drcha_aciertos)
            self.media_aciertos_i = calculate_media_parte(self.izq_aciertos)

            self.media_errores_d = calculate_media_parte(self.drcha_errores)
            self.media_errores_i = calculate_media_parte(self.izq_errores)

            self.canvas_izq, self.raw_data_izq = plt.create_right_hand_two_lines(
                self.izq_errores, self.izq_aciertos, self.tiempo, "izquierda"
            )
            self.size_izq = self.canvas_izq.get_width_height()

            self.surf_izq = pygame.image.fromstring(
                self.raw_data_izq, self.size_izq, "RGB"
            )

            self.canvas_drcha, self.raw_data_drcha = plt.create_right_hand_two_lines(
                self.drcha_errores, self.drcha_aciertos, self.tiempo, "derecha"
            )
            self.size_drcha = self.canvas_drcha.get_width_height()

            self.surf_drcha = pygame.image.fromstring(
                self.raw_data_drcha, self.size_drcha, "RGB"
            )

        # Tracking time
        self.time_hand = 0
        self.pressed_back = pygame.time.get_ticks()

        # Progress bar
        self.bar_rect = pygame.Rect(40, (game.display.get_size()[1]) - 50, 700, 30)
        self.width = 0

    def get_data(self):
        broker = Broker()
        broker.connect()
        self.data = broker.get_score(self.id_exer, self.id_user, 10)
        broker.close()

    def events(self, events):
        self.userDropDown.update(events)
        self.game.current_user = self.userDropDown.main
        self.exerDropDown.update(events)
        if self.button_back.get_pressed() or self.button_back.on_click(events):
            from scenes.menuScene import MenuScene

            return MenuScene(self.game)
        if self.pdfDownload.on_click(events):
            user = self.current_user.split("-")[1]
            filename = f'{user}_{datetime.datetime.now().strftime("%d-%m")}.pdf'
            if not os.path.exists(os.path.isfile(filename)):
                with open(filename, "wb") as file:
                    file.write("")

            doc = MyDocTemplate(filename, self.id_user, self.id_exer)
            doc.create_doc(doc)
        return None

    def update(self, dt):
        if self.current_user != self.game.current_user:
            self.current_user = self.game.current_user
            self.id_exer = get_id(self.exerDropDown.main)
            self.id_user = get_id(self.current_user)
            self.get_data()

            if self.data != []:
                self.best_score, self.best_day = get_best_score(self.data)

                self.media_total_aciertos = calculate_media_total(
                    self.izq_aciertos, self.drcha_aciertos
                )
                self.media_total_fallos = calculate_media_total(
                    self.izq_errores, self.drcha_errores
                )

                self.media_aciertos_d = calculate_media_parte(self.drcha_aciertos)
                self.media_aciertos_i = calculate_media_parte(self.izq_aciertos)

                self.media_errores_d = calculate_media_parte(self.drcha_errores)
                self.media_errores_i = calculate_media_parte(self.izq_errores)

                self.canvas_izq, self.raw_data_izq = plt.create_right_hand_two_lines(
                    self.izq_errores, self.izq_aciertos, self.tiempo, "izquierda"
                )
                self.size_izq = self.canvas_izq.get_width_height()

                self.surf_izq = pygame.image.fromstring(
                    self.raw_data_izq, self.size_izq, "RGB"
                )

                (
                    self.canvas_drcha,
                    self.raw_data_drcha,
                ) = plt.create_right_hand_two_lines(
                    self.drcha_errores, self.drcha_aciertos, self.tiempo, "derecha"
                )
                self.size_drcha = self.canvas_drcha.get_width_height()

                self.surf_drcha = pygame.image.fromstring(
                    self.raw_data_drcha, self.size_drcha, "RGB"
                )

            else:
                self.best_score, self.best_day = 0, 0

        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self):
        # Backgroun colors
        self.game.display.fill(settings.GRANATE)
        pygame.draw.rect(
            self.game.display, settings.AMARILLO, pygame.Rect(40, 160, 1200, 560)
        )

        # Text
        self.game.display.blit(self.historial, (settings.WIDTH // 3 + 30, 10))

        if self.data != [] and self.game.current_user == self.current_user:
            self.mejor = settings.FONTS["arial_small"].render(
                f"-Mejor marca: {self.best_score}", True, settings.BLACK
            )
            self.dia = settings.FONTS["arial_small"].render(
                f"-Fecha: {self.best_day}", True, settings.BLACK
            )

            self.media_fallos = settings.FONTS["arial_small"].render(
                f"-Aciertos medios: {round(self.media_total_fallos,2)}",
                True,
                settings.BLACK,
            )
            self.media_aciertos = settings.FONTS["arial_small"].render(
                f"-Errores medios: {round(self.media_total_aciertos,2)}",
                True,
                settings.BLACK,
            )

            self.media_aciertos_dr = settings.FONTS["arial_small"].render(
                f"-Aciertos medios derecha: {round(self.media_aciertos_d,2)}",
                True,
                settings.BLACK,
            )
            self.media_aciertos_iz = settings.FONTS["arial_small"].render(
                f"-Aciertos medios izquierda: {round(self.media_aciertos_i,2)}",
                True,
                settings.BLACK,
            )

            self.media_err_dr = settings.FONTS["arial_small"].render(
                f"-Errores medios derecha: {round(self.media_errores_d,2)}",
                True,
                settings.BLACK,
            )
            self.media_err_iz = settings.FONTS["arial_small"].render(
                f"-Errores medios izquierda: {round(self.media_errores_i,2)}",
                True,
                settings.BLACK,
            )

            # Statistics rectangle
            self.rect_stats = pygame.Surface((370, 525))  # the size of your rect
            self.rect_stats.set_alpha(128)  # alpha level

            # this fills the entire surface
            self.rect_stats.fill((255, 255, 255))

            # Statistics
            self.game.display.blit(self.rect_stats, (840, 170))
            self.game.display.blit(self.surf_izq, (40, 160))
            self.game.display.blit(self.surf_drcha, (40, 430))
            self.game.display.blit(self.mejor, (870, 230))
            self.game.display.blit(self.estadisticas, (860, 180))
            self.game.display.blit(self.dia, (870, 280))
            self.game.display.blit(self.media_fallos, (870, 330))
            self.game.display.blit(self.media_aciertos, (870, 380))
            self.game.display.blit(self.media_aciertos_dr, (870, 430))
            self.game.display.blit(self.media_aciertos_iz, (870, 480))
            self.game.display.blit(self.media_err_dr, (870, 530))
            self.game.display.blit(self.media_err_iz, (870, 580))

        else:
            # If there is no data
            self.game.display.blit(self.no_data, (100, 200))

        # Buttons
        self.button_back.draw(self.game.display)
        self.pdfDownload.draw(self.game.display)
        self.userDropDown.draw(self.game.display)
        self.exerDropDown.draw(self.game.display)

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
