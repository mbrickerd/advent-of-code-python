"""Test suite for Day 7: No Space Left On Device

This module contains tests for the Day 7 solution, which analyzes filesystem
directory sizes to identify cleanup candidates. The tests verify:

1. Part 1: Finding sum of directories with total size ≤ 100000 bytes
2. Part 2: Finding smallest directory to delete for system update space
"""

from aoc.models.tester import TestSolutionUtility


def test_day07_part1() -> None:
    """Test finding sum of small directories (≤ 100000 bytes).

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=7,
        is_raw=False,
        part_num=1,
        expected=95437,
    )


def test_day07_part2() -> None:
    """Test finding smallest directory to free update space.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=7,
        is_raw=False,
        part_num=2,
        expected=24933642,
    )
