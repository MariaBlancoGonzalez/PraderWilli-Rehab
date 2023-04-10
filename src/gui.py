import pygame

from settings import FONTS
from settings import WHITE, GRANATE, GRIS, BLACK

class ImageButton:
    def __init__(self, image, position, callback, scale = (25,25)):
        self.image = image
        self.scale = scale
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.clicked = False
 
    def on_click(self, event):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        return action

    def update(self):
        if self.clicked:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Button:
    def __init__(self, position, text):
        self.bottom_rect = pygame.Rect((position[0]+6, position[1]+6), (200, 50))
        self.top_rect = pygame.Rect((position[0], position[1]), (200, 50))
        
        self.text = FONTS['medium'].render(text, True, WHITE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.top_rect.center

        self.clicked = False
 
    def on_click(self, event):
        action = False
        pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
                return True
            if not pygame.mouse.get_pressed()[0]:
                return False
        return action
    
    def update(self):
        if self.clicked:
            self.clicked = False

    def draw(self, display):
        top_rect_color = GRANATE

        # Si no pulsamos dibujamos todo en su posición original
        pygame.draw.rect(display, GRIS, self.bottom_rect)
        pygame.draw.rect(display, top_rect_color, self.top_rect)

        display.blit(self.text, self.text_rect) 

class Image:
    def __init__(self, image="", pos = (0,0)):
        self.image = pygame.image.load(image)
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class BackgroundText():
    def __init__(self, text, pos, text_color, color_background, transparency=0):
        font = FONTS['big']

        self.color = text_color
        self.color_background = color_background
        self.transp = transparency

        self.text = font.render(
            text, True, self.color)

        self.text_rect = self.text.get_rect()
        self.pos = pos

        # Definir las dimensiones y el color del fondo
        self.background_rect = pygame.Rect(
            pos[0], pos[1], self.text_rect.width + 20, self.text_rect.height + 20)

        self.background = pygame.Surface(self.background_rect.size)
        self.background.fill(self.color_background)

    def draw(self, screen):
        # screen.blit(screen)
        screen.blit(self.background, (self.pos[0]-10, self.pos[1]-10))
        screen.blit(self.text, self.pos)


class DropDown():

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, option):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.option = option
        self.draw_menu = False
        self.menu_active = False
        
    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.main else 0], rect, 0)
                msg = self.font.render(text, True, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        for i in range(len(self.option)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos) and self.draw_menu:
                self.main = self.option[i]
               
        if not self.menu_active and self.main == '':
            self.draw_menu = False
            
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.main != '':
                    self.draw_menu = False

    def getMain(self):
        return self.main

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = FONTS['medium'].render(self.text, True, self.color)
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
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONTS['medium'].render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text
    
    def reset(self):
        self.text = ""
        self.txt_surface = FONTS['medium'].render(self.text, True, self.color)
        self.active = False

class InputNumberBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = FONTS['medium'].render(self.text, True, self.color)
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
                    elif 48 <= event.key <= 59:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONTS['medium'].render(
                        self.text, True, self.color)
    def get_text(self):
        return self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def reset(self):
        self.text = ''
        self.txt_surface = FONTS['medium'].render(self.text, True, self.color)
