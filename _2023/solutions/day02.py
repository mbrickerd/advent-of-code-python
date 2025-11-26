"""Day 2: Cube Conundrum

This module provides the solution for Advent of Code 2023 - Day 2.

It handles analysis of cube games where colored cubes are drawn from a bag
in multiple sets, with each game having several draws of red, green, and blue cubes.

The module contains a Solution class that inherits from SolutionBase and implements
methods to validate games against thresholds and find minimum required cubes.
"""

from math import prod
import re
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyse cube games for validity and minimum requirements.

    This solution processes games where colored cubes are drawn from a bag.
    Part 1 validates games against thresholds for each color.
    Part 2 calculates the minimum number of cubes required for each game.

    The solution uses regex patterns to extract game IDs and cube counts,
    validating them against thresholds (Part 1) and finding minimum required
    cubes (Part 2).
    """

    thresholds: ClassVar[dict[str, int]] = {"red": 12, "green": 13, "blue": 14}
    color_regex: ClassVar[str] = r"(\d+) (red|green|blue)"
    id_regex: ClassVar[str] = r"Game (\d+)"

    def is_possible(self, data: str) -> bool:
        """Check if a set of cube draws is possible given the thresholds.

        Args:
            data (str): String containing cube counts for a single set

        Returns
        -------
            Boolean indicating whether the draw is possible with given thresholds
        """
        for count, color in re.findall(self.color_regex, data):
            if int(count) > self.thresholds[color]:
                return False

        return True

    def part1(self, data: list[str]) -> int:
        """Sum IDs of games possible with the given cube thresholds.

        Args:
            data (list[str]): List of game strings in format "Game N: X red, Y green, Z blue; ..."

        Returns
        -------
            Sum of IDs for games where all draws are within thresholds
        """
        total = 0
        for game in data:
            match = re.search(self.id_regex, game)
            if match is None:
                continue
            game_id = int(match.group(1))
            sets = game.split(":")[1].split(";")
            if all(self.is_possible(s) for s in sets):
                total += game_id

        return total

    def part2(self, data: list[str]) -> int:
        """Calculate the sum of minimum cube powers for each game.

        Args:
            data (list[str]): List of game strings in format "Game N: X red, Y green, Z blue; ..."

        Returns
        -------
            Sum of the product of minimum required cubes for each color in each game
        """
        total = 0
        for game in data:
            sets = game.split(":")[1].split(";")
            min_cubes = {"red": 0, "green": 0, "blue": 0}
            for s in sets:
                for count, color in re.findall(self.color_regex, s):
                    min_cubes[color] = max(min_cubes[color], int(count))

            total += prod(min_cubes.values())

        return total
