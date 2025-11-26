"""Test suite for Day 1: Trebuchet?!

This module contains tests for the Day 1 solution, which handles extraction of
calibration values from strings containing digits and written numbers. The tests verify:

1. Part 1: Calculation of the sum of calibration values using only numeric digits
2. Part 2: Calculation of the sum of calibration values including written numbers
"""

from aoc.models.tester import TestSolutionUtility


def test_day01_part1() -> None:
    """Test calculating the sum of calibration values using only numeric digits.

    Verifies that the solution correctly extracts the first and last numeric
    digits from each string and calculates the sum of all calibration values.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=1,
        is_raw=False,
        part_num=1,
        expected=142,
    )


def test_day01_part2() -> None:
    """Test calculating the sum of calibration values including written numbers.

    Verifies that the solution correctly extracts the first and last digits
    (numeric or written as words) from each string and calculates the sum of
    all calibration values.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=1,
        is_raw=False,
        part_num=2,
        expected=281,
    )
