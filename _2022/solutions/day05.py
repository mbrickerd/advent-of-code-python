"""Day 5: Supply Stacks

This module provides the solution for Advent of Code 2022 - Day 5.
It handles simulating a cargo crane moving crates between stacks according
to rearrangement procedures, tracking which crates end up on top.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse stack configurations and execute crane movement instructions.
"""

import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Simulate cargo crane operations on supply crate stacks.

    This solution processes supply stack configurations and crane movement
    instructions. Part 1 simulates a crane that moves crates one at a time
    (CrateMover 9000), while Part 2 simulates a crane that can move multiple
    crates simultaneously while preserving their order (CrateMover 9001).

    The solution parses visual stack representations and regex-based movement
    instructions to determine the final configuration of crates.
    """

    def create_stacks(self, stacks_str: str) -> list[list[str]]:
        """Parse visual stack representation into list of stacks.

        Args:
            stacks_str: String containing ASCII art representation of stacks
                with stack numbers on the bottom line

        Returns
        -------
            list[list[str]]: List of stacks where each stack is a list of crate
                labels from bottom to top
        """
        *crates, num_stacks = stacks_str.split("\n")

        N = len(num_stacks.split())  # noqa: N806

        stacks: list[list[str]] = [[] for _ in range(N)]
        crates.reverse()
        for line in crates:
            for idx, crate in enumerate(range(1, len(crates[0]), 4)):
                if crate < len(line) and line[crate].strip():
                    stacks[idx].append(line[crate])

        return stacks

    def parse_instruction(self, instruction: str) -> tuple[int, int, int]:
        """Extract movement parameters from instruction string.

        Args:
            instruction: String in format "move X from Y to Z"

        Returns
        -------
            tuple[int, int, int]: Number of crates to move, source stack index
                (0-indexed), and destination stack index (0-indexed)
        """
        crates_to_move, from_stack, to_stack = map(int, re.findall(r"\d+", instruction))
        return crates_to_move, from_stack - 1, to_stack - 1

    def part1(self, data: str) -> str:
        """Simulate CrateMover 9000 moving crates one at a time.

        The crane moves crates individually, reversing their order when moved.
        Returns the top crate from each stack after all instructions are executed.

        Args:
            data: Raw input string containing stack diagram and instructions
                separated by blank line

        Returns
        -------
            str: String of top crate labels from each stack concatenated together
        """
        stacks_str, procedures_str = data.split("\n\n")
        stacks = self.create_stacks(stacks_str)
        procedures: list[str] = procedures_str.split("\n")

        for procedure in procedures:
            if procedure.strip():
                crates_to_move, from_stack, to_stack = self.parse_instruction(procedure)
                for _ in range(crates_to_move):
                    stacks[to_stack].append(stacks[from_stack].pop())

        return "".join([stack[-1] for stack in stacks])

    def part2(self, data: str) -> str:
        """Simulate CrateMover 9001 moving multiple crates simultaneously.

        The crane moves multiple crates at once, preserving their order.
        Returns the top crate from each stack after all instructions are executed.

        Args:
            data: Raw input string containing stack diagram and instructions
                separated by blank line

        Returns
        -------
            str: String of top crate labels from each stack concatenated together
        """
        stacks_str, procedures_str = data.split("\n\n")
        stacks = self.create_stacks(stacks_str)
        procedures: list[str] = procedures_str.split("\n")

        for procedure in procedures:
            if procedure.strip():
                crates_to_move, from_stack, to_stack = self.parse_instruction(procedure)
                stacks[to_stack].extend(stacks[from_stack][-crates_to_move:])
                stacks[from_stack] = stacks[from_stack][:-crates_to_move]

        return "".join([stack[-1] for stack in stacks if stack])
