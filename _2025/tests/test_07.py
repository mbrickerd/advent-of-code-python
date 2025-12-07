"""Test suite for Day 7: Laser Lab

This module contains tests for the Day 7 solution, which simulates beam
propagation and splitting in a laser lab grid. The tests verify:

1. Part 1: Counting how many splitters are activated by the beam front
2. Part 2: Counting how many distinct beam paths reach the bottom row
"""

from aoc.models.tester import TestSolutionUtility


def test_day07_part1() -> None:
    """Test counting activated splitters along the beam front.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=7,
        is_raw=False,
        part_num=1,
        expected=21,
    )


def test_day07_part2() -> None:
    """Test counting distinct beam paths reaching the bottom row.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=7,
        is_raw=False,
        part_num=2,
        expected=40,
    )
