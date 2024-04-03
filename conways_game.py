import curses
import numpy as np

def count_neighbours(grid, position_x, position_y):
    n_neighbours = 0

    max_y, max_x = grid.shape
    max_x -= 1
    max_y -= 1

    # Start from left and go anticlockwise
    if position_x - 1 >= 0:
        if grid[position_y, position_x - 1]:
            n_neighbours += 1
    if position_x - 1 >= 0 and position_y + 1 <= max_y:
        if grid[position_y + 1, position_x - 1]:
            n_neighbours += 1
    if position_y + 1 <= max_y:
        if grid[position_y + 1, position_x]:
            n_neighbours += 1
    if position_x + 1 <= max_x and position_y + 1 <= max_y:
        if grid[position_y + 1, position_x + 1]:
            n_neighbours += 1
    if position_x + 1 <= max_x:
        if grid[position_y, position_x + 1]:
            n_neighbours += 1
    if position_y - 1 >= 0 and position_x + 1 <= max_x:
        if grid[position_y - 1, position_x + 1]:
            n_neighbours += 1
    if position_y - 1 >= 0:
        if grid[position_y - 1, position_x]:
            n_neighbours += 1
    if position_y - 1 >= 0 and position_x - 1 >= 0:
        if grid[position_y - 1, position_x - 1]:
            n_neighbours += 1

    return(n_neighbours)

def determine_outcome(grid, position_x, position_y):
    current_state = grid[position_y, position_x]
    n_neighbours = count_neighbours(grid, position_x, position_y)

    if not current_state:
        if n_neighbours == 3:
            outcome = True
        else:
            outcome = False
    elif current_state:
        if n_neighbours < 2:
            outcome = False
        elif n_neighbours in {2,3}:
            outcome = True
        elif n_neighbours > 3:
            outcome = False

    return(outcome)


def conway(stdscr):
    k = 0
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    grid = np.zeros((height, width), dtype = bool) # presumably dtype bool will be faster than using int 0 and 1
    grid[1,4] = True
    grid[2,3] = True
    grid[3,3] = True
    grid[3,4] = True
    grid[4,1] = True
    grid[5,2] = True

    while (k != ord('q')):
        stdscr.clear()
        stdscr.attron(curses.color_pair(1))
        new_grid = np.zeros((height, width), dtype = bool)

        # Draw current grid and work out state in next time period
        for x in range(width):
            for y in range(height):
                if grid[y,x]:
                    stdscr.addch(x, y, " ")
                new_grid[y,x] = determine_outcome(grid, x, y)
                
        # first draw current grid, then update with new grid data and wait
        stdscr.refresh()
        grid = new_grid

        k = stdscr.getch()

def main():
    curses.wrapper(conway)

if __name__ == "__main__":
    main()
