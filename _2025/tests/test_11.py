"""Test suite for Day 11: Reactor

This module contains tests for the Day 11 solution, which counts
paths through the reactor's device graph. The tests verify:

1. Part 1: Number of distinct paths from 'you' to 'out'.
2. Part 2: Number of paths from 'svr' to 'out' that also visit
   both 'dac' and 'fft'.
"""

from aoc.models.tester import TestSolutionUtility


def test_day11_part1() -> None:
    """Test counting all paths from 'you' to 'out'.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=11,
        is_raw=False,
        part_num=1,
        expected=5,
    )


def test_day11_part2() -> None:
    """Test counting constrained paths from 'svr' to 'out'.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=11,
        is_raw=False,
        part_num=2,
        expected=2,
    )
