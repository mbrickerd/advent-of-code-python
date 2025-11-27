"""Day 3: Rucksack Reorganization

This module provides the solution for Advent of Code 2022 - Day 3.

It handles finding common items in rucksack compartments and calculating
their priority values based on alphabetical position.

The module contains a Solution class that inherits from SolutionBase and implements
methods to identify misplaced items and calculate priority sums.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Calculate priority sums for misplaced rucksack items.

    This solution processes rucksack contents to find common items across
    compartments or groups. Part 1 finds items appearing in both compartments
    of a single rucksack, while Part 2 finds items common to groups of three
    rucksacks (badges).

    The solution uses set intersection for efficient item comparison and ASCII
    values to calculate item priorities (a-z: 1-26, A-Z: 27-52).
    """

    def part1(self, data: list[str]) -> int:
        """Calculate sum of priorities for items in both rucksack compartments.

        Each rucksack is split into two equal compartments. This method finds
        the item type that appears in both compartments and sums their priorities.

        Args:
            data: List of strings where each string represents items in a rucksack

        Returns
        -------
            int: Sum of priorities for all items appearing in both compartments
                of their respective rucksacks
        """
        score = 0
        for rucksack in data:
            c1, c2 = set(rucksack[: len(rucksack) // 2]), set(rucksack[len(rucksack) // 2 :])
            common_item = c1.intersection(c2).pop()

            if common_item.islower():
                score += ord(common_item) - 96
            else:
                score += ord(common_item) - 64 + 26

        return score

    def part2(self, data: list[str]) -> int:
        """Calculate sum of priorities for badge items across elf groups.

        Elves are divided into groups of three. This method finds the item type
        (badge) that appears in all three rucksacks of each group and sums their
        priorities.

        Args:
            data: List of strings where each string represents items in a rucksack

        Returns
        -------
            int: Sum of priorities for all badge items common to groups of three
                consecutive rucksacks
        """
        score = 0
        for idx in range(0, len(data), 3):
            r1, r2, r3 = data[idx], data[idx + 1], data[idx + 2]
            common_item = set(r1).intersection(set(r2)).intersection(set(r3)).pop()

            if common_item.islower():
                score += ord(common_item) - 96
            else:
                score += ord(common_item) - 64 + 26

        return score
