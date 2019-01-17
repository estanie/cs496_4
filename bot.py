from snake import Snake, Pos
import random

# right, down, left, up
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]


class SnakeBot1(Snake):

    def move(self):
        try:
            self.times
        except AttributeError:
            self.times = 0

        if self.times % 27 == 0:
            self.dir = random.randint(0, 3)
        self.head = Pos(self.head.x+dx[self.dir], self.head.y+dy[self.dir])
        self.trunk.append(self.head)
        self.times+=1

        if len(self.trunk) > self.length:
            del self.trunk[0]