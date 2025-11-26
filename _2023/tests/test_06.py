"""Test suite for Day 6: Wait For It

This module contains tests for the Day 6 solution, which calculates winning strategies for toy
boat races based on button hold duration. The tests verify:

1. Part 1: Product of winning ways across multiple separate races
2. Part 2: Number of winning ways for a single race with concatenated values
"""

from aoc.models.tester import TestSolutionUtility


def test_day06_part1() -> None:
    """Test calculating the product of winning ways for multiple races.

    Verifies that the solution counts winning hold durations for each race and multiplies them
    together, where boat speed equals hold time and distance equals speed times remaining time.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=6,
        is_raw=False,
        part_num=1,
        expected=288,
    )


def test_day06_part2() -> None:
    """Test calculating winning ways for a single concatenated race.

    Verifies that the solution joins all time and distance digits into single values and counts
    the number of button hold durations that beat the record distance.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=6,
        is_raw=False,
        part_num=2,
        expected=71503,
    )
