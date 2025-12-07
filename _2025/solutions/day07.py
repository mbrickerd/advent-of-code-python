"""Day 7: Laser Lab

This module provides the solution for Advent of Code 2025 - Day 7.

It simulates beams traveling downward through a grid containing a start
position ('S'), empty cells ('.'), and splitters ('^') that split beams
diagonally.

The module contains a Solution class that inherits from SolutionBase to
count how many splitters activate (Part 1) and how many distinct beam
paths reach the bottom row (Part 2).
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Simulate vertical beam propagation and splitting in a grid.

    This solution models beams starting from a single source cell 'S' and
    moving one row downward at a time. When a beam enters a splitter '^',
    it splits into two beams that continue diagonally down-left and
    down-right.

    Part 1 tracks a single beam front and counts how many splitters are
    activated at least once. Part 2 uses dynamic programming to count how
    many distinct paths reach the bottom of the grid after all splitting.
    """

    def find_start(self, grid: list[list[str]]) -> tuple[int, int]:
        """Locate the starting cell 'S' in the grid.

        Args:
            grid: 2D character grid of the laser lab

        Returns
        -------
            tuple[int, int]: (x, y) coordinates of the start cell

        Raises
        ------
            ValueError: If no 'S' cell is found in the grid
        """
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == "S":
                    return (x, y)

        err_msg = "No 'S' start cell found in grid!"
        raise ValueError(err_msg)

    def part1(self, data: list[str]) -> int:
        """Count how many splitters are activated along a single beam front.

        Simulates a single front of beams starting from 'S' and moving
        row-by-row downward. Each time a beam enters a '^' splitter, that
        splitter is counted and the beam splits into two beams diagonally
        down-left and down-right for the next row.

        Args:
            data: List of strings representing the lab grid

        Returns
        -------
            int: Number of times splitters are activated across all rows
        """
        grid = [list(row) for row in data]
        start_col, start_row = self.find_start(grid)

        beams: set[int] = {start_col}
        count = 0
        last_row_idx = len(grid) - 1

        current_row = start_row
        while current_row < last_row_idx:
            current_row += 1
            next_beams: set[int] = set()

            for col in beams:
                cell = grid[current_row][col]
                if cell == "^":
                    next_beams.add(col - 1)
                    next_beams.add(col + 1)
                    count += 1
                else:
                    next_beams.add(col)

            beams = next_beams

        return count

    def part2(self, data: list[str]) -> int:
        """Count distinct beam paths that reach the bottom row.

        Uses dynamic programming where dp[r][c] stores how many distinct
        paths can reach cell (r, c). Paths start from the cell below 'S'
        and propagate row-by-row, splitting at '^' cells into diagonal
        positions.

        Args:
            data: List of strings representing the lab grid

        Returns
        -------
            int: Total number of distinct paths that reach the bottom row
        """
        grid = [list(row) for row in data]
        rows, cols = len(grid), len(grid[0])
        start_col, start_row = self.find_start(grid)

        dp = [[0] * cols for _ in range(rows)]

        if start_row + 1 < rows:
            dp[start_row + 1][start_col] = 1

        for r in range(start_row + 1, rows - 1):
            for c in range(cols):
                if dp[r][c] == 0:
                    continue

                cell = grid[r][c]
                if cell == ".":
                    dp[r + 1][c] += dp[r][c]

                elif cell == "^":
                    if c - 1 >= 0:
                        dp[r + 1][c - 1] += dp[r][c]
                    if c + 1 < cols:
                        dp[r + 1][c + 1] += dp[r][c]

                else:
                    dp[r + 1][c] += dp[r][c]

        return sum(dp[rows - 1])
