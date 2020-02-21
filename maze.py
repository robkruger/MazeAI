import time
from random import shuffle, randrange

import pygame
from Cell import Cell
from robot import Robot


class Maze(object):

    def __init__(self, grad, grid_size, robot=None, c=None, s=None, wait=False):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.done = False
        self.w, self.h = pygame.display.get_surface().get_size()
        self.grid_size = grid_size
        self.cell_size = (320 * (self.w / 400)) / self.grid_size[0]
        self.offset = 40 * (self.w / 400)
        self.cells = []
        self.wait = wait
        self.started = False
        for _ in range(self.grid_size[0]):
            self.cells.append([])
        self.gradually = grad

        if s is None:
            self.star_loc = (randrange(self.grid_size[0]), randrange(self.grid_size[1]))
        else:
            self.star_loc = s
        self.star = pygame.image.load("assets/star.png").convert_alpha()
        self.star = pygame.transform.scale(self.star, (int(self.cell_size), int(self.cell_size)))
        self.robot_img = pygame.image.load("assets/robot.png").convert_alpha()
        self.robot_img = pygame.transform.scale(self.robot_img, (int(self.cell_size), int(self.cell_size)))
        if robot is None:
            self.robot = Robot(randrange(self.grid_size[0]), randrange(self.grid_size[1]),
                               self.grid_size[0] * self.grid_size[1], self.grid_size)
        else:
            self.robot = robot
        self.selection_x = 0
        self.selection_y = 0
        self.selection_type = 0
        self.end = False
        self.won = False

        if not (c is None):
            self.cells = c
        else:
            for x in range(self.grid_size[0] - 1):
                cell = Cell(False, True, x, 0)
                self.cells[x].append(cell)
                if self.gradually:
                    time.sleep(0.04)
                    self.parse_events()
                    self.draw()
                for y in range(1, self.grid_size[1]):
                    cell = Cell(True, True, x, y)
                    self.cells[x].append(cell)
                    if self.gradually:
                        time.sleep(0.04)
                        self.parse_events()
                        self.draw()

            for y in range(self.grid_size[1]):
                cell = Cell(True, False, self.grid_size[0] - 1, y)
                self.cells[self.grid_size[0] - 1].append(cell)
                if self.gradually:
                    time.sleep(0.04)
                    self.parse_events()
                    self.draw()

            visited = [[False] * self.grid_size[0] + [True] for _ in range(self.grid_size[0])] + [
                [True] * (self.grid_size[0] + 1)]

            def walk(i, j):
                visited[j][i] = True

                d = []

                if i == 0 and j == 0:
                    d = [(1, 0), (0, 1)]
                elif i == 0 and 0 < j < len(self.cells[0]) - 1:
                    d = [(1, 0), (0, 1), (0, -1)]
                elif 0 < i < len(self.cells) - 1 and j == 0:
                    d = [(1, 0), (0, 1), (-1, 0)]
                elif 0 < i < len(self.cells) - 1 and 0 < j < len(self.cells[0]) - 1:
                    d = [(1, 0), (0, 1), (0, -1), (-1, 0)]
                elif i == len(self.cells) - 1 and 0 < j < len(self.cells[0]) - 2:
                    d = [(0, 1), (0, -1), (-1, 0)]
                elif 0 < i < len(self.cells) - 1 and j == len(self.cells[0]) - 1:
                    d = [(1, 0), (0, -1), (-1, 0)]
                elif i == len(self.cells) - 1 and j == len(self.cells[0]) - 2:
                    d = [(0, -1), (-1, 0)]

                shuffle(d)
                for (xx, yy) in d:
                    if visited[j + yy][i + xx]:
                        continue
                    if xx == -1:
                        self.cells[i - 1][j].toggle_east()
                    elif yy == -1:
                        self.cells[i][j].toggle_north()
                    elif xx == 1:
                        self.cells[i][j].toggle_east()
                    elif yy == 1:
                        self.cells[i][j + 1].toggle_north()

                    if self.gradually:
                        time.sleep(0.1)
                        self.parse_events()
                        self.draw()

                    walk(i + xx, j + yy)

            walk(randrange(self.grid_size[0]), randrange(self.grid_size[1]))

    def parse_events(self, starting_fase=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.selection_x = int((pygame.mouse.get_pos()[0] - self.offset) / self.cell_size)
                    self.selection_y = int((pygame.mouse.get_pos()[1] - self.offset) / self.cell_size)
                elif event.button == 3:
                    self.started = True
        if self.selection_x != -1 or self.selection_y != -1:
            if not self.selection_type:
                self.cells[self.selection_x][self.selection_y].toggle_north()
            else:
                self.cells[self.selection_x][self.selection_y].toggle_east()
            self.selection_type = (self.selection_type + 1) % 2
        self.selection_x = -1
        self.selection_y = -1

        if starting_fase:
            return

        action = self.robot.do_action()
        if action == 'up':
            if self.robot.y == 0:
                self.robot.update(-0.8)
            elif not self.cells[self.robot.x][self.robot.y].north:
                self.robot.y -= 1
                state = int(self.grid_size[1] * self.robot.y + self.robot.x)
                if self.robot.x == self.star_loc[0] and self.robot.y == self.star_loc[1]:
                    self.robot.update(1)
                    self.won = True
                    self.end = True
                elif self.robot.visited[state]:
                    self.robot.update(-0.25)
                else:
                    self.robot.update(-0.04)
            else:
                self.robot.update(-0.75)
        elif action == 'down':
            if self.robot.y == self.grid_size[1] - 1:
                self.robot.update(-0.8)
            elif not self.cells[self.robot.x][self.robot.y + 1].north:
                self.robot.y += 1
                state = int(self.grid_size[1] * self.robot.y + self.robot.x)
                if self.robot.x == self.star_loc[0] and self.robot.y == self.star_loc[1]:
                    self.robot.update(1)
                    self.won = True
                    self.end = True
                elif self.robot.visited[state]:
                    self.robot.update(-0.25)
                else:
                    self.robot.update(-0.04)
            else:
                self.robot.update(-0.75)
        elif action == 'left':
            if self.robot.x == 0:
                self.robot.update(-0.8)
            elif not self.cells[self.robot.x - 1][self.robot.y].east:
                self.robot.x -= 1
                state = int(self.grid_size[1] * self.robot.y + self.robot.x)
                if self.robot.x == self.star_loc[0] and self.robot.y == self.star_loc[1]:
                    self.robot.update(1)
                    self.won = True
                    self.end = True
                elif self.robot.visited[state]:
                    self.robot.update(-0.25)
                else:
                    self.robot.update(-0.04)
            else:
                self.robot.update(-0.75)
        elif action == 'right':
            if self.robot.x == self.grid_size[0] - 1:
                self.robot.update(-0.8)
            elif not self.cells[self.robot.x][self.robot.y].east:
                self.robot.x += 1
                state = int(self.grid_size[1] * self.robot.y + self.robot.x)
                if self.robot.x == self.star_loc[0] and self.robot.y == self.star_loc[1]:
                    self.robot.update(1)
                    self.won = True
                    self.end = True
                elif self.robot.visited[state]:
                    self.robot.update(-0.25)
                else:
                    self.robot.update(-0.04)
            else:
                self.robot.update(-0.75)

        if self.robot.total_reward < self.robot.neg_threshold:
            self.end = True
        if self.wait:
            time.sleep(0.1)

    def draw(self, locations=None):
        self.screen.fill((255, 255, 255))

        if locations is not None:
            for loc in locations:
                pygame.draw.rect(self.screen, (0, 255, 0), (loc[0] * self.cell_size + self.offset,
                                                            loc[1] * self.cell_size + self.offset,
                                                            self.cell_size,
                                                            self.cell_size))

        for x in range(self.grid_size[0]):
            pygame.draw.line(self.screen, (255, 0, 0), (x * self.cell_size + self.offset, self.w - self.offset),
                             (x * self.cell_size + self.offset + self.cell_size, self.w - self.offset))
            pygame.draw.line(self.screen, (255, 0, 0), (x * self.cell_size + self.offset, self.offset),
                             (x * self.cell_size + self.offset + self.cell_size, self.offset))
            pygame.draw.line(self.screen, (255, 0, 0), (self.offset, x * self.cell_size + self.offset),
                             (self.offset, x * self.cell_size + self.offset + self.cell_size))
            pygame.draw.line(self.screen, (255, 0, 0), (self.w - self.offset, x * self.cell_size + self.offset),
                             (self.w - self.offset, x * self.cell_size + self.offset + self.cell_size))

        for x in range(len(self.cells)):
            for y in range(len(self.cells[x])):
                if self.cells[x][y].north:
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (self.cells[x][y].x * self.cell_size + self.offset,
                                      self.cells[x][y].y * self.cell_size + self.offset),
                                     (self.cells[x][y].x * self.cell_size + self.offset + self.cell_size,
                                      self.cells[x][y].y * self.cell_size + self.offset))
                if self.cells[x][y].east:
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (self.cells[x][y].x * self.cell_size + self.offset + self.cell_size,
                                      self.cells[x][y].y * self.cell_size + self.offset),
                                     (self.cells[x][y].x * self.cell_size + self.offset + self.cell_size,
                                      self.cells[x][y].y * self.cell_size + self.offset + self.cell_size))

        if hasattr(self, 'star'):
            self.screen.blit(self.star, (
                self.star_loc[0] * self.cell_size + self.offset, self.star_loc[1] * self.cell_size + self.offset))

        if hasattr(self, 'robot'):
            self.screen.blit(self.robot_img,
                             (self.robot.x * self.cell_size + self.offset, self.robot.y * self.cell_size + self.offset))

        pygame.display.flip()
