GOAL = (9, 9)
MAZE_DEMINSION = 10


def set_maze(MAZE_DEMINSION):
    # use this function to create a square grid and set the open squares
    pass


def open(x, y):
    # Return if the location is movable
    pass


def find_path(start_x, start_y):
    current_loc = (start_x, start_y)
    solution_path = current_loc
    if (0 > start_x > MAZE_DEMINSION) or (0 > start_y > MAZE_DEMINSION):
        return false, null
    if start_x == GOAL[0] and start_y == GOAL[1]:
        return true, solution_path
    if not open(start_x, start_y):
        return false, null
    if find_path(start_x+1, start_y)[0] == true:
        return true, solution_path + find_path(start_x+1, start_y)[1]
    if find_path(start_x-1, start_y)[0] == true:
        return true, solution_path + find_path(start_x+1, start_y)[1]
    if find_path(start_x, start_y+1)[0] == true:
        return true, solution_path + find_path(start_x+1, start_y)[1]
    if find_path(start_x, start_y-1)[0] == true:
        return true, solution_path + find_path(start_x+1, start_y)[1]
    return false, null
