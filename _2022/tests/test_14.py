"""Test suite for Day 14: Regolith Reservoir

This module contains tests for the Day 14 solution, which simulates falling sand
in a cave system with rock formations. The tests verify:

1. Part 1: Counting sand units that settle before falling into abyss
2. Part 2: Counting sand units that settle before blocking the source (with floor)
"""

from aoc.models.tester import TestSolutionUtility


def test_day14_part1() -> None:
    """Test counting sand units before falling into abyss.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=14,
        is_raw=False,
        part_num=1,
        expected=24,
    )


def test_day14_part2() -> None:
    """Test counting sand units before blocking source with floor.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2022,
        day=14,
        is_raw=False,
        part_num=2,
        expected=93,
    )
