import math
import numpy as np
from scipy.linalg import norm
from time import sleep
from matplotlib import pyplot as plt


def a_star(grid, start, goal, k):
    """
    :grid: Numpy Array
    :start: Start coordinates
    :goal: End coordinates
    :k: K for Algorithms
    """
    # Initialize
    INF = 999

    # Heuristic Weight
    weight = k * math.sqrt(2)  # Try 1, 1.5, 2, 2.5, weight = 0 gives Djikstra algorithm
    print(weight)

    # Heuristic Map of all nodes
    xmax = grid.shape[0]
    ymax = grid.shape[1]

    f = np.zeros(grid.shape)
    g = np.zeros(grid.shape)
    h = np.zeros(grid.shape)

    for x in range(xmax):
        for y in range(ymax):
            if (grid[x, y] != INF):
                h[x, y] = weight * norm(list(set(goal)-set([x, y])))
                g[x, y] = INF

    # Initial conditions
    g[start[0], start[1]] = 0
    f[start[0], start[1]] = h[start[0], start[1]]

    closedNodes = np.empty(grid.shape)
    openNodes = [start, g[start[0], start[1]], f[start[0], start[1]], 0]  # [x y G F cameFrom]

    print(openNodes)

    # Solve
    solved = False
    while(len(openNodes) != 0):
        sleep(1)
        print(f)
        print("\n")
        print(openNodes)

        # Find node from open set with smallest F value
        [a, i] = min(openNodes[:, 3])
        
        # Set current node
        current = openNodes[i, :]
        plt.plot(current[0], current[1], 'o', 'color', 'y', 'MarkerFaceColor', 'y')
        
        # If goal is reached, break the loop
        if (current[0:1] == goal):
            closedNodes.append(current)
            solved = True
            break
        
        # Remove current node from open set and add it to closed set
        openNodes[i, :] = []
        closedNodes.append(current)
        
        # For all neighbors of current node
        for x in range(current[0]-1, current[0]+1):
            for y in range(current[1]-1, current[1]+1):
                
                # If out of range skip
                if (x<1 or x>xmax or y<1 or y>ymax):
                    pass
                
                # if object skip
                if (grid[x, y] == INF):
                    pass
                
                # if current node skip
                if ((x, y) == current):
                    pass
                
                # If already in closed set skip
                skip = 0
                for j in range(closedNodes.shape[0]):
                    if(x == closedNodes(j, 0) and y==closedNodes(j, 1)):
                        skip = 1
                        break

                if(skip == 1):
                    pass
                
                a = []
                # Check if already in open set
                if(openNodes.size != 0):
                    for j in range(openNodes.shape[0]):
                        if(x == openNodes[j, 0] and y==openNodes[j, 1]):
                            a = j
                            break
                
                newg = g[current[0], current[1]] + round(norm([current[0]-x, current[1]-y]), 1)
                
                # If not in open set, add to open set
                if(a.size != 0):
                    g[x, y] = newg
                    newf = g[x, y] + h[x, y]
                    newNode = [x, y, g[x, y], newf, closedNodes.size[0]]
                    openNodes = [openNodes, newNode]
                    plt.plot(x, y, 'x', 'color', 'b')
                    pass
                
                # If no better path, skip
                if (newg >= g[x, y]):
                    pass
                
                g[x, y] = newg
                newf = newf + h[x, y]
                openNodes[a, 3:5] = [newg, newf, closedNodes.size[0]]


    if (solved):
        # Path plotting
        j = closedNodes.shape[0]
        path = []
        while(j > 0):
            x = closedNodes[j, 1]
            y = closedNodes[j, 2]
            j = closedNodes[j, 5]
            path = [x, y, path]

        flag = True
    else:
        flag = False

    return [flag, path]
