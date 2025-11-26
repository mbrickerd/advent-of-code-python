"""Day 3: Gear Ratios

This module provides the solution for Advent of Code 2023 - Day 3.

It handles analysis of engine schematics containing numbers and symbols,
where valid part numbers are determined by their adjacency to symbols.

The module contains a Solution class that inherits from SolutionBase and implements
methods to identify valid part numbers and calculate gear ratios.
"""

import math
import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyse engine schematics for valid part numbers and gear ratios.

    This solution processes engine schematics containing numbers and symbols.
    Part 1 identifies valid part numbers by checking their adjacency to symbols.
    Part 2 calculates gear ratios by finding * symbols adjacent to exactly two numbers.

    The solution uses regex patterns to identify numbers and symbols, then
    analyses their positions to determine valid part numbers and gear ratios.
    """

    digit_regex = r"\D"
    symbol_regex = r"[\d\.]"

    def parse_data(
        self, data: list[str]
    ) -> tuple[dict[tuple[int, int], tuple[int, int]], dict[tuple[int, int], str]]:
        """Parse the engine schematic into mappings of numbers and symbols.

        Creates two dictionaries mapping coordinates to numbers and symbols.
        For numbers, each digit's position maps to a tuple of (number, index)
        where index uniquely identifies each full number in the schematic.

        Args:
            data (list[str]): List of strings representing the engine schematic

        Returns
        -------
            Tuple containing two dictionaries:
            - First dict maps positions to (number, index) tuples
            - Second dict maps positions to symbol strings
        """
        nums = {}
        symbols = {}
        idx_num = 0

        for idx, line in enumerate(data):
            line_nums = re.sub(self.digit_regex, " ", line).split()
            offset = 0
            for n in line_nums:
                position = line.index(n, offset)
                for step in range(len(n)):
                    nums[(idx, position + step)] = (int(n), idx_num)

                offset = position + len(n)
                idx_num += 1

            line_symbols = re.sub(self.symbol_regex, " ", line).split()
            offset = 0
            for symbol in line_symbols:
                position = line.index(symbol, offset)
                symbols[(idx, position)] = symbol
                offset = position + 1

        return nums, symbols

    def part1(self, data: list[str]) -> int:
        """Calculate the sum of valid part numbers in the schematic.

        A part number is valid if it is adjacent to any symbol (including diagonally).
        The solution parses the schematic and checks each number's adjacency to symbols.

        Args:
            data (list[str]): List of strings representing the engine schematic

        Returns
        -------
            Sum of all valid part numbers in the schematic
        """
        nums, symbols = self.parse_data(data)
        adjacent_nums = []

        for position in symbols:
            row, col = position
            adjacent_position = [(row + x, col + y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
            adjacent_nums.extend([nums[pos] for pos in adjacent_position if pos in nums])

        return sum(item[0] for item in set(adjacent_nums))

    def part2(self, data: list[str]) -> int:
        """Calculate the sum of gear ratios in the schematic.

        A gear is a * symbol that is adjacent to exactly two part numbers.
        The gear ratio is the product of these two numbers.

        Args:
            data (list[str]): List of strings representing the engine schematic

        Returns
        -------
            Sum of all gear ratios in the schematic
        """
        nums, symbols = self.parse_data(data)
        _sums = 0

        for position, symbol in symbols.items():
            if symbol == "*":
                row, col = position
                adjacent_position = [(row + x, col + y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
                adjacent_nums = {nums[pos] for pos in adjacent_position if pos in nums}
                if len(adjacent_nums) == 2:
                    _sums += math.prod([item[0] for item in adjacent_nums])

        return _sums
