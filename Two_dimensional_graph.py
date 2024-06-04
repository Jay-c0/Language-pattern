"""
2D graphic
"""

import pygame

from ref import *

# SETUP PYGAME
pygame.init()


class Graph:

    def __init__(self):
        # Graph
        self.WIDTH = 200
        self.HEIGHT = 300
        self.window = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.graph_rect = pygame.rect.Rect(75, 25, self.WIDTH, self.HEIGHT)

        # Axis
        self.y_axis_surf = pygame.Surface((30, self.graph_rect.height))
        self.y_axis_rect = pygame.rect.Rect(0, 0, self.y_axis_surf.get_width(), self.y_axis_surf.get_height())

    #
    def y_axis(self):
        pass


    # Render the graph
    def render_graph(self, points, clock):
        self.window.fill(WHITE)
        pygame.draw.rect(self.window, GREY_BG, pygame.rect.Rect(3, 3, self.WIDTH - 6, self.HEIGHT - 6))

        points_len = len(points)

        if points_len < 100:
            for i in range(points_len):
                point_surf = pygame.Surface((1, 1))
                point_surf.fill(WHITE)
                point = points[i]
                last_point = points[i - 1]
                if i > 0:
                    x_pos = ((i - 1) / points_len) * self.WIDTH
                    y_pos = self.HEIGHT - point[1]
                    last_x = ((i - 2) / points_len) * self.WIDTH
                    last_y = self.HEIGHT - last_point[1]

                    point_rect = pygame.rect.Rect(abs(x_pos), y_pos, 1, 1)

                    self.window.blit(point_surf, point_rect)
                    pygame.draw.line(self.window, WHITE, (last_x, last_y), (x_pos, y_pos))
        else:
            for i in range(100):
                point_surf = pygame.Surface((1, 1))
                point_surf.fill(WHITE)

                point = points[-i - 1]
                last_point = points[-i]

                x_pos = self.WIDTH - (2 + (i * 2))
                y_pos = self.HEIGHT - point[1]
                last_x = self.WIDTH - (i * 2)
                last_y = self.HEIGHT - last_point[1]

                point_rect = pygame.rect.Rect(x_pos, y_pos, 1, 1)

                self.window.blit(point_surf, point_rect)
                pygame.draw.line(self.window, WHITE, (last_x, last_y), (x_pos, y_pos))

    # Update graph
    def update(self, points, clock):
        self.render_graph(points, clock)
        txt = pygame.font.SysFont('Comic Sans MS', 30)
        txt_surf = txt.render("hello world!", WHITE, False)
        self.window.blit(txt_surf, (0, 0))


# WINDOW
class Window:

    # Constructor
    def __init__(self, display_width, display_height):
        # Window
        self.WIDTH = 300
        self.HEIGHT = 400
        self.window = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = pygame.rect.Rect((((display_width / 2) - (self.WIDTH / 2)) / 2) - (self.WIDTH / 2),
                                     display_height / 10, self.WIDTH, self.HEIGHT)

        # Graph
        self.graph = Graph()

    # Update the real time graphic window
    def update(self, points, clock):
        # BG
        self.window.fill(WHITE)
        pygame.draw.rect(self.window, GREY_BG, pygame.rect.Rect(3, 3, self.WIDTH - 6, self.HEIGHT - 6))

        # Graph
        self.graph.update(points, clock)
        self.window.blit(self.graph.window, self.graph.graph_rect)



