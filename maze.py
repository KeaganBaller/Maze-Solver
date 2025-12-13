import pygame
from itertools import chain
#Cell types, used by 2D int array
EMPTY=0
WALL=1
START=2
GOAL=3
VISITED=4
FRONTIER=5
PATH=6

#Cell colors, index corresponds with cell value
COLORS=("#303030", "#1c1c1c", "#26ff00", "#ff1100", "#4646c8", "#7878ff", "#fafa34")

class Maze:
    def __init__(self, rows, cols) -> None:
        self.rows=rows
        self.cols=cols
        self.grid=[[EMPTY for i in range(cols)] for i in range(rows)]
        self.start=[]
        self.goal=[]

    def draw(self, surface, rect) -> None:
        _,_,width,height=rect
        cell_width=width/self.cols
        cell_height = height/self.rows
        for row in range(self.rows):
            for col in range(self.cols):
                cell_color=COLORS[self.grid[row][col]]
                cell=pygame.Rect(cell_width*col, cell_height*row, cell_width, cell_height)
                pygame.draw.rect(surface, cell_color, cell)
                pygame.draw.rect(surface, "#4a4a4a", cell, 1) #Outlines

    def pos_to_cell(self, x, y, rect):
        _,_,width,height=rect
        cell_width = width / self.cols
        cell_height = height / self.rows
        col=int(x//cell_width)
        row=int(y//cell_height)
        return row, col

    def set_wall(self, row, col, cell_mode=None, is_dragging=False):
        if is_dragging:
            self.grid[row][col]=cell_mode
        else:
            self.grid[row][col]=WALL if self.grid[row][col]==EMPTY else EMPTY
            return self.grid[row][col]

    def set_start_or_goal(self, row, col):
        flat_list = list(chain.from_iterable(self.grid))
        if START in flat_list and GOAL in flat_list:
            return
        if START not in flat_list:
            self.grid[row][col]=START
        else:
            self.grid[row][col]=GOAL

    def in_bounds(self, row, col) -> bool:
        return 0<=row<self.rows and 0<=col<self.cols

    def neighbors(self, row, col) -> list:
        result=[]
        return result

    def clear(self) -> None:
        self.start=self.goal=None
        self.grid=[[EMPTY for i in range(self.cols)] for i in range(self.rows)]

    def reset_search_result(self) -> None:
        for row in self.rows:
            for col in self.cols:
                if self.grid[row][col] in [VISITED,FRONTIER,PATH]:
                    self.grid[row][col]=EMPTY

