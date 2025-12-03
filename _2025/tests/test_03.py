"""Test suite for Day 3: Maximum Joltage Extraction

This module contains tests for the Day 3 solution, which extracts maximum
numeric values from digit sequences while preserving order. The tests verify:

1. Part 1: Sum of maximum 2-digit values from all power bank readings
2. Part 2: Sum of maximum 12-digit values from all power bank readings
"""
from aoc.models.tester import TestSolutionUtility

def test_day03_part1() -> None:
    """Test extracting and summing maximum 2-digit joltage values.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=3,
        is_raw=False,
        part_num=1,
        expected=357,
    )

def test_day03_part2() -> None:
    """Test extracting and summing maximum 12-digit joltage values.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=3,
        is_raw=False,
        part_num=2,
        expected=3121910778619,
    )
