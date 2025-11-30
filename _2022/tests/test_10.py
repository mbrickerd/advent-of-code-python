"""Test suite for Day 10: Cathode-Ray Tube

This module contains tests for the Day 10 solution, which simulates a simple
CPU executing instructions and calculating signal strengths. The tests verify:

1. Part 1: Sum of signal strengths at specific cycle checkpoints
"""

from aoc.models.tester import TestSolutionUtility


def test_day10_part1() -> None:
    """Test calculating sum of signal strengths at checkpoint cycles.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=10,
        is_raw=False,
        part_num=1,
        expected=13140,
    )
