"""Test suite for Day 5: Supply Stacks

This module contains tests for the Day 5 solution, which simulates cargo crane
operations on supply crate stacks. The tests verify:

1. Part 1: CrateMover 9000 moving crates one at a time (reversing order)
2. Part 2: CrateMover 9001 moving multiple crates simultaneously (preserving order)
"""

from aoc.models.tester import TestSolutionUtility


def test_day05_part1() -> None:
    """Test CrateMover 9000 crane operation with single-crate moves.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=5,
        is_raw=True,
        part_num=1,
        expected="CMZ",
    )


def test_day05_part2() -> None:
    """Test CrateMover 9001 crane operation with multi-crate moves.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=5,
        is_raw=True,
        part_num=2,
        expected="MCD",
    )
