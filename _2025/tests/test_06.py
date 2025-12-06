"""Day 6: Trash Compactor

This module contains tests for the Day 6 solution, which evaluates cephalopod
math worksheets laid out in a compacted, column-wise format. The tests verify:

1. Part 1: Evaluating each vertically aligned problem using the given operator
2. Part 2: Evaluating rotated worksheet problems with column-based parsing
"""

from aoc.models.tester import TestSolutionUtility


def test_day06_part1() -> None:
    """Test evaluating compacted worksheet problems as given.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=6,
        is_raw=False,
        part_num=1,
        expected=4277556,
    )


def test_day06_part2() -> None:
    """Test evaluating rotated worksheet problems parsed column-wise.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=6,
        is_raw=True,
        part_num=2,
        expected=3263827,
    )
