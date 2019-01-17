import random
import pygame
from config import *

class Cell:
    def __init__(self, surface, x = -1, y = -1):
        if x == -1:
            self.x = random.randint(20, screen_width)
        else:
            self.x = x
        if y == -1:
            self.y = random.randint(20, screen_height)
        else:
            self.y = y
        self.mass = 7
        self.surface = surface
        self.color = colors_cells[random.randint(0, len(colors_cells) - 1)]

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.mass)

colors_cells = [(80, 252, 54), (36, 244, 255), (243, 31, 46), (4, 39, 243), (254, 6, 178), (255, 211, 7), (216, 6, 254),
                (145, 255, 7), (7, 255, 182), (255, 6, 86), (147, 7, 255)]

