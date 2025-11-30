"""Day 15: Beacon Exclusion Zone

This module provides the solution for Advent of Code 2022 - Day 15.

It analyzes sensor coverage areas using Manhattan distance to identify positions
where beacons cannot exist and locate the one position where a distress beacon
could be hidden.

The module contains a Solution class that inherits from SolutionBase for
parsing sensor data and computing coverage zones.
"""

import re
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyze sensor coverage to find beacon exclusion zones.

    This solution uses Manhattan distance to determine sensor coverage areas.
    Part 1 counts positions in a specific row where beacons cannot exist.
    Part 2 finds the single position within a bounded area not covered by any
    sensor, which must contain the distress beacon.

    The solution uses range merging for efficient coverage calculation and
    perimeter scanning for finding the uncovered position.
    """

    REGEX: ClassVar[re.Pattern[str]] = re.compile(r"x=(-?\d+), y=(-?\d+)")

    def _manhattan_distance(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> int:
        """Calculate Manhattan distance between two coordinates.

        Args:
            coord1: First coordinate (x, y)
            coord2: Second coordinate (x, y)

        Returns
        -------
            int: Manhattan distance (sum of absolute differences)
        """
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def parse_data(
        self, data: list[str]
    ) -> tuple[dict[tuple[int, int], int], set[tuple[int, int]]]:
        """Parse sensor and beacon positions from input.

        Extracts sensor positions and their closest beacons, calculating the
        Manhattan distance coverage radius for each sensor.

        Args:
            data: List of strings describing sensor-beacon pairs

        Returns
        -------
            tuple: Dictionary mapping sensor positions to their coverage radius,
                and set of all beacon positions
        """
        sensors: dict[tuple[int, int], int] = {}
        beacons: set[tuple[int, int]] = set()

        for line in data:
            matches = re.findall(self.REGEX, line)
            sensor_x, sensor_y = matches[0]
            beacon_x, beacon_y = matches[1]
            sensor: tuple[int, int] = (int(sensor_x), int(sensor_y))
            beacon: tuple[int, int] = (int(beacon_x), int(beacon_y))

            sensors[sensor] = self._manhattan_distance(sensor, beacon)
            beacons.add(beacon)

        return sensors, beacons

    def get_coverage(
        self, sensors: dict[tuple[int, int], int], target_row: int
    ) -> list[tuple[int, int]]:
        """Calculate x-coordinate ranges covered by sensors on target row.

        For each sensor, determines if it covers any part of the target row
        and calculates the x-coordinate range if so.

        Args:
            sensors: Dictionary of sensor positions to coverage radii
            target_row: Y-coordinate of row to analyze

        Returns
        -------
            list[tuple[int, int]]: List of (x_min, x_max) ranges covered on row
        """
        ranges = []

        for (sx, sy), coverage_distance in sensors.items():
            vertical_distance = abs(sy - target_row)
            remaining_distance = coverage_distance - vertical_distance

            if remaining_distance >= 0:
                x_min = sx - remaining_distance
                x_max = sx + remaining_distance
                ranges.append((x_min, x_max))

        return ranges

    def merge_ranges(self, ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """Merge overlapping or adjacent ranges into minimal set.

        Args:
            ranges: List of (start, end) integer ranges

        Returns
        -------
            list[tuple[int, int]]: Sorted list of non-overlapping merged ranges
        """
        if not ranges:
            return []

        ranges.sort()
        merged: list[tuple[int, int]] = []

        for start, end in ranges:
            if not merged or start > merged[-1][1] + 1:
                merged.append((start, end))
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))

        return merged

    def count_covered_positions(self, ranges: list[tuple[int, int]]) -> int:
        """Count total positions covered by ranges.

        Args:
            ranges: List of (start, end) ranges

        Returns
        -------
            int: Total number of positions covered (inclusive)
        """
        return sum(end - start + 1 for start, end in ranges)

    def part1(self, data: list[str]) -> int:
        """Count positions where beacons cannot exist on target row.

        Determines sensor coverage on a specific row (y=10 for examples, y=2000000
        for actual input) and counts positions that must be empty, excluding
        positions where beacons are actually located.

        Args:
            data: List of strings describing sensor-beacon pairs

        Returns
        -------
            int: Number of positions on target row where beacon cannot be present
        """
        target_row = 10 if len(data) < 15 else 2_000_000
        sensors, beacons = self.parse_data(data)
        ranges = self.get_coverage(sensors, target_row)
        merged_ranges = self.merge_ranges(ranges)

        # Only subtract beacons that are ON the target row
        beacons_on_target_row = len([b for b in beacons if b[1] == target_row])

        return self.count_covered_positions(merged_ranges) - beacons_on_target_row

    def part2(self, data: list[str]) -> int:
        """Find tuning frequency of distress beacon location.

        Searches for the single position within bounds (0 to 20 for examples,
        0 to 4000000 for actual input) that is not covered by any sensor.
        Scans perimeters just outside each sensor's range for efficiency.

        Args:
            data: List of strings describing sensor-beacon pairs

        Returns
        -------
            int: Tuning frequency (x * 4000000 + y) of distress beacon position,
                or -1 if not found
        """
        sensors, beacons = self.parse_data(data)

        max_y = max(max(s[1] for s in sensors), max(b[1] for b in beacons))
        search_max = 20 if max_y < 100 else 4_000_000

        for (sx, sy), distance in sensors.items():
            for dx in range(distance + 2):
                dy = (distance + 1) - dx

                for sign_x, sign_y in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    x = sx + dx * sign_x
                    y = sy + dy * sign_y

                    if not (0 <= x <= search_max and 0 <= y <= search_max):
                        continue

                    if all(
                        self._manhattan_distance((x, y), sensor) > dist
                        for sensor, dist in sensors.items()
                    ):
                        return x * 4_000_000 + y

        return -1
