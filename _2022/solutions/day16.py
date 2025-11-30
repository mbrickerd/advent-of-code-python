"""Day 16: Proboscidea Volcanium

This module provides the solution for Advent of Code 2022 - Day 16.

It models valve opening optimization in a volcanic tunnel network, using
dynamic programming to maximize pressure release within time constraints.

The module contains a cached helper function and a Solution class that
inherits from SolutionBase for parsing valve networks and computing optimal
valve opening sequences.
"""

from functools import cache
import re
from typing import ClassVar

import rustworkx as rx

from aoc.models.base import SolutionBase


@cache
def _max_pressure_helper(
    current_valve: str,
    time_left: int,
    unopened: frozenset[str],
    flow_rates: tuple[tuple[str, int], ...],
    distances: tuple[tuple[tuple[str, str], int], ...],
) -> int:
    """Calculate maximum pressure releasable from current state using memoization.

    Recursively explores all possible valve opening sequences, caching results
    to avoid recomputation of identical states. Uses immutable types for caching.

    Args:
        current_valve: Current position in valve network
        time_left: Remaining minutes before eruption
        unopened: Frozenset of valves not yet opened
        flow_rates: Tuple of (valve, rate) pairs for caching
        distances: Tuple of ((valve1, valve2), distance) pairs for caching

    Returns
    -------
        int: Maximum pressure that can be released from this state
    """
    if time_left <= 0 or not unopened:
        return 0

    flow_rates_dict = dict(flow_rates)
    distances_dict = dict(distances)

    best = 0

    for valve in unopened:
        travel_time = distances_dict[(current_valve, valve)]
        time_after_opening = time_left - travel_time - 1

        if time_after_opening > 0:
            pressure = flow_rates_dict[valve] * time_after_opening
            remaining = unopened - {valve}

            total = pressure + _max_pressure_helper(
                valve, time_after_opening, remaining, flow_rates, distances
            )
            best = max(best, total)

    return int(best)


class Solution(SolutionBase):
    """Optimize valve opening sequence to maximize pressure release in volcano.

    This solution models a tunnel network with pressure-release valves. Part 1
    finds the optimal sequence to open valves alone in 30 minutes. Part 2 solves
    for two agents (you and an elephant) working in parallel for 26 minutes.

    Uses graph algorithms to precompute shortest paths between important valves,
    then dynamic programming with memoization to explore valve opening sequences.
    """

    VALVE_REGEX: ClassVar[re.Pattern[str]] = re.compile(r"([A-Z]{2})")
    FLOW_RATE_REGEX: ClassVar[re.Pattern[str]] = re.compile(r"rate=(\d+)")

    def parse_data(
        self, data: list[str]
    ) -> tuple[tuple[tuple[str, int], ...], tuple[tuple[tuple[str, str], int], ...]]:
        """Parse valve network into flow rates and distances between valves.

        Constructs a graph of tunnel connections and uses Dijkstra's algorithm
        to compute shortest paths between all important valves (AA start position
        and any valve with positive flow rate).

        Args:
            data: List of strings describing valves and tunnel connections

        Returns
        -------
            tuple: Immutable flow_rates mapping and distances mapping for caching
        """
        flow_rates: dict[str, int] = {}
        distances: dict[tuple[str, str], int] = {}

        graph: rx.PyGraph = rx.PyGraph()
        valve_to_idx: dict[str, int] = {}
        idx_to_valve: dict[int, str] = {}

        for line in data:
            valve_match = re.search(self.VALVE_REGEX, line)
            rate_match = re.search(self.FLOW_RATE_REGEX, line)

            if valve_match is None or rate_match is None:
                err_msg = f"Invalid line format: {line}"
                raise ValueError(err_msg)

            valve = valve_match.group(1)
            rate = int(rate_match.group(1))

            idx = graph.add_node(valve)
            valve_to_idx[valve] = idx
            idx_to_valve[idx] = valve

            if rate > 0:
                flow_rates[valve] = rate

        for line in data:
            valve_match = re.search(self.VALVE_REGEX, line)
            if valve_match is None:
                err_msg = f"Invalid line format: {line}"
                raise ValueError(err_msg)

            valve = valve_match.group(1)
            tunnels = re.findall(r"[A-Z]{2}", line.split("valve")[-1])
            valve_idx = valve_to_idx[valve]

            for neighbor in tunnels:
                graph.add_edge(valve_idx, valve_to_idx[neighbor], 1)

        important = ["AA", *list(flow_rates.keys())]

        for idx, v1 in enumerate(important):
            for v2 in important[idx + 1 :]:
                idx1, idx2 = valve_to_idx[v1], valve_to_idx[v2]

                dist = rx.dijkstra_shortest_path_lengths(
                    graph, idx1, edge_cost_fn=lambda _: 1, goal=idx2
                )[idx2]

                distances[(v1, v2)] = distances[(v2, v1)] = int(dist)

        return tuple(flow_rates.items()), tuple(distances.items())

    def dfs(
        self,
        current: str,
        time: int,
        unopened: frozenset[str],
        opened: frozenset[str],
        pressure: int,
        flow_rates: dict[str, int],
        distances: dict[tuple[str, str], int],
        results: dict[frozenset[str], int],
    ) -> None:
        """Depth-first search to find all reachable valve combinations and pressures.

        Explores all possible paths through the valve network, recording the best
        pressure achievable for each unique set of opened valves. Used in Part 2
        to find complementary valve sets for parallel agents.

        Args:
            current: Current valve position
            time: Remaining time
            unopened: Set of valves not yet opened
            opened: Set of valves already opened
            pressure: Total pressure released so far
            flow_rates: Valve flow rate mappings
            distances: Shortest path distances between valves
            results: Dictionary to accumulate (opened_set -> best_pressure) mappings
        """
        if opened not in results or pressure > results[opened]:
            results[opened] = pressure

        for valve in unopened:
            travel_time = distances[(current, valve)]
            time_after = time - travel_time - 1

            if time_after > 0:
                valve_pressure = flow_rates[valve] * time_after
                self.dfs(
                    valve,
                    time_after,
                    unopened - {valve},
                    opened | {valve},
                    pressure + valve_pressure,
                    flow_rates,
                    distances,
                    results,
                )

    def part1(self, data: list[str]) -> int:
        """Find maximum pressure releasable by opening valves alone in 30 minutes.

        Starting at valve AA with 30 minutes, determines the optimal sequence
        of valve openings to maximize total pressure released before volcanic
        eruption. Travel between valves and opening each valve costs 1 minute.

        Args:
            data: List of strings describing valve network

        Returns
        -------
            int: Maximum total pressure that can be released
        """
        flow_rates, distances = self.parse_data(data)

        return _max_pressure_helper(
            "AA", 30, frozenset(dict(flow_rates).keys()), flow_rates, distances
        )

    def part2(self, data: list[str]) -> int:
        """Find maximum pressure with you and elephant working in parallel for 26 minutes.

        After spending 4 minutes teaching the elephant, you both have 26 minutes
        to open valves. Finds the optimal division of valves between two agents
        by exploring all possible combinations and selecting non-overlapping sets
        with maximum combined pressure.

        Args:
            data: List of strings describing valve network

        Returns
        -------
            int: Maximum combined pressure achievable with two parallel agents
        """
        flow_rates, distances = self.parse_data(data)
        all_valves = frozenset(dict(flow_rates).keys())

        results: dict[frozenset[str], int] = {frozenset(): 0}

        self.dfs("AA", 26, all_valves, frozenset(), 0, dict(flow_rates), dict(distances), results)

        max_pressure = 0
        items = list(results.items())

        for i in range(len(items)):
            for j in range(i, len(items)):
                combo1, pressure1 = items[i]
                combo2, pressure2 = items[j]

                if not combo1 & combo2:
                    max_pressure = max(max_pressure, pressure1 + pressure2)

        return int(max_pressure)
