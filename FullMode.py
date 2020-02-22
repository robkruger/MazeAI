import copy
from datetime import datetime

from maze import Maze

grid_size = (25, 25)
m = Maze(True, grid_size, None, None, (grid_size[0] - 1, grid_size[1] - 1))
m.robot.x = 0
m.robot.y = 0
while not m.started:
    m.parse_events(True)
    m.draw()
r = copy.deepcopy(m.robot)
c = copy.deepcopy(m.cells)
s = copy.deepcopy(m.star_loc)
l = (r.x, r.y)

print("STARTING TRAINING")
now = datetime.now()

wins = 0
win_percentage = 0
i = 0
r.epsilon = 0.1
r.alpha = 0.9
r.gamma = 0.9

while 1:
    i += 1
    win_percentage = (wins / 100) * 100
    if win_percentage > 90:
        break
    if i % 100 == 0:
        print(i, str(win_percentage) + "%")
        wins = 0
    r.total_reward = 0
    r.x = 0
    r.y = 0
    m = Maze(False, grid_size, r, c, (grid_size[0] - 1, grid_size[1] - 1), True)
    while not m.done:
        m.parse_events()
        m.draw()
        if m.end:
            if m.won:
                wins += 1
            m.done = True

print("TRAINING COMPLETE AFTER " + str(int((datetime.now() - now).total_seconds() + 0.5)) + " SECONDS")

r.total_reward = 0
r.x = 0
r.y = 0
r.epsilon = 0.0
m = Maze(False, grid_size, r, c, (grid_size[0] - 1, grid_size[1] - 1), True)
m.robot.x = 0
m.robot.y = 0
m.robot.update_table = False
locations = [(0, 0)]
while not m.started:
    m.parse_events(True)
    m.draw()
while not m.done:
    if not m.end:
        m.parse_events()
        locations.append((m.robot.x, m.robot.y))
    m.draw(locations)
