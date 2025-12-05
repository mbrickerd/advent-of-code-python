"""Test suite for Day 4: Printing Department

This module contains tests for the Day 4 solution, which analyzes paper roll
grids to determine accessibility and removal order. The tests verify:

1. Part 1: Counting initially accessible paper rolls (fewer than 4 neighbors)
2. Part 2: Counting total rolls removable through iterative process
"""

from aoc.models.tester import TestSolutionUtility


def test_day04_part1() -> None:
    """Test counting initially accessible paper rolls.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=4,
        is_raw=False,
        part_num=1,
        expected=13,
    )


def test_day04_part2() -> None:
    """Test counting total removable paper rolls iteratively.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=4,
        is_raw=False,
        part_num=2,
        expected=43,
    )
