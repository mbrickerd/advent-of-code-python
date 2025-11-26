from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    directions: ClassVar[dict[str, list[tuple[int, int]]]] = {
        "|": [(0, -1), (0, 1)],
        "-": [(1, 0), (-1, 0)],
        "L": [(0, -1), (1, 0)],
        "J": [(0, -1), (-1, 0)],
        "7": [(0, 1), (-1, 0)],
        "F": [(0, 1), (1, 0)],
    }

    def find_start(self, grid: list[list[str]]) -> tuple[int, int]:
        return next(
            (i, j) for i, row in enumerate(grid) for j, char in enumerate(row) if char == "S"
        )

    def get_valid_neighbors(
        self, grid: list[list[int]], x: int, y: int, target_height: int
    ) -> list[tuple[int, int]]:
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < len(grid)
                and 0 <= new_y < len(grid[0])
                and grid[new_x][new_y] == target_height
            ):
                neighbors.append((new_x, new_y))

        return neighbors

    def part1(self, data: list[str]) -> int:
        row, col = self.find_start(data)
        return

    def part2(self, data: list[str]) -> int:
        return
