"""Test suite for Day 2: Cube Conundrum

This module contains tests for the Day 2 solution, which handles analysis of
cube games where colored cubes are drawn from a bag. The tests verify:

1. Part 1: Validation of games against cube color thresholds
2. Part 2: Calculation of minimum required cubes and their power values
"""

from aoc.models.tester import TestSolutionUtility


def test_day02_part1() -> None:
    """Test validating games against cube color thresholds.

    Verifies that the solution correctly identifies games where all cube draws
    are within the specified thresholds (12 red, 13 green, 14 blue) and sums
    their game IDs.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=2,
        is_raw=False,
        part_num=1,
        expected=8,
    )


def test_day02_part2() -> None:
    """Test calculating the sum of minimum cube powers for each game.

    Verifies that the solution correctly finds the minimum number of cubes
    needed for each color in each game and calculates the sum of their
    products (power values).
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=2,
        is_raw=False,
        part_num=2,
        expected=2286,
    )
