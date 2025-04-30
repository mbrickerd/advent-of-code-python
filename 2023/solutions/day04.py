from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2023 - Day 4: Scratchcards.

    This class solves a puzzle involving scoring scratchcards where each card has two sets
    of numbers: winning numbers and numbers you have. In Part 1, cards are scored based
    on matching numbers, with points doubling for each match after the first. In Part 2,
    matching numbers win copies of subsequent cards, which can then win more copies.

    Input format:
        Lines of text where each line represents a scratchcard with the format:
        Card N: [winning numbers] | [numbers you have]

    This class inherits from `SolutionBase` and provides methods to parse scratchcard
    data, calculate points based on matching numbers, and determine the total number
    of scratchcards won through the copying mechanism.
    """

    def parse_data(self, data: list[str]) -> list[tuple[set[int], set[int]]]:
        """Parse scratchcard data into sets of winning numbers and numbers you have.

        Args:
            data: List of strings where each string represents a scratchcard

        Returns
        -------
            List of tuples, where each tuple contains two sets:
            (winning_numbers, numbers_you_have)
        """
        cards = []
        for line in data:
            # Split into card number and numbers part
            card_part = line.split(": ")[1]

            # Split into winning numbers and numbers you have
            winning_part, have_part = card_part.split(" | ")

            # Convert string numbers to sets of integers
            winning_numbers = set(int(num) for num in winning_part.split())
            numbers_you_have = set(int(num) for num in have_part.split())

            cards.append((winning_numbers, numbers_you_have))

        return cards

    def part1(self, data: list[str]) -> int:
        """Calculate total points from all scratchcards.

        For each card, the first matching number is worth 1 point, and each
        subsequent match doubles the card's value.

        Args:
            data: List of strings containing scratchcard data

        Returns
        -------
            Total points from all scratchcards
        """
        cards = self.parse_data(data)
        total_points = 0

        for winning_numbers, numbers_you_have in cards:
            # Find matching numbers
            matches = len(winning_numbers & numbers_you_have)

            # Calculate points for this card
            if matches > 0:
                points = 1 << (matches - 1)  # Same as 2^(matches-1)
                total_points += points

        return total_points

    def part2(self, data: list[str]) -> int:
        """Calculate total number of scratchcards after processing copies.

        Each matching number on a card wins a copy of the next N cards, where N
        is the number of matches. Copies of cards can also win more copies.

        Args:
            data: List of strings containing scratchcard data

        Returns
        -------
            Total number of scratchcards including original cards and copies
        """
        cards = self.parse_data(data)
        # Initialize card counts (start with 1 of each)
        card_counts = [1] * len(cards)

        # Process each card
        for i, (winning_numbers, numbers_you_have) in enumerate(cards):
            # Get number of matches for this card
            matches = len(winning_numbers & numbers_you_have)

            # For each match, add copies to subsequent cards
            for j in range(matches):
                next_card = i + 1 + j
                # Only process if we're not past the end of the cards
                if next_card < len(cards):
                    # Add copies based on how many of current card we have
                    card_counts[next_card] += card_counts[i]

        # Sum up total number of cards
        return sum(card_counts)
