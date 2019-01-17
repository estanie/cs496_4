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
        self.color = getColor()

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.mass)
