import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        row, col = cell
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                y = row + dy
                x = col + dx
                if 0 <= y < self.rows and 0 <= x < self.cols:
                    neighbours.append(self.curr_generation[y][x])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = []
        for y in range(self.rows):
            new_row = []
            for x in range(self.cols):
                neighbours = self.get_neighbours((y, x))
                alive = self.curr_generation[y][x] == 1
                if alive and (2 <= sum(neighbours) <= 3):
                    new_row.append(1)
                elif not alive and sum(neighbours) == 3:
                    new_row.append(1)
                else:
                    new_row.append(0)
            new_grid.append(new_row)
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        rows = len(lines)
        cols = len(lines[0]) if rows > 0 else 0
        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = [[int(ch) for ch in line] for line in lines]
        game.prev_generation = copy.deepcopy(game.curr_generation)
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write("".join(str(cell) for cell in row) + "\n")
