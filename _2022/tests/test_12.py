"""Test suite for Day 12: Hill Climbing Algorithm

This module contains tests for the Day 12 solution, which finds shortest paths
on a heightmap with elevation climbing constraints. The tests verify:

1. Part 1: Finding shortest path from marked start (S) to end (E)
2. Part 2: Finding shortest path from any low elevation point to end
"""

from aoc.models.tester import TestSolutionUtility


def test_day12_part1() -> None:
    """Test finding shortest path from start marker to end.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=12,
        is_raw=False,
        part_num=1,
        expected=31,
    )


def test_day12_part2() -> None:
    """Test finding shortest path from any low elevation point.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=12,
        is_raw=False,
        part_num=2,
        expected=29,
    )
