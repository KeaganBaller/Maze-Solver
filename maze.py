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
    def __init__(self, rows: int, cols: int) -> None:
        """
        Method to set default values of maze object.
        :param rows: Takes in desired rows
        :param cols: Takes in desired columns
        """
        self.rows=rows
        self.cols=cols
        self.grid=[[EMPTY for i in range(cols)] for i in range(rows)]
        self.start=None
        self.goal=None

    def draw(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """
        Draws the maze based on grid setup, inside the given rectangle area
        """
        _,_,width,height=rect
        cell_width=width/self.cols
        cell_height = height/self.rows
        for row in range(self.rows):
            for col in range(self.cols):
                cell_color=COLORS[self.grid[row][col]]
                cell=pygame.Rect(cell_width*col, cell_height*row, cell_width, cell_height)
                pygame.draw.rect(surface, cell_color, cell)
                pygame.draw.rect(surface, "#4a4a4a", cell, 1) #Outlines

    def pos_to_cell(self, x: int, y: int, rect: pygame.Rect) -> tuple[int,int]:
        """
        Takes in the mouse coordinates and converts to grid position
        :return: Tuple of row and column
        """
        _,_,width,height=rect
        cell_width = width / self.cols
        cell_height = height / self.rows
        col=int(x//cell_width)
        row=int(y//cell_height)
        return row, col

    def set_wall(self, row: int, col: int, cell_mode:int=None, is_dragging:bool=False) -> int:
        """
        Sets the wall of a point determined by row and col parameter
        :param row: Used for setting wall
        :param col: Used for setting wall
        :param cell_mode: Used when is_dragging passes in the bool True, maintains same cell type when dragging mouse
        :param is_dragging: Set to false by default, only changes if mouse is dragging
        :return: integer value indicating cell type, used for cell_mode parameter in next reference
        """
        if self.grid[row][col] == START: self.start = None
        elif self.grid[row][col] == GOAL: self.goal = None

        if is_dragging:
            self.grid[row][col]=cell_mode
        else:
            self.grid[row][col]=WALL if self.grid[row][col]==EMPTY else EMPTY
            return self.grid[row][col]


    def set_start_or_goal(self, row: int, col: int) -> None:
        """
        Sets the starting point and goal point. First right-click=Start, Second right-click=Goal
        :param row: Used for setting position in grid
        :param col: Used for setting position in grid
        """
        flat_list = list(chain.from_iterable(self.grid))
        if START in flat_list and GOAL in flat_list:
            return
        if START not in flat_list:
            self.grid[row][col]=START
            self.start=(row, col)
        else:
            self.grid[row][col]=GOAL
            self.goal = (row, col)

    def in_bounds(self, row: int, col: int) -> bool:
        """
        Checks if index is in bounds of grid
        :return: Boolean indicating if it's in bounds or not
        """
        return 0<=row<self.rows and 0<=col<self.cols

    def neighbors(self, row: int, col: int, m:int=1) -> list:
        """
        Determines the neighboring cells in 4 directions of a given position, used for maze solving algorithms
        :param row: Row position
        :param col: Column position
        :param m: Used as a stepper multiplier for generating maze wall thickness
        :return: List of neighboring cell positions
        """
        result=[]
        for dr,dc in [(1*m,0), (-1*m,0), (0,1*m), (0,-1*m)]:
            nr,nc=row+dr, col+dc
            if self.in_bounds(nr, nc):
                result.append([nr, nc])
        return result

    def clear(self) -> None:
        """
        Clears grid entirely
        """
        self.start=self.goal=None
        self.grid=[[EMPTY for i in range(self.cols)] for i in range(self.rows)]

    def fill(self) -> None:
        """
        Used for maze generator function, starts the grid full of walls instead of empty cells
        """
        self.start=self.goal=None
        self.grid=[[WALL for i in range(self.cols)] for i in range(self.rows)]

    def reset_search_result(self) -> None:
        """
        Only resets the cell types used when running solver, walls and start/goal cells remain
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] in [VISITED,FRONTIER,PATH]:
                    self.grid[row][col]=EMPTY

