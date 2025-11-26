"""Day 1: Trebuchet?!

This module provides the solution for Advent of Code 2023 - Day 1.

It handles extraction of calibration values from strings containing digits
and written numbers.

The module contains a Solution class that inherits from SolutionBase and implements
methods to extract and process calibration values from input strings.
"""

import re
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Extract and process calibration values from strings.

    This solution handles strings containing calibration values that need to be
    extracted by finding the first and last digits. Part 1 handles numeric digits
    only, while Part 2 extends this to include digits written as words.

    The solution uses regex pattern matching to find both numeric digits and
    written numbers, converting them to their numerical representations.
    """

    number_map: ClassVar[dict[str, str]] = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    pattern: ClassVar[str] = r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))"

    def part1(self, data: list[str]) -> int:
        """Calculate the sum of calibration values using only numeric digits.

        Args:
            data (list[str]): List of strings containing calibration values.

        Returns
        -------
            The sum of all calibration values, where each value is formed by
            combining the first and last numeric digits in each string.
        """
        total = 0
        for line in data:
            digits = [c for c in line if c.isdigit()]
            if digits:
                total += int(digits[0] + digits[-1])
        return total

    def part2(self, data: list[str]) -> int:
        """Calculate the sum of calibration values including written numbers.

        Args:
            data (list[str]): List of strings containing calibration values and written numbers.

        Returns
        -------
            The sum of all calibration values, where each value is formed by
            combining the first and last digits (numeric or written) in each string.
        """
        total = 0
        for line in data:
            matches = re.findall(self.pattern, line)
            if matches:
                first = self.number_map.get(matches[0], matches[0])
                last = self.number_map.get(matches[-1], matches[-1])
                total += int(first + last)
        return total
