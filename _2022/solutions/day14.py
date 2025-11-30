"""Day 14: Regolith Reservoir

This module provides the solution for Advent of Code 2022 - Day 14.

It simulates falling sand in a cave system with rock formations, tracking
how sand accumulates as it falls from a source point following gravity rules.

The module contains a Solution class that inherits from SolutionBase for
parsing rock formations and simulating sand physics.
"""

from itertools import pairwise
import re
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Simulate falling sand in cave system with rock formations.

    This solution models sand falling from point (500, 0) following physics rules:
    sand tries to move down, then down-left, then down-right. Part 1 counts sand
    units that settle before falling into the abyss. Part 2 adds an infinite floor
    and counts units until the source is blocked.

    The simulation uses set-based collision detection for efficient position tracking.
    """

    REGEX: ClassVar[re.Pattern[str]] = re.compile(r"(\d+,\d+)")
    SAND_SOURCE: ClassVar[tuple[int, int]] = (500, 0)

    def parse_data(self, data: list[str]) -> set[tuple[int, int]]:
        """Parse rock formation coordinates into occupied positions set.

        Converts line segment notation (e.g., "498,4 -> 498,6 -> 496,6") into
        individual coordinate points by drawing lines between each pair of points.

        Args:
            data: List of strings describing rock paths as coordinate pairs
                separated by " -> "

        Returns
        -------
            set[tuple[int, int]]: Set of (x, y) coordinates occupied by rocks
        """
        rocks = set()

        for line in data:
            matches = re.findall(self.REGEX, line)
            coords = [(int(x), int(y)) for x, y in [match.split(",") for match in matches]]

            for (x1, y1), (x2, y2) in pairwise(coords):
                # Vertical line
                if x1 == x2:
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        rocks.add((x1, y))

                # Horizontal line
                else:
                    for x in range(min(x1, x2), max(x1, x2) + 1):
                        rocks.add((x, y1))

        return rocks

    def simulate(
        self, rocks: set[tuple[int, int]], max_depth: int, *, has_floor: bool = False
    ) -> int:
        """Simulate sand falling and settling until termination condition met.

        Each sand unit falls from source (500, 0) following movement rules:
        1. Try to move down (0, +1)
        2. Try to move down-left (-1, +1)
        3. Try to move down-right (+1, +1)
        4. If all blocked, settle at current position

        Args:
            rocks: Set of rock positions that block sand
            max_depth: Maximum y-coordinate of rocks (for abyss detection)
            has_floor: If True, simulate infinite floor at max_depth + 2

        Returns
        -------
            int: Number of sand units that settled before termination condition
        """
        settled_sand = set()
        fall_offsets = [(0, 1), (-1, 1), (1, 1)]  # down, down-left, down-right
        floor_level = max_depth + 2 if has_floor else None

        while True:
            sand_x, sand_y = self.SAND_SOURCE

            while True:
                if has_floor and sand_y + 1 == floor_level:
                    settled_sand.add((sand_x, sand_y))
                    break

                if not has_floor and sand_y >= max_depth:
                    return len(settled_sand)

                moved = False
                for dx, dy in fall_offsets:
                    next_pos = (sand_x + dx, sand_y + dy)

                    if next_pos not in rocks and next_pos not in settled_sand:
                        sand_x, sand_y = next_pos
                        moved = True
                        break

                if not moved:
                    settled_sand.add((sand_x, sand_y))

                    if has_floor and (sand_x, sand_y) == self.SAND_SOURCE:
                        return len(settled_sand)

                    break

    def part1(self, data: list[str]) -> int:
        """Count sand units that settle before falling into abyss.

        Simulates sand falling until a unit falls past the lowest rock formation,
        indicating it would fall forever into the endless void below.

        Args:
            data: List of strings describing rock formations

        Returns
        -------
            int: Number of sand units that came to rest before sand starts
                flowing into the abyss
        """
        rocks = self.parse_data(data)
        max_depth = max(y for _, y in rocks)

        return self.simulate(rocks, max_depth, has_floor=False)

    def part2(self, data: list[str]) -> int:
        """Count sand units that settle before blocking the source.

        Adds an infinite horizontal floor 2 units below the lowest rock.
        Simulates until sand accumulates to block the source point at (500, 0).

        Args:
            data: List of strings describing rock formations

        Returns
        -------
            int: Number of sand units that came to rest before the source
                becomes blocked (including the unit that blocks it)
        """
        rocks = self.parse_data(data)
        max_depth = max(y for _, y in rocks)

        return self.simulate(rocks, max_depth, has_floor=True)
