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

import real_time_graph
import Two_dimensional_graph
import Three_dimensional_graph
import Text_window

# SETUP PYGAME
pygame.init()
display = pygame.display.set_mode((1024, 640), pygame.RESIZABLE)

# CSV FILE
filename = "points.csv"
file = open(filename, "w")
file.truncate()
file.close()


# KEY
class Key:

    # Constructor
    def __init__(self, name):
        self.name = name
        self.percentage = 1
        self.touch = 0

    # When a key is pressed
    def touched(self, key_touched):
        self.touch += 1
        self.percentage = abs((self.touch / key_touched) * 100)


# MAIN LOOP
def main():

    # Quit
    escape = False

    # Clock
    game_clock = 0

    # Key
    key_press = [False, 0]
    key_touched = 0
    keys = []

    # Windows
    real_time_graph_window = real_time_graph.Window(display.get_width(), display.get_height())
    points = real_time_graph_window.cursor.points

    two_dimensional_graph_window = Two_dimensional_graph.Window(display.get_width(), display.get_height())

    three_dimensional_graph_window = Three_dimensional_graph.Window(display.get_width(), display.get_height())

    text_window = Text_window.Window(display.get_width(), display.get_height(), 0)

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
                    if event.key in range(255):
                        key_touched += 1
                        key_find = 0
                        key_pressed = 0
                        for key in keys:
                            if key.name == event.key:
                                key_pressed = key
                                key.touched(key_touched)
                                key_find = 1
                        if key_find == 0:
                            key_pressed = Key(event.key)
                            key_pressed.touched(key_touched)
                            keys.append(key_pressed)
                        key_press = [True, key_pressed]

        # Windows
        real_time_graph_window.update(key_press, game_clock)
        two_dimensional_graph_window.update(points)
        three_dimensional_graph_window.update(points)
        text_window.update(key_press)
        if text_window.quit:
            text_window = Text_window.Window(display.get_width(), display.get_height(), text_window.text_num + 1)

        # Display
        display.blit(real_time_graph_window.window, real_time_graph_window.rect)
        display.blit(two_dimensional_graph_window.window, two_dimensional_graph_window.rect)
        display.blit(three_dimensional_graph_window.window, three_dimensional_graph_window.rect)
        display.blit(text_window.window, text_window.rect)
        pygame.display.update()

        # Clock
        game_clock += 1
        if game_clock == 1:
            points.remove(points[0])

        # Key pressed
        key_press = [False, 0]

    with open(filename, "r+", newline='') as csv_file:
        point_writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for point in points:
            line = str(point[0]) + "/" + str(point[1])
            point_writer.writerow(line)


# RUNNING THE PROGRAM
if __name__ == '__main__':
    main()
