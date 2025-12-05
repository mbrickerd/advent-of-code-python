"""Day 5: Cafeteria

This module provides the solution for Advent of Code 2025 - Day 5.

It processes a database of fresh ingredient ID ranges and a list of available
ingredient IDs to determine which ingredients are fresh and how many IDs fall
within any fresh range.

The module contains a Solution class that inherits from SolutionBase and
implements logic for checking freshness and merging overlapping ranges.
"""

import re

from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyze ingredient ID ranges to determine freshness and coverage.

    This solution works with inclusive integer ranges representing fresh
    ingredient IDs. Part 1 counts how many available ingredient IDs are fresh
    (they fall into at least one range). Part 2 merges overlapping and adjacent
    ranges and computes how many distinct IDs are covered in total.

    The implementation uses regex-based parsing for ranges and a standard
    interval merge algorithm to handle overlapping fresh ID ranges.
    """

    REGEX: ClassVar[re.Pattern[str]] = re.compile(r"(\d+)-(\d+)$")

    def parse_data(self, data: str) -> tuple[list[tuple[int, int]], list[int]]:
        """Parse fresh ID ranges and available ingredient IDs from input.

        The input consists of a block of inclusive fresh ID ranges, a blank
        line, and then a block of available ingredient IDs, one per line.

        Args:
            data: Raw puzzle input as a single string

        Returns
        -------
            tuple[list[tuple[int, int]], list[int]]:
                - List of (start, end) tuples for fresh ID ranges
                - List of available ingredient IDs
        """
        fresh, available = data.split("\n\n")

        ranges: list[tuple[int, int]] = []
        for line in fresh.splitlines():
            if not line:
                continue

            match = self.REGEX.search(line)
            if not match:
                msg = f"Invalid ingredient range: {line}"
                raise ValueError(msg)

            start, end = int(match.group(1)), int(match.group(2))
            ranges.append((start, end))

        return ranges, [int(x) for x in available.splitlines() if x]

    @staticmethod
    def is_fresh(ingredient: int, interval: tuple[int, int]) -> bool:
        """Check whether an ingredient ID is fresh for a single range.

        Args:
            ingredient: Ingredient ID to check
            interval: Inclusive range (start, end) for fresh IDs

        Returns
        -------
            bool: True if ingredient is within the range, False otherwise
        """
        start, end = interval
        return start <= ingredient <= end

    def part1(self, data: str) -> int:
        """Count available ingredient IDs that are fresh.

        An ingredient ID is considered fresh if it falls into at least one
        of the inclusive fresh ID ranges.

        Args:
            data: Raw puzzle input as a single string

        Returns
        -------
            int: Number of available ingredient IDs that are fresh
        """
        ranges, ingredients = self.parse_data(data)
        count = 0

        for ingredient in ingredients:
            for interval in ranges:
                if self.is_fresh(ingredient, interval):
                    count += 1
                    break

        return count

    def part2(self, data: str) -> int:
        """Count total number of distinct fresh ingredient IDs.

        This part merges overlapping and adjacent fresh ID ranges and then
        counts how many distinct ingredient IDs are covered by the merged
        ranges.

        Args:
            data: Raw puzzle input as a single string

        Returns
        -------
            int: Total count of distinct ingredient IDs that are fresh
        """
        ranges, _ = self.parse_data(data)
        ranges = sorted(ranges, key=lambda interval: interval[0])

        total = 0
        current_start, current_end = ranges[0]

        for start, end in ranges[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                total += current_end - current_start + 1
                current_start, current_end = start, end

        total += current_end - current_start + 1
        return total
