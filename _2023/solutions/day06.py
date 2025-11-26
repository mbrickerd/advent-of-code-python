"""Day 6: Wait For It

This module provides the solution for Advent of Code 2023 - Day 6.

It handles toy boat race calculations where holding a button increases the
boat's speed but reduces available travel time. The puzzle requires determining
how many different button hold durations will result in beating the record distance.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse race data, count winning strategies, and calculate results for
both multiple races and a single combined race.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Calculate winning strategies for toy boat races.

    This solution handles two types of race processing:
    Part 1 treats each number as a separate race and multiplies the winning
    strategies together. Part 2 combines all numbers into a single race and
    counts the winning strategies for that one race.

    The solution uses brute-force iteration to test each possible button
    hold duration and determine which ones beat the record distance.
    """

    def parse_data(
        self, data: list[str], *, part_2: bool = False
    ) -> tuple[list[int], list[int]] | tuple[int, int]:
        """Parse input lines into race times and record distances.

        Each line contains numbers representing either race times or record distances.
        For Part 1, numbers are parsed as separate values. For Part 2, all digits
        are concatenated into single large numbers.

        Args:
            data (list[str]): List containing two strings for times and distances
            part_2 (bool): If True, join numbers into single values instead of lists

        Returns
        -------
            Tuple of (times, distances) where each element is either:
            - Lists of integers for Part 1
            - Single integer values for Part 2
        """
        if part_2:
            times: int = int("".join(data[0].split(":")[1].split()))
            distances: int = int("".join(data[1].split(":")[1].split()))
            return times, distances

        times_list: list[int] = [int(x) for x in data[0].split(":")[1].split()]
        distances_list: list[int] = [int(x) for x in data[1].split(":")[1].split()]
        return times_list, distances_list

    def count_wins(self, time: int, record_distance: int) -> int:
        """Count number of ways to win a single race.

        For each possible button hold duration, the boat's speed equals the hold
        duration in mm/ms. The remaining time determines travel distance. Any
        hold duration that produces a distance exceeding the record is counted.

        Args:
            time (int): Race duration in milliseconds
            record_distance (int): Record distance to beat in millimeters

        Returns
        -------
            Number of different hold durations that beat the record
        """
        winning_ways = 0

        for hold_time in range(time + 1):
            distance = hold_time * (time - hold_time)
            if distance > record_distance:
                winning_ways += 1

        return winning_ways

    def part1(self, data: list[str]) -> int:
        """Calculate product of winning ways for each separate race.

        Treats each number as a separate race. For each race, calculates
        the number of ways to win and multiplies all results together.

        Args:
            data (list[str]): List containing two strings for times and distances

        Returns
        -------
            Product of the number of ways to win each race
        """
        times_raw, distances_raw = self.parse_data(data)
        times: list[int] = times_raw  # type: ignore[assignment]
        distances: list[int] = distances_raw  # type: ignore[assignment]

        result = 1
        for time, record_distance in zip(times, distances, strict=False):
            winning_ways = self.count_wins(time, record_distance)
            result *= winning_ways

        return result

    def part2(self, data: list[str]) -> int:
        """Calculate number of ways to win single race with joined values.

        Combines all digits from the input into single large numbers for both
        time and distance, creating one race with much larger values.

        Args:
            data (list[str]): List containing two strings for times and distances

        Returns
        -------
            Number of ways to win the single combined race
        """
        time_raw, distance_raw = self.parse_data(data, part_2=True)
        time: int = time_raw  # type: ignore[assignment]
        distance: int = distance_raw  # type: ignore[assignment]

        return self.count_wins(time, distance)
