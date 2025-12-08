"""Test suite for Day 8: Playground

This module contains tests for the Day 8 solution, which connects junction
boxes in 3D space by shortest distance to form electrical circuits. The tests
verify:

1. Part 1: Product of sizes of three largest circuits after 1000 shortest connections
2. Part 2: X-coordinate product of final pair forming single circuit
"""

from aoc.models.tester import TestSolutionUtility


def test_day08_part1() -> None:
    """Test product of three largest circuits after fixed connections.

    This test runs the solution for Part 1 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=8,
        is_raw=False,
        part_num=1,
        expected=40,
    )


def test_day08_part2() -> None:
    """Test X-coordinate product of final merge into single circuit.

    This test runs the solution for Part 2 of the puzzle against the
    provided test input and compares the result with the expected output.
    """
    TestSolutionUtility.run_test(
        year=2025,
        day=8,
        is_raw=False,
        part_num=2,
        expected=25272,
    )
