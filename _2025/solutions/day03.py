"""Day 3: Maximum Joltage Extraction

This module provides the solution for Advent of Code 2025 - Day 3.

It finds the maximum numeric value that can be formed by selecting k digits
from a string while maintaining their original order.

The module contains a Solution class that inherits from SolutionBase for
extracting optimal digit sequences from power bank readings.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Extract maximum joltage values from digit sequences.

    This solution finds the largest k-digit number that can be formed from
    a string of digits while preserving their original order. Part 1 extracts
    2-digit values, while Part 2 extracts 12-digit values. Uses a greedy
    monotonic stack algorithm for optimal digit selection.

    The algorithm ensures maximum value by keeping larger digits when possible
    and removing smaller preceding digits when necessary.
    """

    def find_max_joltage(self, bank: str, k: int) -> int:
        """Find maximum k-digit number from digit string preserving order.

        Uses a monotonic decreasing stack to greedily select the k largest
        digits while maintaining their relative order. Removes digits that
        would prevent forming a larger number.

        Args:
            bank: String of digits representing power bank reading
            k: Number of digits to select for the output value

        Returns
        -------
            int: Maximum k-digit number that can be formed from the input digits
                while preserving their original order
        """
        digits = [int(c) for c in bank]
        n = len(digits)
        remove = n - k
        stack: list[int] = []

        for d in digits:
            while remove > 0 and stack and stack[-1] < d:
                stack.pop()
                remove -= 1

            stack.append(d)

        if remove > 0:
            stack = stack[:-remove]

        value = 0
        for d in stack[:k]:
            value = value * 10 + d

        return value

    def part1(self, data: list[str]) -> int:
        """Calculate sum of maximum 2-digit joltages from all power banks.

        Each power bank reading is a string of digits. Extracts the maximum
        2-digit number from each reading (preserving digit order) and returns
        the sum of all such values.

        Args:
            data: List of power bank readings (digit strings)

        Returns
        -------
            int: Sum of maximum 2-digit values from all readings
        """
        return sum([self.find_max_joltage(line, 2) for line in data])

    def part2(self, data: list[str]) -> int:
        """Calculate sum of maximum 12-digit joltages from all power banks.

        Each power bank reading is a string of digits. Extracts the maximum
        12-digit number from each reading (preserving digit order) and returns
        the sum of all such values.

        Args:
            data: List of power bank readings (digit strings)

        Returns
        -------
            int: Sum of maximum 12-digit values from all readings
        """
        return sum([self.find_max_joltage(line, 12) for line in data])
