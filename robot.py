import random

import numpy as np


class Robot(object):

    def __init__(self, x, y, maze_size, grid_size):
        self.x = x
        self.y = y
        self.size = maze_size
        LEFT = 0
        UP = 1
        RIGHT = 2
        DOWN = 3

        self.actions = {
            LEFT: 'left',
            UP: 'up',
            RIGHT: 'right',
            DOWN: 'down'
        }

        self.num_actions = len(self.actions)
        self.epsilon = 0.1
        self.alpha = 0.9
        self.gamma = 0.9
        self.neg_threshold = (-0.5 * self.size)

        self.q = np.zeros([maze_size, self.num_actions])
        self.visited = np.zeros(maze_size)
        self.state = 0
        self.action = random.choice(self.actions)
        self.total_reward = 0
        self.update_table = True
        self.grid_size = grid_size

    def do_action(self):
        self.state = int(self.grid_size[1] * self.y + self.x)
        self.visited[self.state] = 1
        if random.uniform(0, 1) < self.epsilon:
            self.action = random.choice(range(len(self.actions)))
        else:
            self.action = np.argmax(self.q[self.state])
        return self.actions[self.action]

    def update(self, reward):
        self.total_reward += reward
        new_state = int(self.grid_size[1] * self.y + self.x)
        old_value = self.q[self.state, self.action]
        next_max = np.max(self.q[new_state])

        if self.update_table:
            new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
            self.q[self.state, self.action] = new_value

        self.state = new_state
