from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2023 - Day 5: If You Give A Seed A Fertilizer.

    This class solves a puzzle involving mapping seeds through various conversion stages
    (soil, fertilizer, water, light, temperature, humidity, and location). Each stage
    has its own mapping rules that convert source numbers to destination numbers based
    on ranges.

    Input format:
        Multiple sections separated by blank lines:
        - First line: "seeds: " followed by seed numbers
        - Multiple mapping sections, each starting with a header (e.g., "seed-to-soil map:")
        - Each mapping section contains lines of three numbers:
            [destination_start source_start range_length]

    Part 1 processes individual seed numbers through all mappings.
    Part 2 treats seed numbers as pairs representing ranges (start and length).

    This class inherits from `SolutionBase` and provides methods to parse the input,
    convert numbers through mapping ranges, and find the lowest final location number.
    """

    def parse_data(
        self, data: list[str], *, use_ranges: bool = False
    ) -> tuple[list[int], dict[str, list[str]]]:
        """Parse input data into seeds and mapping sections.

        Args:
            data: Raw input lines
            use_ranges: If True, parse seed numbers as pairs representing ranges

        Returns
        -------
            Tuple of:
                - seeds: List of individual numbers or list of (start, length)
                    tuples if `use_ranges=True`
                - mappings: Dict mapping section names to lists of
                    [dest_start, source_start, range_len]
        """
        # Initialize data structures
        seeds = []
        mappings = {}
        current_map = None

        for line in data:
            # Skip empty lines
            if not line.strip():  # Added strip() to handle whitespace lines
                continue

            # Parse seeds line
            if line.startswith("seeds:"):
                seed_numbers = [int(x) for x in line.split(":")[1].strip().split()]
                if use_ranges:
                    # Convert pairs of numbers into (start, length) tuples
                    seeds = []
                    for i in range(0, len(seed_numbers), 2):
                        if i + 1 < len(seed_numbers):  # Ensure we have a pair
                            seeds.append((seed_numbers[i], seed_numbers[i + 1]))

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

        Args:
            start: Starting seed number
            length: Length of range to process
            mappings: Dictionary of mapping ranges for each stage

        Returns
        -------
            Lowest location number found in the range
        """
        lowest_location = float("inf")

        # Process each seed in the range
        for seed in range(start, start + length):
            location = self.map_seed(seed, mappings)
            lowest_location = min(lowest_location, location)

        return lowest_location

    def convert(self, num: int, ranges: list[int]) -> int:
        """Convert a single number through one mapping section's ranges.

        Args:
            num: Number to convert
            ranges: List of [dest_start, source_start, range_len] mappings

        Returns
        -------
            Converted number, or original number if no range matches
        """
        for dst_start, src_start, length in ranges:
            if src_start <= num < src_start + length:
                # Calculate offset from source_start and add to dest_start
                offset = num - src_start
                return dst_start + offset

        # If no range matches, number maps to itself
        return num

    def map_seed(self, seed: int, mappings: dict[str, list[list[int]]]):
        """Process a seed number through all mapping stages.

        Args:
            seed: Initial seed number
            mappings: Dictionary of mapping ranges for each stage

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
        """Solve part 1: Process individual seed numbers.

        Args:
            data: Raw input data

        Returns
        -------
            Lowest location number found across all seeds
        """
        seeds, mappings = self.parse_data(data)

        locations = set()
        for seed in seeds:
            locations.add(self.map_seed(seed, mappings))

        return min(locations)

    def part2(self, data: list[str]) -> int:
        """Solve part 2: Process seed numbers as ranges.

        Args:
            data: Raw input data

        Returns
        -------
            Lowest location number found across all seed ranges
        """
        # Parse data with ranges enabled
        seed_ranges, mappings = self.parse_data(data, use_ranges=True)

        # Find lowest location across all ranges
        lowest_location = float("inf")

        for start, length in seed_ranges:
            range_lowest = self.process_seed_range(start, length, mappings)
            lowest_location = min(lowest_location, range_lowest)

        return lowest_location if lowest_location != float("inf") else None
