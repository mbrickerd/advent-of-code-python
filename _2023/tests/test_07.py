"""Test suite for Day 7: Camel Cards

This module contains tests for the Day 7 solution, which ranks and scores poker-like hands to
calculate total winnings. The tests verify:

1. Part 1: Ranking hands using standard poker hand types and card values
2. Part 2: Ranking hands with 'J' cards acting as jokers for strongest hand formation
"""

from aoc.models.tester import TestSolutionUtility


def test_day07_part1() -> None:
    """Test calculating total winnings using standard poker rankings.

    Verifies that the solution correctly ranks hands by type and card values, then calculates
    total winnings as the sum of rank times bid for each hand.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=7,
        is_raw=False,
        part_num=1,
        expected=6440,
    )


def test_day07_part2() -> None:
    """Test calculating total winnings with joker rules enabled.

    Verifies that the solution treats 'J' cards as jokers that strengthen hand types while
    being weakest for tiebreaking, then calculates total winnings.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=7,
        is_raw=False,
        part_num=2,
        expected=5905,
    )
