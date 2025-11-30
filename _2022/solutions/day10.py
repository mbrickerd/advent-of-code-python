"""Day 10: Cathode-Ray Tube

This module provides the solution for Advent of Code 2022 - Day 10.

It simulates a simple CPU with register operations (addx, noop) and tracks
signal strengths at specific cycles. Part 2 renders a CRT display based on
the register value during each cycle.

The module contains a CPU class for simulation and a Solution class that
inherits from SolutionBase.
"""

import re
from typing import ClassVar

from loguru import logger

from aoc.models.base import SolutionBase


class CPU:
    """Simulate a simple CPU with register X and cycle-based operations.

    The CPU executes two instructions: addx (takes 2 cycles, adds value to X)
    and noop (takes 1 cycle, does nothing). Register X starts at 1 and is used
    to control both signal strength calculations and CRT sprite positioning.
    """

    REGEX: ClassVar[re.Pattern] = re.compile(r"^(addx) (-?\d+)$|^(noop)$")

    def __init__(self) -> None:
        """Initialize CPU with register X at 1 and cycle counter at 1."""
        self.register_X = 1
        self.cycle = 1
        self.waiting_add = 0
        self.wait = 0
        self.sum_of_registers = 0
        self.display: str = ""

    def run(self, command: str) -> None:
        """Parse and queue a command for execution.

        Args:
            command: Either "addx V" or "noop" instruction
        """
        match = self.REGEX.match(command)

        if match and match.group(1) == "addx":
            self.wait = 2
            self.waiting_add = int(match.group(2))

        else:  # noop
            self.wait = 1
            self.waiting_add = 0

    def advance_cycle(self, part_2: bool | None = None) -> None:
        """Advance one CPU cycle, updating signal strength and register.

        Signal strength is calculated at cycles 20, 60, 100, 140, 180, 220.
        Register X is updated after an instruction completes its wait cycles.

        Args:
            part_2: If True, also render CRT pixel for this cycle
        """
        if self.cycle in [20, 60, 100, 140, 180, 220]:
            self.sum_of_registers += self.cycle * self.register_X

        if part_2:
            self.draw_pixel()

        # Advance cycle
        self.cycle += 1
        self.wait -= 1

        # Update register when instruction completes
        if self.wait == 0:
            self.register_X += self.waiting_add

    def draw_pixel(self) -> None:
        """Draw one CRT pixel based on sprite position and current cycle.

        The CRT is 40 pixels wide. A 3-pixel wide sprite is centered at
        register X position. If the current pixel position overlaps with
        the sprite, draw '#', otherwise draw '.'.
        """
        sprite_positions = [self.register_X - 1, self.register_X, self.register_X + 1]
        pixel_position = (self.cycle - 1) % 40

        if pixel_position in sprite_positions:
            self.display += "#"

        else:
            self.display += "."

        if len(self.display) == 40:
            logger.info(f"{self.display}")
            self.display = ""


class Solution(SolutionBase):
    """Simulate CPU operations and render CRT display.

    This solution implements a simple CPU simulator that executes addx and noop
    instructions over multiple cycles. Part 1 calculates signal strengths at
    specific cycles (20, 60, 100, 140, 180, 220). Part 2 renders a 40-pixel
    wide CRT display where pixels are lit based on sprite position.
    """

    def solve_part(self, data: list[str], *, part_2: bool = False) -> CPU:
        """Run CPU simulation through all instructions.

        Processes instructions sequentially, advancing the CPU cycle-by-cycle
        until all instructions complete and the CPU becomes idle.

        Args:
            data: List of CPU instructions (addx or noop)
            part_2: If True, enable CRT display rendering

        Returns
        -------
            CPU: CPU instance after all instructions complete with accumulated
                signal strengths and display output
        """
        cpu = CPU()
        instructions = data.copy()

        while len(instructions) > 0 or cpu.wait > 0:
            # If CPU is idle, load next instruction
            if cpu.wait == 0 and len(instructions) > 0:
                line = instructions.pop(0)
                cpu.run(line)

            # Advance one cycle
            cpu.advance_cycle(part_2=part_2)

        return cpu

    def part1(self, data: list[str]) -> int:
        """Calculate sum of signal strengths at cycles 20, 60, 100, 140, 180, 220.

        Signal strength is the cycle number multiplied by register X value during
        that cycle. The sum provides insight into CPU behavior during execution.

        Args:
            data: List of CPU instructions

        Returns
        -------
            int: Sum of signal strengths at the six specified cycles
        """
        cpu = self.solve_part(data)
        return cpu.sum_of_registers

    def part2(self, data: list[str]) -> None:
        """Render CRT display output to console.

        The CRT draws 40x6 pixels, rendering one pixel per cycle. A 3-pixel
        sprite centered at register X determines if each pixel is lit ('#')
        or dark ('.'). The output spells an 8-letter message.

        Args:
            data: List of CPU instructions

        Returns
        -------
            None: Display is printed to console during execution
        """
        _ = self.solve_part(data, part_2=True)
