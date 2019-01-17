import random, math

screen_width, screen_height = (500, 500)

# right, down, left, up
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]


def getColor():
    return [random.randint(0,255),random.randint(0,255),random.randint(0,255)]


def getDistance(pos1, pos2):
    diffX = math.fabs(pos1.x - pos2.x)
    diffY = math.fabs(pos1.y - pos2.y)

    return ((diffX ** 2) + (diffY ** 2)) ** (0.5)
