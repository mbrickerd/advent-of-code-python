"""Day 12: Hill Climbing Algorithm

This module provides the solution for Advent of Code 2022 - Day 12.

It implements pathfinding on a heightmap grid to find the shortest route
from low elevation to high elevation with movement constraints.

The module contains a Coordinate class for position tracking and a Solution
class that inherits from SolutionBase for solving the hill climbing puzzle.
"""

from collections import deque
from typing import ClassVar

from aoc.models.base import SolutionBase


class Coordinate:
    """Represent a 2D grid position with x (column) and y (row) coordinates.

    Uses standard (x, y) convention where x is horizontal and y is vertical.
    Provides equality comparison and hashing for use in sets and dictionaries
    during pathfinding operations.
    """

    def __init__(self, x: int, y: int):
        """Initialize coordinate with column and row position.

        Args:
            x: Column index (horizontal position)
            y: Row index (vertical position)
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Return string representation of coordinate."""
        return f"Coordinate(x={self.x}, y={self.y})"

    def __eq__(self, other: object) -> bool:
        """Check equality based on x and y values."""
        if not isinstance(other, Coordinate):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Generate hash for use in sets and dictionaries."""
        return hash((self.x, self.y))


class Solution(SolutionBase):
    """Find shortest path on heightmap with elevation climbing constraints.

    This solution implements breadth-first search (BFS) to find the shortest
    path on a grid where each cell has an elevation (a-z). Part 1 finds the
    shortest path from a single start point (S) to the end point (E). Part 2
    finds the shortest path from any low elevation point ('a' or 'S') to the end.

    Movement is constrained: you can only move to adjacent cells (up, down, left,
    right) if the destination elevation is at most 1 higher than current elevation.
    """

    DIRECTIONS: ClassVar[list[tuple[int, int]]] = [
        (1, 0),  # right
        (0, -1),  # up
        (-1, 0),  # left
        (0, 1),  # down
    ]

    def find_start_end(self, grid: list[list[str]]) -> tuple[Coordinate, Coordinate]:
        """Locate start (S) and end (E) positions in the heightmap.

        Args:
            grid: 2D grid of elevation characters

        Returns
        -------
            tuple[Coordinate, Coordinate]: Start and end coordinates

        Raises
        ------
            ValueError: If start or end position cannot be found
        """
        start: Coordinate | None = None
        end: Coordinate | None = None

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == "S":
                    start = Coordinate(x, y)

                elif cell == "E":
                    end = Coordinate(x, y)

                if start and end:
                    return start, end

        if not start or not end:
            err_msg = "Could not find start or end position"
            raise ValueError(err_msg)

        return start, end

    def get_height(self, grid: list[list[str]], coord: Coordinate) -> int:
        """Get numeric elevation value for a coordinate.

        Converts characters to elevation values: 'a'=97, 'z'=122.
        Special cases: 'S' is treated as 'a', 'E' is treated as 'z'.

        Args:
            grid: 2D grid of elevation characters
            coord: Position to check

        Returns
        -------
            int: ASCII value representing elevation (97-122)
        """
        value = grid[coord.y][coord.x]
        if value == "S":
            return ord("a")

        if value == "E":
            return ord("z")

        return ord(value)

    def bfs(self, grid: list[list[str]], start: Coordinate, end: Coordinate) -> int:
        """Run breadth-first search from start to end coordinate.

        Uses BFS to find the shortest path while respecting elevation constraints:
        can only move to cells that are at most 1 elevation higher.

        Args:
            grid: 2D grid of elevation characters
            start: Starting coordinate
            end: Target coordinate

        Returns
        -------
            int: Number of steps in shortest path, or -1 if no path exists
        """
        n_rows, n_cols = len(grid), len(grid[0])

        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            position, steps = queue.popleft()

            if position == end:
                return steps

            for dx, dy in self.DIRECTIONS:
                new_x = position.x + dx
                new_y = position.y + dy
                new_position = Coordinate(new_x, new_y)

                if not (0 <= new_x < n_cols and 0 <= new_y < n_rows):
                    continue

                if new_position in visited:
                    continue

                current_height = self.get_height(grid, position)
                new_height = self.get_height(grid, new_position)
                if new_height > current_height + 1:
                    continue

                visited.add(new_position)
                queue.append((new_position, steps + 1))

        return -1

    def part1(self, data: list[str]) -> int:
        """Find shortest path from marked start (S) to end (E).

        Searches for the minimum number of steps needed to reach the best
        signal location (E) from the starting position (S) while respecting
        elevation climbing constraints.

        Args:
            data: List of strings representing the heightmap grid

        Returns
        -------
            int: Minimum number of steps from S to E
        """
        grid = [list(row) for row in data]
        start, end = self.find_start_end(grid)

        return self.bfs(grid, start, end)

    def part2(self, data: list[str]) -> int:
        """Find shortest path from any lowest elevation point to end (E).

        Identifies the best hiking trail by finding the shortest path from
        any cell at elevation 'a' (including 'S') to the end point (E).
        Tests all possible low-elevation starting points.

        Args:
            data: List of strings representing the heightmap grid

        Returns
        -------
            int: Minimum number of steps from any 'a' elevation cell to E,
                or -1 if no valid path exists
        """
        grid = [list(row) for row in data]
        _, end = self.find_start_end(grid)

        starts = [
            Coordinate(x, y)
            for y, row in enumerate(grid)
            for x, cell in enumerate(row)
            if cell in ["a", "S"]
        ]

        valid_paths = [steps for start in starts if (steps := self.bfs(grid, start, end)) != -1]

        return min(valid_paths) if valid_paths else -1
