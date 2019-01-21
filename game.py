import pygame
import numpy as np
from snake import Snake
from bot import randomSnake
from cell import Cell
from config import *

class Game:
    def __init__(self, show_game=False):
        print("게임 세팅")
        """실행할 때 한 번만 불림."""
        self.show_game = show_game
        #pygame 환경 셋팅

        if self.show_game:
            pygame.init()
            t_surface = pygame.Surface((95, 25), pygame.SRCALPHA)  # transparent rect for score
            t_lb_surface = pygame.Surface((155, 278), pygame.SRCALPHA)  # transparent rect for leaderboard
            t_surface.fill((50, 50, 50, 80))
            t_lb_surface.fill((50, 50, 50, 80))
            pygame.display.set_caption("Slither.io")
            self.clock = pygame.time.Clock()
            self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.surface = ''

        self.total_game = 0

    def reset(self):
        print("게임 초기화")
        """지렁이들, 셀 위치, 내 위치와 보상값 초기화."""
        self.current_reward = 0
        self.total_game += 1
        self.cell_list = list()

        blob = Snake(self.surface, "ME")
        self.snake_list = [blob]

        for i in range(0, BOT_NUMBER):
            self.snake_list.append(randomSnake(self.surface, i))

        self.spawn_cells(CELL_COUNT)
        return self._get_state()

    def step(self, action=4):
        """게임 실행하는 부분."""
        if self.show_game:
            # 게임 종료할 건지 event 받는 부분.
            # for e in pygame.event.get():
            #     if e.type == pygame.KEYDOWN:
            #         if e.key == pygame.K_ESCAPE:
            #             pygame.quit()
            #             quit()
            #     if e.type == pygame.QUIT:
            #         pygame.quit()
            #         quit()
            pass
        my_previous_length = self.snake_list[0].length
        for snake in self.snake_list[1:]:
            snake.update(self.cell_list, self.snake_list)

        for i in range(1, BOT_NUMBER):
            tmp = self.snake_list[:]
            snake = tmp[i]

            tmp.remove(snake)
            if snake.crash(tmp):
                j = 0
                for c in snake.getTrunk():
                    if j % 3 == 0:
                        self.cell_list.append(Cell(self.surface, c.x, c.y))
                    j += 1
                self.snake_list[i] = randomSnake(self.surface, i)

        self.snake_list[0].update(self.cell_list, self.snake_list, action, is_me=True)
        gameover = self.snake_list[0].crash(self.snake_list[1:])

        while len(self.cell_list) < CELL_COUNT:
            self.cell_list.append(Cell(self.surface))

        if self.show_game:
            self.draw()

        if gameover:
            reward = -1
        else:
            reward = self.snake_list[0].length - my_previous_length

        self.current_reward += reward

        return self._get_state(), reward, gameover

    def draw(self):
        """show_game 이 True인 경우, 게임을 보여줌."""
        clock = pygame.time.Clock()
        clock.tick(30)

        self.surface.fill((242, 251, 255))
        self.draw_grid()

        for c in self.cell_list:
            c.draw()

        for snake in self.snake_list:
            snake.draw()

        pygame.display.flip()

    def spawn_cells(self, num_of_cells):
        for i in range(num_of_cells):
            cell = Cell(self.surface)
            self.cell_list.append(cell)

    def draw_grid(self):
        for i in range(0, 500, 25):
            pygame.draw.line(self.surface, (230, 240, 240), (0, i), (SCREEN_WIDTH, i), 3)
            pygame.draw.line(self.surface, (230, 240, 240), (i, 0), (i, SCREEN_HEIGHT), 3)

    def _get_state(self):
        """게임의 상태를 가져옴.

        게임 상태는 250*250 셀로 구성되어 있고,
        cell은 2, 부딪힐만한건 -1이고, 내 몸통은 1이다. 빈 곳은 0임.
        모델을 일단 그대로 써보고 싶으니까, 2차원 -> 1차원으로 변환해 사용.

        TODO(gayeon): 여기 만들기..
        """
        state = np.zeros((SEND_WIDTH * 2, SEND_HEIGHT * 2))

        sx = self.snake_list[0].head.x - SEND_WIDTH
        sy = self.snake_list[0].head.y - SEND_HEIGHT

        for cell in self.cell_list:
            x, y = (cell.x-sx, cell.y-sy)
            if x < SEND_WIDTH * 2 and x >= 0 and y < SEND_HEIGHT * 2 and y >= 0:
                state[x, y] = 2

        for pos in self.snake_list[0].trunk:
            x, y = (pos.x - sx, pos.y - sy)
            if x < SEND_WIDTH * 2 and x >= 0 and y < SEND_HEIGHT * 2 and y >= 0:
                state[x, y] = 1

        for snake in self.snake_list[1:]:
            for pos in snake.trunk:
                x, y = (pos.x - sx, pos.y - sy)
                if x < SEND_WIDTH * 2 and x >= 0 and y < SEND_HEIGHT * 2 and y >= 0:
                    state[x, y] = -1
        return state
