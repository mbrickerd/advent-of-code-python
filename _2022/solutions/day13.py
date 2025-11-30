"""Day 13: Distress Signal

This module provides the solution for Advent of Code 2022 - Day 13.

It implements recursive comparison of nested list structures to determine
correct packet ordering based on specific comparison rules.

The module contains a Solution class that inherits from SolutionBase for
parsing and comparing packet data to decode a distress signal.
"""

from ast import literal_eval
from functools import cmp_to_key
from typing import Any

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Compare and sort nested list packets to decode distress signal.

    This solution implements custom comparison logic for nested lists and integers
    following specific ordering rules. Part 1 identifies pairs already in correct
    order and sums their indices. Part 2 sorts all packets with divider packets
    and calculates the decoder key.

    The comparison rules handle integers, lists, and mixed types with automatic
    type conversion when comparing integers against lists.
    """

    def _parse_group(self, group: str) -> tuple[list, list]:
        """Parse a pair of packet strings into list structures.

        Uses literal_eval to safely parse bracket-delimited packet notation
        into Python list structures.

        Args:
            group: String containing two packet lines separated by newline

        Returns
        -------
            tuple[list, list]: Left and right packet as parsed list structures
        """
        left, right = group.strip().split("\n")
        return literal_eval(left), literal_eval(right)

    def compare(self, left: Any, right: Any) -> int:
        """Compare two packet values recursively following distress signal rules.

        Comparison rules:
        - Both integers: compare numerically
        - Both lists: compare element-by-element, then by length
        - Mixed types: convert integer to single-element list and retry

        Args:
            left: Left packet value (int or list)
            right: Right packet value (int or list)

        Returns
        -------
            int: -1 if left < right (correct order), 0 if equal (continue),
                1 if left > right (incorrect order)
        """
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return -1

            if left > right:
                return 1

            return 0

        if isinstance(left, list) and isinstance(right, list):
            for idx in range(min(len(left), len(right))):
                result = self.compare(left[idx], right[idx])
                if result != 0:
                    return result

            if len(left) < len(right):
                return -1

            if len(left) > len(right):
                return 1

            return 0

        if isinstance(left, int):
            return self.compare([left], right)

        return self.compare(left, [right])

    def part1(self, data: str) -> int:
        """Find sum of indices of packet pairs already in correct order.

        Examines each pair of packets and identifies which are already correctly
        ordered according to the distress signal comparison rules. Returns the
        sum of 1-based indices for pairs in correct order.

        Args:
            data: Raw input string with packet pairs separated by blank lines

        Returns
        -------
            int: Sum of 1-indexed pair numbers that are already in correct order
        """
        score = 0

        for idx, group in enumerate(data.split("\n\n"), start=1):
            left, right = self._parse_group(group)

            if self.compare(left, right) == -1:
                score += idx

        return score

    def part2(self, data: str) -> int:
        """Calculate decoder key by sorting packets with divider packets.

        Adds two divider packets [[2]] and [[6]] to all packets, sorts them
        using the distress signal comparison rules, and calculates the decoder
        key as the product of the 1-based indices of the divider packets.

        Args:
            data: Raw input string with packet pairs separated by blank lines

        Returns
        -------
            int: Decoder key (product of divider packet indices after sorting)
        """
        packets: list[Any] = [[[2]], [[6]]]
        for group in data.split("\n\n"):
            left, right = self._parse_group(group)
            packets.append(left)
            packets.append(right)

        packets.sort(key=cmp_to_key(self.compare))
        return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
