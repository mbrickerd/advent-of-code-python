"""Day 9: Mirage Maintenance

This module provides the solution for Advent of Code 2023 - Day 9.

It handles extrapolation of environmental sensor readings by analyzing sequences
of values and their differences. The puzzle involves predicting future and past
values in sequences using recursive difference analysis until reaching all zeros.

The module contains a Solution class that inherits from SolutionBase and implements
methods to calculate difference sequences, extrapolate values forward and backward,
and sum predictions across multiple sensor histories.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Extrapolate sensor readings using recursive difference analysis.

    This solution handles two types of extrapolation:
    Part 1 predicts the next value in each sequence by calculating successive
    differences until reaching all zeros, then summing values back up.
    Part 2 predicts the previous value by working backwards through the same
    difference sequences.

    The solution builds a pyramid of difference rows and uses them to
    extrapolate values in either direction.
    """

    def get_differences(self, numbers: list[int]) -> list[list[int]]:
        """Calculate successive difference sequences until reaching all zeros.

        Creates rows of differences between consecutive numbers, repeating until
        a row contains only zeros. Each new row has one fewer element than the
        previous row.

        Args:
            numbers (list[int]): Initial sequence of numbers to analyze

        Returns
        -------
            List of lists representing the difference pyramid, with the original
            sequence as the first row and the all-zeros row as the last
        """
        rows = [numbers.copy()]

        while True:
            new_row = [b - a for a, b in zip(rows[-1], rows[-1][1:], strict=False)]

            # If all zeros, append an extra zero
            if all(x == 0 for x in new_row):
                new_row.append(0)
                rows.append(new_row)
                break

            rows.append(new_row)

        return rows

    def extrapolate(self, numbers: list[int], *, backwards: bool = False) -> int:
        """Extrapolate the next or previous value in a sequence.

        Builds the difference pyramid and either sums the last values of each row
        for forward extrapolation, or recursively subtracts first values for
        backward extrapolation.

        Args:
            numbers (list[int]): Sequence of numbers to extrapolate from
            backwards (bool): If True, extrapolate the previous value instead of next

        Returns
        -------
            The extrapolated value (next or previous depending on backwards flag)
        """
        rows = self.get_differences(numbers)

        if backwards:
            # Start from second to last row
            for i in range(len(rows) - 1, 0, -1):
                # Get the new first value by subtracting the first value of current row
                # from the first value of the row above it
                new_first = rows[i - 1][0] - rows[i][0]
                # Prepend this value to the row above
                rows[i - 1].insert(0, new_first)

            return rows[0][0]

        values = [row[-1] for row in rows[::-1]]
        return sum(values)

    def part1(self, data: list[str]) -> int:
        """Calculate sum of extrapolated next values for all sequences.

        Parses each line as a sequence of integers, extrapolates the next value
        for each sequence, and returns the sum of all extrapolated values.

        Args:
            data (list[str]): List of strings where each line contains space-separated numbers

        Returns
        -------
            Sum of all extrapolated next values
        """
        return sum([self.extrapolate(list(map(int, row.split()))) for row in data])

    def part2(self, data: list[str]) -> int:
        """Calculate sum of extrapolated previous values for all sequences.

        Parses each line as a sequence of integers, extrapolates the previous value
        for each sequence using backward analysis, and returns the sum of all
        extrapolated values.

        Args:
            data (list[str]): List of strings where each line contains space-separated numbers

        Returns
        -------
            Sum of all extrapolated previous values
        """
        return sum([self.extrapolate(list(map(int, row.split())), backwards=True) for row in data])
