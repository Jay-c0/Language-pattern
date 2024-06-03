import pygame

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