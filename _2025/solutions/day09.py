r"""Day 9: Movie Theater

This module provides the solution for Advent of Code 2025 - Day 9

It finds the largest axis-aligned rectangle that can be formed in a tile grid
using red tiles as opposite corners (Part 1), then extends the search to allow
rectangles that include both red and \"green\" tiles (Part 2).

The module contains a Solution class that inherits from SolutionBase and
implements coordinate compression, flood fill, and rectangle validation
to efficiently search the space of candidate rectangles.
"""

from collections import deque
from dataclasses import dataclass
from typing import ClassVar

from aoc.models.base import SolutionBase


@dataclass(frozen=True, slots=True)
class CompressedTiles:
    xs: list[int]
    ys: list[int]
    coords: list[tuple[int, int]]  # (x_idx, y_idx)

    @property
    def width(self) -> int:
        return len(self.xs)

    @property
    def height(self) -> int:
        return len(self.ys)

    @property
    def N(self) -> int:  # noqa: N802
        return len(self.coords)


class Solution(SolutionBase):
    """Find largest valid rectangles in a movie theater tile grid.

    The input is a list of coordinates where tiles are red. Part 1 treats the
    rest of the grid as unconstrained and finds the largest possible rectangle
    using any two red tiles as opposite corners. Part 2 connects the red tiles
    into a loop of red+green tiles and flood-fills the interior to mark all
    green tiles, then searches for the largest rectangle that only contains
    red or green tiles.

    Coordinate compression is used to keep the grid small, and a brute-force
    rectangle search is combined with a grid mask to validate candidate areas.
    """

    DIRECTIONS: ClassVar[tuple[tuple[int, int], ...]] = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def parse_data(self, data: list[str]) -> CompressedTiles:
        tiles = [tuple(map(int, line.split(","))) for line in data if line.strip()]

        xs = sorted({x for x, _ in tiles})
        ys = sorted({y for _, y in tiles})

        x_to_idx = {x: i for i, x in enumerate(xs)}
        y_to_idx = {y: i for i, y in enumerate(ys)}

        coords = [(x_to_idx[x], y_to_idx[y]) for x, y in tiles]
        return CompressedTiles(xs=xs, ys=ys, coords=coords)

    def calculate_area(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

    def construct_grid(self, height: int, width: int, value: int = 0) -> list[list[int]]:
        return [[value] * width for _ in range(height)]

    def construct_bool_grid(
        self, height: int, width: int, *, value: bool = False
    ) -> list[list[bool]]:
        return [[value] * width for _ in range(height)]

    def mark_red_tiles(self, grid: list[list[int]], coords: list[tuple[int, int]]) -> None:
        for x_idx, y_idx in coords:
            grid[y_idx][x_idx] = 1

    def mark_green_boundary(self, grid: list[list[int]], coords: list[tuple[int, int]]) -> None:
        N = len(coords)  # noqa: N806
        for i in range(N):
            x1, y1 = coords[i]
            x2, y2 = coords[(i + 1) % N]

            if x1 == x2:
                y_min, y_max = sorted((y1, y2))
                for y in range(y_min, y_max + 1):
                    if grid[y][x1] == 0:
                        grid[y][x1] = 2

            elif y1 == y2:
                x_min, x_max = sorted((x1, x2))
                for x in range(x_min, x_max + 1):
                    if grid[y1][x] == 0:
                        grid[y1][x] = 2

            else:
                err_msg = "Non axis-aligned segment in input"
                raise ValueError(err_msg)

    def seed_if_outside_empty(
        self,
        grid: list[list[int]],
        outside: list[list[bool]],
        queue: deque[tuple[int, int]],
        x: int,
        y: int,
    ) -> None:
        if grid[y][x] == 0 and not outside[y][x]:
            outside[y][x] = True
            queue.append((x, y))

    def flood_fill_outside_zeros(self, grid: list[list[int]]) -> list[list[bool]]:
        height = len(grid)
        width = len(grid[0])

        outside = self.construct_bool_grid(height, width, value=False)
        queue: deque[tuple[int, int]] = deque()

        for x in range(width):
            self.seed_if_outside_empty(grid, outside, queue, x, 0)
            self.seed_if_outside_empty(grid, outside, queue, x, height - 1)

        for y in range(height):
            self.seed_if_outside_empty(grid, outside, queue, 0, y)
            self.seed_if_outside_empty(grid, outside, queue, width - 1, y)

        while queue:
            x, y = queue.popleft()
            for dx, dy in self.DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (
                    nx in range(width)
                    and ny in range(height)
                    and not outside[ny][nx]
                    and grid[ny][nx] == 0
                ):
                    outside[ny][nx] = True
                    queue.append((nx, ny))

        return outside

    def fill_interior_as_green(self, grid: list[list[int]], outside: list[list[bool]]) -> None:
        height = len(grid)
        width = len(grid[0])

        for y in range(height):
            for x in range(width):
                if grid[y][x] == 0 and not outside[y][x]:
                    grid[y][x] = 2

    def rectangle_all_non_zero(
        self,
        grid: list[list[int]],
        x_left: int,
        x_right: int,
        y_top: int,
        y_bottom: int,
    ) -> bool:
        for y in range(y_top, y_bottom + 1):
            row = grid[y]
            for x in range(x_left, x_right + 1):
                if row[x] == 0:
                    return False

        return True

    def part1(self, data: list[str]) -> int:
        r"""Find largest rectangle area using two red tiles as opposite corners.

        For every pair of red tiles that differ in both x and y, this method
        computes the area of the axis-aligned rectangle they define and tracks
        the maximum. The actual grid size does not matter due to the use of
        red tile coordinates only.

        Args:
            data: List of \"X,Y\" strings representing red tile positions

        Returns
        -------
            int: Largest rectangle area using two red tiles as opposite corners
        """
        tiles = self.parse_data(data)

        if tiles.N < 2:
            return 0

        max_area = 0
        N = tiles.N  # noqa: N806

        for i in range(N):
            x1_idx, y1_idx = tiles.coords[i]
            for j in range(i + 1, N):
                x2_idx, y2_idx = tiles.coords[j]
                if x1_idx == x2_idx or y1_idx == y2_idx:
                    continue

                x1, y1 = tiles.xs[x1_idx], tiles.ys[y1_idx]
                x2, y2 = tiles.xs[x2_idx], tiles.ys[y2_idx]
                area = self.calculate_area(x1, y1, x2, y2)

                if area > max_area:
                    max_area = area

        return max_area

    def part2(self, data: list[str]) -> int:
        r"""Find largest rectangle area using only red and green tiles.

        First, the red tiles are connected in input order with axis-aligned
        segments forming a loop; these segments become green tiles. Then, a
        flood fill from the outside marks all empty tiles reachable from the
        boundary as \"outside\". Any remaining empty tiles inside the loop are
        also marked green. Finally, the method checks all red-opposite-corner
        rectangles and keeps the largest whose interior contains only red or
        green tiles (no empty tiles).

        Args:
            data: List of \"X,Y\" strings representing red tile positions in loop order

        Returns
        -------
            int: Largest rectangle area that uses red tiles as opposite corners
                and includes only red or green tiles inside
        """
        tiles = self.parse_data(data)

        if tiles.N < 2:
            return 0

        grid = self.construct_grid(tiles.height, tiles.width, 0)
        self.mark_red_tiles(grid, tiles.coords)
        self.mark_green_boundary(grid, tiles.coords)

        outside = self.flood_fill_outside_zeros(grid)
        self.fill_interior_as_green(grid, outside)

        max_area = 0
        N = tiles.N  # noqa: N806

        for i in range(N):
            x1_idx, y1_idx = tiles.coords[i]
            for j in range(i + 1, N):
                x2_idx, y2_idx = tiles.coords[j]
                if x1_idx == x2_idx or y1_idx == y2_idx:
                    continue

                x_left, x_right = sorted((x1_idx, x2_idx))
                y_top, y_bottom = sorted((y1_idx, y2_idx))

                if not self.rectangle_all_non_zero(grid, x_left, x_right, y_top, y_bottom):
                    continue

                x1, y1 = tiles.xs[x1_idx], tiles.ys[y1_idx]
                x2, y2 = tiles.xs[x2_idx], tiles.ys[y2_idx]
                area = self.calculate_area(x1, y1, x2, y2)

                if area > max_area:
                    max_area = area

        return max_area
