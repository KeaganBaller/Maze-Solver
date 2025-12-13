import pygame
import pygame_gui
from maze import Maze
WIDTH=900
HEIGHT=600
MAZE_BOX=pygame.Rect(0, 0, 600, 600)
def main():
    #Stuff to not mess with
    pygame.init()
    pygame.display.set_caption('Maze Solver')
    window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(pygame.Color('#181818'))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    rows, cols = 20, 20
    maze = Maze(rows, cols)

    #All the buttons
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
        options_list=["20x20", "25x25", "30x30"],
        starting_option="20x20",
        relative_rect=pygame.Rect((620, 190), (260, 40)),
        manager=manager,
    )

    algorithm_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((620, 250), (260, 25)),
        text="Solving Algorithm",
        manager=manager,
    )
    algorithm_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=["BFS", "DFS", "A*"],
        starting_option="BFS",
        relative_rect=pygame.Rect((620, 280), (260, 40)),
        manager=manager,
    )

    info_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((620, 330), (260, 80)),
        text="Left-click/hold: toggle wall\n"
             "Right-click: set start/goal\n\n",
        manager=manager)

    clock = pygame.time.Clock()
    is_running = True
    dragging=False
    cell_mode=None
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                r,c = maze.pos_to_cell(x,y, MAZE_BOX)
                if maze.in_bounds(r,c):
                    if event.button==1:
                        cell_mode = maze.set_wall(r, c)
                        dragging = True
                    elif event.button==3:
                        maze.set_start_or_goal(r,c)
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    x,y=event.pos
                    r, c = maze.pos_to_cell(x, y, MAZE_BOX)
                    if maze.in_bounds(r, c):
                        maze.set_wall(r, c, cell_mode, is_dragging=True)
            if event.type == pygame.MOUSEBUTTONUP:
                dragging=False

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        pygame.draw.rect(window_surface, (20, 20, 20), MAZE_BOX)
        maze.draw(window_surface, MAZE_BOX)

        manager.draw_ui(window_surface)

        pygame.display.update()



if __name__ == "__main__":
    main()