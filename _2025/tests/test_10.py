"""Test suite for Day 10: Factory

This module contains tests for the Day 10 solution, which configures factory
machines by pressing buttons to match indicator light diagrams and, later,
joltage requirements. The tests verify:

1. Part 1: Fewest total button presses to match all indicator light patterns
2. Part 2: Fewest total button presses to satisfy all joltage requirements
"""

from aoc.models.tester import TestSolutionUtility


def test_day10_part1() -> None:
    """Test computing minimal presses to match indicator lights for all machines.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=10,
        is_raw=False,
        part_num=1,
        expected=7,
    )


def test_day10_part2() -> None:
    """Test computing minimal presses to satisfy joltage requirements for all machines.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=10,
        is_raw=False,
        part_num=2,
        expected=33,
    )
