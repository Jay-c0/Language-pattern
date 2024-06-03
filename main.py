# Language pattern program

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
        self.x_pos = x
        self.y_pos = y

        # Velocity
        self.velocity = 0
        self.gravity = 10
        self.pos_goal = self.y_pos

        # Rectangle
        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, 16, 16)
        self.rect_border = pygame.rect.Rect(self.x_pos - 4, self.y_pos - 4, 24, 24)

    def key_touched(self, key):
        if self.y_pos > 100:
            self.pos_goal -= key.percentage * 3
        if key.percentage > 10:
            self.gravity = 0

    # Updating the point
    def update(self):
        # Clock
        self.clock += 1
        # Updating velocity / gravity
        if self.gravity < 10:
            self.gravity += 1
        if self.clock % 10 == 0:
            self.velocity = (self.pos_goal - self.y_pos) / 3
            self.y_pos += self.velocity
            if self.pos_goal < display.get_height() - self.rect.height - 100:
                self.pos_goal += 1 + self.gravity
        # Updating rect
        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, 16, 16)
        self.rect_border = pygame.rect.Rect(self.x_pos - 4, self.y_pos - 4, 24, 24)


# KEY
class Key:

    # Constructor
    def __init__(self, name):
        self.name = name
        self.percentage = 1
        self.touch = 0

    def touched(self, key_touched):
        self.touch += 1
        if key_touched < 100:
            self.percentage = abs((self.touch / key_touched) * 50)
        else:
            self.percentage = abs((self.touch / key_touched) * 200)


# MAIN LOOP
def main():

    # Clock
    clock = 0

    # Points
    points = []

    # Cursor
    cursor = Cursor((display.get_width() / 2) - 8, display.get_height() - 100)

    # Key
    key_touched = 0
    keys = []

    while True:
        # Background
        display.fill((0, 0, 0))

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                else:
                    key_touched += 1
                    key_find = 0
                    key_press = 0
                    for key in keys:
                        if key.name == event.key:
                            key_press = key
                            key.touched(key_touched)
                            key_find = 1
                    if key_find == 0:
                        key_press = Key(event.key)
                        key_press.touched(key_touched)
                        keys.append(key_press)
                    cursor.key_touched(key_press)

        # Points
        if clock % 10 == 0:
            points.append(Point(cursor.rect.x, cursor.rect.y))

        # Cursor
        cursor.update()

        # Blit on display
        # Points
        for i in range(len(points)):
            point = points[i]
            if i > 0:
                last_point = points[i - 1]
                pygame.draw.line(display, (255, 255, 255), (point.rect.x, point.rect.y), (last_point.rect.x, last_point.rect.y))
            point.update(clock)
            display.blit(point.surf, point.rect)
        # Cursor
        display.blit(cursor.surf, cursor.rect)
        pygame.draw.ellipse(display, DARK_BLUE, cursor.rect_border, cursor.rect_border.width)
        pygame.draw.ellipse(display, BLUE, cursor.rect, cursor.rect.width)

        # Display
        pygame.display.update()

        # Clock
        clock += 1


# RUNNING THE PROGRAM
if __name__ == '__main__':
    main()
