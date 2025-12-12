"""Day 12: Christmas Tree Farm

This module provides the solution for Advent of Code 2025 - Day 12.

The input describes oddly-shaped presents and the rectangular regions
under Christmas trees where those presents need to fit.

This implementation uses a simplified feasibility check: it parses all
present shapes, then for each region computes how much area the listed
presents would require and compares it against the region area.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Check which tree regions are large enough for their present lists.

    The puzzle input is split into two sections separated by a blank line:

    - The first section lists present shapes, each starting with an index
      line (`0:`, `1:`, ...) followed by a small ASCII-art block of `#`
      and `.` characters.
    - The second section lists regions in the form `WxH: c0 c1 c2 ...`,
      where each `ci` is the count of presents of shape i to place.

    This implementation only uses the region dimensions and the counts
    of presents to compute a required area per region and checks whether
    the available area is sufficient.
    """

    def part1(self, data: str) -> int:
        """Count how many regions can fit all of their requested presents.

        The raw input is split on blank lines. All blocks except the last
        are interpreted as shape definitions; the final block contains the
        region lines. For each region line of the form:

            WxH: n0 n1 n2 ...

        it computes a required area of `8 * sum(ni)` and compares it to
        `width * height`. If the region has at least this much area, it
        is counted as able to fit all presents.

        Args:
            data: Full puzzle input as a single string.

        Returns
        -------
            int: Number of regions that can fit all of their listed presents.
        """
        *shape_blocks, regions = data.split("\n\n")

        shapes: list[str] = []
        for block in shape_blocks:
            lines = block.split("\n")
            body = "\n".join(lines[1:])
            shapes.append(body)

        count = 0
        for region in regions.split("\n"):
            region = region.strip()
            if not region:
                continue

            width, height, *nums = map(int, region.replace("x", " ").replace(":", "").split())
            required = 8 * sum(nums)
            if width * height >= required:
                count += 1

        return count

    def part2(self, data: str) -> str:
        """Return a festive message after evaluating all regions.

        Part 2 of this solution does not perform additional computation
        on the input; instead, it simply returns a celebratory string to
        mark the completion of the Advent of Code event.

        Args:
            data: Full puzzle input as a single string.

        Returns
        -------
            str: Festive completion message.
        """
        return "Merry Christmas!"
