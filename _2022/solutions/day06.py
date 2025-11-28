"""Day 6: Tuning Trouble

This module provides the solution for Advent of Code 2022 - Day 6.

It handles detecting start-of-packet and start-of-message markers in a
datastream by finding sequences of unique characters.

The module contains a Solution class that inherits from SolutionBase and implements
methods to identify the first position where all characters in a sliding window are distinct.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Detect signal markers in communication device datastream.

    This solution processes a datastream buffer to locate signal markers.
    Part 1 finds the start-of-packet marker (4 distinct characters), while
    Part 2 finds the start-of-message marker (14 distinct characters).

    The solution uses a sliding window approach with set operations to
    efficiently identify positions where all characters are unique.
    """

    def find_signal(self, data: list[str], length: int) -> int | None:
        """Find position after first occurrence of unique character sequence.

        Uses a sliding window to scan the datastream and identifies the first
        position where the previous 'length' characters are all distinct.

        Args:
            data: List containing single string of datastream characters
            length: Number of distinct characters required for signal marker

        Returns
        -------
            int: Number of characters processed when marker is first detected
                (position after the last character of the marker sequence)
        """
        data = list(data[0])
        for idx in range(len(data)):
            if idx >= length:
                signal = data[idx - length : idx]
                if len(set(signal)) == length:
                    return idx

        return None

    def part1(self, data: list[str]) -> int | None:
        """Detect start-of-packet marker (4 unique characters).

        Finds the position after the first sequence of 4 distinct characters
        in the datastream, indicating the device can begin packet reception.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Number of characters processed before start-of-packet marker
                is detected
        """
        return self.find_signal(data, 4)

    def part2(self, data: list[str]) -> int | None:
        """Detect start-of-message marker (14 unique characters).

        Finds the position after the first sequence of 14 distinct characters
        in the datastream, indicating the device can begin message reception.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Number of characters processed before start-of-message marker
                is detected
        """
        return self.find_signal(data, 14)
