"""Day 6: Trash Compactor

This module provides the solution for Advent of Code 2025 - Day 6.

It evaluates cephalopod math worksheets presented in a compacted, column-wise
format where numbers and operators are aligned vertically across multiple rows.

The module contains a Solution class that inherits from SolutionBase for parsing
and evaluating these rotated math expressions.
"""

import math

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Evaluate cephalopod math worksheets in compacted column format.

    This solution processes worksheets where numbers and operators are aligned
    vertically in columns. Part 1 evaluates problems by grouping numbers and
    operators by column position. Part 2 handles rotated worksheets by parsing
    columns in reverse order.

    Uses zip transposition to read columns vertically and dynamic expression
    evaluation to compute results with both addition and multiplication operators.
    """

    def part1(self, data: list[str]) -> int:
        """Evaluate compacted worksheet problems reading columns left-to-right.

        Transposes the worksheet rows into columns, where each column represents
        either a multi-digit number or an operator (+ or *). Evaluates each
        vertical math problem using the operator in the final column.

        Args:
            data: List of worksheet rows as strings

        Returns
        -------
            int: Sum of all evaluated math problems from the worksheet
        """
        cols = list(zip(*[row.strip().split() for row in data], strict=False))
        score = 0

        for group in cols:
            nums, operator = group[:-1], group[-1]
            score += eval(operator.join(nums))  # noqa: S307

        return score

    def part2(self, data: str) -> int:
        """Evaluate rotated worksheet problems reading columns right-to-left.

        Parses the worksheet by reversing each row first, then transposing to
        read columns from right to left. Identifies blank columns as problem
        separators and evaluates expressions where '*' means multiplication
        and '+' means addition of all numbers in the problem.

        Args:
            data: Raw worksheet input as a single string

        Returns
        -------
            int: Sum of all evaluated rotated math problems
        """
        lines = data.rstrip("\n").splitlines()

        max_width = max(len(line) for line in lines)
        lines = [line.ljust(max_width) for line in lines]

        operators = []
        problems = []
        current_problem = []

        for col in zip(*[line[::-1] for line in lines], strict=False):
            if all(char == " " for char in col):
                continue

            digit_chars = [char for char in col[:-1] if char != " "]
            has_digits = bool(digit_chars)

            if has_digits:
                current_problem.append(int("".join(digit_chars)))

            if col[-1] != " ":
                operators.append(col[-1])
                problems.append(current_problem)
                current_problem = []

        return sum(
            [
                (math.prod(problem) if operator == "*" else sum(problem))
                for operator, problem in zip(operators, problems, strict=False)
            ]
        )
