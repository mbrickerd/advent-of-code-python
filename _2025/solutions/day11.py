"""Day 11: Reactor

This module provides the solution for Advent of Code 2025 - Day 11.

It models a directed graph of devices and counts how many distinct
paths exist between given endpoints, with optional requirements to
visit specific devices along the way.

The module contains a Solution class that inherits from SolutionBase
and implements graph construction plus memoized depth-first search
for efficient path counting.
"""

import re
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Count device paths through the reactor wiring graph.

    Each input line describes a device and its outgoing connections in
    the form 'name: out1 out2 ...'. Data flows only along these edges.

    Part 1 counts all distinct paths from 'you' (the device next to you)
    to 'out' (the main reactor output). Part 2 counts only those paths
    from 'svr' (the server rack) to 'out' that also visit both 'dac'
    and 'fft' at least once, in any order.
    """

    REGEX: ClassVar[re.Pattern[str]] = re.compile(r"(\w{3})")

    def construct_graph(self, data: list[str]) -> dict[str, list[str]]:
        """Parse device connection lines into an adjacency list.

        Each non-empty line starts with a three-letter device name
        followed by zero or more three-letter device names it connects
        to via its outputs.

        Args:
            data: List of strings describing device connections

        Returns
        -------
            dict[str, list[str]]: Mapping from device name to list of
            device names reachable via its outputs.
        """
        graph: dict[str, list[str]] = {}
        for line in data:
            tokens = re.findall(self.REGEX, line)
            if not tokens:
                continue

            node, outputs = tokens[0], tokens[1:]
            graph[node] = outputs

        return graph

    def dfs(
        self,
        graph: dict[str, list[str]],
        node: str,
        target: str,
        cache: dict[tuple[str, bool, bool], int],
        *,
        seen_dac: bool,
        seen_fft: bool,
        require_both: bool,
    ) -> int:
        """Count paths from current node to target with optional device constraints.

        Uses a memoized depth-first search where the state includes the
        current node and whether 'dac' and 'fft' have already been seen
        along the current path.

        Args:
            graph: Adjacency list of the device network.
            node: Current device name.
            target: Destination device to reach (typically 'out').
            cache: Memoization dictionary keyed by (node, seen_dac, seen_fft).
            seen_dac: Whether 'dac' has been visited so far on this path.
            seen_fft: Whether 'fft' has been visited so far on this path.
            require_both: If True, only count paths that have visited both
                'dac' and 'fft' by the time they reach target.

        Returns
        -------
            int: Number of valid paths from node to target for this state.
        """
        if node == "dac":
            seen_dac = True

        if node == "fft":
            seen_fft = True

        state = (node, seen_dac, seen_fft)
        if state in cache:
            return cache[state]

        if node == target:
            if require_both:
                cache[state] = 1 if (seen_dac and seen_fft) else 0
            else:
                cache[state] = 1
            return cache[state]

        total = 0
        for nxt in graph.get(node, []):
            total += self.dfs(
                graph,
                nxt,
                target,
                cache,
                seen_dac=seen_dac,
                seen_fft=seen_fft,
                require_both=require_both,
            )

        cache[state] = total
        return total

    def part1(self, data: list[str]) -> int:
        """Count all paths from 'you' to 'out' in the reactor graph.

        Builds the directed device graph from the input and then runs a
        memoized DFS from 'you' to 'out', counting every distinct path
        that data could follow through the devices.

        Args:
            data: List of device connection lines.

        Returns
        -------
            int: Number of distinct paths from 'you' to 'out'.
        """
        graph = self.construct_graph(data)
        cache: dict[tuple[str, bool, bool], int] = {}
        return self.dfs(
            graph,
            "you",
            "out",
            cache,
            seen_dac=False,
            seen_fft=False,
            require_both=False,
        )

    def part2(self, data: list[str]) -> int:
        """Count paths from 'svr' to 'out' that pass through both 'dac' and 'fft'.

        Builds the same device graph but now counts only those paths that
        start at 'svr', end at 'out', and visit both 'dac' and 'fft' at
        least once somewhere along the path.

        Args:
            data: List of device connection lines.

        Returns
        -------
            int: Number of paths from 'svr' to 'out' that visit both
            'dac' and 'fft'.
        """
        graph = self.construct_graph(data)
        cache: dict[tuple[str, bool, bool], int] = {}
        return self.dfs(
            graph,
            "svr",
            "out",
            cache,
            seen_dac=False,
            seen_fft=False,
            require_both=True,
        )
