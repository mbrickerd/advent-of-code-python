"""Test suite for Day 2: Rock Paper Scissors

This module contains tests for the Day 2 solution, which calculates rock-paper-scissors
game scores based on different strategy interpretations. The tests verify:

1. Part 1: Calculating total score when second column represents your move choice
2. Part 2: Calculating total score when second column represents desired outcome
"""

from aoc.models.tester import TestSolutionUtility


def test_day02_part1() -> None:
    """Test calculating score with second column as move choice.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=2,
        is_raw=False,
        part_num=1,
        expected=15,
    )


def test_day02_part2() -> None:
    """Test calculating score with second column as desired outcome.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=2,
        is_raw=False,
        part_num=2,
        expected=12,
    )
