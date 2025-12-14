from collections import deque
from typing import Any, Generator

from maze import Maze, WALL, START, GOAL, VISITED, FRONTIER, PATH, EMPTY
import random
"""
DISCLAIMER:
- Used ChatGPT and tutorials for learning and figuring out how to use BFS and DFS algorithms.
- Only AI-Generated function is the maze generator, a user tool that was created as an afterthought.
- Everything else was coded based on brief, undetailed steps given by ChatGPT and tutorials.

- To allow each step to generate individually rather than all at once, yield is used.
"""
def bfs_algorithm(maze: Maze) -> Generator[None, Any, None]:
    """
    Breadth-first search, generates solving animation.
    """
    maze.reset_search_result() #Clears any previous search paths

    #Double-ended queue data structure recommended for BFS performance
    queue=deque()
    queue.append(maze.start)

    breadcrumbs={maze.start:None} #Tracks each discovered cell and initial cell, used for final path
    start_row,start_col=maze.start
    maze.grid[start_row][start_col]=START

    while queue: #Only stops when queue is fully empty
        row,col=queue.popleft()
        if (row,col)!=maze.start and (row,col)!=maze.goal:
            maze.grid[row][col]=VISITED
            yield
        if (row,col)==maze.goal:
            break

        for nr, nc in maze.neighbors(row,col):
            if maze.grid[nr][nc]==WALL or (nr, nc) in breadcrumbs:
                continue
            breadcrumbs[(nr,nc)]=(row, col)
            if (nr, nc) != maze.start and (nr, nc) != maze.goal:
                maze.grid[nr][nc] = FRONTIER
            queue.append((nr,nc))

    #Reconstructs path if reached
    if maze.goal in breadcrumbs:
        node=maze.goal
        while node is not None:
            row,col=node
            if maze.grid[row][col] not in [START, GOAL]:
                maze.grid[row][col]=PATH
            node=breadcrumbs[node]
            yield


def dfs_algorithm(maze: Maze) -> Generator[None, Any, None]:
    """
    Depth-first search, generates solving animation
    """
    maze.reset_search_result()
    breadcrumbs = {maze.start: None}
    stack=[maze.start]
    while stack:
        row, col=stack.pop()
        if maze.grid[row][col]==VISITED:
            continue
        if (row,col)!=maze.start and (row,col)!=maze.goal:
            maze.grid[row][col]=VISITED
            yield
        if (row,col)==maze.goal:
            break
        for nr, nc in maze.neighbors(row, col):
            if maze.grid[nr][nc] == WALL or (nr, nc) in breadcrumbs:
                continue
            breadcrumbs[(nr, nc)] = (row, col)
            stack.append((nr, nc))
            if (nr, nc) != maze.start and (nr, nc) != maze.goal:
                maze.grid[nr][nc] = FRONTIER

    #Reconstructs path if reached
    if maze.goal in breadcrumbs:
        node=maze.goal
        while node is not None:
            row,col=node
            if maze.grid[row][col] not in [START, GOAL]:
                maze.grid[row][col]=PATH
            node=breadcrumbs[node]
            yield

def maze_generator(maze: Maze) -> None:
    """
    Depth-first search-based maze generator, an option if user prefers to generate maze automatically
    """
    maze.fill()
    start_r, start_c = 1, 1
    maze.grid[start_r][start_c] = EMPTY
    stack = [(start_r, start_c)]
    while stack:
        r, c = stack.pop()
        #Only consider neighbors 2 cells away
        neighbors = [(nr, nc) for nr, nc in maze.neighbors(r, c, 2) if maze.grid[nr][nc] == WALL]
        if not neighbors:
            continue
        stack.append((r, c))
        nr, nc = random.choice(neighbors)
        wall_r = (r + nr) // 2
        wall_c = (c + nc) // 2
        maze.grid[wall_r][wall_c] = EMPTY
        maze.grid[nr][nc] = EMPTY

        stack.append((nr, nc))