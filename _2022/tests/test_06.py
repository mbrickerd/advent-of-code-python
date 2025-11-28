"""Test suite for Day 6: Tuning Trouble

This module contains tests for the Day 6 solution, which detects signal markers
in a communication device datastream. The tests verify:

1. Part 1: Finding start-of-packet marker (4 unique characters)
2. Part 2: Finding start-of-message marker (14 unique characters)
"""

from aoc.models.tester import TestSolutionUtility


def test_day06_part1() -> None:
    """Test detecting start-of-packet marker with 4 unique characters.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=6,
        is_raw=False,
        part_num=1,
        expected=11,
    )


def test_day06_part2() -> None:
    """Test detecting start-of-message marker with 14 unique characters.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=6,
        is_raw=False,
        part_num=2,
        expected=26,
    )
