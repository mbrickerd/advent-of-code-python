from math import prod
import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2023 - Day 2: Cube Conundrum.

    This class solves a puzzle involving a game where colored cubes are drawn from
    a bag in multiple sets. Each game consists of several draws, and each draw
    reveals a certain number of red, green, and blue cubes.

    Input format:
        List of strings where each line represents a game in the format:
        "Game N: X red, Y green, Z blue; A red, B green, C blue; ..."

    The solution uses regex patterns to extract game IDs and cube counts,
    validating them against thresholds (Part 1) and finding minimum required
    cubes (Part 2).
    """

    thresholds = {"red": 12, "green": 13, "blue": 14}
    color_regex = r"(\d+) (red|green|blue)"
    id_regex = r"Game (\d+)"

    def is_possible(self, data: str) -> bool:
        """Check if a set of cube draws is possible given the thresholds.

        Examines each color count in the draw and verifies it doesn't
        exceed the predefined thresholds (12 red, 13 green, 14 blue).

        Args:
            data: String containing cube counts for a single set
                 Example: "3 blue, 4 red"

        Returns
        -------
            Boolean indicating whether the draw is possible with given thresholds
        """
        # Check if all extracted counts are within the thresholds
        for count, color in re.findall(self.color_regex, data):
            if int(count) > self.thresholds[color]:
                return False  # Violates threshold

        return True

    def part1(self, data: list[str]) -> int:
        """Sum IDs of games possible with the given cube thresholds.

        Processes each game to determine if all its sets are possible
        given the cube limits (12 red, 13 green, 14 blue). For valid
        games, adds their ID to the running sum.

        Args:
            data: List of strings containing game configurations

        Returns
        -------
            Sum of IDs of all possible games
        """
        count = 0
        for game in data:
            game_id, sets = game.split(":")[0], game.split(":")[-1].strip().split(";")
            game_id = int(re.search(self.id_regex, game_id).group(1))
            if all([self.is_possible(cubes) for cubes in sets]):
                count += game_id

        return count

    def part2(self, data: list[str]) -> int:
        """Calculate sum of power of minimum cube sets needed for each game.

        For each game, determines the minimum number of cubes of each color
        that would be needed to make the game possible. The power of a set
        is the product of the minimum required numbers of red, green, and
        blue cubes.

        Args:
            data: List of strings containing game configurations

        Returns
        -------
            Sum of the power of minimum required cube sets across all games
        """
        total = 0
        for row in data:
            cubes = {"red": 0, "green": 0, "blue": 0}
            game = row.split(":")[-1].strip()

            for count, color in re.findall(self.color_regex, game):
                if int(count) > cubes[color]:
                    cubes[color] = int(count)

            total += prod(cubes.values())

        return total
