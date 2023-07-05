import pygame

from broker import DataBroker
from scenes.scene import Scene
import settings.settings as settings
from settings.settings_0 import ID_DIAGONALES, EXER_0_JSON
from settings.settings_1 import ID_SQUAD, EXER_1_JSON
from settings.settings_2 import ID_BALLS, EXER_2_JSON

from ui.gui import Button, DropDown, ImageButton
from ui.source import Source
from ui.table import Tabla

from tracking.tracker_utils import *

from utils import *
from stats.calc import *
import stats.plots as plt
from stats.stats import Stats

class RecordScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "RecordScene"

        # Text
        self.historial = settings.FONTS["header"].render("Historial", True, settings.BLACK)
        self.fontUnderline = settings.FONTS["arial_small"]
        
        self.no_data = self.fontUnderline.render(f"No hay datos disponibles", True, settings.BLACK)
        self.estadisticas = self.fontUnderline.render(f"Estadisticas", True, settings.BLACK)

        # Buttons
        self.button_back = Button((100, 20), "Volver", settings.AMARILLO, 200, settings.BLACK)
        self.button_datos = Button((self.game.display.get_size()[0]*0.75, 20), "Ver datos", settings.AMARILLO, 200, settings.BLACK)
        self.userDropDown = DropDown(
            [settings.GRISCLARO, settings.WHITE],
            [settings.WHITE, settings.GRISCLARO],
            self.game.display.get_size()[0]*0.1,
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
            self.game.display.get_size()[0]*0.45,
            110,
            200,
            35,
            settings.FONTS["arial_small"],
            f"{game.exer_list[0]}",
            game.exer_list,
        )
        self.button_arrow_left = Button((45, self.game.display.get_size()[1]*0.55), "<", settings.GRANATE, 50)
        self.button_arrow_right = Button((self.game.display.get_size()[0]-100, self.game.display.get_size()[1]*0.55), ">", settings.GRANATE, 50)

        self.button_group = [self.button_back,self.button_datos,self.exerDropDown,self.userDropDown,self.button_arrow_left,self.button_arrow_right]

        # Sources
        self.right_source = Source(self.game.display, settings.MANO_DERECHA)
        self.left_source = Source(self.game.display, settings.MANO_IZQUIERDA)
        self.hands = pygame.sprite.Group([self.right_source, self.left_source])
        self.action = ""
        # Initiate dropdown
        self.current_exer = self.exerDropDown.main
        self.current_user = game.current_user
        self.id_exer = get_id(self.exerDropDown.main)

        self.redim = False
        if self.game.display.get_size()[1] > 800:
            self.space = 50
            self.rect_height = 725
            self.graph_dim = [12, 3]
            self.pos_y = 400
        else:
            self.space = 35
            self.rect_height = 525
            self.graph_dim = [8, 2.8]
            self.pos_y = 273

        if int(self.id_exer) == ID_DIAGONALES:
            self.current_activity_object = Stats(self.id_exer, game.display, EXER_0_JSON)
        elif int(self.id_exer) == ID_BALLS:
            self.current_activity_object = Stats(self.id_exer, game.display, EXER_2_JSON)
        elif int(self.id_exer) == ID_SQUAD:
            self.current_activity_object = Stats(self.id_exer, game.display, EXER_1_JSON)
        self.current_activity_object.create_measures(self.graph_dim)
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
        self.new_dim = False
        self.page = 0
    def resized(self):
        
        if self.game.display.get_size()[1] > 800:
            self.space = 50
            self.rect_height = 680
            self.graph_dim = [12, 3]
            self.pos_y = 400
            self.new_dim = True
        else:
            self.space = 35
            self.rect_height = 525
            self.graph_dim = [8, 2.8]
            self.pos_y = 273
            self.new_dim = True

        self.bar_rect = pygame.Rect(40, (self.game.display.get_size()[1]) - 50, 700, 30)
        self.button_datos.change_pos((self.game.display.get_size()[0]*0.75,20))

        self.button_arrow_left.change_pos((45, self.game.display.get_size()[1]*0.55),50)
        self.button_arrow_right.change_pos((self.game.display.get_size()[0]-100, self.game.display.get_size()[1]*0.55),50)

        self.userDropDown.change_pos(self.game.display.get_size()[0]*0.1,110,200,35)
        self.exerDropDown.change_pos(self.game.display.get_size()[0]*0.45,110,200,35)

        self.redim = True
        

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

        if self.current_user != self.userDropDown.main or self.current_exer != self.exerDropDown.main:
            self.current_user = self.userDropDown.main
            self.current_exer = self.exerDropDown.main
            self.id_exer = get_id(self.current_exer)

            if int(self.id_exer) == ID_DIAGONALES:
                self.current_activity_object = Stats(self.id_exer, self.game.display, EXER_0_JSON)
            elif int(self.id_exer) == ID_BALLS:
                self.current_activity_object = Stats(self.id_exer, self.game.display, EXER_2_JSON)
            elif int(self.id_exer) == ID_SQUAD:
                self.current_activity_object = Stats(self.id_exer, self.game.display, EXER_1_JSON)
           
            self.current_activity_object.create_measures(self.graph_dim)
            self.current_activity_object.create_table(0)

        pos = pygame.mouse.get_pos()
        if any(button.rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return None

    def render(self):
        # Background colors
        self.game.display.fill(settings.GRANATE)
        pygame.draw.rect(self.game.display, settings.AMARILLO, pygame.Rect(40, 160, self.game.display.get_size()[0]-80, self.game.display.get_size()[1]-220))
        for i in range(4):
            # Rectangulo grande
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (40, 160, self.game.display.get_size()[0]-80, self.game.display.get_size()[1]-220), 2)

        # Text
        self.game.display.blit(self.historial, (self.game.display.get_size()[0]*0.4, 10))

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
            if self.new_dim:
                self.current_activity_object.graphs = []
                self.current_activity_object.stats = []
                self.current_activity_object.create_measures(self.graph_dim)
            self.fontUnderline.set_underline(True)
            if self.ver_datos == False:
                # Draw graphs and stats depending on the game
                # Statistics rectangle
                rect_stats = pygame.Surface((370, self.rect_height))  # the size of your rect
                rect_stats.set_alpha(128)  # alpha level
                # this fills the entire surface
                rect_stats.fill((255, 255, 255))
                self.game.display.blit(rect_stats, (self.game.display.get_size()[0]-450, 170))

                if int(self.id_exer) == ID_DIAGONALES:
                    # Gráficas
                    stats = self.current_activity_object.stats
                    graphs = self.current_activity_object.graphs

                    self.game.display.blit(graphs[0][1], (42, 162))
                    self.game.display.blit(graphs[1][1], (42, 162+self.pos_y))

                    # Statistics
                    self.game.display.blit(self.estadisticas, (self.game.display.get_size()[0]-420, 180))
                    
                    counter = 230
                    for i in range(len(stats)):
                        self.game.display.blit(settings.FONTS["arial_small"].render(
                            f"{stats[i][0]} {stats[i][1]}",
                            True,
                            settings.BLACK,
                        ), (self.game.display.get_size()[0]-410, counter))
                        counter += self.space

                elif int(self.id_exer) == ID_SQUAD:
                    graphs = self.current_activity_object.graphs
                    stats = self.current_activity_object.stats

                    # Gráficas
                    self.game.display.blit(graphs[0][1], (42, 162))
                    self.game.display.blit(graphs[1][1], (42, 162+self.pos_y))

                    # Statistics
                    self.game.display.blit(self.estadisticas, (self.game.display.get_size()[0]-420, 180))

                    counter = 230
                    for i in range(len(stats)):
                        self.game.display.blit(settings.FONTS["arial_small"].render(
                            f"{stats[i][0]} {stats[i][1]}",
                            True,
                            settings.BLACK,
                        ), (self.game.display.get_size()[0]-410, counter))
                        counter += self.space

                elif int(self.id_exer) == ID_BALLS:
                    stats = self.current_activity_object.stats
                    graphs = self.current_activity_object.graphs
                    # Gráficas
                    self.game.display.blit(graphs[0][1], (42, 162))

                    # Statistics
                    self.game.display.blit(self.estadisticas, (self.game.display.get_size()[0]-420, 180))

                    counter = 230
                    for i in range(len(stats)-2):
                        self.game.display.blit(settings.FONTS["arial_small"].render(
                            f"{stats[i][0]} {stats[i][1]}",
                            True,
                            settings.BLACK,
                        ), (self.game.display.get_size()[0]-410, counter))
                        counter += self.space

                    self.game.display.blit(settings.FONTS["arial_small"].render(
                        f"{stats[len(stats)-2][0]} {stats[len(stats)-2][1]}",
                        True,
                        settings.BLACK,
                    ), (130, self.game.display.get_size()[1]-250))
                    self.game.display.blit(settings.FONTS["arial_small"].render(
                        f"{stats[len(stats)-1][0]} {stats[len(stats)-1][1]}",
                        True,
                        settings.BLACK,
                    ), (130, self.game.display.get_size()[1]-200))

                    self.game.display.blit(settings.FONTS["arial_small"].render(
                        f"*Los registros recogidos la misma fecha con el mismo tiempo se muestran acumulados",
                        True,
                        settings.BLACK,
                    ), (120, self.game.display.get_size()[1]-150))

            else:
                # Dibujar la tabla
                if self.redim == True:
                    self.current_activity_object.table.change_window(self.game.display)
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
        self.new_dim = False

    def update(self, frame):
        self.pose_tracker.pose_tracking(frame)

        coefficient = settings.WIDTH_LOAD_BAR / settings.TIME_BUTTONS
        left_hand, right_hand = get_hands_points(self.pose_tracker.landmark_process)

        self.left_source.update_position(left_hand)
        self.right_source.update_position(right_hand)

        # Colisiones
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
        if pygame.sprite.spritecollideany(self.button_datos, self.hands) != None:
            self.time_hand = count(self.pressed_datos)
            self.action = "Datos"
        else:
            self.pressed_datos = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient

        if self.action == "":
            self.time_hand, self.width = reset_time()

        if self.time_hand > settings.TIME_BUTTONS:
            if self.action == "Volver":
                self.button_back.set_pressed(True)
            elif self.action == "Datos":
                self.ver_datos = True if self.ver_datos == False else False
                if self.ver_datos:
                    self.button_datos.change_text("Visualizaciones")
                else:
                    self.button_datos.change_text("Ver datos")
                self.pressed_datos = pygame.time.get_ticks()
            elif self.action == "<":
                self.button_arrow_left.set_pressed(True)
            elif self.action == ">":
                self.button_arrow_right.set_pressed(True)
            self.time_hand, self.width = reset_time()
        self.action = ""

    def change_inches(self, fig):
        return fig.set_size_inches(self.graph_dim[0], self.graph_dim[1])