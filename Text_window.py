"""
User interface
(Text to type)
"""

import pygame
import random

from ref import *

# SETUP PYGAME
pygame.init()


# TEXT WINDOW
class Window:

    def __init__(self, display_width, display_height, text_num):
        # Graph
        self.WIDTH = display_width - 60
        self.HEIGHT = 100
        self.window = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = pygame.rect.Rect(30, display_height - self.HEIGHT - 30, self.WIDTH, self.HEIGHT)

        # Font
        self.font = pygame.font.SysFont('Courier new', 30)

        # Text
        if text_num == len(TEXTS): self.text_num = 0
        else: self.text_num = text_num
        self.text = TEXTS[self.text_num]
        self.text_alpha = 0

        # Key
        self.BACKSPACE = 8
        self.SPACE = 32
        self.shift = False

        self.key_pressed = []

        # Cursor
        self.cursor = 0
        self.cursor_blink = False

        # Letter
        self.letter_typed = []
        self.letter_dict = {}
        for i in range(255):
            k = pygame.key.name(i)
            if k == "_":
                self.letter_dict.update({self.SPACE: k})
            elif k != "":
                self.letter_dict.update({i: k})
        
        # Variables
        self.done = False
        self.quit = False

    # Render the text and the cursor
    def render_text(self):
        if not self.done and self.text_alpha < 256:
            self.text_alpha += 1
        elif self.done:
            self.text_alpha -= 1
            if self.text_alpha == -1:
                self.quit = True
        
        cursor_pos_x = []

        txt_width = 0
        x_pos = 0

        for i in range(len(self.text)):
            if i > 0:
                txt_width += 5
            letter = self.text[i]
            txt_letter = self.font.render(letter, True, WHITE)
            txt_width += txt_letter.get_width()
            cursor_pos_x.append(i * (1 + txt_letter.get_width()))

        txt_surf = pygame.Surface((txt_width, txt_letter.get_height()))
        txt_surf.fill(GREY_BG)
    
        letter_typed = 0
        for i in range(len(self.text)):
            letter = self.text[i]
            try:
                key_pressed_name = self.letter_dict[self.key_pressed[i][0]]
                if (pygame.key.get_mods() & pygame.KMOD_SHIFT and key_pressed_name.upper() == letter and self.key_pressed[i][1] == -1)\
                        or self.key_pressed[i][1] == 1:
                    self.key_pressed[i][1] = 1
                    txt_letter = self.font.render(letter, True, BLUE)
                    letter_typed += 1
                elif letter == key_pressed_name and self.key_pressed[i][1] == -1:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        txt_letter = self.font.render(letter, True, RED)
                        self.key_pressed[i][1] = 0
                    else:
                        txt_letter = self.font.render(letter, True, BLUE)
                        self.key_pressed[i][1] = 1
                        letter_typed += 1
                else:
                    self.key_pressed[i][1] = 0
                    txt_letter = self.font.render(letter, True, RED)
            except IndexError:
                txt_letter = self.font.render(letter, True, WHITE)

            txt_surf.blit(txt_letter, (x_pos, 0))
            txt_surf.set_alpha(self.text_alpha)
            x_pos += txt_letter.get_width() + 5

        if letter_typed == len(self.text):
            self.done = True

        self.window.blit(txt_surf, ((self.WIDTH / 2) - (txt_surf.get_width() / 2), (self.HEIGHT / 2) - (txt_surf.get_height() / 2)))


    # Update the text window
    def update(self, key_press):
        # BG
        self.window.fill(WHITE)
        pygame.draw.rect(self.window, GREY_BG, pygame.rect.Rect(3, 3, self.WIDTH - 6, self.HEIGHT - 6))
        # Text
        self.render_text()

        # Key
        if key_press[0]:
            if key_press[1].name != self.BACKSPACE:
                self.key_pressed.append([key_press[1].name, -1])
            else:
                if len(self.key_pressed) > 0:
                    self.key_pressed.pop(len(self.key_pressed) - 1)
