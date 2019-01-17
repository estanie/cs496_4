import pygame
from config import *

class Pos:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


# TODO(gayeon): 반경 세팅을 내 width 맞춰서 하기.. width 설정을 길이에 맞춰서 적용시키기...
class Snake:
    def __init__(self, surface, name=""):
        self.startX = random.randint(100, 400)
        self.startY = random.randint(100, 400)
        self.trunk = [Pos(self.startX, self.startY)]
        self.head = Pos(self.startX, self.startY)
        self.width = 5
        self.dir = 0
        self.length = 1
        self.surface = surface
        self.color = getColor()
        self.name = name
        print(name, self.startX, self.startY)

    def update(self, cell_list, enem_list):
        self.move(cell_list, enem_list)
        self.collisionDetection(cell_list)

    def getTrunk(self):
        return self.trunk

    def crash(self, snakeList):
        for snake in snakeList:
            for pos in snake.getTrunk():
                if getDistance(pos, self.head) < snake.width:
                    return True

        return self.head.x >= screen_width or self.head.x < 0 or self.head.y >= screen_height or self.head.y < 0

    def collisionDetection(self, cell_list):
        for cell in cell_list:
            if (getDistance((cell), (self.head)) < self.width):
                self.length += 1
                self.width += 0.05
                cell_list.remove(cell)
                return True
        return False

    def move(self, cell_list=[], enem_list=[]):
        event = pygame.key.get_pressed()
        if (event[pygame.K_RIGHT]):
            self.dir = 0
        if (event[pygame.K_DOWN]):
            self.dir = 1
        if (event[pygame.K_LEFT]):
            self.dir = 2
        if (event[pygame.K_UP]):
            self.dir = 3

        self.head = Pos(self.head.x+dx[self.dir], self.head.y+dy[self.dir])
        self.trunk.append(self.head)

        if len(self.trunk) > self.length:
            del self.trunk[0]

    def drawText(self, message, pos, color=(0, 0, 0)):
        self.surface.blit(pygame.font.SysFont('Ubuntu', 20, True).render(message, 1, color), pos)

    def draw(self):
        for pos in self.trunk:
            pygame.draw.circle(self.surface, self.color, (int(pos.x), int(pos.y)), int(self.width))

        if (len(self.name) > 0):
            self.drawText(self.name, (self.head.x, self.head.y))


