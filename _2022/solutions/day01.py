"""Day 1: Calorie Counting

This module provides the solution for Advent of Code 2022 - Day 1.

It handles the calculation of total calories carried by elves based on
their food inventory lists separated by blank lines.

The module contains a Solution class that inherits from SolutionBase and implements
methods to identify the elves carrying the most calories.
"""

from itertools import groupby, islice

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Calculate total calories carried by elves from inventory data.

    This solution parses elf inventory lists separated by blank lines and calculates
    the total calories carried by each elf. Part 1 identifies the elf carrying the
    most calories, while Part 2 finds the total calories carried by the top three elves.

    The solution uses itertools.groupby to efficiently separate elf inventories and
    processes calorie sums in a memory-efficient manner.
    """

    def get_elves(self, data: list[str]) -> dict[int, int]:
        """Parse elf inventories and return sorted calorie totals.

        Args:
            data: List of strings representing calorie values, separated by empty strings

        Returns
        -------
            dict[int, int]: Dictionary mapping elf rank (1-indexed) to total calories,
                sorted in descending order by calorie count
        """
        result = (
            sum(int(item) for item in sublist) for item, sublist in groupby(data, key=bool) if item
        )
        return dict(enumerate(sorted(result, reverse=True), start=1))

    def part1(self, data: list[str]) -> int:
        """Find the maximum calories carried by any single elf.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Total calories carried by the elf with the most calories
        """
        elves = self.get_elves(data)
        return next(iter(elves.values()))

    def part2(self, data: list[str]) -> int:
        """Calculate total calories carried by the top three elves.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Sum of calories carried by the three elves with the most calories
        """
        elves = self.get_elves(data)
        return sum(islice(elves.values(), 3))
