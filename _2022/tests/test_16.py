"""Test suite for Day 16: Proboscidea Volcanium

This module contains tests for the Day 16 solution, which optimizes valve
opening sequences in a volcanic tunnel network. The tests verify:

1. Part 1: Maximum pressure with single agent in 30 minutes
2. Part 2: Maximum pressure with two parallel agents in 26 minutes
"""

from aoc.models.tester import TestSolutionUtility


def test_day16_part1() -> None:
    """Test maximizing pressure release with single agent.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=16,
        is_raw=False,
        part_num=1,
        expected=1651,
    )


def test_day16_part2() -> None:
    """Test maximizing pressure release with two parallel agents.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=16,
        is_raw=False,
        part_num=2,
        expected=1707,
    )
