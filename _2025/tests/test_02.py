"""Test suite for Day 2: Gift Shop

This module contains tests for the Day 2 solution, which identifies and sums
invalid product IDs from a list of ranges. The tests verify:

1. Part 1: Summing IDs where a digit sequence is repeated exactly twice.
2. Part 2: Summing IDs where a digit sequence is repeated at least twice.
"""

from aoc.models.tester import TestSolutionUtility


def test_day02_part1() -> None:
    """Test summing invalid IDs with a twice-repeated digit sequence.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=2,
        is_raw=False,
        part_num=1,
        expected=1227775554,
    )


def test_day02_part2() -> None:
    """Test summing invalid IDs with a digit sequence repeated at least twice.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=2,
        is_raw=False,
        part_num=2,
        expected=4174379265,
    )
