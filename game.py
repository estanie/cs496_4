import pygame
from snake import Snake
from bot import randomSnake, SnakeBot1, SnakeBot2, SnakeBot3, SnakeBot4
from cell import Cell
from config import *

#pygame 환경 셋팅
pygame.init()
t_surface = pygame.Surface((95, 25), pygame.SRCALPHA)  # transparent rect for score
t_lb_surface = pygame.Surface((155, 278), pygame.SRCALPHA)  # transparent rect for leaderboard
t_surface.fill((50, 50, 50, 80))
t_lb_surface.fill((50, 50, 50, 80))
pygame.display.set_caption("Slither.io")
clock = pygame.time.Clock()
surface = pygame.display.set_mode((screen_width, screen_height))

cell_list = list()
cell_count = 50
bot_number = 8


def spawn_cells(numOfCells):
    for i in range(numOfCells):
        cell = Cell(surface)
        cell_list.append(cell)


def draw_grid():
    for i in range(0, 500, 25):
        pygame.draw.line(surface, (230, 240, 240), (0, i), (screen_width, i), 3)
        pygame.draw.line(surface, (230, 240, 240), (i, 0), (i, screen_height), 3)

blob = Snake(surface, "ME")
snakeList = [blob]

for i in range(0, bot_number):
    snakeList.append(randomSnake(surface, i))

spawn_cells(cell_count)
gameover = False

print("PLAY")
while not gameover:
    clock.tick(70)
    for e in pygame.event.get():
        if (e.type == pygame.KEYDOWN):
            if (e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        if (e.type == pygame.QUIT):
            pygame.quit()
            quit()
    for snake in snakeList:
        snake.update(cell_list, snakeList)

    surface.fill((242, 251, 255))
    if blob.crash(snakeList[1:]):
        gameover = True
        print("gameover")

    tmp = snakeList[:]
    for i in range(1, bot_number):
        tmp = snakeList[:]
        snake = tmp[i]

        tmp.remove(snake)
        if snake.crash(tmp):
            j = 0
            for c in snake.getTrunk():
                if j % 3 == 0:
                    cell_list.append(Cell(surface, c.x, c.y))
                j+=1
            snakeList[i] = randomSnake(surface, i)
        tmp = snakeList[:]

    # surface.fill((0,0,0))
    draw_grid()
    while len(cell_list) < cell_count:
        cell_list.append(Cell(surface))

    for c in cell_list:
        c.draw()

    for snake in snakeList:
        snake.draw()

    pygame.display.flip()

