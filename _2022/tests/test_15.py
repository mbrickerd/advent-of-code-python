"""Test suite for Day 15: Beacon Exclusion Zone

This module contains tests for the Day 15 solution, which analyzes sensor
coverage using Manhattan distance to locate exclusion zones and find hidden
beacons. The tests verify:

1. Part 1: Counting positions where beacons cannot exist on a target row
2. Part 2: Finding the tuning frequency of the hidden distress beacon
"""

from aoc.models.tester import TestSolutionUtility


def test_day15_part1() -> None:
    """Test counting impossible beacon positions on target row.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=15,
        is_raw=False,
        part_num=1,
        expected=26,
    )


def test_day15_part2() -> None:
    """Test finding tuning frequency of distress beacon location.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=15,
        is_raw=False,
        part_num=2,
        expected=56000011,
    )
