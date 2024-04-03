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
    pad_height = 300
    pad_width = 300
    pad = curses.newpad(pad_height, pad_width)
    pad.clear()
    pad.keypad(True)
    k = 0
    window_loc_y = int(pad_height/2)
    window_loc_x = int(pad_width/2) # where the window starts within the pad
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    height = curses.LINES
    width = curses.COLS
 
    grid = np.zeros((pad_height - 1, pad_width - 1), dtype = bool) # presumably dtype bool will be faster than using int 0 and 1

    # Generate some random alive cells to fill in the frid
    rng = np.random.default_rng()
    rand_rownums = rng.integers(pad_height - 2, size = int(pad_width*pad_height / 2))
    rand_colnums = rng.integers(pad_width - 2, size = int(pad_width*pad_height / 2))
    rand_points = zip(rand_rownums, rand_colnums) # there's duplicate points here but I'm not that bothered at this stage

    for point in rand_points:
        grid[point[0], point[1]] = True

    while (k != ord('q')):
        pad.clear()
        pad.attron(curses.color_pair(1))
        new_grid = np.zeros((pad_height - 1, pad_width - 1), dtype = bool)

        # Move screen when arrow keys pressed
        if k == curses.KEY_UP:
            window_loc_y -= 1
        elif k == curses.KEY_RIGHT:
            window_loc_x += 1
        elif k == curses.KEY_DOWN:
            window_loc_y += 1
        elif k == curses.KEY_LEFT:
            window_loc_x -= 1

        # Draw current grid and work out state in next time period
        for x in range(pad_width - 1):
            for y in range(pad_height - 1):
                if grid[y,x]:
                    pad.addch(y, x, " ")
                new_grid[y,x] = determine_outcome(grid, x, y)
                
        # first display current grid, then update with new grid data and wait
        pad.refresh(window_loc_y, window_loc_x, 
                    0,0 ,
                    height - 1, width - 1)
        grid = new_grid

        k = pad.getch()

def main():
    curses.wrapper(conway)

if __name__ == "__main__":
    main()
