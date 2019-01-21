from snake import Snake, Pos
from config import *

def randomSnake(surface, i):
    sel = random.randint(1,3)
    sel = 1
    if sel == 1:
        return SnakeBot1(surface, str(i)+"Bot1")
    if sel == 2:
        return SnakeBot2(surface, str(i)+"Bot2")
    if sel == 3:
        return SnakeBot3(surface, str(i)+"Bot3")

# 무작위 행동
class SnakeBot1(Snake):
    def move(self, cell_list = [], enem_list = [], action=-1):
        try:
            self.times
        except AttributeError:
            self.times = 0

        try:
            self.dist
        except AttributeError:
            self.dist = random.randint(10,40)

        if self.times % self.dist == 0:
            self.dist = random.randint(10, 40)
            self.dir = random.randint(0, 3)
            tmp = self.head
            for i in range(3):
                self.head = tmp
                self.head = Pos(self.head.x + dx[self.dir], self.head.y + dy[self.dir])
                if self.crash(enem_list):
                    self.dir += 1
                    self.dir %= 4
                else:
                    break
        else:
            self.head = Pos(self.head.x + dx[self.dir], self.head.y + dy[self.dir])
        self.trunk.append(self.head)
        self.times+=1

        if len(self.trunk) > self.length:
            del self.trunk[0]

# Cell 이 많이 있는 곳으로 감
class SnakeBot2(Snake):
    def move(self, cell_list=[], enem_list=[], action=-1):
        try:
            self.times
        except AttributeError:
            self.times = 0

        try:
            self.dist
        except AttributeError:
            self.dist = 0

        dist = [500, 500, 500, 500]
        # right down left up
        cell_count = [0, 0, 0, 0]
        for cell in cell_list:
            d = getDistance(cell, self.head)
            if d < 1000:
                x_dist = self.head.x - cell.x
                y_dist = self.head.y - cell.y
                if math.fabs(x_dist) > math.fabs(y_dist):
                    if x_dist >= 0:
                        cell_count[0] += 1
                        dist[0] = min(dist[0], d)
                    else:
                        cell_count[2] += 1
                        dist[2] = min(dist[2], d)

                else:
                    if y_dist > 0:
                        cell_count[1] += 1
                        dist[1] = min(dist[1], d)
                    else:
                        cell_count[3] += 1
                        dist[3] = min(dist[3], d)

        self.dir = dist.index(min(dist))
        idx = 0
        for val in dist:
            if idx != self.dir and math.fabs(val - dist[self.dir]) < 3:
                self.dir = cell_count.index(max(cell_count[idx], cell_count[self.dir]))
            idx+=1

        self.times += 1
        self.head = Pos(self.head.x + dx[self.dir], self.head.y + dy[self.dir])
        self.trunk.append(self.head)
        if len(self.trunk) > self.length:
            del self.trunk[0]


# 적이 가까이 없는 곳으로 감.
class SnakeBot3(Snake):
    def move(self, cell_list=[], enem_list=[], action=-1):
        # right down left up
        dist = [0, 0, 0, 0]
        enem_count = [0, 0, 0, 0]
        for enem in enem_list:
            for pos in enem.getTrunk():
                d = getDistance(pos, self.head)
                if d < 1000:
                    x_dist = self.head.x - pos.x
                    y_dist = self.head.y - pos.y
                    if math.fabs(x_dist) > math.fabs(y_dist):
                        if x_dist >= 0:
                            enem_count[0] += 1
                            dist[0] = max(dist[0], d)
                        else:
                            enem_count[2] += 1
                            dist[2] = max(dist[2], d)
                    else:
                        if y_dist > 0:
                            enem_count[1] += 1
                            dist[1] = max(dist[1], d)
                        else:
                            enem_count[3] += 1
                            dist[3] = max(dist[3], d)

        try:
            self.times
        except AttributeError:
            self.times = 0

        try:
            self.dist
        except AttributeError:
            self.dist = random.randint(10, 40)
        if 0 in enem_count:
            if self.times > self.dist:
                self.dir = random.randint(0, 3)
                self.times = 0
                self.dist = random.randint(10, 40)
            else:
                self.times += 1
        else:
            self.dir = dist.index(max(dist))
            # self.dir = enem_count.index(min(enem_count))
        self.head = Pos(self.head.x + dx[self.dir], self.head.y + dy[self.dir])
        self.trunk.append(self.head)

        if len(self.trunk) > self.length:
            del self.trunk[0]


# 점수. 부딪힐 것 같으면 -500점. cell 있으면 3점, 가까이 있는 순서로 50, 30, 20, 10
class SnakeBot4(Snake):
    def move(self, cell_list=[], enem_list=[], action=-1):
        # right down left up
        dist = [0, 0, 0, 0]
        score = [0, 0, 0, 0]

        self.head = Pos(self.head.x + dx[self.dir], self.head.y + dy[self.dir])
        self.trunk.append(self.head)

        if len(self.trunk) > self.length:
            del self.trunk[0]