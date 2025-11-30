"""Test suite for Day 13: Distress Signal

This module contains tests for the Day 13 solution, which compares and sorts
nested list packets to decode a distress signal. The tests verify:

1. Part 1: Finding sum of indices for packet pairs in correct order
2. Part 2: Calculating decoder key by sorting packets with dividers
"""

from aoc.models.tester import TestSolutionUtility


def test_day13_part1() -> None:
    """Test finding sum of correctly ordered packet pair indices.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=13,
        is_raw=True,
        part_num=1,
        expected=13,
    )


def test_day13_part2() -> None:
    """Test calculating decoder key from sorted packets.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=13,
        is_raw=True,
        part_num=2,
        expected=140,
    )
