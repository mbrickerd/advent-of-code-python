"""Day 22: Monkey Market

This module provides the solution for Advent of Code 2024 - Day 22.

It solves a puzzle about analyzing pseudorandom secret number sequences and
price patterns in a monkey marketplace. Buyers use secret numbers to generate
prices, and finding optimal price change sequences maximizes banana earnings.

The solution involves simulating pseudorandom number generation through bitwise
operations (XOR and modulo), tracking price changes across multiple buyers, and
identifying the most profitable sequence of four consecutive price changes.

The module contains a Solution class that inherits from SolutionBase and
implements methods to transform secret numbers and analyze price patterns.
"""

from collections import defaultdict
from itertools import pairwise

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyze secret numbers and price patterns in the monkey marketplace.

    This solution implements pseudorandom number analysis:
    - Part 1: Calculate sum of secret numbers after 2000 transformations
    - Part 2: Find optimal price change sequence across all buyers

    The solution uses bitwise operations (XOR) and modulo arithmetic to generate
    pseudorandom sequences, then analyzes price patterns to maximize profits.
    """

    rounds: int = 2000

    def transform_secret(self, secret: int) -> int:
        """Transform a secret number through bitwise operations.

        Applies three sequential transformations using multiplication, division,
        XOR (mix), and modulo (prune) operations. Each step mixes a calculated
        value into the secret using XOR, then prunes the result using modulo
        16777216 to keep values in range.

        Args:
            secret (int): The secret number to transform

        Returns
        -------
            Transformed secret number after applying all three steps
        """
        secret = ((secret * 64) ^ secret) % 16777216
        secret = ((secret // 32) ^ secret) % 16777216
        return ((secret * 2048) ^ secret) % 16777216

    def part1(self, data: list[str]) -> int:
        """Calculate sum of secret numbers after 2000 transformations.

        Processes each initial secret number through 2000 rounds of transformation,
        then sums all final secret values. This simulates the pseudorandom number
        generation for each buyer over a full day.

        Args:
            data (list[str]): List of strings containing initial secret numbers

        Returns
        -------
            Sum of all secret numbers after 2000 transformation rounds
        """
        secrets = []
        for secret in map(int, data):
            for _ in range(self.rounds):
                secret = self.transform_secret(secret)

            secrets.append(secret)

        return sum(secrets)

    def part2(self, data: list[str]) -> int:
        """Find the price change sequence that maximizes total bananas.

        Generates price sequences for each buyer by taking the ones digit of
        transformed secret numbers. Analyzes all possible sequences of four
        consecutive price changes and identifies which sequence yields the
        highest total price across all buyers when they first encounter it.

        Args:
            data (list[str]): List of strings containing initial secret numbers

        Returns
        -------
            Maximum total bananas obtainable from any four-change sequence
        """
        prices = []
        for secret in map(int, data):
            price = []
            for _ in range(self.rounds):
                secret = self.transform_secret(secret)
                price.append(secret % 10)

            prices.append(price)

        changes = [[b - a for a, b in pairwise(p)] for p in prices]
        amounts: defaultdict[tuple[int, ...], int] = defaultdict(int)

        for buyer_idx, change in enumerate(changes):
            keys = set()
            for i in range(len(change) - 3):
                key = tuple(change[i : i + 4])
                if key in keys:
                    continue

                amounts[key] += prices[buyer_idx][i + 4]
                keys.add(key)

        return max(amounts.values())
