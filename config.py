import random, math

SCREEN_WIDTH, SCREEN_HEIGHT = (500, 500)

# 내 주변 += 얼마만큼 넘길건지
SEND_WIDTH, SEND_HEIGHT = (15, 15)

# right, down, left, up
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

CELL_COUNT = 50
BOT_NUMBER = 8


def getColor():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


def getDistance(pos1, pos2):
    diffX = math.fabs(pos1.x - pos2.x)
    diffY = math.fabs(pos1.y - pos2.y)

    return ((diffX ** 2) + (diffY ** 2)) ** (0.5)
