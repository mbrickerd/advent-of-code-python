import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2023 - Day 1: Trebuchet?!

    This class solves a puzzle involving calibration values embedded in strings,
    where the values need to be extracted by finding the first and last digits
    in each string. Part 2 extends this to include digits written as words.

    Input format:
        List of strings where each line contains a mixture of:
        - Single digits (0-9)
        - Letters and other characters
        - Written number words (one, two, three, etc.)

    The solution uses regex pattern matching to find both numeric digits and
    written numbers, converting them to their numerical representations.
    """

    number_map = {
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
    pattern = r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))"

    def part1(self, data: list[str]) -> int:
        """Extract and sum calibration values using only numeric digits.

        Processes each line to find the first and last numeric digits,
        combining them to form a two-digit number. If only one digit
        is found, it's used as both first and last digit.

        Args:
            data: List of strings containing calibration values

        Returns
        -------
            Sum of all calibration values
        """
        values = []
        for row in data:
            digits = [char for char in row if char.isdigit()]
            if digits:
                digit = int(digits[0] + digits[-1]) if len(digits) > 1 else int(digits[0] * 2)
                values.append(digit)

        return sum(values)

    def part2(self, data: list[str]) -> int:
        """Extract and sum calibration values using both digits and written numbers.

        Processes each line to find the first and last occurrence of either
        numeric digits or written number words (e.g., "one", "two", etc.).
        Written numbers are converted to their digit equivalents before
        combining them to form a two-digit number.

        Uses positive lookahead regex pattern to handle overlapping matches
        (e.g., "oneight" contains both "one" and "eight").

        Args:
            data: List of strings containing calibration values with both
                  numeric and written numbers

        Returns
        -------
            Sum of all calibration values
        """
        values = []
        for row in data:
            digits = []
            for match in re.finditer(self.pattern, row):
                # group(1) contains the actual matched digit/word
                digit = match.group(1)

                # Convert word to digit if it's a word
                digit = self.number_map.get(digit, digit)
                digits.append(digit)

            if digits:
                value = int(digits[0] + digits[-1])
                values.append(value)

        return sum(values)
