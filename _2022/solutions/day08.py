"""Day 8: Treetop Tree House

This module provides the solution for Advent of Code 2022 - Day 8.

It handles analyzing tree visibility in a grid based on height comparisons
and calculating scenic scores for potential tree house locations.

The module contains a Solution class that inherits from SolutionBase and implements
methods to count visible trees and determine optimal viewing locations.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyze tree grid for visibility and scenic score calculations.

    This solution processes a grid of tree heights to determine visibility
    and viewing distances. Part 1 counts trees visible from outside the grid
    (where all trees between it and an edge are shorter). Part 2 calculates
    scenic scores based on viewing distances in all four directions.

    The solution uses directional scanning to check visibility conditions
    and compute viewing distances for tree house placement optimization.
    """

    def part1(self, data: list[str]) -> int:
        """Count trees visible from outside the grid.

        A tree is visible if all trees between it and an edge (in at least one
        direction: up, down, left, or right) are shorter. All edge trees are
        automatically visible.

        Args:
            data: List of strings where each string is a row of single-digit
                tree heights (0-9)

        Returns
        -------
            int: Total number of trees visible from outside the grid when
                looking directly along any row or column
        """
        grid = [[int(x) for x in list(row)] for row in data]
        rows, cols = len(grid), len(grid[0])

        score = 2 * rows + 2 * cols - 4

        for i in range(rows):
            for j in range(cols):
                # Inner trees
                if i > 0 and j > 0 and i < rows - 1 and j < cols - 1:
                    current_height = grid[i][j]

                    if (
                        # Up direction
                        all(grid[r][j] < current_height for r in range(i - 1, -1, -1))
                        # Down direction
                        or all(grid[r][j] < current_height for r in range(i + 1, len(grid)))
                        # Left direction
                        or all(grid[i][c] < current_height for c in range(j - 1, -1, -1))
                        # Right direction
                        or all(grid[i][c] < current_height for c in range(j + 1, len(grid[0])))
                    ):
                        score += 1

        return score

    def part2(self, data: list[str]) -> int:
        """Find highest scenic score possible for any tree.

        Scenic score is calculated by multiplying viewing distances in all four
        directions. Viewing distance is how many trees can be seen before the
        view is blocked by a tree of equal or greater height (or reaching edge).

        Args:
            data: List of strings where each string is a row of single-digit
                tree heights (0-9)

        Returns
        -------
            int: Maximum scenic score among all trees in the grid (product of
                viewing distances in up, down, left, and right directions)
        """
        grid = [[int(x) for x in list(row)] for row in data]
        rows, cols = len(grid), len(grid[0])
        scores: list[int] = []

        for i in range(rows):
            for j in range(cols):
                # Inner trees
                if i > 0 and j > 0 and i < rows - 1 and j < cols - 1:
                    current_height = grid[i][j]
                    up_score, down_score, left_score, right_score = 0, 0, 0, 0

                    # Up direction
                    r = i - 1
                    while r >= 0:
                        up_score += 1
                        if grid[r][j] >= current_height:
                            break

                        r -= 1

                    # Down direction
                    r = i + 1
                    while r < rows:
                        down_score += 1
                        if grid[r][j] >= current_height:
                            break

                        r += 1

                    # Left direction
                    c = j - 1
                    while c >= 0:
                        left_score += 1
                        if grid[i][c] >= current_height:
                            break

                        c -= 1

                    # Right direction
                    c = j + 1
                    while c < cols:
                        right_score += 1
                        if grid[i][c] >= current_height:
                            break

                        c += 1

                    scores.append(up_score * down_score * left_score * right_score)

        return max(scores)
