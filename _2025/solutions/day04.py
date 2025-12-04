"""Day 4: Printing Department

This module provides the solution for Advent of Code 2025 - Day 4.

It processes a grid of paper rolls to determine which are accessible based
on the number of adjacent rolls. A roll is accessible if it has fewer than
four neighbors.

The module contains a Solution class to calculate the number of initially
accessible rolls (Part 1) and the total number of rolls that can be removed
iteratively (Part 2).
"""

from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Determine accessible and removable paper rolls from a grid layout.

    This solution scans a grid representing paper roll locations ('@'). A roll
    is deemed accessible if it has fewer than four adjacent rolls (including
    diagonals).

    Part 1 counts the number of rolls that are initially accessible.
    Part 2 simulates the process of removing all accessible rolls, re-evaluating
    accessibility, and repeating until no more rolls can be removed, counting
    the total number of removed rolls.
    """

    DIRECTIONS: ClassVar[list[tuple[int, int]]] = [
        (-1, -1),  # up-left
        (-1, 0),  # up
        (-1, 1),  # up-right
        (0, -1),  # left
        (0, 1),  # right
        (1, -1),  # down-left
        (1, 0),  # down
        (1, 1),  # down-right
    ]

    def find_open_spaces(self, grid: list[list[str]], rows: int, cols: int) -> list[tuple[int, int]]:
        """Find all accessible paper rolls in the current grid.

        An accessible roll is one marked '@' with fewer than four adjacent '@' rolls.

        Args:
            grid: The current grid of paper rolls and empty spaces.
            rows: The number of rows in the grid.
            cols: The number of columns in the grid.

        Returns
        -------
            list[tuple[int, int]]: A list of (row, col) coordinates for accessible rolls.
        """
        positions = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "@":
                    continue

                count = 0
                for dr, dc in self.DIRECTIONS:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                        count += 1

                if count < 4:
                    positions.append((r, c))

        return positions

    def part1(self, data: list[str]) -> int:
        """Count the number of paper rolls that are initially accessible.

        This method parses the input grid and counts how many paper rolls ('@')
        have fewer than four adjacent rolls.

        Args:
            data: A list of strings representing the grid layout.

        Returns
        -------
            int: The total number of initially accessible paper rolls.
        """
        grid = [list(row) for row in data]
        rows, cols = len(grid), len(grid[0])
        return len(self.find_open_spaces(grid, rows, cols))

    def part2(self, data: list[str]) -> int:
        """Count the total number of rolls that can be removed.

        This method simulates the iterative removal of accessible paper rolls.
        In each step, it finds all accessible rolls, adds them to a total count,
        removes them from the grid (by changing '@' to '.'), and then repeats
        the process until no more rolls are accessible.

        Args:
            data: A list of strings representing the initial grid layout.

        Returns
        -------
            int: The total number of paper rolls that can be removed.
        """
        grid = [list(row) for row in data]
        rows, cols = len(grid), len(grid[0])
        positions = self.find_open_spaces(grid, rows, cols)

        count = 0
        while (c := len(positions)) > 0:
            count += c
            for y, x in positions:
                grid[y][x] = "."

            positions = self.find_open_spaces(grid, rows, cols)

        return count
