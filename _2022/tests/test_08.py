"""Test suite for Day 8: Treetop Tree House

This module contains tests for the Day 8 solution, which analyzes tree visibility
and scenic scores in a grid for tree house placement. The tests verify:

1. Part 1: Counting trees visible from outside the grid
2. Part 2: Finding the highest scenic score for optimal tree house placement
"""

from aoc.models.tester import TestSolutionUtility


def test_day08_part1() -> None:
    """Test counting trees visible from outside the grid.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=8,
        is_raw=False,
        part_num=1,
        expected=21,
    )


def test_day08_part2() -> None:
    """Test finding highest scenic score for tree house location.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=8,
        is_raw=False,
        part_num=2,
        expected=8,
    )
