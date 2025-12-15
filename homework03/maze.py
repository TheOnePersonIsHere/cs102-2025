from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    pass


def bin_tree_maze(
        rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        up_possible = x - 2 >= 0
        right_possible = y + 2 < cols

        directions = []

        if up_possible:
            directions.append(('up', x - 2, y))
        if right_possible:
            directions.append(('right', x, y + 2))

        if directions:
            direction, next_x, next_y = choice(directions)

            if direction == 'up':
                grid[x - 1][y] = " "
            elif direction == 'right':
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

    pass


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    pass


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    pass


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    pass


def solve_maze(
        grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]],
Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    rows = len(grid)
    cols = len(grid[0])

    exits = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "X":
                exits.append((i, j))

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

        exit1, exit2 = exits[0], exits[1]

        k = 1
        while maze_copy[exit2[0]][exit2[1]] == 0:
            maze_copy = make_step(maze_copy, k)
            k += 1

            if k > rows * cols:
                break

        if maze_copy[exit2[0]][exit2[1]] == 0:
            return grid, None

        path = shortest_path(maze_copy, exit2)

        return maze_copy, path

    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
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
