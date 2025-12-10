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

from aoc.models.base import SolutionBase


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
        tiles = [tuple(map(int, line.split(","))) for line in data]

        if len(tiles) < 2:
            return 0

        # Coordinate compression (space distortion)
        xs = sorted({x for x, _ in tiles})
        ys = sorted({y for _, y in tiles})

        x_to_idx = {x: i for i, x in enumerate(xs)}
        y_to_idx = {y: i for i, y in enumerate(ys)}

        compressed_tiles: list[tuple[int, int]] = [(x_to_idx[x], y_to_idx[y]) for x, y in tiles]

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
        tiles = [tuple(map(int, line.split(","))) for line in data if line.strip()]

        if len(tiles) < 2:
            return 0

        # Coordinate compression
        xs = sorted({x for x, _ in tiles})
        ys = sorted({y for _, y in tiles})
        x_to_idx = {x: i for i, x in enumerate(xs)}
        y_to_idx = {y: i for i, y in enumerate(ys)}
        compressed = [(x_to_idx[x], y_to_idx[y]) for x, y in tiles]

        w, h = len(xs), len(ys)
        # 0 = empty, 1 = red, 2 = green
        grid = [[0] * w for _ in range(h)]

        # Mark red tiles
        for cx, cy in compressed:
            grid[cy][cx] = 1

        # Draw green boundary segments between consecutive reds (wrap around)
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
                err_msg = "Non axis-aligned segment in input"
                raise ValueError(err_msg)

        # Flood-fill outside empty cells
        outside = [[False] * w for _ in range(h)]
        q: deque[tuple[int, int]] = deque()

        # Seed flood fill from outer boundary
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

        # Search for largest valid rectangle (only red/green inside)
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
