"""Day 9: Rope Bridge

This module provides the solution for Advent of Code 2022 - Day 9.

It handles simulating rope physics as knots move across a bridge, tracking
positions visited by the tail knot(s) as the head follows movement instructions.

The module contains a Solution class that inherits from SolutionBase and implements
methods to model rope movement with different rope lengths and knot configurations.
"""

from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Simulate rope bridge physics with moving head and following tail knots.

    This solution models rope movement where the head moves according to
    directional instructions and tail knots follow to remain adjacent. Part 1
    simulates a rope with 2 knots (head and tail), while Part 2 extends to
    a rope with 10 knots where each knot follows the one before it.

    The solution uses coordinate tracking and distance-based movement rules
    to determine when and how tail knots must move to stay connected.
    """

    DIRECTIONS: ClassVar[dict[str, tuple[int, int]]] = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }

    def part1(self, data: list[str]) -> int:
        """Count positions visited by tail in a 2-knot rope simulation.

        Simulates a rope with head and tail knots. The head moves according to
        instructions, and the tail follows when it becomes more than 1 step away.
        Tail moves diagonally when necessary to stay adjacent to the head.

        Args:
            data: List of movement instructions in format "DIRECTION STEPS"
                (e.g., "R 4" means move right 4 steps)

        Returns
        -------
            int: Number of unique positions visited by the tail knot at least once
        """
        head = [0, 0]
        tail = [0, 0]
        visited = {(0, 0)}

        for line in data:
            direction, steps = line.split()
            dx, dy = self.DIRECTIONS[direction]

            for _ in range(int(steps)):
                # Move head
                head[0] += dx
                head[1] += dy

                # Check if tail needs to move
                diff_x = head[0] - tail[0]
                diff_y = head[1] - tail[1]

                # If head is more than 1 step away in any direction
                if abs(diff_x) > 1 or abs(diff_y) > 1:
                    # Move tail one step towards head using sign function
                    tail[0] += 1 if diff_x > 0 else (-1 if diff_x < 0 else 0)
                    tail[1] += 1 if diff_y > 0 else (-1 if diff_y < 0 else 0)

                visited.add((tail[0], tail[1]))

        return len(visited)

    def part2(self, data: list[str]) -> int:
        """Count positions visited by tail in a 10-knot rope simulation.

        Simulates a rope with 10 knots numbered 0-9, where knot 0 is the head.
        Each knot follows the one before it using the same movement rules as
        Part 1. Tracks positions visited by the final tail knot (knot 9).

        Args:
            data: List of movement instructions in format "DIRECTION STEPS"
                (e.g., "R 4" means move right 4 steps)

        Returns
        -------
            int: Number of unique positions visited by the final tail knot (knot 9)
                at least once
        """
        knots = [[0, 0] for _ in range(10)]
        visited = {(0, 0)}

        for line in data:
            direction, steps = line.split()
            dx, dy = self.DIRECTIONS[direction]

            for _ in range(int(steps)):
                # Move head (knot 0)
                knots[0][0] += dx
                knots[0][1] += dy

                # Each subsequent knot follows the one before it
                for i in range(1, 10):
                    diff_x = knots[i - 1][0] - knots[i][0]
                    diff_y = knots[i - 1][1] - knots[i][1]

                    if abs(diff_x) > 1 or abs(diff_y) > 1:
                        knots[i][0] += 1 if diff_x > 0 else (-1 if diff_x < 0 else 0)
                        knots[i][1] += 1 if diff_y > 0 else (-1 if diff_y < 0 else 0)

                # Track where the final tail (knot 9) goes
                visited.add((knots[9][0], knots[9][1]))

        return len(visited)
