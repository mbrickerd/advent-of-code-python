"""Day 4: Scratchcards

This module provides the solution for Advent of Code 2023 - Day 4.

It handles scoring scratchcards where each card has two sets of numbers:
winning numbers and numbers you have. Points are calculated based on matching
numbers, and cards can win copies of subsequent cards.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse scratchcard data, calculate points, and determine total cards won.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Process scratchcards to calculate points and total cards won.

    This solution handles two types of scoring for scratchcards:
    Part 1 calculates points based on matching numbers, with points doubling
    for each match after the first. Part 2 tracks how many copies of cards
    are won through the matching mechanism.

    The solution uses sets to efficiently find matching numbers between
    winning numbers and numbers you have on each card.
    """

    def parse_data(self, data: list[str]) -> list[tuple[set[int], set[int]]]:
        """Parse scratchcard data into sets of winning numbers and numbers you have.

        Each line of input represents a scratchcard with the format:
        Card N: [winning numbers] | [numbers you have]

        Args:
            data (list[str]): List of strings where each string represents a scratchcard

        Returns
        -------
            List of tuples, where each tuple contains two sets:
            (winning_numbers, numbers_you_have)
        """
        cards = []
        for line in data:
            card_part = line.split(": ")[1]
            winning_part, have_part = card_part.split(" | ")
            winning_numbers = {int(num) for num in winning_part.split()}
            numbers_you_have = {int(num) for num in have_part.split()}

            cards.append((winning_numbers, numbers_you_have))

        return cards

    def part1(self, data: list[str]) -> int:
        """Calculate total points from all scratchcards.

        Points are calculated as 2^(n-1) where n is the number of matching numbers.
        Cards with no matches are worth 0 points.

        Args:
            data (list[str]): List of strings representing scratchcards

        Returns
        -------
            Total points from all scratchcards
        """
        cards = self.parse_data(data)
        total_points = 0

        for winning_numbers, numbers_you_have in cards:
            matches = len(winning_numbers & numbers_you_have)
            if matches > 0:
                points = 1 << (matches - 1)
                total_points += points

        return total_points

    def part2(self, data: list[str]) -> int:
        """Calculate total number of scratchcards won through copying.

        Each matching number wins a copy of the next card. These copies
        can then win more copies of subsequent cards.

        Args:
            data (list[str]): List of strings representing scratchcards

        Returns
        -------
            Total number of scratchcards won, including originals and copies
        """
        cards = self.parse_data(data)
        card_counts = [1] * len(cards)

        for i, (winning_numbers, numbers_you_have) in enumerate(cards):
            matches = len(winning_numbers & numbers_you_have)
            for j in range(matches):
                next_card = i + 1 + j
                if next_card < len(cards):
                    card_counts[next_card] += card_counts[i]

        return sum(card_counts)
