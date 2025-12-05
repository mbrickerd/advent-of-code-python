"""Test suite for Day 5: Cafeteria

This module contains tests for the Day 5 solution, which analyzes fresh
ingredient ID ranges and available ingredient IDs. The tests verify:

1. Part 1: Counting available IDs that are fresh
2. Part 2: Counting total distinct fresh IDs after merging ranges
"""

from aoc.models.tester import TestSolutionUtility


def test_day05_part1() -> None:
    """Test counting fresh available ingredient IDs.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=5,
        is_raw=True,
        part_num=1,
        expected=3,
    )


def test_day05_part2() -> None:
    """Test counting total distinct fresh IDs after merging ranges.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=5,
        is_raw=True,
        part_num=2,
        expected=14,
    )
