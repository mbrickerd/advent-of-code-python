"""Test suite for Day 1: Calorie Counting

This module contains tests for the Day 1 solution, which calculates total calories
carried by elves based on their inventory lists. The tests verify:

1. Part 1: Finding the elf carrying the most calories
2. Part 2: Calculating the total calories carried by the top three elves
"""

from aoc.models.tester import TestSolutionUtility


def test_day01_part1() -> None:
    """Test finding the elf carrying the most calories.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=1,
        is_raw=False,
        part_num=1,
        expected=24000,
    )


def test_day01_part2() -> None:
    """Test calculating total calories carried by top three elves.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=1,
        is_raw=False,
        part_num=2,
        expected=45000,
    )
