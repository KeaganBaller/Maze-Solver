import pygame
import pygame_gui
import sys
from maze import Maze
from algorithms import bfs_algorithm, dfs_algorithm, maze_generator

#Declared window attributes as constants
WIDTH=900
HEIGHT=600
MAZE_BOX=pygame.Rect(0, 0, 600, 600)

def main() -> None:
    """Run the Maze Solver UI loop"""

    #Setup code that shouldn't be touched, source: pygame_gui documentation
    try:
        pygame.init()
        pygame.display.set_caption('Maze Solver')
        window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(pygame.Color('#181818'))
        manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    except Exception as e:
        print(f"Error when initializing pygame and pygame_gui: {e}")
        sys.exit(0)

    solving_algorithms={"BFS":bfs_algorithm, "DFS":dfs_algorithm} #Used for referencing functions

    #Default settings and maze instance
    solver_choice="BFS"
    rows = cols = 15
    maze = Maze(rows, cols)

    #All the buttons and labels for pygame_gui
    run_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((620, 50), (260, 40)),
            text="Run Solver",
            manager=manager,
        )

    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((620, 100), (260, 40)),
        text="Reset Maze",
        manager=manager,
    )

    size_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((620, 160), (260, 25)),
        text="Grid Size",
        manager=manager,
    )

    size_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=["10x10", "15x15", "20x20", "25x25", "30x30", "100x100"],
        starting_option="15x15",
        relative_rect=pygame.Rect((620, 190), (260, 40)),
        manager=manager,
    )

    algorithm_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((620, 250), (260, 25)),
        text="Solving Algorithm",
        manager=manager,
    )
    algorithm_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=["BFS", "DFS"],
        starting_option="BFS",
        relative_rect=pygame.Rect((620, 280), (260, 40)),
        manager=manager,
    )
    instruction_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((620, 330), (260, 80)),
        text="Left-click/hold: toggle wall\n"
             "Right-click: set start/goal\n\n",
        manager=manager)

    clear_path_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((620, 420), (260, 40)),
        text="Clear solution path",
        manager=manager,
    )
    generate_maze_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((620, 470), (260, 40)),
        text="Generate maze",
        manager=manager,
    )

    clock = pygame.time.Clock()

    #Status variables
    is_running = True
    solver=None
    solving=False
    dragging=False
    cell_mode=None

    #Event loop for pygame
    while is_running:
        #If you want faster results, you could increase the value inside clock.tick
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            #Mouse press
            if event.type == pygame.MOUSEBUTTONDOWN: #Che
                x,y=event.pos
                r,c = maze.pos_to_cell(x,y, MAZE_BOX)
                if maze.in_bounds(r,c):
                    if event.button==1:
                        cell_mode = maze.set_wall(r, c)
                        dragging = True
                    elif event.button==3:
                        maze.set_start_or_goal(r,c)

            #Mouse motion
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    x,y=event.pos
                    r, c = maze.pos_to_cell(x, y, MAZE_BOX)
                    if maze.in_bounds(r, c):
                        maze.set_wall(r, c, cell_mode, is_dragging=True)

            #Mouse click released
            if event.type == pygame.MOUSEBUTTONUP:
                dragging=False

            manager.process_events(event)

            #Button click
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == run_button: #Runs solving algorithm of choice
                    if maze.start and maze.goal:
                        solver=solving_algorithms[solver_choice](maze)
                        solving=True
                elif event.ui_element == reset_button: #Clears entire maze
                    maze.clear()
                elif event.ui_element == clear_path_button: #Clears only the final solved path
                    if not solving:
                        maze.reset_search_result()
                elif event.ui_element == generate_maze_button: #Generates a random maze
                    if not solving:
                        try:
                            maze_generator(maze)
                        except Exception as e:
                            print(f"Error with maze generation: {e}")

            #Dropdown selection changed
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == size_dropdown: #Rebuilds maze with new size
                    selection=event.text.split("x")
                    rows,cols=[int(i) for i in selection]
                    maze = Maze(rows, cols)
                elif event.ui_element == algorithm_dropdown: #Allows user to switch solving algorithm
                    solver_choice=event.text

        if solving and solver is not None:
            try:
                next(solver) #Runs one solver step for every frame
            except StopIteration: #Stops when solving algorithm finishes
                solving = False
                solver = None

        #Part of setup code grabbed from pygame_gui documentation
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        pygame.draw.rect(window_surface, (20, 20, 20), MAZE_BOX)
        maze.draw(window_surface, MAZE_BOX)
        manager.draw_ui(window_surface)
        pygame.display.update()



if __name__ == "__main__":
    main()