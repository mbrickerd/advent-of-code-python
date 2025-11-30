"""Test suite for Day 11: Monkey in the Middle

This module contains tests for the Day 11 solution, which simulates monkeys
throwing items based on worry levels and divisibility tests. The tests verify:

1. Part 1: Monkey business level after 20 rounds with worry relief
2. Part 2: Monkey business level after 10,000 rounds without worry relief
"""

from aoc.models.tester import TestSolutionUtility


def test_day11_part1() -> None:
    """Test calculating monkey business with 20 rounds and worry relief.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=11,
        is_raw=True,
        part_num=1,
        expected=10605,
    )


def test_day11_part2() -> None:
    """Test calculating monkey business with 10,000 rounds without relief.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=11,
        is_raw=True,
        part_num=2,
        expected=2713310158,
    )
