from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid, coord):
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    grid[x][y] = " "

    if x % 2 == 0 and x - 1 >= 0:
        grid[x - 1][y] = " "
    elif y % 2 == 0 and y - 1 >= 0:
        grid[x][y - 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    grid: List[List[Union[str, int]]] = [["■" for _ in range(cols)] for _ in range(rows)]

    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            grid[x][y] = " "

            up_possible = x > 1
            right_possible = y < cols - 2

            if up_possible:
                grid[x - 1][y] = " "
            elif right_possible:
                grid[x][y + 1] = " "

    if random_exit:
        x1 = randint(0, rows - 1)
        y1 = choice([0, cols - 1]) if x1 not in (0, rows - 1) else randint(0, cols - 1)

        x2 = randint(0, rows - 1)
        y2 = choice([0, cols - 1]) if x2 not in (0, rows - 1) else randint(0, cols - 1)
    else:
        x1, y1 = 0, cols - 2
        x2, y2 = rows - 1, 1

    grid[x1][y1] = "X"
    grid[x2][y2] = "X"

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

    if grid[x][y] != "X":
        return False

    walls = 0

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy

        if nx < 0 or nx >= rows or ny < 0 or ny >= cols:
            walls += 1
        elif grid[nx][ny] == "■":
            walls += 1

    if (x, y) in [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]:
        return walls == 2

    if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
        return walls == 3

    return False


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
                    maze_copy[i][j] = -1

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
