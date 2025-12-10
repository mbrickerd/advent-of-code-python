"""Boilerplate solution template for Advent of Code daily challenges.

This module provides a template class for solving Advent of Code puzzle problems.
It includes a base structure with two method stubs (part1 and part2) that can be
implemented for specific day's challenges.

The template follows the SolutionBase pattern used across the Advent of Code solutions,
allowing for consistent handling of input parsing and solution execution.
"""

from collections import deque

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution template for Advent of Code daily puzzle.

    This class provides a standardized structure for implementing solutions to
    daily Advent of Code challenges. It inherits from SolutionBase and includes
    method stubs for part1 and part2 of the puzzle.

    Subclasses should override these methods with specific implementation logic
    for parsing input and solving the puzzle requirements.
    """

    def part1(self, data: list[str]) -> int:
        """Solve the first part of the daily puzzle.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Solution for part 1 of the puzzle
        """
        tiles = [tuple(map(int, line.split(","))) for line in data]

        if len(tiles) < 2:
            return 0

        # Coordinate compression ("space distortion")
        xs = sorted({x for x, _ in tiles})
        ys = sorted({y for _, y in tiles})

        x_to_idx = {x: i for i, x in enumerate(xs)}
        y_to_idx = {y: i for i, y in enumerate(ys)}

        # Compressed positions of red tiles
        compressed_tiles: list[tuple[int, int]] = [(x_to_idx[x], y_to_idx[y]) for x, y in tiles]

        # Group tiles by compressed row/column if you want small pruning later
        # but the brute-force over all pairs is already fine for AoC sizes.
        max_area = 0
        n = len(compressed_tiles)

        for i in range(n):
            x1_idx, y1_idx = compressed_tiles[i]
            for j in range(i + 1, n):
                x2_idx, y2_idx = compressed_tiles[j]

                # Opposite corners must differ in both x and y to form area
                if x1_idx == x2_idx or y1_idx == y2_idx:
                    continue

                # Get original coordinates
                x1 = xs[x1_idx]
                y1 = ys[y1_idx]
                x2 = xs[x2_idx]
                y2 = ys[y2_idx]

                width = abs(x2 - x1) + 1
                height = abs(y2 - y1) + 1
                area = width * height

                if area > max_area:
                    max_area = area

        return max_area

    def part2(self, data: list[str]) -> int:
        """Solve the second part of the daily puzzle.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Solution for part 2 of the puzzle
        """
        tiles = [tuple(map(int, line.split(","))) for line in data if line.strip()]

        if len(tiles) < 2:
            return 0

        xs = sorted({x for x, _ in tiles})
        ys = sorted({y for _, y in tiles})
        x_to_idx = {x: i for i, x in enumerate(xs)}
        y_to_idx = {y: i for i, y in tiles}
        y_to_idx = {y: i for i, y in enumerate(ys)}
        compressed = [(x_to_idx[x], y_to_idx[y]) for x, y in tiles]

        w, h = len(xs), len(ys)
        grid = [[0] * w for _ in range(h)]  # 0 = empty, 1 = red, 2 = green

        # Mark red tiles
        for cx, cy in compressed:
            grid[cy][cx] = 1

        # Draw green boundary segments between consecutive reds (wrap)
        n = len(compressed)
        for i in range(n):
            x1, y1 = compressed[i]
            x2, y2 = compressed[(i + 1) % n]
            if x1 == x2:
                ys_min, ys_max = sorted((y1, y2))
                for y in range(ys_min, ys_max + 1):
                    if grid[y][x1] == 0:
                        grid[y][x1] = 2
            elif y1 == y2:
                xs_min, xs_max = sorted((x1, x2))
                for x in range(xs_min, xs_max + 1):
                    if grid[y1][x] == 0:
                        grid[y1][x] = 2
            else:
                raise ValueError("Non axis-aligned segment in input")

        # Flood-fill outside empty cells
        outside = [[False] * w for _ in range(h)]
        q: deque[tuple[int, int]] = deque()

        for x in range(w):
            if grid[0][x] == 0:
                outside[0][x] = True
                q.append((x, 0))
            if grid[h - 1][x] == 0:
                outside[h - 1][x] = True
                q.append((x, h - 1))
        for y in range(h):
            if grid[y][0] == 0:
                outside[y][0] = True
                q.append((0, y))
            if grid[y][w - 1] == 0:
                outside[y][w - 1] = True
                q.append((w - 1, y))

        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not outside[ny][nx] and grid[ny][nx] == 0:
                    outside[ny][nx] = True
                    q.append((nx, ny))

        # Interior empty cells become green
        for y in range(h):
            for x in range(w):
                if grid[y][x] == 0 and not outside[y][x]:
                    grid[y][x] = 2

        max_area = 0
        n = len(compressed)

        for i in range(n):
            x1i, y1i = compressed[i]
            for j in range(i + 1, n):
                x2i, y2i = compressed[j]
                if x1i == x2i or y1i == y2i:
                    continue

                xl, xr = sorted((x1i, x2i))
                yt, yb = sorted((y1i, y2i))

                # Check rectangle only contains red/green
                ok = True
                for yy in range(yt, yb + 1):
                    row = grid[yy]
                    for xx in range(xl, xr + 1):
                        if row[xx] == 0:
                            ok = False
                            break
                    if not ok:
                        break

                if not ok:
                    continue

                x1, y1 = xs[x1i], ys[y1i]
                x2, y2 = xs[x2i], ys[y2i]
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                if area > max_area:
                    max_area = area

        return max_area
