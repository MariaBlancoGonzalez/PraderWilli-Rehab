import pygame

from settings.settings import FONTS
from settings.settings import WHITE, GRANATE, GRIS, BLACK

class ImageButton:
    def __init__(self, image, position, callback, scale=(25, 25)):
        self.image = image
        self.scale = scale
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.__clicked = False

    def resized(self, x,y):
        self.rect.x = x
        self.rect.y = y

    def on_click(self, event):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.get_clicked_state():
                action = True
                self.__clicked = True
            if not pygame.mouse.get_pressed()[0]:
                self.__clicked = False

        return action
    def get_lowest_center_point(self):
        center_x = self.rect.x + self.rect.width // 2
        lowest_y = self.rect.y + self.rect.height
        return (center_x, lowest_y+3)

    def get_clicked_state(self):
        return self.__clicked

    def set_clicked_true(self):
        self.__clicked = True

    def set_clicked_false(self):
        self.__clicked = False

    def update(self):
        if self.get_clicked_state():
            self.__clicked = False

    def update(self):
        if self.get_clicked_state():
            self.__clicked = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, color=GRANATE, width=200, color_text=WHITE):
        self.bottom_rect = pygame.Rect((position[0] + 6, position[1] + 6), (width, 50))
        self.rect = pygame.Rect((position[0], position[1]), (width, 50))
        self.color = color
        self.text = FONTS["medium"].render(text, True, color_text)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center
        self.color_text = color_text

        self.__pressed = False
        self.__clicked = False

        self.fillColors = {
            "normal": self.color,
            "hover": "#666666",
            "pressed": "#333333",
        }
    def change_pos(self, position, width=200):
        self.bottom_rect = pygame.Rect((position[0] + 6, position[1] + 6), (width, 50))
        self.rect = pygame.Rect((position[0], position[1]), (width, 50))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def change_text(self, text):
        self.text = FONTS["medium"].render(text, True, self.color_text)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def on_click(self, event):
        pos = pygame.mouse.get_pos()
        for ev in event:
            if (
                not self.rect.collidepoint(pos)
                and self.color != self.fillColors["normal"]
            ):
                self.color = self.fillColors["normal"]
                self.set_clicked(False)
                self.set_pressed(False)

            if self.rect.collidepoint(pos) and not self.get_clicked():
                self.color = self.fillColors["hover"]

            if ev.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
                self.color = self.fillColors["pressed"]
                self.set_clicked(True)

            elif (
                ev.type == pygame.MOUSEBUTTONUP
                and self.get_clicked()
                and self.rect.collidepoint(pos)
            ):
                return True

        return False

    def set_pressed(self, bool):
        self.__pressed = bool

    def get_pressed(self):
        return self.__pressed

    def get_clicked(self):
        return self.__clicked

    def set_clicked(self, bool):
        self.__clicked = bool

    def draw(self, display):
        pygame.draw.rect(display, GRIS, self.bottom_rect)
        pygame.draw.rect(display, self.color, self.rect)
        for i in range(4):
            pygame.draw.rect(display, (0, 0, 0),
                             self.rect, 2)
        display.blit(self.text, self.text_rect)


class Image:
    def __init__(self, image="", pos=(0, 0)):
        self.image = pygame.image.load(image)
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class BackgroundText:
    def __init__(self, text, pos, text_color, color_background, transparency=0):
        font = FONTS["big"]

        self.color = text_color
        self.color_background = color_background
        self.transp = transparency

        self.text = font.render(text, True, self.color)

        self.text_rect = self.text.get_rect()
        self.pos = pos

        # Definir las dimensiones y el color del fondo
        self.background_rect = pygame.Rect(
            pos[0], pos[1], self.text_rect.width + 20, self.text_rect.height + 20
        )

        self.background = pygame.Surface(self.background_rect.size)
        self.background.fill(self.color_background)

    def draw(self, screen):
        # screen.blit(screen)
        screen.blit(self.background, (self.pos[0] - 10, self.pos[1] - 10))
        screen.blit(self.text, self.pos)


class DropDown:
    def __init__(self, color_menu, color_option, x, y, w, h, font, main, option):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.option = option
        self.draw_menu = False
        self.menu_active = False
    
    def change_pos(self, x,y,w,h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(
                    surf, self.color_option[1 if i == self.main else 0], rect, 0
                )
                msg = self.font.render(text, True, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        for i in range(len(self.option)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos) and self.draw_menu:
                self.main = self.option[i]

        if not self.menu_active and self.main == "":
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.main != "":
                    self.draw_menu = False
    
    def resized(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def getMain(self):
        return self.main


class InputBox:
    def __init__(self, x, y, w, h, text=str()):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = FONTS["medium"].render(self.text, True, self.color)
        self.active = False
    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = WHITE if self.active else BLACK
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.type == pygame.KEYDOWN:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONTS["medium"].render(
                        self.text, True, self.color
                    )

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text

    def reset(self):
        self.text = ''
        self.txt_surface = FONTS["medium"].render(self.text, True, self.color)
        self.active = False


class InputNumberBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = FONTS["medium"].render(self.text, True, self.color)
        self.active = False
        self.comma = True
    def handle_event(self, events):
        self.comma = False if '.' in self.text or ',' in self.text else True
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = WHITE if self.active else BLACK
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    # For numbers
                    elif 48 <= event.key <= 59:
                        self.text += event.unicode
                    # For commas 46 = '.' and 44 = ','
                    elif event.key == 46 and self.comma:
                        self.text += event.unicode
                        self.comma = False
                    # Re-render the text.
                    self.txt_surface = FONTS["medium"].render(
                        self.text, True, BLACK
                    )

    def get_text(self):

        if self.text != "":
            if str(self.text)[0] == '.':
                return ""
        return self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def reset(self):
        self.text = ""
        self.txt_surface = FONTS["medium"].render(self.text, True, self.color)
