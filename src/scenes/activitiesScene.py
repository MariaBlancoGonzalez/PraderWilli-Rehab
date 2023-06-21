import pygame

import settings.settings as settings

from settings.settings_0 import EXER_0_CONFIG
from settings.settings_1 import EXER_1_CONFIG
from settings.settings_2 import EXER_2_CONFIG

from scenes.scene import Scene
from pose_tracking.tracker_utils import *
from ui.gui import Button, ImageButton, InputNumberBox
from ui.source import Source
from scenes.timeDownScene import TimeDown

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
        self.txt_time_appear = settings.FONTS["small"].render(
            "Tiempo en el que los elementos aparecen", True, settings.BLACK
        )
        self.txt_elemento_trampa= settings.FONTS["small"].render(
            "Porcentaje de trampa [0, 1]", True, settings.BLACK
        )
        self.txt_angulo= settings.FONTS["small"].render(
            "Ángulo [1, 360]", True, settings.BLACK
        )
        self.txt_probabilidad_balls= settings.FONTS["small"].render(
            "Probabilidad bolas [1, 100]", True, settings.BLACK
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
        self.img_diagonales = pygame.image.load(settings.MINIATURA_DIAGONALES)
        self.img_squad = pygame.image.load(settings.MINIATURA_SQUAD)
        self.img_balls = pygame.image.load(settings.MINIATURA_BALLS)
        self.img_modify = pygame.image.load(settings.MODIFY)

        pos = self.game.display.get_size()[0]
        # Buttons
        self.diagonales = ImageButton(
            self.img_diagonales, (pos*0.05, 120), "diagonales", (pos*0.3, self.game.display.get_size()[1]*0.4)
        )#(270, 330)
        self.squad = ImageButton(
            self.img_squad, (pos*0.35, 120), "squad", (pos*0.3, self.game.display.get_size()[1]*0.4)
        )
        self.balls = ImageButton(
            self.img_balls, (pos*0.65, 120), "balls", (pos*0.3, self.game.display.get_size()[1]*0.4)
        )
        
        self.button_modify_diagonales = ImageButton(self.img_modify, self.diagonales.get_lowest_center_point(), "modificar", (30, 30))
        self.button_modify_squad = ImageButton(self.img_modify, self.squad.get_lowest_center_point(), "modificar", (30, 30))
        self.button_modify_balls = ImageButton(self.img_modify, self.balls.get_lowest_center_point(), "modificar", (30, 30))

        self.button_calibrate = Button((pos*0.75, 30), "Calibrar", settings.AMARILLO, 200, settings.BLACK)
        self.button_back = Button((pos*0.1, 30), "Volver", settings.AMARILLO, 200, settings.BLACK)

        self.button_apply = Button((pos*0.75, self.game.display.get_size()[1] - 100), "Aplicar")
        self.button_apply_squad = Button(
            (pos*0.75, self.game.display.get_size()[1] - 100), "Aplicar")
        self.button_apply_balls = Button(
            (pos*0.75, self.game.display.get_size()[1] - 100), "Aplicar")

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
        self.right_source = Source(self.game.display, settings.MANO_DERECHA, (90,90))
        self.left_source = Source(self.game.display, settings.MANO_IZQUIERDA, (90,90))

        # About modifiers
        self.modify_components = False
        self.modify_squad = False
        self.modify_balls = False

        pos_y = self.button_modify_diagonales.get_lowest_center_point()[1]+100
        # Input text diagonals
        self.input_time = InputNumberBox(100, pos_y, 200, 35, text="")
        self.input_time_appear = InputNumberBox(450, pos_y, 200, 35, text="")
        self.input_trap_element = InputNumberBox(900, pos_y, 200, 35)

        # Input text squad
        self.input_time_squad = InputNumberBox(100, pos_y, 200, 35, text="")
        self.input_time_do_squad = InputNumberBox(450, pos_y, 200, 35, text="")
        self.input_angle = InputNumberBox(900, pos_y, 200, 35, text="")

        # Input text balls
        self.input_time_balls = InputNumberBox(100, pos_y, 200, 35, text="")
        self.input_time_do_balls = InputNumberBox(450, pos_y, 200, 35, text="")
        self.input_prob_element = InputNumberBox(900, pos_y, 200, 35)
        
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
        
    
    def resized(self):
        self.bar_rect = pygame.Rect(100, (self.game.display.get_size()[1]) - 90, 700, 30)

        
        pos = self.game.display.get_size()[0]
        self.button_modify_diagonales.resized(pos*0.15, 500)
        self.button_modify_squad.resized(pos*0.5, 390)
        self.button_modify_balls.resized(pos*0.805, 390)
        
        # Buttons
        self.diagonales = ImageButton(
            self.img_diagonales, (pos*0.05, 120), "diagonales", (pos*0.3, self.game.display.get_size()[1]*0.4)
        )#(270, 330)
        self.squad = ImageButton(
            self.img_squad, (pos*0.35, 120), "squad", (pos*0.3, self.game.display.get_size()[1]*0.4)
        )
        self.balls = ImageButton(
            self.img_balls, (pos*0.65, 120), "balls", (pos*0.3, self.game.display.get_size()[1]*0.4)
        )
        self.button_modify_diagonales = ImageButton(self.img_modify, self.diagonales.get_lowest_center_point(), "modificar", (30, 30))
        self.button_modify_squad = ImageButton(self.img_modify, self.squad.get_lowest_center_point(), "modificar", (30, 30))
        self.button_modify_balls = ImageButton(self.img_modify, self.balls.get_lowest_center_point(), "modificar", (30, 30))

        self.button_calibrate.change_pos((pos*0.75, 30))
        self.button_back.change_pos((pos*0.1, 30))

        self.button_apply.change_pos((pos*0.75, self.game.display.get_size()[1] - 100))
        self.button_apply_squad.change_pos((pos*0.75, self.game.display.get_size()[1] - 100))
        self.button_apply_balls.change_pos((pos*0.75, self.game.display.get_size()[1] - 100))

        pos_y = self.button_modify_diagonales.get_lowest_center_point()[1]+100
        # Input text diagonals
        self.input_time = InputNumberBox(100, pos_y, 200, 35, text="")
        self.input_time_appear = InputNumberBox(450, pos_y, 200, 35, text="")
        self.input_trap_element = InputNumberBox(900, pos_y, 200, 35)

        # Input text squad
        self.input_time_squad = InputNumberBox(100, pos_y, 200, 35, text="")
        self.input_time_do_squad = InputNumberBox(450, pos_y, 200, 35, text="")
        self.input_angle = InputNumberBox(900, pos_y, 200, 35, text="")

        # Input text balls
        self.input_time_balls = InputNumberBox(100, pos_y, 200, 35, text="")
        self.input_time_do_balls = InputNumberBox(450, pos_y, 200, 35, text="")
        self.input_prob_element = InputNumberBox(900, pos_y, 200, 35)

    def draw(self):
        self.game.display.fill(settings.GRANATE)

        pygame.draw.rect(
            self.game.display, settings.AMARILLO, pygame.Rect(50, 100, self.game.display.get_size()[0]-100, self.game.display.get_size()[1]-130)
        )

        for i in range(4):
            # Rectangulo grande
            pygame.draw.rect(self.game.display, (0, 0, 0),
                             (50, 100, self.game.display.get_size()[0]-100, self.game.display.get_size()[1]-130), 2)

        self.button_calibrate.draw(self.game.display)
        self.button_back.draw(self.game.display)

        self.game.display.blit(self.activities, (settings.WIDTH*0.35, 10))

        self.diagonales.draw(self.game.display)
        self.squad.draw(self.game.display)
        self.balls.draw(self.game.display)

        self.button_modify_diagonales.draw(self.game.display)
        self.button_modify_squad.draw(self.game.display)
        self.button_modify_balls.draw(self.game.display)

        self.right_source.draw(self.game.display)
        self.left_source.draw(self.game.display)

        # Modificadores
        if self.modify_components:
            for i in range(4):
                pygame.draw.rect(self.game.display, (0, 0, 0),
                                 (80, self.button_modify_diagonales.get_lowest_center_point()[1], self.game.display.get_size()[0]-150, self.game.display.get_size()[1]*0.27), 2)
            pos = self.button_modify_diagonales.get_lowest_center_point()[1]
            self.game.display.blit(self.txt_modificadores, (100, pos+20))
            self.game.display.blit(self.txt_time, (100, pos+70))
            self.game.display.blit(self.txt_time_appear, (450, pos+70))
            self.game.display.blit(self.txt_elemento_trampa, (900, pos+70))
            
            self.input_time.draw(self.game.display)
            self.input_time_appear.draw(self.game.display)
            self.input_trap_element.draw(self.game.display)
            
            self.button_apply.draw(self.game.display)
        elif self.modify_squad:
            for i in range(4):
                pygame.draw.rect(self.game.display, (0, 0, 0),
                                 (80, self.button_modify_squad.get_lowest_center_point()[1], self.game.display.get_size()[0]-150, self.game.display.get_size()[1]*0.27), 2)
            
            pos = self.button_modify_squad.get_lowest_center_point()[1]
            self.game.display.blit(self.txt_modificadores, (100, pos+20))
            self.game.display.blit(self.txt_time, (100, pos+70))
            self.game.display.blit(self.txt_change_time_squad, (450, pos+70))
            self.game.display.blit(self.txt_angulo, (900, pos+70))

            self.input_angle.draw(self.game.display)
            self.input_time_squad.draw(self.game.display)
            self.input_time_do_squad.draw(self.game.display)

            self.button_apply_squad.draw(self.game.display)

        elif self.modify_balls:
            for i in range(4):
                pygame.draw.rect(self.game.display, (0, 0, 0),
                                 (80, self.button_modify_balls.get_lowest_center_point()[1], self.game.display.get_size()[0]-150, self.game.display.get_size()[1]*0.27), 2)
            pos = self.button_modify_balls.get_lowest_center_point()[1]
            self.game.display.blit(self.txt_modificadores, (100, pos+20))
            self.game.display.blit(self.txt_time, (100, pos+70))
            self.game.display.blit(self.txt_change_time_ball, (450, pos+70))
            self.game.display.blit(self.txt_probabilidad_balls, (900, pos+70))
            
            self.input_time_balls.draw(self.game.display)
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

        if self.button_calibrate.get_pressed() or self.button_calibrate.on_click(
            events):
            from scenes.calibrationScene import CalibrationScene
            return CalibrationScene(self.game)

        if self.button_apply.get_pressed() or self.button_apply.on_click(events):
            if self.input_time.get_text() != "":
                new_json_value(EXER_0_CONFIG, "TIEMPO_JUEGO", int(self.input_time.get_text()))

            if self.input_time_appear.get_text() != "":
                new_json_value(EXER_0_CONFIG, "VELOCIDAD_ENTRE_BOLAS", float(self.input_time_appear.get_text()))

            if self.input_trap_element.get_text() != "" and float(self.input_trap_element.get_text()) > 0 and float(self.input_trap_element.get_text()) <= 1:
                new_json_value(EXER_0_CONFIG, "PORCENTAJE_TRAMPAS", float(self.input_trap_element.get_text()))

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
            time_squad = read(EXER_1_CONFIG, "TIEMPO_JUEGO_SQUAD")
            if self.input_time_squad.get_text() != "":
                new_json_value(EXER_1_CONFIG, "TIEMPO_JUEGO_SQUAD", int(self.input_time_squad.get_text()))
                tiempo_squad = int(self.input_time_squad.get_text())

            if self.input_time_do_squad.get_text() != "" and int(self.input_time_do_squad.get_text()) <= tiempo_squad:
                new_json_value(EXER_1_CONFIG, "VELOCIDAD_SQUAD", (float(self.input_time_do_squad.get_text())))
            if self.input_angle.get_text() != "" and int(self.input_angle.get_text()) >= 1 and int(self.input_angle.get_text()) <=360:
                new_json_value(EXER_1_CONFIG, "ANGLE", (float(self.input_angle.get_text())))
            
            self.input_time_squad.reset()
            self.input_time_do_squad.reset()
            self.input_angle.reset()
            self.modify_squad= False
            self.button_modify_squad.update()

        if self.modify_squad:
            self.input_time_squad.handle_event(events)
            self.input_time_do_squad.handle_event(events)
            self.input_angle.handle_event(events)

        if self.button_apply_balls.get_pressed() or self.button_apply_balls.on_click(events):
            if self.input_time_balls.get_text() != "":
                new_json_value(EXER_2_CONFIG, "TIEMPO_JUEGO_MOVILIDAD", int(self.input_time_balls.get_text()))

            if self.input_time_do_balls.get_text() != "":
                new_json_value(EXER_2_CONFIG, "BALL_SPEED", int(self.input_time_do_balls.get_text()))

            if self.input_prob_element.get_text() != "" and int(self.input_prob_element.get_text()) >= 1 and int(self.input_prob_element.get_text()) <=100:
                new_json_value(EXER_2_CONFIG, "PROBABILIDAD", int(self.input_prob_element.get_text()))
            
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
            self.time_hand, self.width = reset_time()
            self.reset_timer_after()

    def reset_timer_after(self):
        self.pressed_diagonales = pygame.time.get_ticks()
        self.pressed_back = pygame.time.get_ticks()
        self.pressed_apply = pygame.time.get_ticks()
        self.pressed_calibrate = pygame.time.get_ticks()
        self.pressed_balls = pygame.time.get_ticks()
        self.pressed_squad = pygame.time.get_ticks()

    def update(self, dt):
        self.diagonales.update()
        self.squad.update()
        self.balls.update()
        pos = pygame.mouse.get_pos()
        if any(button.top_rect.collidepoint(pos) for button in self.button_group):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
