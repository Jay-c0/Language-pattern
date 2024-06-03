"""
Language Pattern Program

To see if there is any pattern in phrases we type on the computer

Layout:

        1                  2                3
|---------------| |---------------| |---------------|
|               | |               | |               |
|               | |               | |               |
|               | |               | |               |
|---------------| |---------------| |---------------|
         |------------------------------|
         |                              |
         |                              |
         |------------------------------|
                         4

1: 2D graph
2: real time graph
3: 3D extrapolated graph
4: text to type

"""

# MAIN
import pygame
import csv

from ref import *

# SETUP PYGAME
pygame.init()
display = pygame.display.set_mode((500, 500), pygame.RESIZABLE)

# CSV FILE
filename = "points.csv"
file = open(filename, "w")
file.truncate()
file.close()


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


# KEY
class Key:

    # Constructor
    def __init__(self, name):
        self.name = name
        self.percentage = 1
        self.touch = 0

    def touched(self, key_touched):
        self.touch += 1
        self.percentage = abs((self.touch / key_touched) * 100)


# MAIN LOOP
def main():

    # Quit
    escape = False

    # Clock
    game_clock = 0

    # Points
    points = []

    # Cursor
    cursor = Cursor((display.get_width() / 2) - 8, display.get_height() - 100)

    # Key
    key_touched = 0
    keys = []

    while not escape:
        # Background
        display.fill((0, 0, 0))

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                escape = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escape = True
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
        if game_clock % 10 == 0:
            points.append(Point(cursor.rect.x, cursor.rect.y))

        # Cursor
        cursor.update(game_clock)

        # Blit on display
        # Points
        for i in range(len(points)):
            point = points[i]
            if i > 0:
                last_point = points[i - 1]
                pygame.draw.line(display, (255, 255, 255), (point.rect.x, point.rect.y), (last_point.rect.x, last_point.rect.y))
            point.update(game_clock)
            display.blit(point.surf, point.rect)
        # Cursor
        display.blit(cursor.surf, cursor.rect)
        pygame.draw.ellipse(display, DARK_BLUE, cursor.rect_border, cursor.rect_border.width)
        pygame.draw.ellipse(display, BLUE, cursor.rect, cursor.rect.width)

        # Display
        pygame.display.update()

        # Clock
        game_clock += 1

    with open(filename, "r+", newline='') as csvfile:
        point_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for point in cursor.points:
            line = str(point[0]) + "/" + str(point[1])
            point_writer.writerow(line)


# RUNNING THE PROGRAM
if __name__ == '__main__':
    main()
