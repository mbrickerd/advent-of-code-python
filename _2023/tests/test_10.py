"""Test suite for Day 10: Pipe Maze

This module contains tests for the Day 10 solution, which navigates through a maze
of metal pipes to find a continuous loop. The tests verify:

1. Part 1: Finding the farthest point in the loop from the starting position
2. Part 2: Calculating the number of tiles enclosed within the loop
"""

from aoc.models.tester import TestSolutionUtility


def test_day10_part1() -> None:
    """Test finding the farthest point in the pipe loop.

    Verifies that the solution traces the continuous pipe loop from the starting
    position 'S' and correctly calculates the maximum distance, which is half the
    total loop length.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=10,
        is_raw=False,
        part_num=1,
        expected=4,
    )


def test_day10_part2() -> None:
    """Test counting tiles enclosed within the pipe loop.

    Verifies that the solution identifies the main loop and correctly counts interior
    tiles using a scanline approach with crossing number algorithm to determine which
    tiles are inside versus outside the loop boundary.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=10,
        is_raw=False,
        part_num=2,
        expected=10,
    )
