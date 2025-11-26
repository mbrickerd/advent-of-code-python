"""Test suite for Day 3: Gear Ratios

This module contains tests for the Day 3 solution, which analyzes engine
schematics for valid part numbers and gear ratios. The tests verify:

1. Part 1: Identification and summing of valid part numbers adjacent to symbols
2. Part 2: Calculation of gear ratios from '*' symbols adjacent to exactly
    two numbers
"""

from aoc.models.tester import TestSolutionUtility


def test_day03_part1() -> None:
    """Test summing valid part numbers in the schematic.

    Verifies that the solution correctly finds part numbers adjacent
    to any symbol and sums all valid part numbers.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=3,
        is_raw=False,
        part_num=1,
        expected=4361,
    )


def test_day03_part2() -> None:
    """Test calculation of gear ratios in the schematic.

    Verifies that the solution finds '*' symbols adjacent to exactly two part
    numbers and sums their gear ratios.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=3,
        is_raw=False,
        part_num=2,
        expected=467835,
    )
