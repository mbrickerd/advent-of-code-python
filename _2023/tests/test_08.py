"""Test suite for Day 8: Haunted Wasteland

This module contains tests for the Day 8 solution, which navigates a network of nodes using
left/right instructions to reach destination nodes. The tests verify:

1. Part 1: Finding the number of steps from 'AAA' to 'ZZZ' following instructions
2. Part 2: Finding steps for multiple simultaneous paths using LCM of cycle lengths
"""

from aoc.models.tester import TestSolutionUtility


def test_day08_part1() -> None:
    """Test navigating from 'AAA' to 'ZZZ' through the network.

    Verifies that the solution correctly follows left/right instructions through the node network
    and counts the number of steps required to reach the destination node 'ZZZ'.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=8,
        is_raw=False,
        part_num=1,
        expected=6,
    )


def test_day08_part2() -> None:
    """Test simultaneous navigation for multiple starting positions.

    Verifies that the solution finds cycle lengths for all paths starting at nodes ending in 'A'
    and calculates the LCM to determine when all paths reach nodes ending in 'Z' simultaneously.
    """
    TestSolutionUtility.run_test(
        year=2023,
        day=8,
        is_raw=False,
        part_num=2,
        expected=6,
    )
