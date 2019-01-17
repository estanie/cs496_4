from snake import Snake, Pos
import random
from config import *

def randomSnake(surface, i):
    sel = random.randint(1,4)

    if sel == 1:
        return SnakeBot1(surface, str(i)+"Bot1")
    if sel == 2:
        return SnakeBot2(surface, str(i)+"Bot2")
    if sel == 3:
        return SnakeBot3(surface, str(i)+"Bot3")
    if sel == 4:
        return SnakeBot4(surface, str(i)+"Bot4")

# 무작위 행동
class SnakeBot1(Snake):
    def move(self, cell_list = [], enem_list = []):
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
        self.head = Pos(self.head.x+dx[self.dir], self.head.y+dy[self.dir])
        self.trunk.append(self.head)
        self.times+=1

        if len(self.trunk) > self.length:
            del self.trunk[0]

# Cell 이 많이 있는 곳으로 감
class SnakeBot2(Snake):
    def move(self, cell_list=[], enem_list=[]):

        # right down left up
        cell_count = [0, 0, 0, 0]
        for cell in cell_list:
            if getDistance(cell, self.head) < 1000:
                x_dist = self.head.x - cell.x
                y_dist = self.head.y - cell.y
                if math.fabs(x_dist) > math.fabs(y_dist):
                    if x_dist >= 0:
                        cell_count[0] += 1
                    else:
                        cell_count[2] += 1
                else:
                    if y_dist > 0:
                        cell_count[1] += 1
                    else:
                        cell_count[3] += 1

        try:
            self.times
        except AttributeError:
            self.times = 0

        try:
            self.dist
        except AttributeError:
            self.dist = random.randint(10,40)

        if cell_count[0] == cell_count[1] and cell_count[1] == cell_count[2] and cell_count[2] and cell_count[3]:
            if self.times > self.dist:
                self.dir = random.randint(0,3)
                self.times = 0
                self.dist = random.randint(10,40)
            else:
                self.times+=1
        else:
            self.dir = cell_count.index(max(cell_count))

        self.head = Pos(self.head.x + dx[self.dir], self.head.y + dy[self.dir])
        self.trunk.append(self.head)

        if len(self.trunk) > self.length:
            del self.trunk[0]


# 적이 가까이 없는 곳으로 감.
class SnakeBot3(Snake):
    def move(self, cell_list=[], enem_list=[]):
        # right down left up
        enem_count = [0, 0, 0, 0]
        for enem in enem_list:
            for pos in enem.getTrunk():
                if getDistance(pos, self.head) < 1000:
                    x_dist = self.head.x - pos.x
                    y_dist = self.head.y - pos.y
                    if math.fabs(x_dist) > math.fabs(y_dist):
                        if x_dist >= 0:
                            enem_count[0] += 1
                        else:
                            enem_count[2] += 1
                    else:
                        if y_dist > 0:
                            enem_count[1] += 1
                        else:
                            enem_count[3] += 1

        try:
            self.times
        except AttributeError:
            self.times = 0

        try:
            self.dist
        except AttributeError:
            self.dist = random.randint(10, 40)

        if enem_count[0] == enem_count[1] and enem_count[1] == enem_count[2] and enem_count[2] and enem_count[3]:
            if self.times > self.dist:
                self.dir = random.randint(0, 3)
                self.times = 0
                self.dist = random.randint(10, 40)
            else:
                self.times += 1
        else:
            self.dir = enem_count.index(min(enem_count))
        self.head = Pos(self.head.x + dx[self.dir], self.head.y + dy[self.dir])
        self.trunk.append(self.head)

        if len(self.trunk) > self.length:
            del self.trunk[0]

# 적이 멀리 있고, cell이 가까운 곳으로 감
class SnakeBot4(Snake):
    def move(self, cell_list=[], enem_list=[]):
        # right down left up
        count = [0, 0, 0, 0]
        for cell in cell_list:
            if getDistance(cell, self.head) < 1000:
                x_dist = self.head.x - cell.x
                y_dist = self.head.y - cell.y
                if math.fabs(x_dist) > math.fabs(y_dist):
                    if x_dist >= 0:
                        count[0] += 2
                    else:
                        count[2] += 2
                else:
                    if y_dist > 0:
                        count[1] += 2
                    else:
                        count[3] += 2

        for enem in enem_list:
            for pos in enem.getTrunk():
                if getDistance(pos, self.head) < 1000:
                    x_dist = self.head.x - pos.x
                    y_dist = self.head.y - pos.y
                    if math.fabs(x_dist) > math.fabs(y_dist):
                        if x_dist >= 0:
                            count[0] -= 3
                        else:
                            count[2] -= 3
                    else:
                        if y_dist > 0:
                            count[1] -= 3
                        else:
                            count[3] -= 3
        try:
            self.times
        except AttributeError:
            self.times = 0

        try:
            self.dist
        except AttributeError:
            self.dist = random.randint(10, 40)

        if count[0] == count[1] and count[1] == count[2] and count[2] and count[3]:
            if self.times > self.dist:
                self.dir = random.randint(0, 3)
                self.times = 0
                self.dist = random.randint(10, 40)
            else:
                self.times += 1
        else:
            self.dir = count.index(max(count))
        self.head = Pos(self.head.x + dx[self.dir], self.head.y + dy[self.dir])
        self.trunk.append(self.head)

        if len(self.trunk) > self.length:
            del self.trunk[0]
