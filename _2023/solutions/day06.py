from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2023 - Day 6: Wait For It

    This class solves a puzzle involving toy boat races where you need to
    determine the number of ways to win each race by holding a button for
    different durations. The boat's speed increases for each millisecond
    the button is held, but holding time counts against race duration.

    Input format:
        Two lines of text:
        - Line 1: Race durations (in milliseconds)
        - Line 2: Record distances (in millimeters)

    Part 1 treats each number as a separate race.
    Part 2 joins all numbers into a single race time and distance.
    """

    def parse_data(self, data: list[str], *, part_2: bool = False) -> tuple[list[int], list[int]]:
        """Parse input lines into race times and record distances.

        For part 1, splits each line into separate numbers.
        For part 2, joins all numbers into a single value.

        Args:
            data: List containing two strings - times and distances
            part_2: If True, join numbers into single values instead of list

        Returns
        -------
            Tuple of (times, distances) where each element is either:
            - Lists of integers for part 1
            - Single integer values for part 2
        """
        if part_2:
            times = int("".join(data[0].split(":")[1].split()))
            distances = int("".join(data[1].split(":")[1].split()))
        else:
            times = [int(x) for x in data[0].split(":")[1].split()]
            distances = [int(x) for x in data[1].split(":")[1].split()]

        return times, distances

    def count_wins(self, time: int, record_distance: int) -> int:
        """Count number of ways to win a single race.

        For each possible button hold duration:
        - Boat speed equals the hold duration in mm/ms
        - Travel time is race duration minus hold duration
        - Distance traveled is speed * travel time

        Args:
            time: Race duration in milliseconds
            record_distance: Record distance to beat in millimeters

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

        Processes each race independently and multiplies the number
        of ways to win each race together.

        Args:
            data: List containing two strings - times and distances

        Returns
        -------
            Product of the number of ways to win each race
        """
        times, distances = self.parse_data(data)
        result = 1

        for time, record_distance in zip(times, distances, strict=False):
            winning_ways = self.count_wins(time, record_distance)
            result *= winning_ways

        return result

    def part2(self, data: list[str]) -> int:
        """Calculate number of ways to win single race with joined values.

        Treats all numbers as digits of a single large number for both
        time and distance, creating one much longer race.

        Args:
            data: List containing two strings - times and distances

        Returns
        -------
            Number of ways to win the single combined race
        """
        time, distance = self.parse_data(data, part_2=True)
        return self.count_wins(time, distance)
