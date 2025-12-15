from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    grid[x][y] = " "

    if x % 2 == 0:
        if x - 1 >= 0 and (x - 1) % 2 == 1:
            grid[x - 1][y] = " "
        if x + 1 < len(grid) and (x + 1) % 2 == 1:
            grid[x + 1][y] = " "
    elif y % 2 == 0:
        if y - 1 >= 0 and (y - 1) % 2 == 1:
            grid[x][y - 1] = " "
        if y + 1 < len(grid[0]) and (y + 1) % 2 == 1:
            grid[x][y + 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    grid = [["■" for _ in range(cols)] for _ in range(rows)]
    empty_cells = []

    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        up_possible = x - 2 >= 0
        right_possible = y + 2 < cols

        directions = []
        if up_possible:
            directions.append(("up", x - 2, y))
        if right_possible:
            directions.append(("right", x, y + 2))

        if directions:
            direction, next_x, next_y = choice(directions)
            if direction == "up":
                grid[x - 1][y] = " "
            elif direction == "right":
                grid[x][y + 1] = " "

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
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
        return path[::-1]
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

    if grid[x][y] != "X":
        return False

    count_walls = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] == "■":
                count_walls += 1
        else:
            count_walls += 1

    if (x == 0 and y == 0) or (x == 0 and y == cols - 1) or \
            (x == rows - 1 and y == 0) or (x == rows - 1 and y == cols - 1):
        return count_walls >= 2

    if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
        return count_walls >= 3

    return count_walls >= 2


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

    if len(exits) == 1:
        return grid, [exits[0]]

    if len(exits) == 2:
        for exit_coord in exits:
            if encircled_exit(grid, exit_coord):
                return grid, None

        maze_copy = deepcopy(grid)
        for i in range(rows):
            for j in range(cols):
                if maze_copy[i][j] == "X":
                    maze_copy[i][j] = 1
                elif maze_copy[i][j] == " ":
                    maze_copy[i][j] = 0
                elif maze_copy[i][j] == "■":
                    maze_copy[i][j] = 0

        exit1, exit2 = exits[0], exits[1]
        k = 1
        while maze_copy[exit2[0]][exit2[1]] == 0:
            maze_copy = make_step(maze_copy, k)
            k += 1
            if k > rows * cols:
                break

        exit2_value = maze_copy[exit2[0]][exit2[1]]
        if isinstance(exit2_value, int) and exit2_value == 0:
            return grid, None

        path = shortest_path(maze_copy, exit2)
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
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))