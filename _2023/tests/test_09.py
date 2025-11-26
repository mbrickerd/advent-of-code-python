"""Test suite for Day 9: Mirage Maintenance

This module contains tests for the Day 9 solution, which extrapolates sequences by computing
successive differences until reaching all zeros. The tests verify:

1. Part 1: Extrapolating the next value forward for each sequence
2. Part 2: Extrapolating the previous value backward for each sequence
"""

from aoc.models.tester import TestSolutionUtility


def test_day09_part1() -> None:
    """Test forward extrapolation of sequence values.

    Verifies that the solution computes difference rows until all zeros, then extrapolates the
    next value by summing the last values of each row.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=9,
        is_raw=False,
        part_num=1,
        expected=114,
    )


def test_day09_part2() -> None:
    """Test backward extrapolation of sequence values.

    Verifies that the solution extrapolates the previous value by working backwards through
    difference rows and prepending calculated values to find the first element.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=9,
        is_raw=False,
        part_num=2,
        expected=2,
    )
