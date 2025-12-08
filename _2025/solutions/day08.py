"""Day 8: Playground

This module provides the solution for Advent of Code 2025 - Day 8.

It simulates connecting electrical junction boxes in 3D space by distance
to form circuits, using union-find to track component sizes as connections
are added in order of increasing Euclidean distance.

The module contains a DSU (Disjoint Set Union) dataclass for efficient
circuit merging and a Solution class that inherits from SolutionBase.
"""

from dataclasses import dataclass
import math
from typing import Self

from aoc.models.base import SolutionBase


@dataclass
class DSU:
    """Disjoint set union structure for tracking junction box circuits.

    Maintains parent and component size arrays to efficiently perform
    union-find operations with path compression and union by size for
    optimal circuit merging.
    """

    parent: list[int]
    size: list[int]

    @classmethod
    def with_n(cls, n: int) -> Self:
        """Create DSU with n singleton junction box circuits.

        Args:
            n: Number of junction boxes

        Returns
        -------
            DSU: New instance with each box in its own circuit
        """
        return cls(parent=list(range(n)), size=[1] * n)

    def find(self, x: int) -> int:
        """Find root representative of junction box x's circuit with path compression."""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]

        return x

    def union(self, a: int, b: int) -> bool:
        """Merge circuits containing junction boxes a and b.

        Args:
            a: First junction box index
            b: Second junction box index

        Returns
        -------
            bool: True if circuits were merged, False if already connected
        """
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


class Solution(SolutionBase):
    """Connect junction boxes by shortest distance to form electrical circuits.

    This solution connects junction boxes in 3D space using strings of lights,
    always connecting the closest unconnected pair. Uses Kruskal's algorithm
    approach with Euclidean distance sorting and DSU for cycle detection.

    Part 1: After 1000 shortest connections (10 for examples), multiply sizes
    of the three largest circuits. Part 2: Connect until single circuit, return
    product of X-coordinates of final merge pair.
    """

    def build_edges(self, boxes: list[list[int]]) -> list[tuple[float, int, int]]:
        """Compute all pairwise Euclidean distances between junction boxes.

        Args:
            boxes: List of 3D coordinates [x, y, z] for each junction box

        Returns
        -------
            list[tuple[float, int, int]]: Sorted edges (distance, box_i, box_j)
        """
        N = len(boxes)  # noqa: N806
        edges: list[tuple[float, int, int]] = []
        for i in range(N):
            for j in range(i + 1, N):
                d = math.dist(boxes[i], boxes[j])
                edges.append((d, i, j))

        edges.sort(key=lambda e: e[0])
        return edges

    def find_largest_circuits(
        self,
        boxes: list[list[int]],
        pairs_to_process: int,
    ) -> int:
        """Process shortest connections and return product of 3 largest circuits.

        Args:
            boxes: List of 3D junction box coordinates
            pairs_to_process: Number of shortest connections to make (1000 for real input)

        Returns
        -------
            int: Product of sizes of three largest circuits after specified connections
        """
        N = len(boxes)  # noqa: N806
        edges = self.build_edges(boxes)
        dsu = DSU.with_n(N)

        for processed_pairs, (_, u, v) in enumerate(edges, start=1):
            dsu.union(u, v)
            if processed_pairs == pairs_to_process:
                break

        comp_sizes: dict[int, int] = {}
        for i in range(N):
            root = dsu.find(i)
            comp_sizes[root] = comp_sizes.get(root, 0) + 1

        sizes = sorted(comp_sizes.values(), reverse=True)
        a, b, c = sizes[0], sizes[1], sizes[2]
        return a * b * c

    def last_merge_x_product(self, boxes: list[list[int]]) -> int:
        """Return X-coordinate product of final pair forming single circuit.

        Args:
            boxes: List of 3D junction box coordinates

        Returns
        -------
            int: Product of X coordinates of last two boxes connected

        Raises
        ------
            ValueError: If boxes don't form a single connected circuit
        """
        N = len(boxes)  # noqa: N806
        edges = self.build_edges(boxes)
        dsu = DSU.with_n(N)

        components = N
        last_u: int | None = None
        last_v: int | None = None

        for _, u, v in edges:
            if dsu.union(u, v):
                components -= 1
                last_u, last_v = u, v
                if components == 1:
                    x1, x2 = boxes[last_u][0], boxes[last_v][0]
                    return x1 * x2

        err_msg = "Did not reach a single circuit"
        raise ValueError(err_msg)

    def part1(self, data: list[str]) -> int:
        """Multiply sizes of 3 largest circuits after 1000 shortest connections.

        Uses small input (10 connections) for examples, full input (1000 connections).

        Args:
            data: List of 'X,Y,Z' coordinate strings

        Returns
        -------
            int: Product of sizes of three largest circuits after cutoff
        """
        boxes = [list(map(int, line.split(","))) for line in data]
        pairs = 10 if len(boxes) <= 20 else 1000
        return self.find_largest_circuits(boxes, pairs_to_process=pairs)

    def part2(self, data: list[str]) -> int:
        """X-coordinate product of final pair connecting all junction boxes.

        Continues connecting closest pairs until single circuit formed.

        Args:
            data: List of 'X,Y,Z' coordinate strings

        Returns
        -------
            int: Product of X coordinates from final successful connection
        """
        boxes = [list(map(int, line.split(","))) for line in data]
        return self.last_merge_x_product(boxes)
