"""Day 4: Camp Cleanup

This module provides the solution for Advent of Code 2022 - Day 4.

It handles finding overlapping section assignments between pairs of elves
and counting pairs with fully contained or partially overlapping ranges.

The module contains a Solution class that inherits from SolutionBase and implements
methods to analyze section assignment ranges for cleanup duty conflicts.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyze section assignment overlaps for camp cleanup pairs.

    This solution processes pairs of section ID ranges assigned to elves
    for camp cleanup duty. Part 1 counts pairs where one range fully contains
    the other, while Part 2 counts pairs with any overlap at all.

    The solution uses set operations to efficiently determine subset and
    intersection relationships between ranges of section IDs.
    """

    def part1(self, data: list[str]) -> int:
        """Count pairs where one assignment range fully contains the other.

        Each line contains two ranges separated by a comma. This method finds
        pairs where one elf's section assignment is a complete subset of their
        partner's assignment.

        Args:
            data: List of strings where each string contains two ranges in
                format "start1-end1,start2-end2"

        Returns
        -------
            int: Number of assignment pairs where one range fully contains
                the other
        """
        score = 0
        for pair in data:
            elf1, elf2 = pair.split(",")

            elf1_start, elf1_end = (int(x) for x in elf1.split("-"))
            elf2_start, elf2_end = (int(x) for x in elf2.split("-"))

            if set(range(elf1_start, elf1_end + 1)).issubset(
                set(range(elf2_start, elf2_end + 1))
            ) or set(range(elf2_start, elf2_end + 1)).issubset(
                set(range(elf1_start, elf1_end + 1))
            ):
                score += 1

        return score

    def part2(self, data: list[str]) -> int:
        """Count pairs where assignment ranges overlap at all.

        Each line contains two ranges separated by a comma. This method finds
        pairs where the elves' section assignments have any sections in common.

        Args:
            data: List of strings where each string contains two ranges in
                format "start1-end1,start2-end2"

        Returns
        -------
            int: Number of assignment pairs where the ranges have any overlap
        """
        score = 0
        for pair in data:
            elf1, elf2 = pair.split(",")

            elf1_start, elf1_end = (int(x) for x in elf1.split("-"))
            elf2_start, elf2_end = (int(x) for x in elf2.split("-"))

            if set(range(elf1_start, elf1_end + 1)).intersection(
                set(range(elf2_start, elf2_end + 1))
            ) or set(range(elf2_start, elf2_end + 1)).intersection(
                set(range(elf1_start, elf1_end + 1))
            ):
                score += 1

        return score
