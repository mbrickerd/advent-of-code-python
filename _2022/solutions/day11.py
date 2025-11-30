"""Day 11: Monkey in the Middle

This module provides the solution for Advent of Code 2022 - Day 11.

It simulates monkeys throwing items based on worry levels and divisibility tests,
tracking inspection counts to calculate the level of monkey business.

The module contains a Monkey class for individual monkey behavior and a Solution
class that inherits from SolutionBase for running the simulation.
"""

from collections.abc import Callable
from math import lcm
import re

from aoc.models.base import SolutionBase


class Monkey:
    """Represent a monkey with items, operations, and throwing rules.

    Each monkey holds items with worry levels, performs an operation on each
    item during inspection, tests divisibility, and throws items to other
    monkeys based on the test result.
    """

    def __init__(self, data: str) -> None:
        """Parse monkey configuration from input block.

        Args:
            data: Multi-line string containing monkey ID, starting items,
                operation, divisibility test, and throw targets
        """
        lines = data.strip().split("\n")

        match = re.search(r"Monkey (\d+):", lines[0])
        if match is None:
            err_msg = "Invalid monkey ID format"
            raise ValueError(err_msg)
        self._id = int(match.group(1))

        match = re.search(r"Starting items: ([\d, ]+)", lines[1])
        if match is None:
            err_msg = "Invalid starting items format"
            raise ValueError(err_msg)
        self.items = [int(x) for x in match.group(1).split(", ")]

        match = re.search(r"Operation: new = (.*)$", lines[2])
        if match is None:
            err_msg = "Invalid operation format"
            raise ValueError(err_msg)
        operation_str = match.group(1)
        self.operation = self._parse_operation(operation_str)

        match = re.search(r"Test: divisible by (\d+)$", lines[3])
        if match is None:
            err_msg = "Invalid test format"
            raise ValueError(err_msg)
        self.divisor = int(match.group(1))

        match = re.search(r"If true: throw to monkey (\d+)$", lines[4])
        if match is None:
            err_msg = "Invalid if_true format"
            raise ValueError(err_msg)
        self.if_true = int(match.group(1))

        match = re.search(r"If false: throw to monkey (\d+)$", lines[5])
        if match is None:
            err_msg = "Invalid if_false format"
            raise ValueError(err_msg)
        self.if_false = int(match.group(1))

        self.inspection_count = 0

    def _parse_operation(self, operation_str: str) -> Callable[[int], int]:
        """Parse operation string into executable function.

        Args:
            operation_str: Expression like "old * 19" or "old + 6"

        Returns
        -------
            Callable[[int], int]: Function that applies operation to worry level
        """
        return lambda old: eval(operation_str, {"old": old})  # noqa: S307

    def inspect_items(self, lcm_value: int, *, is_relieved: bool) -> list[tuple[int, int]]:
        """Inspect all held items and determine where to throw them.

        For each item: increment inspection count, apply operation, optionally
        divide by 3 (Part 1) or modulo by LCM (Part 2), test divisibility,
        and determine target monkey.

        Args:
            is_relieved: If True, divide worry level by 3 after inspection (Part 1)
            lcm_value: Least common multiple of all monkey divisors for modulo
                operation to keep numbers manageable (Part 2)

        Returns
        -------
            list[tuple[int, int]]: List of (worry_level, target_monkey_id) tuples
                for items to be thrown
        """
        throws: list[tuple[int, int]] = []

        for item in self.items:
            self.inspection_count += 1
            worry_level = self.operation(item)

            if is_relieved:
                worry_level //= 3
            else:
                worry_level %= lcm_value

            # Test and determine target
            if worry_level % self.divisor == 0:
                throws.append((worry_level, self.if_true))

            else:
                throws.append((worry_level, self.if_false))

        self.items = []
        return throws


class Solution(SolutionBase):
    """Simulate monkey item-throwing game and calculate monkey business.

    This solution simulates monkeys playing keep-away with items. Part 1
    runs 20 rounds with worry relief (divide by 3), while Part 2 runs
    10,000 rounds without relief, using LCM modulo arithmetic to keep
    worry levels manageable.

    Monkey business is the product of the two highest inspection counts.
    """

    def simulate(self, data: str, rounds: int, *, is_relieved: bool) -> int:
        """Run monkey simulation for specified rounds.

        Each round, monkeys take turns inspecting and throwing all their items.
        Uses LCM of all divisors to prevent worry levels from growing too large
        in Part 2 while preserving divisibility test results.

        Args:
            data: Raw input containing monkey configurations
            rounds: Number of rounds to simulate
            is_relieved: If True, divide worry by 3 after each inspection

        Returns
        -------
            int: Monkey business level (product of top 2 inspection counts)
        """
        monkeys = [Monkey(block) for block in data.split("\n\n")]
        lcm_value = lcm(*[m.divisor for m in monkeys])

        for _ in range(rounds):
            for monkey in monkeys:
                throws = monkey.inspect_items(lcm_value, is_relieved=is_relieved)
                for item, target_id in throws:
                    monkeys[target_id].items.append(item)

        counts = sorted([m.inspection_count for m in monkeys], reverse=True)
        return counts[0] * counts[1]

    def part1(self, data: str) -> int:
        """Calculate monkey business after 20 rounds with worry relief.

        After each inspection, worry level is divided by 3 (rounded down)
        because you're relieved the item wasn't damaged.

        Args:
            data: Raw input containing monkey configurations

        Returns
        -------
            int: Product of top 2 inspection counts after 20 rounds
        """
        return self.simulate(data, rounds=20, is_relieved=True)

    def part2(self, data: str) -> int:
        """Calculate monkey business after 10,000 rounds without relief.

        Worry levels are no longer divided by 3, causing them to grow rapidly.
        Uses modulo by LCM of all divisors to keep numbers manageable while
        preserving divisibility test outcomes.

        Args:
            data: Raw input containing monkey configurations

        Returns
        -------
            int: Product of top 2 inspection counts after 10,000 rounds
        """
        return self.simulate(data, rounds=10_000, is_relieved=False)
