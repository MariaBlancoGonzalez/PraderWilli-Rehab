import pygame

from broker import No_DB
from scenes.scene import Scene
import settings

from ui.gui import Button, DropDown, ImageButton
from ui.source import Source
from ui.table import Tabla

from pose_tracking.tracker_utils import *
from utils import *
from stats.calc import *
import stats.plots as plt
from stats.diagonalesStats import DiagonalesStats
from stats.squadStats import SquadStats
from stats.ballsStats import BallStats

class RecordScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "RecordScene"

        # Text
        self.historial = settings.FONTS["header"].render(
            "Historial", True, settings.BLACK
        )
        self.fontUnderline = settings.FONTS["arial_small"]
        
        self.no_data = self.fontUnderline.render(
            f"No hay datos disponibles", True, settings.BLACK
        )
        self.estadisticas = self.fontUnderline.render(
            f"Estadisticas", True, settings.BLACK
        )
        # Images
        self.imagePDF = pygame.image.load(settings.PDF)

        # Buttons
        self.button_back = Button((100, 20), "Volver", settings.AMARILLO)
        self.button_datos = Button((950, 20), "Ver datos", settings.AMARILLO)
        self.userDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            100,
            110,
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
            110,
            200,
            35,
            settings.FONTS["arial_small"],
            f"{game.exer_list[0]}",
            game.exer_list,
        )
        self.button_arrow_left = Button(
            (45, settings.HEIGHT // 2), "<", settings.GRANATE, 50
        )
        self.button_arrow_right = Button(
            (1178, settings.HEIGHT // 2), ">", settings.GRANATE, 50
        )

        self.button_group = [
            self.button_back,
            self.button_datos,
            self.exerDropDown,
            self.userDropDown,
            self.button_arrow_left,
            self.button_arrow_right,
        ]

        # Sources
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        # Initiate dropdown
        self.current_exer = self.exerDropDown.main
        self.current_user = game.current_user
        self.id_exer = get_id(self.exerDropDown.main)
        self.id_user = get_id(self.game.current_user)

        if int(self.id_exer) == settings.ID_DIAGONALES:
            self.current_activity_object = DiagonalesStats(game.current_user, self.id_exer, self.id_user, game.display)
        elif int(self.id_exer) == settings.ID_BALLS:
            self.current_activity_object = BallStats(game.current_user, self.id_exer, self.id_user, game.display)
        elif int(self.id_exer) == settings.ID_SQUAD:
            self.current_activity_object = SquadStats(game.current_user, self.id_exer, self.id_user, game.display)
        self.current_activity_object.create_measures()
        self.current_activity_object.create_table(0)

        self.ver_datos = False
        # Tracking time
        self.time_hand = 0
        self.pressed_back = pygame.time.get_ticks()
        self.pressed_right = pygame.time.get_ticks()
        self.pressed_left = pygame.time.get_ticks()
        self.pressed_datos = pygame.time.get_ticks()

        # Progress bar
        self.bar_rect = pygame.Rect(40, (game.display.get_size()[1]) - 50, 700, 30)
        self.width = 0

        self.page = 0

    def events(self, events):
        self.userDropDown.update(events)
        self.exerDropDown.update(events)

        if self.button_back.get_pressed() or self.button_back.on_click(events):
            from scenes.menuScene import MenuScene
            return MenuScene(self.game)

        if self.button_datos.get_pressed() or self.button_datos.on_click(events):
            self.ver_datos = True if self.ver_datos == False else False
            if self.ver_datos:
                self.button_datos.change_text("Visualizaciones")
            else:
                self.button_datos.change_text("Ver datos")

        if self.button_arrow_left.get_pressed() or self.button_arrow_left.on_click(
            events
        ):
            self.current_activity_object.table.update_page(-1)
            self.time_hand, self.width = reset_time()
            self.button_arrow_left.set_pressed(False)
        if self.button_arrow_right.get_pressed() or self.button_arrow_right.on_click(
            events
        ):
            self.current_activity_object.table.update_page(1)
            self.time_hand, self.width = reset_time()
            self.button_arrow_right.set_pressed(False)

        return None

    def update(self, dt):
        if self.current_user != self.userDropDown.main or self.current_exer != self.exerDropDown.main:
            self.current_user = self.userDropDown.main
            self.id_user = get_id(self.current_user)
            self.current_exer = self.exerDropDown.main
            self.id_exer = get_id(self.current_exer)

            if int(self.id_exer) == settings.ID_DIAGONALES:
                self.current_activity_object = DiagonalesStats(
                    self.current_user, self.id_exer, self.id_user, self.game.display)
            elif int(self.id_exer) == settings.ID_BALLS:
                self.current_activity_object = BallStats(
                    self.current_user, self.id_exer, self.id_user, self.game.display)
            elif int(self.id_exer) == settings.ID_SQUAD:
                self.current_activity_object = SquadStats(
                    self.current_user, self.id_exer, self.id_user, self.game.display)
            self.current_activity_object.create_measures()
            self.current_activity_object.create_table(0)

        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self):
        # Background colors
        self.game.display.fill(settings.GRANATE)
        pygame.draw.rect(self.game.display, settings.AMARILLO, pygame.Rect(40, 160, 1200, 560))
        for i in range(4):
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (40, 160, 1200, 560), 2)
        # Text
        self.game.display.blit(self.historial, (settings.WIDTH // 3 + 30, 10))

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

        if self.current_activity_object.data != []:
            self.fontUnderline.set_underline(True)
            if self.ver_datos == False:
                # Draw graphs and stats depending on the game
                # Statistics rectangle
                rect_stats = pygame.Surface((370, 525))  # the size of your rect
                rect_stats.set_alpha(128)  # alpha level
                # this fills the entire surface
                rect_stats.fill((255, 255, 255))
                self.game.display.blit(rect_stats, (840, 170))

                if int(self.id_exer) == settings.ID_DIAGONALES:
                    stats = self.current_activity_object.stats
                    graphs = self.current_activity_object.graphs
                    
                    # Gráficas
                    self.game.display.blit(graphs[0][1], (42, 162))
                    self.game.display.blit(graphs[1][1], (42, 435))

                    # Statistics
                    self.game.display.blit(self.estadisticas, (860, 180))
                    
                    counter = 230
                    for i in range(len(stats)):
                        self.game.display.blit(settings.FONTS["arial_small"].render(
                            f"{stats[i][0]} {stats[i][1]}",
                            True,
                            settings.BLACK,
                        ), (870, counter))
                        counter += 50

                elif int(self.id_exer) == settings.ID_SQUAD:
                    graphs = self.current_activity_object.graphs
                    stats = self.current_activity_object.stats

                    # Gráficas
                    self.game.display.blit(graphs[0][1], (42, 162))
                    self.game.display.blit(graphs[1][1], (42, 435))

                    # Statistics
                    self.game.display.blit(self.estadisticas, (860, 180))

                    counter = 230
                    for i in range(len(stats)):
                        self.game.display.blit(settings.FONTS["arial_small"].render(
                            f"{stats[i][0]} {stats[i][1]}",
                            True,
                            settings.BLACK,
                        ), (870, counter))
                        counter += 50

                elif int(self.id_exer) == settings.ID_BALLS:
                    stats = self.current_activity_object.stats
                    graphs = self.current_activity_object.graphs
                    # Gráficas
                    self.game.display.blit(graphs[0][1], (42, 182))

                    # Statistics
                    self.game.display.blit(self.estadisticas, (860, 180))

                    counter = 230
                    for i in range(len(stats)-2):
                        self.game.display.blit(settings.FONTS["arial_small"].render(
                            f"{stats[i][0]} {stats[i][1]}",
                            True,
                            settings.BLACK,
                        ), (870, counter))
                        counter += 50

                    self.game.display.blit(settings.FONTS["arial_small"].render(
                        f"{stats[len(stats)-2][0]} {stats[len(stats)-2][1]}",
                        True,
                        settings.BLACK,
                    ), (130, 570))
                    self.game.display.blit(settings.FONTS["arial_small"].render(
                        f"{stats[len(stats)-1][0]} {stats[len(stats)-1][1]}",
                        True,
                        settings.BLACK,
                    ), (130, 620))

                    self.game.display.blit(settings.FONTS["arial_small"].render(
                        f"*Los registros recogidos la misma fecha con el mismo tiempo se muestran acumulados",
                        True,
                        settings.BLACK,
                    ), (120, 680))

            else:
                # Dibujar la tabla
                self.fontUnderline.set_underline(False)
                self.current_activity_object.table.dibujar(self.page)
                self.button_arrow_left.draw(self.game.display)
                self.button_arrow_right.draw(self.game.display)
        else:
            self.game.display.blit(settings.FONTS["arial_small"].render(
                f"No hay datos disponibles",
                True,
                settings.BLACK,
            ), (120, 180))

        # Buttons
        self.button_back.draw(self.game.display)
        self.button_datos.draw(self.game.display)
        self.userDropDown.draw(self.game.display)
        self.exerDropDown.draw(self.game.display)

    def check_collide(self, left, right):
        if self.button_back.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_back.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Volver"
        elif self.button_datos.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_datos.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Datos"
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
        if action == "Datos":
            self.time_hand = count(self.pressed_datos)
        else:
            self.pressed_datos = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if action == "":
            self.time_hand, self.width = reset_time()

        if self.time_hand > settings.TIME_BUTTONS:
            if action == "Volver":
                self.button_back.set_pressed(True)
            elif action == "Datos":
                self.ver_datos = True if self.ver_datos == False else False
                if self.ver_datos:
                    self.button_datos.change_text("Visualizaciones")
                else:
                    self.button_datos.change_text("Ver datos")
                self.pressed_datos = pygame.time.get_ticks()
            elif action == "<":
                self.button_arrow_left.set_pressed(True)
            elif action == ">":
                self.button_arrow_right.set_pressed(True)
            self.time_hand, self.width = reset_time()