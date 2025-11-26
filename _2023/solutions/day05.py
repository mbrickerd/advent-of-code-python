"""Day 5: If You Give A Seed A Fertilizer

This module provides the solution for Advent of Code 2023 - Day 5.

It handles mapping seeds through various conversion stages (soil, fertilizer,
water, light, temperature, humidity, and location). Each stage has mapping
rules that convert source numbers to destination numbers based on ranges.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse input data, convert numbers through mapping stages, and find the
lowest final location number for both individual seeds and seed ranges.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Process seeds through mapping stages to find lowest location numbers.

    This solution handles two types of seed processing:
    Part 1 processes individual seed numbers through all mapping stages.
    Part 2 treats seed numbers as pairs representing ranges (start and length)
    and processes entire ranges to find the lowest location.

    The solution uses range-based mappings to efficiently convert numbers through
    multiple stages of transformations.
    """

    def parse_data(
        self, data: list[str], *, use_ranges: bool = False
    ) -> tuple[list[int] | list[tuple[int, int]], dict[str, list[list[int]]]]:
        """Parse input data into seeds and mapping sections.

        Each line of input is processed to extract seed numbers and mapping rules.
        The input format includes a seeds line followed by multiple mapping sections,
        each with a header and range definitions.

        Args:
            data (list[str]): List of strings where each string is a line from the input
            use_ranges (bool): If True, parse seed numbers as (start, length) pairs

        Returns
        -------
            Tuple containing:
            - seeds: List of individual numbers or list of (start, length) tuples
            - mappings: Dict mapping section names to lists of [dest_start, source_start, range_len]
        """
        # Initialize data structures
        seeds: list[int] | list[tuple[int, int]] = []
        mappings: dict[str, list[list[int]]] = {}
        current_map: str | None = None

        for line in data:
            # Skip empty lines
            if not line.strip():  # Added strip() to handle whitespace lines
                continue

            # Parse seeds line
            if line.startswith("seeds:"):
                seed_numbers = [int(x) for x in line.split(":")[1].strip().split()]
                if use_ranges:
                    # Convert pairs of numbers into (start, length) tuples
                    seeds = [
                        (seed_numbers[i], seed_numbers[i + 1])
                        for i in range(0, len(seed_numbers), 2)
                        if i + 1 < len(seed_numbers)
                    ]
                else:
                    seeds = seed_numbers
                continue

            # Check for new mapping section
            if "map:" in line:
                current_map = line.split(" map:")[0]
                mappings[current_map] = []
                continue

            # Parse mapping numbers if we're in a mapping section
            if current_map and line[0].isdigit():
                numbers = [int(x) for x in line.split()]
                if len(numbers) == 3:
                    mappings[current_map].append(numbers)

        return seeds, mappings

    def process_seed_range(
        self, start: int, length: int, mappings: dict[str, list[list[int]]]
    ) -> int:
        """Process a range of seed numbers to find lowest location number.

        Iterates through each seed in the specified range, mapping it through
        all conversion stages to find the minimum final location value.

        Args:
            start (int): Starting seed number for the range
            length (int): Number of seeds in the range
            mappings (dict[str, list[list[int]]]): Dictionary of mapping ranges for each stage

        Returns
        -------
            Lowest location number found in the range
        """
        lowest_location: int | float = float("inf")

        # Process each seed in the range
        for seed in range(start, start + length):
            location = self.map_seed(seed, mappings)
            lowest_location = min(lowest_location, location)

        return int(lowest_location)

    def convert(self, num: int, ranges: list[list[int]]) -> int:
        """Convert a single number through one mapping section's ranges.

        Checks each range to see if the number falls within its source range.
        If a match is found, the number is converted to the destination range.
        If no match is found, the number maps to itself.

        Args:
            num (int): Number to convert
            ranges (list[list[int]]): List of [dest_start, source_start, range_len] mappings

        Returns
        -------
            Converted number, or original number if no range matches
        """
        for range_item in ranges:
            dst_start: int
            src_start: int
            length: int
            dst_start, src_start, length = range_item

            if src_start <= num < src_start + length:
                # Calculate offset from source_start and add to dest_start
                offset = num - src_start
                return dst_start + offset

        # If no range matches, number maps to itself
        return num

    def map_seed(self, seed: int, mappings: dict[str, list[list[int]]]) -> int:
        """Process a seed number through all mapping stages.

        Takes an initial seed value and applies each mapping stage in sequence
        to produce the final location number.

        Args:
            seed (int): Initial seed number
            mappings (dict[str, list[list[int]]]): Dictionary of mapping ranges for each stage

        Returns
        -------
            Final location number after applying all mappings
        """
        current_value = seed

        # Process through each mapping stage in order
        for name in mappings:
            current_value = self.convert(current_value, mappings[name])

        return current_value

    def part1(self, data: list[str]) -> int:
        """Calculate lowest location number from individual seed numbers.

        Processes each seed number through all mapping stages and finds
        the minimum final location value.

        Args:
            data (list[str]): List of strings representing the puzzle input

        Returns
        -------
            Lowest location number found across all seeds
        """
        seeds_raw, mappings = self.parse_data(data)
        seeds: list[int] = seeds_raw  # type: ignore[assignment]

        locations = set()
        for seed in seeds:
            locations.add(self.map_seed(seed, mappings))

        return min(locations)

    def part2(self, data: list[str]) -> int:
        """Calculate lowest location number from seed ranges.

        Treats seed numbers as pairs representing ranges (start and length).
        Processes all seeds in each range to find the minimum location.

        Args:
            data (list[str]): List of strings representing the puzzle input

        Returns
        -------
            Lowest location number found across all seed ranges
        """
        # Parse data with ranges enabled
        seed_ranges_raw, mappings = self.parse_data(data, use_ranges=True)
        seed_ranges: list[tuple[int, int]] = seed_ranges_raw  # type: ignore[assignment]

        # Find lowest location across all ranges
        lowest_location: int | float = float("inf")
        for start, length in seed_ranges:
            range_lowest = self.process_seed_range(start, length, mappings)
            lowest_location = min(lowest_location, range_lowest)

        return int(lowest_location) if lowest_location != float("inf") else 0
