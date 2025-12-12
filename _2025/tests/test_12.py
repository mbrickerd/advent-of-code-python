"""Test suite for Day 12: Christmas Tree Farm

This module contains tests for the Day 12 solution, which checks for
each rectangular region under a Christmas tree whether it can fit all
requested oddly-shaped presents. The tests verify:

1. Part 1: Counting how many regions can fit their listed presents
"""

from aoc.models.tester import TestSolutionUtility


def test_day12_part1() -> None:
    """Test counting regions that can fit all presents.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=12,
        is_raw=True,
        part_num=1,
        expected=3,
    )
