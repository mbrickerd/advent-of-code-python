"""Day 1: Circular Dial Rotation

This module provides the solution for Advent of Code 2025 - Day 1.

It simulates rotating a circular dial (positions 0-99) based on movement
instructions, counting how many times the dial points at position 0.

The module contains a Solution class that inherits from SolutionBase for
parsing dial movements and tracking zero position counts.
"""

import re
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Simulate circular dial rotations and count zero position occurrences.

    This solution models a 100-position circular dial starting at position 50.
    Instructions specify clockwise (R) or counterclockwise (L) rotations by
    a number of steps. Part 1 counts endings at position 0. Part 2 counts every
    pass through position 0 during rotations.

    Uses modular arithmetic for efficient dial position tracking.
    """

    DIAL_SIZE: ClassVar[int] = 100
    START_POSITION: ClassVar[int] = 50
    MOVE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"(L|R)(\d+)$")

    def parse_move(self, move: str) -> tuple[str, int]:
        """Parse movement instruction into direction and step count.

        Args:
            move: Instruction string like "L68" or "R48"

        Returns
        -------
            tuple[str, int]: Direction ("L" or "R") and number of steps

        Raises
        ------
            ValueError: If instruction format is invalid
        """
        match = self.MOVE_PATTERN.match(move)
        if not match:
            err_msg = f"Invalid move: {move}"
            raise ValueError(err_msg)

        return match.group(1), int(match.group(2))

    def move_jump(self, position: int, direction: str, steps: int) -> tuple[int, int]:
        """Move dial by steps using modular arithmetic, count final zero landings.

        Args:
            position: Current dial position (0-99)
            direction: "L" (counterclockwise) or "R" (clockwise)
            steps: Number of positions to rotate

        Returns
        -------
            tuple[int, int]: (new_position, zero_count) where zero_count is 1 if
                final position is 0, else 0
        """
        if direction == "L":
            new_position = (position - steps) % self.DIAL_SIZE
        else:
            new_position = (position + steps) % self.DIAL_SIZE

        zero_count = 1 if new_position == 0 else 0

        return new_position, zero_count

    def move_step(self, position: int, direction: str, steps: int) -> tuple[int, int]:
        """Move dial one position at a time, counting every pass through zero.

        Args:
            position: Current dial position (0-99)
            direction: "L" (counterclockwise) or "R" (clockwise)
            steps: Number of positions to rotate

        Returns
        -------
            tuple[int, int]: (final_position, total_zero_count) where total_zero_count
                includes every time position 0 is passed during rotation
        """
        zero_count = 0
        step_direction = -1 if direction == "L" else 1

        for _ in range(steps):
            position = (position + step_direction) % self.DIAL_SIZE
            if position == 0:
                zero_count += 1

        return position, zero_count

    def part1(self, data: list[str]) -> int:
        """Count dial rotations that end exactly at position 0.

        Starting at position 50, processes all rotation instructions and counts
        how many times the dial ends precisely at position 0 after each move.
        Uses efficient modular arithmetic for large rotations.

        Args:
            data: List of rotation instructions (e.g., ["R48", "L68"])

        Returns
        -------
            int: Total number of rotations ending at position 0
        """
        position = self.START_POSITION
        zero_count = 1 if position == 0 else 0

        for move in data:
            direction, steps = self.parse_move(move)
            position, zeros = self.move_jump(position, direction, steps)
            zero_count += zeros

        return zero_count

    def part2(self, data: list[str]) -> int:
        """Count every time dial passes through position 0 during rotations.

        Tracks position 0 crossings during step-by-step rotations, not just final
        positions. A full rotation (100 steps) in either direction passes through
        0 exactly once.

        Args:
            data: List of rotation instructions (e.g., ["R48", "L68"])

        Returns
        -------
            int: Total number of times position 0 is visited during all rotations
        """
        position = self.START_POSITION
        zero_count = 0

        for move in data:
            direction, steps = self.parse_move(move)
            position, zeros = self.move_step(position, direction, steps)
            zero_count += zeros

        return zero_count
