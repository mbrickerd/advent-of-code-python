from collections import Counter
from dataclasses import dataclass
from enum import IntEnum

from aoc.models.base import SolutionBase


class HandType(IntEnum):
    """Enumeration of possible poker hand types in order of increasing strength.

    Each hand type is assigned an integer value from 1 to 7, where higher
    values represent stronger hands.
    """

    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_KIND = 6
    FIVE_OF_KIND = 7


@dataclass
class Hand:
    """Represents a hand in the Camel Cards game.

    This class handles the logic for evaluating and comparing poker hands,
    including special rules for jokers in part 2 of the puzzle.

    Attributes
    ----------
        cards: A string of 5 characters representing the cards in the hand
        bid: The bid amount associated with this hand
        use_jokers: Boolean flag indicating whether to treat 'J' as jokers
        card_values: Dictionary mapping card symbols to their numeric values
        type: The HandType enum value representing this hand's strength
    """

    cards: str
    bid: int
    use_jokers: bool = False

    def __post_init__(self):
        """Initialize derived attributes after instance creation.

        Sets up the `card_values` dictionary based on whether jokers are in use,
        and determines the hand type. When jokers are in use, 'J' has the lowest
        value (1) but can act as any card for determining hand type.
        """
        self.card_values = {str(i): i for i in range(2, 10)}
        if self.use_jokers:
            self.card_values.update({"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14})

        else:
            self.card_values.update({"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14})

        self.type = self.get_hand_type()

    def get_hand_type(self) -> HandType:
        """Determine the type of poker hand.

        Analyzes the cards to determine the hand type, handling jokers specially
        when use_jokers is True. Jokers will be counted as whatever card would
        make the hand strongest.

        Returns
        -------
            HandType enum value representing the strength of this hand
        """
        counts = Counter(self.cards)

        if self.use_jokers and "J" in counts and counts["J"] < 5:
            joker_count = counts["J"]
            del counts["J"]

            if counts:  # If there are non-joker cards
                most_common = counts.most_common(1)[0][0]
                counts[most_common] += joker_count

            else:  # All cards are jokers
                return HandType.FIVE_OF_KIND

        count_values = sorted(counts.values(), reverse=True)

        if count_values[0] == 5:
            return HandType.FIVE_OF_KIND

        elif count_values[0] == 4:
            return HandType.FOUR_OF_KIND

        elif count_values[0] == 3 and count_values[1] == 2:
            return HandType.FULL_HOUSE

        elif count_values[0] == 3:
            return HandType.THREE_OF_KIND

        elif count_values[0] == 2 and count_values[1] == 2:
            return HandType.TWO_PAIR

        elif count_values[0] == 2:
            return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    def __lt__(self, other: "Hand") -> bool:
        """Compare two hands to determine which is weaker.

        First compares hand types, then breaks ties by comparing individual
        cards from left to right using their card_values.

        Args:
            other: Another `Hand` instance to compare against

        Returns
        -------
            `True` if this hand is weaker than the other hand
        """
        if self.type != other.type:
            return self.type < other.type

        for self_card, other_card in zip(self.cards, other.cards, strict=False):
            if self_card != other_card:
                return self.card_values[self_card] < self.card_values[other_card]

        return False


class Solution(SolutionBase):
    """Solution for Advent of Code 2023 - Day 7: Camel Cards.

    This class implements solutions for a poker-like card game where hands
    need to be ranked and scored. Part 1 uses standard poker hand rankings,
    while Part 2 introduces jokers that can act as any card for making the
    strongest possible hand.

    Input format:
        List of strings where each line contains a five-card hand and a bid
        amount separated by a space.
    """

    def parse_data(self, data: list[str], use_jokers: bool = False) -> list[Hand]:
        """Parse input strings into Hand objects.

        Args:
            data: List of strings containing hand and bid information
            use_jokers: Whether to treat 'J' cards as jokers

        Returns
        -------
            List of Hand objects representing the input data
        """
        hands = []
        for line in data:
            cards, bid = line.split()
            hands.append(Hand(cards, int(bid), use_jokers))

        return hands

    def solve_part(self, data: list[str], use_jokers: bool) -> int:
        """Calculate total winnings for either part of the puzzle.

        Common solving logic for both parts. Parses hands, sorts them by strength,
        and calculates total winnings as the sum of (rank × bid) for each hand.
        The only difference between parts is whether jokers are enabled.

        Args:
            data: List of strings containing hand and bid information
            use_jokers: Whether to treat 'J' cards as jokers

        Returns
        -------
            Total winnings across all hands
        """
        hands = self.parse_data(data, use_jokers=use_jokers)
        sorted_hands = sorted(hands)

        return sum(rank * hand.bid for rank, hand in enumerate(sorted_hands, 1))

    def part1(self, data: list[str]) -> int:
        """Calculate total winnings using standard poker hand rankings.

        Processes each hand normally (no jokers), sorts them by strength,
        and calculates winnings as the sum of (rank × bid) for each hand.

        Args:
            data: List of strings containing hand and bid information

        Returns
        -------
            Total winnings across all hands
        """
        return self.solve_part(data, use_jokers=False)

    def part2(self, data: list[str]) -> int:
        """Calculate total winnings with jokers rule in effect.

        Similar to part1, but with 'J' cards acting as jokers that can be
        any card for making the strongest possible hand, while being the
        weakest card for breaking ties.

        Args:
            data: List of strings containing hand and bid information

        Returns
        -------
            Total winnings across all hands using joker rules
        """
        return self.solve_part(data, use_jokers=True)
