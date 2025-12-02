"""Boilerplate solution template for Advent of Code daily challenges.

This module provides a template class for solving Advent of Code puzzle problems.
It includes a base structure with two method stubs (part1 and part2) that can be
implemented for specific day's challenges.

The template follows the SolutionBase pattern used across the Advent of Code solutions,
allowing for consistent handling of input parsing and solution execution.
"""

from collections.abc import Callable
from functools import partial

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution template for Advent of Code daily puzzle.

    This class provides a standardized structure for implementing solutions to
    daily Advent of Code challenges. It inherits from SolutionBase and includes
    method stubs for part1 and part2 of the puzzle.

    Subclasses should override these methods with specific implementation logic
    for parsing input and solving the puzzle requirements.
    """

    def has_repeated_sequence(self, n: int, num_repeats: int | None = None) -> bool:
        s = str(n)
        length = len(s)

        if num_repeats:
            if num_repeats <= 1:
                return False

            if length % num_repeats != 0:
                return False

            size = length // num_repeats
            return s == s[:size] * num_repeats

        else:  # Check for any number of repetitions > 1
            for k in range(2, length + 1):
                if length % k == 0:
                    size = length // k
                    if s == s[:size] * k:
                        return True

            return False

    def solve_part(self, data: list[str], func: Callable) -> int:
        """Calculates the sum of numbers in ranges that satisfy the check_func."""
        invalid = 0
        for line in data[0].split(","):
            start, end = map(int, line.split("-"))
            for product in range(start, end + 1):
                if func(product):
                    invalid += product

        return invalid

    def part1(self, data: list[str]) -> int:
        """Solve the first part of the daily puzzle.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Solution for part 1 of the puzzle
        """
        check_for_two_repeats = partial(self.has_repeated_sequence, num_repeats=2)
        return self.solve_part(data, check_for_two_repeats)

    def part2(self, data: list[str]) -> int:
        """Solve the second part of the daily puzzle.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Solution for part 2 of the puzzle
        """
        return self.solve_part(data, self.has_repeated_sequence)
