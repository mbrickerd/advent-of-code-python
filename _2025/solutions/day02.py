"""Day 2: Gift Shop

This module provides the solution for Advent of Code 2025 - Day 2.

It identifies invalid product IDs within given ranges. An ID is considered
invalid if it is formed by a repeating sequence of digits.

The module contains a Solution class that inherits from SolutionBase for
parsing ID ranges and summing the invalid IDs found.
"""

from collections.abc import Callable
from functools import partial

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Find and sum invalid product IDs based on repeating digit patterns.

    This solution processes a string of comma-separated ID ranges (e.g., "1-10,20-30").
    It checks each ID in every range to see if it matches a specific pattern of
    repeating digits.

    Part 1 defines an invalid ID as one made of a digit sequence repeated twice (e.g., 1212).
    Part 2 expands this to any ID made of a sequence repeated at least twice (e.g., 1212, 121212).
    """

    def has_repeated_sequence(self, n: int, num_repeats: int | None = None) -> bool:
        """Check if a number consists of a repeating sequence of digits.

        Args:
            n: The integer to check.
            num_repeats: If an integer, checks for exactly that many repetitions.
                         If None, checks for any number of repetitions (>= 2).

        Returns
        -------
            bool: True if the number is formed by a repeating sequence, False otherwise.
        """
        s = str(n)
        length = len(s)

        if num_repeats:
            if num_repeats <= 1:
                return False

            if length % num_repeats != 0:
                return False

            size = length // num_repeats
            return s == s[:size] * num_repeats

        # Check for any number of repetitions from 2 up to the length of the string
        for k in range(2, length + 1):
            if length % k == 0:
                size = length // k
                if s == s[:size] * k:
                    return True

        return False

    def solve_part(self, data: list[str], func: Callable[[int], bool]) -> int:
        """Find and sum invalid IDs based on a check function.

        Parses the input string of ranges, iterates through each number, and applies
        the provided checking function to identify and sum invalid IDs.

        Args:
            data: A list containing one string of comma-separated ranges.
            func: A callable that takes an integer and returns True if it's invalid.

        Returns
        -------
            int: The sum of all invalid product IDs found.
        """
        invalid_sum = 0
        for line in data[0].split(","):
            start, end = map(int, line.split("-"))
            for product_id in range(start, end + 1):
                if func(product_id):
                    invalid_sum += product_id

        return invalid_sum

    def part1(self, data: list[str]) -> int:
        """Calculate the sum of invalid IDs where a digit sequence is repeated twice.

        An ID is invalid if it's formed by a sequence of digits repeated
        exactly twice (e.g., `6464` from `64`). This method sums all such
        IDs found in the input ranges.

        Args:
            data: A list containing the input string of ID ranges.

        Returns
        -------
            int: The total sum of invalid IDs for Part 1.
        """
        check_func = partial(self.has_repeated_sequence, num_repeats=2)
        return self.solve_part(data, check_func)

    def part2(self, data: list[str]) -> int:
        """Calculate the sum of invalid IDs where a digit sequence is repeated at least twice.

        An ID is invalid if it's formed by a sequence of digits repeated two
        or more times (e.g., `1212` or `121212`). This method sums all such
        IDs found in the input ranges.

        Args:
            data: A list containing the input string of ID ranges.

        Returns
        -------
            int: The total sum of invalid IDs for Part 2.
        """
        return self.solve_part(data, self.has_repeated_sequence)
