"""Test suite for Day 4: Camp Cleanup

This module contains tests for the Day 4 solution, which analyzes section assignment
overlaps for camp cleanup pairs. The tests verify:

1. Part 1: Counting pairs where one assignment range fully contains the other
2. Part 2: Counting pairs where assignment ranges have any overlap
"""

from aoc.models.tester import TestSolutionUtility


def test_day04_part1() -> None:
    """Test counting pairs with fully contained assignment ranges.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=4,
        is_raw=False,
        part_num=1,
        expected=2,
    )


def test_day04_part2() -> None:
    """Test counting pairs with any overlapping assignment ranges.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=4,
        is_raw=False,
        part_num=2,
        expected=4,
    )
