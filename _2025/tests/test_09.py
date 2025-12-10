"""Test suite for Day 9: Movie Theater

This module contains tests for the Day 9 solution, which finds the largest
rectangles in a movie theater tile grid using red tiles as opposite corners.
The tests verify:

1. Part 1: Largest rectangle area using any two red tiles as opposite corners
2. Part 2: Largest rectangle area using only red and green tiles
"""

from aoc.models.tester import TestSolutionUtility


def test_day09_part1() -> None:
    """Test finding largest rectangle using red tiles as opposite corners.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=9,
        is_raw=False,
        part_num=1,
        expected=50,
    )


def test_day09_part2() -> None:
    """Test finding largest rectangle using only red and green tiles.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=9,
        is_raw=False,
        part_num=2,
        expected=24,
    )
