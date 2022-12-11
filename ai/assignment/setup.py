import numpy as np
from matplotlib import pyplot as plt
from astar import a_star
from time import sleep


##### Dijkstra and A* Algorithm #####

# Init
INF = 999

# Define Number of Nodes
xmax = 6
ymax = 5

# Define the Start and Goal coordinates
start = [0, 0]
goal  = [5, 4]


# Nodes
grid = np.zeros((xmax, ymax))

# To define objects, set their grid(x, y) to 999
grid[0, 1] = INF
grid[2, 1] = INF
grid[2, 3] = INF
grid[3, 1] = INF
grid[3, 4] = INF
grid[4, 4] = INF
# grid[12, 6:8]  = INF
# grid[16, 4:10] = INF

plt.figure(1)

# surf(grid)

gray = [0.5, 0.5, 0.5]

plt.plot(start[0], start[1], 's', 'MarkerFaceColor', 'b')
plt.plot(goal[0],  goal[1],  's', 'MarkerFaceColor', 'g')

# k=0;  # Set k=0 for Dijkstra's Algorithm
k=1     # Set k=1 for Astar's algorithm

[flag, path] = a_star(grid, start, goal, k)

if(flag):
    print('Path Found')
    for j in range(len(path)):
        plt.plot(path[j, 0], path[j, 1], 'X', 'color', 'r')
        sleep(1)

    plt.plot(start[0], start[1], 's', 'MarkerFaceColor', 'r')
    plt.plot(goal[1],   goal[1], 's', 'MarkerFaceColor', 'g')
else:
    print('No Path Found')

