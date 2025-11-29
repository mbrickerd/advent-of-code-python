"""Test suite for Day 9: Rope Bridge

This module contains tests for the Day 9 solution, which simulates rope physics
with moving knots on a bridge. The tests verify:

1. Part 1: Tracking positions visited by tail in a 2-knot rope
2. Part 2: Tracking positions visited by final tail in a 10-knot rope
"""

from aoc.models.tester import TestSolutionUtility


def test_day09_part1() -> None:
    """Test counting positions visited by tail in 2-knot rope.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=9,
        is_raw=False,
        part_num=1,
        expected=13,
    )


def test_day09_part2() -> None:
    """Test counting positions visited by final tail in 10-knot rope.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=9,
        is_raw=False,
        part_num=2,
        expected=36,
    )
