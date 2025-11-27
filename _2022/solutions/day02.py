"""Day 2: Rock Paper Scissors

This module provides the solution for Advent of Code 2022 - Day 2.

It handles rock-paper-scissors game scoring based on opponent moves and
desired outcomes using efficient dictionary lookups.

The module contains a Solution class that inherits from SolutionBase and implements
methods to calculate total scores for different game strategies.
"""

from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Calculate rock-paper-scissors game scores with strategic outcomes.

    This solution processes rock-paper-scissors rounds and calculates scores.
    Part 1 interprets the second column as your move choice, while Part 2
    interprets it as the desired outcome (lose/draw/win).

    The solution uses dictionary lookups for efficient move resolution and
    scoring, avoiding complex conditional branching.
    """

    NORMALISED_MAP: ClassVar[dict[str, str]] = {
        "A": "R",
        "B": "P",
        "C": "S",
        "X": "R",
        "Y": "P",
        "Z": "S",
    }

    WINS: ClassVar[dict[str, str]] = {
        "R": "S",  # Rock beats Scissors
        "P": "R",  # Paper beats Rock
        "S": "P",  # Scissors beats Paper
    }

    LOSES: ClassVar[dict[str, str]] = {
        "S": "R",  # Scissors loses to Rock
        "R": "P",  # Rock loses to Paper
        "P": "S",  # Paper loses to Scissors
    }

    POINT_MAP: ClassVar[dict[str, int]] = {
        "R": 1,  # Rock
        "P": 2,  # Paper
        "S": 3,  # Scissors
    }

    OUTCOME_MAP: ClassVar[dict[str, int]] = {
        "X": 0,  # Loss
        "Y": 3,  # Tie
        "Z": 6,  # Win
    }

    def part1(self, data: list[str]) -> int:
        """Calculate total score when second column represents your move.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Total score from all rounds where X/Y/Z are interpreted as
                Rock/Paper/Scissors respectively
        """
        score = 0
        for round_str in data:
            opponent_letter, self_letter = round_str.split()
            opponent_choice = self.NORMALISED_MAP[opponent_letter]
            self_choice = self.NORMALISED_MAP[self_letter]

            score += self.POINT_MAP[self_choice] + (
                3
                if self_choice == opponent_choice
                else 6
                if self.WINS[self_choice] == opponent_choice
                else 0
            )

        return score

    def part2(self, data: list[str]) -> int:
        """Calculate total score when second column represents desired outcome.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Total score from all rounds where X/Y/Z are interpreted as
                lose/draw/win outcomes respectively
        """
        score = 0
        for round_str in data:
            opponent_letter, outcome_letter = round_str.split()
            opponent_choice = self.NORMALISED_MAP[opponent_letter]
            outcome = self.OUTCOME_MAP[outcome_letter]

            self_choice = (
                opponent_choice
                if outcome == 3
                else (self.LOSES[opponent_choice] if outcome == 6 else self.WINS[opponent_choice])
            )

            score += outcome + self.POINT_MAP[self_choice]

        return score
