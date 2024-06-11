"""
3D graphic
"""

import pygame
import math as m
import random as rand

from ref import *

# SETUP PYGAME
pygame.init()


# GRAPHIC
class Graph:

    def __init__(self):
        # Graph
        self.WIDTH = 200
        self.HEIGHT = 300
        self.window = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.graph_rect = pygame.rect.Rect(50, 50, self.WIDTH, self.HEIGHT)

        #Points
        self.Y_POS = self.HEIGHT - (m.tan(m.radians(30)) * (self.WIDTH / 2))
        self.X_POS = self.WIDTH / 10
        self.Z_POS = self.WIDTH - (self.WIDTH / 10)
        self.ZERO_POS = (self.WIDTH / 2, self.Y_POS - (((self.WIDTH / 2) - self.X_POS) * m.tan(m.radians(30))))
        self.points_3d = []

        # Font
        self.font = pygame.font.SysFont('Courier new', 15)

    # Update graph
    def update(self, points):
        self.window.fill(GREY_BG)

        y_axe_pos = [self.ZERO_POS, (self.WIDTH / 2, self.Y_POS - (self.HEIGHT / 2))]
        x_axe_pos = [(self.X_POS, self.Y_POS), self.ZERO_POS]
        z_axe_pos = [self.ZERO_POS, (self.Z_POS, self.Y_POS)]
        pygame.draw.line(self.window, WHITE, y_axe_pos[0], y_axe_pos[1])
        pygame.draw.line(self.window, WHITE, x_axe_pos[0], x_axe_pos[1])
        pygame.draw.line(self.window, WHITE, z_axe_pos[0], z_axe_pos[1])

        get_x = lambda x : (-x, (m.tan(m.radians(30)) * x))
        get_z = lambda z : (z, (m.tan(m.radians(30)) * z))
        get_y = lambda x, y, z : (x[1] + z[1]) - y

        for i in range(len(points)):
            point_surf = pygame.Surface((2, 2))
            point_surf.fill(WHITE)

            x_pos = self.ZERO_POS[0]
            y_pos = self.ZERO_POS[1]

            point = points[i]
            y = point[1] / 20
            print(y)
            a = 4
            if i > 0:
                x = y  ** 2
                z = (a * y ** 2) - y
            else:
                x = y
                z = x

            x_3d_pos = get_x(x)
            z_3d_pos = get_z(z)
            y_3d_pos = get_y(x_3d_pos, y, z_3d_pos)

            x_pos += x_3d_pos[0] + z_3d_pos[0]
            y_pos += y_3d_pos

            self.window.blit(point_surf, (x_pos, y_pos))


# WINDOW
class Window:

    # Constructor
    def __init__(self, display_width, display_height):
        # Window
        self.WIDTH = 300
        self.HEIGHT = 400
        self.window = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = pygame.rect.Rect((((3 * display_width) / 4) - (self.WIDTH / 2)) + (self.WIDTH / 4), display_height / 10, self.WIDTH ,self.HEIGHT )

        # Graph
        self.graph = Graph()

    # Update the real time graphic window
    def update(self, points):
        # BG
        self.window.fill(WHITE)
        pygame.draw.rect(self.window, GREY_BG, pygame.rect.Rect(3, 3, self.WIDTH - 6, self.HEIGHT - 6))

        #Graph
        self.graph.update(points)
        self.window.blit(self.graph.window, self.graph.graph_rect)
