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
        self.y_axis_rect = pygame.rect.Rect(30, 25, self.y_axis_surf.get_width(), self.y_axis_surf.get_height())

        self.x_axis_surf = pygame.Surface((self.graph_rect.width, 30))
        self.x_axis_rect = pygame.rect.Rect(75, 340, self.x_axis_surf.get_width(), self.x_axis_surf.get_height())

        # Font
        self.font = pygame.font.SysFont('Courier new', 15)

    # Rendering x axis
    def render_x_axis(self, points):
        self.x_axis_surf.fill(GREY_BG)

        line_n = 20
        points_len = len(points)
        if points_len < 100:
            for point in points:
                if point[0] % line_n == 0:
                    x_pos = (point[0] / points_len) * self.x_axis_surf.get_width()
                    pygame.draw.line(self.x_axis_surf, WHITE, (x_pos, 0), (x_pos, self.x_axis_surf.get_height()))

                    txt = self.font.render(str(int(point[0])), True, WHITE)
                    self.x_axis_surf.blit(txt, (x_pos - txt.get_width() - 3, self.x_axis_surf.get_height() - txt.get_height()))

            pygame.draw.line(self.x_axis_surf, WHITE, (1, 0), (1, self.x_axis_surf.get_height()))
            txt = self.font.render("0", True, WHITE)
            self.x_axis_surf.blit(txt, (3, self.x_axis_surf.get_height() - txt.get_height()))
        else:
            max_point = points[-1][0]
            for i in range(100):
                point = points[i - 100]
                if point[0] % line_n == 0:
                    x_pos = self.x_axis_surf.get_width() - ((max_point - point[0]) * (self.x_axis_surf.get_width() / 100))
                    pygame.draw.line(self.x_axis_surf, WHITE, (x_pos, 0), (x_pos, self.x_axis_surf.get_height()))

                    txt = self.font.render(str(int(point[0])), True, WHITE)
                    self.x_axis_surf.blit(txt, (x_pos - txt.get_width() - 3, self.x_axis_surf.get_height() - txt.get_height()))

    # Rendering y axis
    def render_y_axis(self):
        self.y_axis_surf.fill(GREY_BG)

        line_n = 5
        for i in range(line_n):
            y_pos = self.y_axis_surf.get_height() - (200 * ((i + 1) / line_n))
            txt = self.font.render(str((i * int(200 / line_n)) + int(200 / line_n)), True, WHITE)
            self.y_axis_surf.blit(txt, (0, y_pos))

            pygame.draw.line(self.y_axis_surf, WHITE, (self.y_axis_surf.get_width(), y_pos), (0, y_pos))
        pygame.draw.line(self.y_axis_surf, WHITE, (self.y_axis_surf.get_width(), self.y_axis_surf.get_height() - 1),
                         (0, self.y_axis_surf.get_height() - 1))
        txt = self.font.render("0", True, WHITE)
        self.y_axis_surf.blit(txt, (0, self.y_axis_surf.get_height() - txt.get_height()))

    # Render the graph
    def render_graph(self, points):
        self.window.fill(WHITE)
        pygame.draw.rect(self.window, GREY_BG, pygame.rect.Rect(3, 3, self.WIDTH - 6, self.HEIGHT - 6))

        points_len = len(points)

        if points_len < 100:
            for i in range(points_len):
                point_surf = pygame.Surface((1, 1))
                point_surf.fill(WHITE)
                point = points[i]
                last_point = points[i - 1]

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
    def update(self, points):
        # Graph
        self.render_graph(points)
        # Axis
        self.render_y_axis()
        self.render_x_axis(points)


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
    def update(self, points):
        # BG
        self.window.fill(WHITE)
        pygame.draw.rect(self.window, GREY_BG, pygame.rect.Rect(3, 3, self.WIDTH - 6, self.HEIGHT - 6))

        # Graph
        self.graph.update(points)
        self.window.blit(self.graph.window, self.graph.graph_rect)
        self.window.blit(self.graph.y_axis_surf, self.graph.y_axis_rect)
        self.window.blit(self.graph.x_axis_surf, self.graph.x_axis_rect)
