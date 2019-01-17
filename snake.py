import pygame, random, math
import cell as c
from config import *

colors_players = [(37, 7, 255), (35, 183, 253), (48, 254, 241), (19, 79, 251), (255, 7, 230), (255, 7, 23),
                  (6, 254, 13)]

def getDistance(pos1, pos2):
    diffX = math.fabs(pos1.x - pos2.x)
    diffY = math.fabs(pos1.y - pos2.y)

    return ((diffX ** 2) + (diffY ** 2)) ** (0.5)

# right, down, left, up
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]


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
        self.color = colors_players[random.randint(0, len(colors_players) - 1)]
        self.name = name
        print(name, self.startX, self.startY)

    def update(self, cell_list):
        self.move()
        self.collisionDetection(cell_list)

    def getTrunk(self):
        return self.trunk

    def crash(self, snakeList):
        for snake in snakeList:
            for pos in snake.getTrunk():
                if getDistance(pos, self.head) < 10:
                    return True

        return self.head.x >= screen_width or self.head.x < 0 or self.head.y >= screen_height or self.head.y < 0

    def collisionDetection(self, cell_list):
        for cell in cell_list:
            if (getDistance((cell), (self.head)) < 10):
                self.length += 1
                self.width += 0.05
                cell_list.remove(cell)
                cell = c.Cell(self.surface)
                cell_list.append(cell)
                return True
        return False

    def move(self):
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


