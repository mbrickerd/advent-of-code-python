"""Day 10: Pipe Maze

This module provides the solution for Advent of Code 2023 - Day 10.

It handles navigation through a two-dimensional maze of metal pipes to find
a continuous loop containing an animal. The puzzle involves tracing the loop
to find the farthest point from the start and counting tiles enclosed within.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse the pipe grid, traverse the loop, calculate distances, and
determine the area enclosed by the loop using the shoelace formula and Pick's theorem.
"""

import re
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Trace pipe loops and calculate enclosed areas in a grid maze.

    This solution handles two types of calculations:
    Part 1 finds the farthest point in the loop from the starting position by
    tracing the continuous pipe path and measuring distances.
    Part 2 calculates the number of tiles enclosed within the loop using
    either a scanline approach with regex pattern matching or geometric
    algorithms (shoelace formula and Pick's theorem).

    The solution determines the actual pipe type at 'S' by analyzing adjacent
    connections, then traces the complete loop through the maze.
    """

    adj_dirs: ClassVar[list[tuple[int, int]]] = [
        (-1, 0),  # top
        (0, 1),  # right
        (1, 0),  # bottom
        (0, -1),  # left
    ]

    symbol_connects: ClassVar[dict[str, tuple[int, int, int, int]]] = {
        "|": (1, 0, 1, 0),  # top, right, bottom, left
        "-": (0, 1, 0, 1),
        "L": (1, 1, 0, 0),
        "J": (1, 0, 0, 1),
        "7": (0, 0, 1, 1),
        "F": (0, 1, 1, 0),
    }

    adj_connect_types: ClassVar[dict[tuple[int, int], str]] = {
        (-1, 0): "F|7",  # top can connect to F, |, or 7
        (0, 1): "7-J",  # right can connect to 7, -, or J
        (1, 0): "L|J",  # bottom can connect to L, |, or J
        (0, -1): "F-L",  # left can connect to F, -, or L
    }

    def parse_map(
        self, data: list[str]
    ) -> tuple[list[list[str]], tuple[int, int], set[tuple[int, int]]]:
        """Parse the pipe maze and trace the main loop.

        Identifies the starting position, determines the actual pipe type at 'S'
        by analyzing adjacent connections, and traces the complete loop using BFS.

        Args:
            data (list[str]): List of strings representing the pipe grid

        Returns
        -------
            Tuple containing:
            - grid: Two-dimensional list with 'S' replaced by actual pipe type
            - start: Starting position (row, column)
            - visited: Set of all positions in the main loop
        """
        start: tuple[int, int] | None = None
        grid: list[list[str]] = []

        for h, line in enumerate(data):
            grid.append(list(line))
            if "S" in line:
                start = (h, line.index("S"))

        if start is None:
            error_msg = "Starting position 'S' not found in grid"
            raise ValueError(error_msg)

        # Determine what pipe type 'S' actually represents
        adjs = [0, 0, 0, 0]  # top, right, bottom, left
        for i, adj in enumerate(self.adj_dirs):
            pos = tuple(a + b for a, b in zip(start, adj, strict=False))
            if (
                0 <= pos[0] < len(grid)
                and 0 <= pos[1] < len(grid[0])
                and grid[pos[0]][pos[1]] in self.adj_connect_types[adj]
            ):
                adjs[i] = 1

        # Replace 'S' with the actual pipe symbol
        adjs_tuple: tuple[int, int, int, int] = (adjs[0], adjs[1], adjs[2], adjs[3])
        grid[start[0]][start[1]] = {v: k for k, v in self.symbol_connects.items()}[adjs_tuple]

        # BFS to find all nodes in the loop
        queue: list[tuple[int, int]] = [start]
        visited: set[tuple[int, int]] = set()

        while queue:
            pos = queue.pop(0)
            if pos in visited:
                continue
            visited.add(pos)

            if grid[pos[0]][pos[1]] in " .":
                continue

            sym = grid[pos[0]][pos[1]]
            _dirs = [self.adj_dirs[i] for i, v in enumerate(self.symbol_connects[sym]) if v == 1]

            for dy, dx in _dirs:
                next_pos = (pos[0] + dy, pos[1] + dx)
                if 0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0]):
                    queue.append(next_pos)

        return grid, start, visited

    def part1(self, data: list[str]) -> int:
        """Calculate the farthest distance from the starting position in the loop.

        Traces the loop and returns the distance to the farthest point, which
        is half the loop length since the loop is continuous.

        Args:
            data (list[str]): List of strings representing the pipe grid

        Returns
        -------
            Maximum distance from the starting position to any point in the loop
        """
        _map, _start, _loop_nodes = self.parse_map(data)
        return len(_loop_nodes) // 2

    def part2(self, data: list[str]) -> int:
        """Calculate the number of tiles enclosed within the loop.

        Uses a scanline approach with regex pattern matching to identify tiles
        inside the loop. Replaces non-loop tiles with dots, then uses crossing
        number algorithm to count interior points.

        Args:
            data (list[str]): List of strings representing the pipe grid

        Returns
        -------
            Number of tiles enclosed by the loop
        """
        _map, _start, _loop_nodes = self.parse_map(data)
        row_counts = []

        for h, items in enumerate(_map):
            # Replace non-loop tiles with dots
            line_list = [v if (h, w) in _loop_nodes else "." for w, v in enumerate(items)]
            line: str = "".join(line_list)

            # Simplify corner patterns to vertical pipes for crossing detection
            # L-7 is a U-turn that crosses once
            line = re.sub(r"L-*7", "|", line)
            # L-J is two parallel lines (crosses twice)
            line = re.sub(r"L-*J", "||", line)
            # F-7 is two parallel lines (crosses twice)
            line = re.sub(r"F-*7", "||", line)
            # F-J is a U-turn that crosses once
            line = re.sub(r"F-*J", "|", line)

            cross = 0
            inside = 0

            for c in line:
                if c == "." and cross % 2:
                    inside += 1
                elif c in "F7LJ|":
                    cross += 1
            row_counts.append(inside)

        return sum(row_counts)
