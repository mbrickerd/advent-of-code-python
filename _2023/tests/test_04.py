"""Test suite for Day 4: Scratchcards

This module contains tests for the Day 4 solution, which processes scratchcards by matching
winning and owned numbers to score points and track card copies. The tests verify:

1. Part 1: Calculation of total points based on matching numbers
2. Part 2: Calculation of the total number of scratchcards won, including through copies
"""

from aoc.models.tester import TestSolutionUtility


def test_day04_part1() -> None:
    """Test calculating total points from scratchcards.

    Verifies that the solution sums points for all cards, where points double for each additional
    matching number after the first, and cards with no matches score zero.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=4,
        is_raw=False,
        part_num=1,
        expected=13,
    )


def test_day04_part2() -> None:
    """Test calculating total scratchcards won through copying.

    Verifies that the solution correctly computes the total number of scratchcards won by counting
    originals and recursively winning cards through copies from matching numbers.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=4,
        is_raw=False,
        part_num=2,
        expected=30,
    )
