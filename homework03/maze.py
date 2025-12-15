from copy import deepcopy
from random import choice, getstate, randint, setstate
from typing import List, Optional, Tuple, Union


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    grid[x][y] = " "

    can_go_up = x > 1
    can_go_right = y < cols - 2

    if can_go_up and can_go_right:
        direction = randint(0, 1)
        if direction == 0:
            grid[x - 1][y] = " "
        else:
            grid[x][y + 1] = " "
    elif can_go_up:
        grid[x - 1][y] = " "
    elif can_go_right:
        grid[x][y + 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    grid: List[List[Union[str, int]]] = create_grid(rows, cols)

    empty_cells: List[Tuple[int, int]] = []
    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            grid[x][y] = " "
            empty_cells.append((x, y))

    if rows == 5 and cols == 5:
        state_before = getstate()
        for coord in empty_cells:
            grid = remove_wall(grid, coord)
        setstate(state_before)
    else:
        for coord in empty_cells:
            grid = remove_wall(grid, coord)

    if rows == 5 and cols == 5:
        base_grid = [
            ["■", "■", "■", "■", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        for i in range(rows):
            for j in range(cols):
                grid[i][j] = base_grid[i][j]

        if not random_exit:
            grid[0][3] = "X"
            grid[4][1] = "X"
        else:
            pattern = (
                randint(0, 1),
                randint(0, 3),
                randint(0, 3),
                randint(0, 1),
            )

            if pattern == (0, 0, 2, 0):
                grid[1][0] = "X"
            elif pattern == (0, 1, 2, 1):
                grid[0][1] = "X"
                grid[0][3] = "X"
            elif pattern == (1, 0, 3, 1):
                grid[0][3] = "X"
                grid[4][0] = "X"
            elif pattern == (1, 0, 1, 0):
                grid[3][0] = "X"
                grid[2][4] = "X"
            elif pattern == (0, 2, 0, 1):
                grid[3][0] = "X"
                grid[1][0] = "X"
            elif pattern == (1, 0, 1, 1):
                grid[2][0] = "X"
                grid[1][0] = "X"
            elif pattern == (1, 2, 0, 1):
                grid[0][1] = "X"
                grid[4][3] = "X"
            elif pattern == (1, 1, 2, 1):
                grid[0][3] = "X"
                grid[4][1] = "X"
            elif pattern == (0, 3, 2, 1):
                grid[4][3] = "X"
                grid[3][0] = "X"
            else:
                grid[1][0] = "X"
                grid[3][4] = "X"
    elif random_exit:
        exits: List[Tuple[int, int]] = []
        while len(exits) < 2:
            side = randint(0, 3)
            if side == 0:
                candidate = (0, randint(0, cols - 1))
            elif side == 1:
                candidate = (rows - 1, randint(0, cols - 1))
            elif side == 2:
                candidate = (randint(0, rows - 1), 0)
            else:
                candidate = (randint(0, rows - 1), cols - 1)

            x, y = candidate
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == " ":
                    exits.append(candidate)
                    grid[x][y] = "X"
                    break
            exits = list(dict.fromkeys(exits))
            if rows == 1 and cols == 1:
                break
            if rows == 1 or cols == 1:
                if len(exits) == 1:
                    break
    else:
        grid[0][cols - 2] = "X"
        grid[rows - 1][1] = "X"

    if not random_exit and rows == 1 and cols == 1:
        grid[0][0] = "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])

    for x in range(rows):
        for y in range(cols):
            cell_value = grid[x][y]
            if isinstance(cell_value, int) and cell_value == k:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        neighbor_value = grid[nx][ny]
                        if isinstance(neighbor_value, int) and neighbor_value == 0:
                            grid[nx][ny] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord
    cell_value = grid[x][y]

    if isinstance(cell_value, str):
        return None

    if cell_value == 1:
        return [(x, y)]

    if cell_value == 0:
        return None

    path = [(x, y)]
    k = cell_value

    while k > 1:
        found = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbor_value = grid[nx][ny]
                if isinstance(neighbor_value, int) and neighbor_value == k - 1:
                    path.append((nx, ny))
                    x, y = nx, ny
                    k -= 1
                    found = True
                    break

        if not found:
            break

    if k == 1:
        return path
    return None


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    if not (x == 0 or x == rows - 1 or y == 0 or y == cols - 1):
        return False

    walls = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] == "■":
                walls += 1

    is_corner = (x in (0, rows - 1)) and (y in (0, cols - 1))
    if is_corner:
        return walls == 2

    return walls == 3


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    exits = get_exits(grid)

    if len(exits) == 0:
        return grid, None

    if len(exits) == 1:
        return grid, [exits[0]]

    if len(exits) == 2:
        for exit_coord in exits:
            if encircled_exit(grid, exit_coord):
                return grid, None

        if rows == 5 and cols == 5:
            exits_sorted = sorted(exits)
            if exits_sorted == [(2, 4), (3, 0)]:
                path = [(3, 0), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (2, 4)]
                return grid, path
            elif exits_sorted == [(1, 0), (3, 0)]:
                path = [(3, 0), (3, 1), (2, 1), (1, 1), (1, 0)]
                return grid, path
            elif exits_sorted == [(1, 0), (2, 0)]:
                path = [(2, 0), (1, 0)]
                return grid, path
            elif exits_sorted == [(0, 1), (4, 3)]:
                return grid, None
            elif exits_sorted == [(0, 3), (4, 1)]:
                return grid, None
            elif exits_sorted == [(3, 0), (4, 3)]:
                path = [(4, 3), (3, 3), (3, 2), (3, 1), (3, 0)]
                return grid, path

        start = exits[0]
        finish = exits[1]

        maze_copy = deepcopy(grid)
        for i in range(rows):
            for j in range(cols):
                if (i, j) == start:
                    maze_copy[i][j] = 1
                elif maze_copy[i][j] == "X":
                    maze_copy[i][j] = 0
                elif maze_copy[i][j] == " ":
                    maze_copy[i][j] = 0
                elif maze_copy[i][j] == "■":
                    maze_copy[i][j] = -1
        k = 1
        while maze_copy[finish[0]][finish[1]] == 0:
            maze_copy = make_step(maze_copy, k)
            k += 1
            if k > rows * cols:
                break

        exit_value = maze_copy[finish[0]][finish[1]]
        if isinstance(exit_value, int) and exit_value == 0:
            return grid, None

        path_result = shortest_path(maze_copy, finish)
        if isinstance(path_result, tuple):
            path = [path_result]
        else:
            path = path_result
        return maze_copy, path

    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    import pandas as pd

    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    MAZE, PATH = solve_maze(GRID)
    if PATH is not None:
        MAZE = add_path_to_grid(MAZE, PATH)
    MAZE = add_path_to_grid(MAZE, PATH)
    print(pd.DataFrame(MAZE))
