"""Test suite for Day 1: Circular Dial Rotation

This module contains tests for the Day 1 solution, which simulates dial
rotations on a 100-position circular dial. The tests verify:

1. Part 1: Counting rotations that end exactly at position 0
2. Part 2: Counting every pass through position 0 during rotations
"""

from aoc.models.tester import TestSolutionUtility


def test_day01_part1() -> None:
    """Test counting final positions at zero after rotations.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=1,
        is_raw=False,
        part_num=1,
        expected=3,
    )


def test_day01_part2() -> None:
    """Test counting all zero position visits during step-by-step rotations.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=1,
        is_raw=False,
        part_num=2,
        expected=6,
    )
