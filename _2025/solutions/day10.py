"""Day 10: Factory

This module provides the solution for Advent of Code 2025 - Day 10.

It works with incomplete machine manuals that only list indicator light
diagrams, button wiring schematics, and joltage requirements.

Part 1 ignores joltages and finds the minimum number of button presses
needed to reach each machine's target light pattern from all-off.
Part 2 uses the same button sets but treats joltages as a linear system
to satisfy numeric requirements for each machine.
"""

from collections import deque
import math
import re
from typing import ClassVar

from numpy import transpose
from scipy.optimize import linprog

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Configure factory machines by solving light and joltage constraints.

    Each input line encodes a single machine description with three parts:
    - Square brackets []: the target indicator light pattern ('.' = off, '#' = on)
    - Parentheses ()   : button wiring schematics listing which lights they toggle
    - Curly braces {}  : joltage requirements for the machine

    Part 1 starts from all lights off and uses BFS over light states to find
    the fewest presses to reach the target pattern, ignoring joltages.
    Part 2 models joltages as a linear integer system and uses a solver to
    find the minimum number of button presses that satisfies the target
    joltage vector.
    """

    REGEX: ClassVar[re.Pattern[str]] = re.compile(r"\[([^\]]*)]|\(([^)]*)\)|\{([^}]*)}")

    def parse_data(self, line: str) -> tuple[list[str], list[tuple[int, ...]], list[int]]:
        """Parse a single machine description into lights, buttons, and joltage.

        The line must contain exactly one indicator light diagram in square
        brackets, zero or more button wiring schematics in parentheses, and
        one joltage requirements list in curly braces.

        Args:
            line: Raw input line describing a machine

        Returns
        -------
            tuple[list[str], list[tuple[int, ...]], list[int]]:
                - List of characters for the light diagram
                - List of buttons, each as a tuple of light indices they toggle
                - List of joltage targets for the machine
        """
        square: list[str] = []
        parentheses: list[tuple[int, ...]] = []
        curly: list[int] = []

        for match in self.REGEX.finditer(line):
            gr1, gr2, gr3 = match.groups()
            if gr1 is not None:
                square = list(gr1)
            elif gr2 is not None:
                parentheses.append(tuple(map(int, gr2.split(","))))
            elif gr3 is not None:
                curly = list(map(int, gr3.split(",")))

        if square is None or curly is None:
            err_msg = f"Invalid line (missing [] or {{}}): {line!r}"
            raise ValueError(err_msg)

        if curly:
            useful_parentheses = [btn for btn in parentheses if any(curly[idx] > 0 for idx in btn)]
            parentheses = useful_parentheses

        return square, parentheses, curly

    def to_light_state(self, lights: list[str]) -> tuple[int, ...]:
        """Convert a light pattern ('.'/'#') into a boolean tuple state."""
        return tuple(ch == "#" for ch in lights)

    def apply_button(self, state: tuple[int, ...], button: tuple[int, ...]) -> tuple[int, ...]:
        """Toggle a set of indicator lights according to a button wiring.

        Args:
            state: Current boolean light state as a tuple
            button: Tuple of indices of lights to toggle

        Returns
        -------
            tuple[int, ...]: New light state after pressing the button once
        """
        arr = list(state)
        for idx in button:
            arr[idx] = not arr[idx]

        return tuple(arr)

    def min_presses_for_lights(self, lights: list[str], buttons: list[tuple[int, ...]]) -> int:
        """Compute minimum presses to reach target light pattern using BFS.

        Treats each distinct light state as a node in a graph and each button
        press as an edge to a new state. Performs a breadth-first search from
        the all-off state until the target pattern is reached.

        Args:
            lights: Target light diagram as list of '.' and '#'
            buttons: List of button wirings as tuples of indices

        Returns
        -------
            int: Minimum number of button presses to reach target pattern

        Raises
        ------
            ValueError: If the target pattern cannot be reached
        """
        goal = self.to_light_state(lights)
        start: tuple[int, ...] = tuple(False for _ in goal)

        q: deque[tuple[tuple[int, ...], int]] = deque()
        q.append((start, 0))
        visited: set[tuple[int, ...]] = set()

        while q:
            curr, steps = q.popleft()
            if curr == goal:
                return steps

            if curr in visited:
                continue

            visited.add(curr)

            for btn in buttons:
                nxt = self.apply_button(curr, btn)
                if nxt not in visited:
                    q.append((nxt, steps + 1))

        err_msg = f"Unreachable lights pattern {lights} with given buttons"
        raise ValueError(err_msg)

    def button_to_vector(self, button: tuple[int, ...], num_slots: int) -> list[int]:
        """Convert a button wiring into a vector for the joltage equation system.

        Args:
            button: Tuple of indices affected by this button
            num_slots: Length of the target joltage vector

        Returns
        -------
            list[int]: Vector with 1s at affected indices and 0 otherwise
        """
        vec = [0] * num_slots
        for idx in button:
            vec[idx] = 1
        return vec

    def min_presses_for_machine(
        self,
        buttons: list[tuple[int, ...]],
        target: list[int],
    ) -> int:
        """Compute minimum button presses to satisfy machine joltage constraints.

        Models each button as contributing a fixed amount to one or more joltage
        slots and solves a linear system with integrality constraints where
        the objective is to minimize the total number of button presses.

        Args:
            buttons: List of button wirings as tuples of indices
            target: Desired joltage values for the machine

        Returns
        -------
            int: Minimum number of button presses to meet the joltage target

        Raises
        ------
            ValueError: If no combination of button presses can satisfy target
        """
        if not target:
            return 0

        N = len(buttons)  # noqa: N806
        num_jolt = len(target)

        if N == 0:
            if any(t != 0 for t in target):
                err_msg = f"Unreachable target {target} with given buttons"
                raise ValueError(err_msg)
            return 0

        # Objective: minimize total button presses
        c = [1] * N

        # Build equality constraints: sum(button_vectors * presses) = target
        A_eq = [self.button_to_vector(btn, num_jolt) for btn in buttons]  # noqa: N806
        A_eq = transpose(A_eq)  # noqa: N806
        b_eq = target
        integrality = [1] * N

        res = linprog(
            c,
            A_eq=A_eq,
            b_eq=b_eq,
            integrality=integrality,
        )

        if not res.success:
            err_msg = f"Unreachable target {target} with given buttons"
            raise ValueError(err_msg)

        return int(math.ceil(sum(res.x)))

    def part1(self, data: list[str]) -> int:
        """Sum minimum button presses to match indicator lights for all machines.

        For each machine, parses the light diagram and button schematics, then
        runs a BFS to find the fewest presses needed to reach the target
        light configuration from all-off, ignoring joltage requirements.

        Args:
            data: List of machine descriptions, one per line

        Returns
        -------
            int: Total of minimum button presses across all machines
        """
        score = 0

        for line in data:
            lights, buttons, _ = self.parse_data(line)
            score += self.min_presses_for_lights(lights, buttons)

        return score

    def part2(self, data: list[str]) -> int:
        """Sum minimum button presses to satisfy joltage requirements for all machines.

        For each machine, parses the button schematics and joltage requirements.
        It then builds and solves an integer linear program to find the minimum
        total presses needed so the combined button effects match the joltage
        target exactly.

        Args:
            data: List of machine descriptions, one per line

        Returns
        -------
            int: Total minimum button presses to satisfy all joltage constraints
        """
        score = 0

        for line in data:
            _, buttons, joltage = self.parse_data(line)
            score += self.min_presses_for_machine(buttons, joltage)

        return score
