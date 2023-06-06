import pygame

import settings
from scenes.scene import Scene
from pose_tracking.tracker_utils import *
from ui.gui import Button, ImageButton, InputNumberBox
from ui.source import Source

from utils import *

class ActivitiesScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self._name_scene = "ActivitiesScene"

        # Text
        self.activities = settings.FONTS["header"].render(
            "Actividades", True, settings.BLACK
        )
        self.txt_modificadores = settings.FONTS["medium"].render(
            "Modificadores.", True, settings.BLACK
        )
        self.txt_time = settings.FONTS["small"].render(
            "Tiempo de juego (segundos)", True, settings.BLACK
        )
        self.txt_diagonales = settings.FONTS["small"].render(
            "Diagonales superiores", True, settings.BLACK
        )
        self.txt_squad = settings.FONTS["small"].render(
            "Sentadillas", True, settings.BLACK
        )
        self.txt_balls = settings.FONTS["small"].render(
            "Esquivar pelotas", True, settings.BLACK
        )
        self.txt_time_appear = settings.FONTS["small"].render(
            "Tiempo en el que los elementos aparecen", True, settings.BLACK
        )
        self.txt_elemento_trampa= settings.FONTS["small"].render(
            "Porcentaje de trampa [0,1]", True, settings.BLACK
        )
        self.txt_probabilidad_balls= settings.FONTS["small"].render(
            "Probabilidad bolas [1,100]", True, settings.BLACK
        )
        self.txt_change_mano = settings.FONTS["small"].render(
            "Elegir miniatura de manos", True, settings.BLACK
        )
        self.txt_change_acierto = settings.FONTS["small"].render(
            "Elegir miniatura aciertos", True, settings.BLACK
        )
        self.txt_change_error = settings.FONTS["small"].render(
            "Elegir miniatura error", True, settings.BLACK
        )
        self.txt_change_time_squad = settings.FONTS["small"].render(
            "Tiempo entre sentadillas", True, settings.BLACK
        )
        self.txt_change_time_ball = settings.FONTS["small"].render(
            "Velocidad de las pelotas", True, settings.BLACK
        )

        # Images
        img_diagonales = pygame.image.load(settings.MINIATURA_DIAGONALES)
        img_squad = pygame.image.load(settings.MINIATURA_SQUAD)
        img_balls = pygame.image.load(settings.MINIATURA_BALLS)
        img_modify = pygame.image.load(settings.MODIFY)

        # Buttons
        self.diagonales = ImageButton(
            img_diagonales, (150, 150), "diagonales", (200, 200)
        )
        self.squad = ImageButton(
            img_squad, (550, 150), "squad", (200, 200)
        )
        self.balls = ImageButton(
            img_balls, (950, 150), "balls", (200, 200)
        )
        
        self.button_modify_diagonales = ImageButton(img_modify, (230, 390), "modificar", (30, 30))
        self.button_modify_squad = ImageButton(
            img_modify, (630, 390), "modificar", (30, 30))
        self.button_modify_balls = ImageButton(
            img_modify, (1030, 390), "modificar", (30, 30))
        self.button_calibrate = Button((970, 30), "Calibrar", settings.AMARILLO)
        self.button_back = Button((170, 30), "Volver", settings.AMARILLO)
        self.button_apply = Button((940, self.game.display.get_size()[1] - 180), "Aplicar")
        self.button_apply_squad = Button(
            (940, self.game.display.get_size()[1] - 180), "Aplicar")
        self.button_apply_balls = Button(
            (940, self.game.display.get_size()[1] - 180), "Aplicar")

        self.button_group = [
            self.button_back,
            self.button_calibrate,
            self.button_modify_diagonales,
            self.diagonales,
            self.squad,
            self.button_apply,
            self.button_apply_squad,
            self.button_modify_squad,
            self.button_apply_balls,
            self.button_modify_balls,
            self.balls
        ]

        # Sources
        self.right_source = Source(self.game.display, settings.PUNTERO_ROJO)
        self.left_source = Source(self.game.display, settings.PUNTERO_ROJO)

        # About modifiers
        self.modify_components = False
        self.modify_squad = False
        self.modify_balls = False

        # Input text diagonals
        self.input_time = InputNumberBox(100, 520, 200, 35, text="")
        self.input_time_appear = InputNumberBox(100, 610, 200, 35, text="")
        self.input_trap_element = InputNumberBox(500, 520, 200, 35)

        # Input text squad
        self.input_time_squad = InputNumberBox(100, 520, 200, 35, text="")
        self.input_time_do_squad = InputNumberBox(100, 610, 200, 35, text="")

        # Input text balls
        self.input_time_balls = InputNumberBox(100, 520, 200, 35, text="")
        self.input_time_do_balls = InputNumberBox(100, 610, 200, 35, text="")
        self.input_prob_element = InputNumberBox(500, 520, 200, 35)
        
        # Tracking time
        self.time_hand = 0
        self.pressed_diagonales = pygame.time.get_ticks()
        self.pressed_squad = pygame.time.get_ticks()
        self.pressed_balls = pygame.time.get_ticks()
        self.pressed_calibrate = pygame.time.get_ticks()
        self.pressed_apply = pygame.time.get_ticks()
        self.pressed_back = pygame.time.get_ticks()

        # Progress bar
        self.bar_rect = pygame.Rect(
            100, (self.game.display.get_size()[1]) - 90, 700, 30
        )
        self.width = 0

    def draw(self):
        self.game.display.fill(settings.GRANATE)

        pygame.draw.rect(
            self.game.display, settings.AMARILLO, pygame.Rect(50, 100, 1180, 650)
        )
        for i in range(4):
            # Rectangulo grande
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (50, 100, 1180, 650), 2)
            # Rectangulos de los juegos
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (130, 130, 240, 300), 2)
            pygame.draw.rect(self.game.display, settings.AMARILLO_OSCURO,
                             (129, 129, 239, 299))
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (530, 130, 240, 300), 2)
            pygame.draw.rect(self.game.display, settings.AMARILLO_OSCURO,
                             (529, 129, 239, 299))
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (930, 130, 240, 300), 2)
            pygame.draw.rect(self.game.display, settings.AMARILLO_OSCURO,
                             (929, 129, 239, 299))

        self.button_calibrate.draw(self.game.display)
        self.button_back.draw(self.game.display)
        self.button_modify_diagonales.draw(self.game.display)
        self.button_modify_squad.draw(self.game.display)
        self.button_modify_balls.draw(self.game.display)
        self.game.display.blit(self.activities, (settings.WIDTH // 3, 10))

        self.game.display.blit(self.txt_diagonales, (150, 360))
        self.game.display.blit(self.txt_squad, (600, 360))
        self.game.display.blit(self.txt_balls, (980, 360))
        self.diagonales.draw(self.game.display)
        self.squad.draw(self.game.display)
        self.balls.draw(self.game.display)
        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)

        # Modificadores
        if self.modify_components:
            for i in range(4):
                pygame.draw.rect(self.game.display, (0, 0, 0),
                                 (80, 440, 1110, 240), 2)
            self.game.display.blit(self.txt_modificadores, (100, 450))
            self.game.display.blit(self.txt_time, (100, 490))
            self.input_time.draw(self.game.display)
            self.game.display.blit(self.txt_time_appear, (100, 580))
            self.game.display.blit(self.txt_elemento_trampa, (500, 490))
            self.input_time_appear.draw(self.game.display)
            self.input_trap_element.draw(self.game.display)
            self.button_apply.draw(self.game.display)
        elif self.modify_squad:
            for i in range(4):
                pygame.draw.rect(self.game.display, (0, 0, 0),
                                 (80, 440, 1110, 240), 2)
            self.game.display.blit(self.txt_modificadores, (100, 450))
            self.game.display.blit(self.txt_time, (100, 490))
            self.input_time_squad.draw(self.game.display)
            self.game.display.blit(self.txt_change_time_squad, (100, 580))
            self.input_time_do_squad.draw(self.game.display)
            self.button_apply_squad.draw(self.game.display)
        elif self.modify_balls:
            for i in range(4):
                pygame.draw.rect(self.game.display, (0, 0, 0),
                                 (80, 440, 1110, 240), 2)
            self.game.display.blit(self.txt_modificadores, (100, 450))
            self.game.display.blit(self.txt_time, (100, 490))
            self.input_time_balls.draw(self.game.display)
            self.game.display.blit(self.txt_change_time_ball, (100, 580))
            self.game.display.blit(self.txt_probabilidad_balls, (500, 490))
            self.input_time_do_balls.draw(self.game.display)
            self.input_prob_element.draw(self.game.display)
            self.button_apply_balls.draw(self.game.display)

        # Draw progress bar
        pygame.draw.rect(
            self.game.display,
            settings.WHITE,
            (101, (self.game.display.get_size()[1]) - 90, self.width, 30),
        )
        pygame.draw.rect(self.game.display, settings.BLACK, self.bar_rect, 2)

    def events(self, events):
        if self.diagonales.on_click(events) or self.diagonales.get_clicked_state():
            self.diagonales.clicked = True
            from scenes.diagonalesScene import DiagonalsScene
            return DiagonalsScene(self.game)

        if self.squad.on_click(events) or self.squad.get_clicked_state():
            self.squad.clicked = True
            from scenes.squadScene import SquadScene
            return SquadScene(self.game)

        if self.balls.on_click(events) or self.balls.get_clicked_state():
            self.balls.clicked = True
            from scenes.ballScene import BallScene
            return BallScene(self.game)

        if self.button_back.get_pressed() or self.button_back.on_click(events):
            from scenes.menuScene import MenuScene
            return MenuScene(self.game)

        if self.button_modify_diagonales.on_click(events):
            self.modify_components = True
            self.modify_balls = False
            self.modify_squad = False

        if self.button_modify_squad.on_click(events):
            self.modify_squad = True
            self.modify_components = False
            self.modify_balls = False

        if self.button_modify_balls.on_click(events):
            self.modify_balls = True
            self.modify_components = False
            self.modify_squad = False

        if self.button_calibrate.get_pressed() or self.button_calibrate.on_click(
            events):
            from scenes.calibrationScene import CalibrationScene
            return CalibrationScene(self.game)

        if self.button_apply.get_pressed() or self.button_apply.on_click(events):
            if self.input_time.get_text() != "":
                new_json_value(settings.EXER_0_CONFIG, "TIEMPO_JUEGO", int(self.input_time.get_text()))

            if self.input_time_appear.get_text() != "":
                new_json_value(settings.EXER_0_CONFIG, "VELOCIDAD_ENTRE_BOLAS", float(self.input_time_appear.get_text()))

            if self.input_trap_element.get_text() != "" and float(self.input_trap_element.get_text()) > 0 and float(self.input_trap_element.get_text()) < 1:
                new_json_value(settings.EXER_0_CONFIG, "PORCENTAJE_TRAMPAS", float(self.input_trap_element.get_text()))

            self.input_trap_element.reset()
            self.input_time.reset()
            self.input_time_appear.reset()
            self.modify_components = False
            self.button_modify_diagonales.update()

        if self.modify_components:
            self.input_time.handle_event(events)
            self.input_time_appear.handle_event(events)
            self.input_trap_element.handle_event(events)
        
        if self.button_apply_squad.get_pressed() or self.button_apply_squad.on_click(events):
            if self.input_time_squad.get_text() != "":
                new_json_value(settings.EXER_1_CONFIG, "TIEMPO_JUEGO_SQUAD", int(self.input_time_squad.get_text()))
            if self.input_time_do_squad.get_text() != "":
                new_json_value(settings.EXER_1_CONFIG, "VELOCIDAD_SQUAD", (float(self.input_time_do_squad.get_text())))
            
            self.input_time_squad.reset()
            self.input_time_do_squad.reset()
            self.modify_squad= False
            self.button_modify_squad.update()

        if self.modify_squad:
            self.input_time_squad.handle_event(events)
            self.input_time_do_squad.handle_event(events)

        if self.button_apply_balls.get_pressed() or self.button_apply_balls.on_click(events):
            if self.input_time_balls.get_text() != "":
                new_json_value(settings.EXER_2_CONFIG, "TIEMPO_JUEGO_MOVILIDAD", int(self.input_time_balls.get_text()))

            if self.input_time_do_balls.get_text() != "":
                new_json_value(settings.EXER_2_CONFIG, "BALL_SPEED", int(self.input_time_do_balls.get_text()))

            if self.input_prob_element.get_text() != "" and int(self.input_prob_element.get_text()) >= 1 and int(self.input_prob_element.get_text()) <=100:
                new_json_value(settings.EXER_2_CONFIG, "PROBABILIDAD", int(self.input_prob_element.get_text()))
            
            self.input_prob_element.reset()
            self.input_time_balls.reset()
            self.input_time_do_balls.reset()
            self.modify_balls = False
            self.button_modify_balls.update()

        if self.modify_balls:
            self.input_time_balls.handle_event(events)
            self.input_time_do_balls.handle_event(events)
            self.input_prob_element.handle_event(events)

        return None

    def check_collide(self, left, right):
        if self.diagonales.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.diagonales.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Diagonales"
        elif self.squad.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.squad.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Squad"
        elif self.balls.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.balls.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Balls"
        elif self.button_calibrate.top_rect.collidepoint(
            left.rect.centerx, left.rect.centery
        ) or self.button_calibrate.top_rect.collidepoint(
            right.rect.centerx, right.rect.centery
        ):
            return "Calibrate"
        elif self.button_back.top_rect.collidepoint(
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
        if action == "Diagonales":
            self.time_hand = count(self.pressed_diagonales)
        else:
            self.pressed_diagonales = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Squad":
            self.time_hand = count(self.pressed_squad)
        else:
            self.pressed_squad = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Balls":
            self.time_hand = count(self.pressed_balls)
        else:
            self.pressed_balls = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Calibrate":
            self.time_hand = count(self.pressed_calibrate)
        else:
            self.pressed_calibrate = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Aplicar":
            self.time_hand = count(self.pressed_apply)
        else:
            self.pressed_apply = pygame.time.get_ticks()
        # ------------------------------------------
        if action == "Volver":
            self.time_hand = count(self.pressed_back)
        else:
            self.pressed_back = pygame.time.get_ticks()

        self.width = self.time_hand * coefficient
        if self.width > settings.WIDTH_LOAD_BAR + 10:
            print(self.width)
            if action == "Diagonales":
                self.diagonales.set_clicked_true()
            elif action == "Squad":
                self.squad.set_clicked_true()
            elif action == "Balls":
                self.balls.set_clicked_true()
            elif action == "Calibrate":
                self.button_calibrate.set_pressed(True)
            elif action == "Aplicar":
                self.button_apply.set_pressed(True)
            elif action == "Volver":
                self.button_back.set_pressed(True)

        if action == "":
            self.time_hand, self.width = reset_time()
        if self.time_hand >= settings.TIME_BUTTONS:
            if action == "Diagonales":
                self.diagonales.set_clicked_true()
            elif action == "Squad":
                self.squad.set_clicked_true()
            elif action == "Balls":
                self.balls.set_clicked_true()
            elif action == "Calibrate":
                self.button_calibrate.set_pressed(True)
            elif action == "Aplicar":
                self.button_apply.set_pressed(True)
            elif action == "Volver":
                self.button_back.set_pressed(True)

    def update(self, dt):
        self.diagonales.update()
        self.squad.update()
        self.balls.update()
        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
