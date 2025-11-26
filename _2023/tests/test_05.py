"""Test suite for Day 5: If You Give A Seed A Fertilizer

This module contains tests for the Day 5 solution, which maps seeds through multiple conversion
stages to find the lowest location number. The tests verify:

1. Part 1: Processing individual seed numbers through all mapping stages
2. Part 2: Processing seed number ranges to find the lowest location
"""

from aoc.models.tester import TestSolutionUtility


def test_day05_part1() -> None:
    """Test finding the lowest location for individual seed numbers.

    Verifies that the solution correctly maps each seed through all conversion stages (soil,
    fertilizer, water, light, temperature, humidity, location) and finds the minimum location.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=5,
        is_raw=False,
        part_num=1,
        expected=35,
    )


def test_day05_part2() -> None:
    """Test finding the lowest location for seed number ranges.

    Verifies that the solution correctly interprets seed numbers as range pairs (start, length)
    and finds the minimum location across all seeds in all ranges.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=5,
        is_raw=False,
        part_num=2,
        expected=46,
    )
