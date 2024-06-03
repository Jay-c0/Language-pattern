"""
Real time graphic window
"""

import pygame

from ref import *

# SETUP PYGAME
pygame.init()
display = pygame.display.set_mode((500, 500), pygame.RESIZABLE)


# POINTS
class Point:

    # Constructor
    def __init__(self, x, y):
        # Surface
        self.surf = pygame.Surface((1, 1))
        self.surf.fill((255, 255, 255))

        # Position
        self.x_pos = x
        self.y_pos = y

        # Rectangle
        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, 3, 3)

    # Updating the point
    def update(self, clock):
        if clock % 5 == 0:
            self.x_pos -= 1
        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, 3, 3)


# CURSOR
class Cursor:

    # Constructor
    def __init__(self, x, y):
        # Clock
        self.clock = 0
        # Surface
        self.surf = pygame.Surface((16, 16))
        self.surf.fill((0, 0, 0))

        # Position
        self.INIT_POS = y
        self.y_pos_goal = y
        self.x_pos = x
        self.y_pos = y

        # Points
        self.points_x = 0
        self.points_y = y
        self.points = [[x, y]]

        # Rectangle
        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, 16, 16)
        self.rect_border = pygame.rect.Rect(self.x_pos - 4, self.y_pos - 4, 24, 24)

    # Get the value of the key pressed
    def key_touched(self, key):
        self.y_pos_goal = self.y_pos - (key.percentage * 3)

    # Updating the point
    def update(self, clock):
        # Clock
        self.clock += 1
        # Updating y position
        if self.y_pos > self.y_pos_goal and self.y_pos > 100:
            self.y_pos -= 2
        else:
            if self.y_pos < self.INIT_POS:
                self.y_pos += 3
                self.y_pos_goal += 2
        # Updating rect
        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, 16, 16)
        self.rect_border = pygame.rect.Rect(self.x_pos - 4, self.y_pos - 4, 24, 24)
        # Updating points
        if clock % 10 == 0:
            self.points_x += 1
            self.points_y = 400 - self.y_pos
            self.points.append([abs(self.points_x), abs(self.points_y)])


# WINDOW
class Window:

    # Constructor
    def __init__(self, w, h, display):
        # Window
        self.window = pygame.Surface((w, h))
        self.rect = pygame.rect.Rect(0, 0, w, h)

        # Points
        self.points = []
        self.cursor = Cursor((display.get_width() / 2) - 8, display.get_height() - 100)

    # Update the real time graphic window
    def update(self, key_press, clock):
        # Key pressed
        if key_press[0]:
            self.cursor.key_touched(key_press[1])
        # Points
        if clock % 10 == 0:
            self.points.append(Point(self.cursor.rect.x, self.cursor.rect.y))

        # Cursor
        self.cursor.update(clock)

        # Blit on display
        self.window.fill((0, 0, 0))
        # Points
        for i in range(len(self.points)):
            point = self.points[i]
            if i > 0:
                last_point = self.points[i - 1]
                pygame.draw.line(self.window, (255, 255, 255), (point.rect.x, point.rect.y),
                                 (last_point.rect.x, last_point.rect.y))
            point.update(clock)
            self.window.blit(point.surf, point.rect)
        # Cursor
        self.window.blit(self.cursor.surf, self.cursor.rect)
        pygame.draw.ellipse(self.window, DARK_BLUE, self.cursor.rect_border, self.cursor.rect_border.width)
        pygame.draw.ellipse(self.window, BLUE, self.cursor.rect, self.cursor.rect.width)

