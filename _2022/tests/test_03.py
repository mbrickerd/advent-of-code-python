"""Test suite for Day 3: Rucksack Reorganization

This module contains tests for the Day 3 solution, which calculates priority sums
for misplaced items in rucksack compartments. The tests verify:

1. Part 1: Finding items appearing in both compartments of each rucksack
2. Part 2: Finding badge items common to groups of three rucksacks
"""

from aoc.models.tester import TestSolutionUtility


def test_day03_part1() -> None:
    """Test calculating priority sum for items in both compartments.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=3,
        is_raw=False,
        part_num=1,
        expected=157,
    )


def test_day03_part2() -> None:
    """Test calculating priority sum for badge items across elf groups.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=3,
        is_raw=False,
        part_num=2,
        expected=70,
    )
