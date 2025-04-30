from math import lcm
import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    regex = r"(\w{3})\s*=\s*\((\w{3}),\s*(\w{3})\)"

    def parse_to_dict(self, data: list[str]) -> dict[str, tuple[str, str]]:
        return {match[1]: (match[2], match[3]) for s in data if (match := re.match(self.regex, s))}

    def part1(self, data: list[str]) -> int:
        instructions = [1 if x == "R" else 0 for x in data[0]]
        nodes = self.parse_to_dict(data[2:])

        # Start at 'AAA'
        position = "AAA"
        steps = 0

        # Use direct list indexing for instruction lookup
        while position != "ZZZ":
            direction = instructions[steps % len(instructions)]
            position = nodes[position][direction]
            steps += 1

        return steps

    def part2(self, data: list[str]) -> int:
        instructions = [1 if x == "R" else 0 for x in data[0]]
        nodes = self.parse_to_dict(data[2:])

        # Find all starting positions (nodes ending in 'A')
        positions = [node for node in nodes if node.endswith("A")]

        # Find cycle length for each starting position
        cycles = []
        for position in positions:
            steps = 0
            current = position

            # Keep track of (position, instruction_index) states we've seen
            seen = {}

            while True:
                instruction_idx = steps % len(instructions)
                state = (current, instruction_idx)

                # If we've found a Z-ending node, record the steps and break
                if current.endswith("Z"):
                    cycles.append(steps)
                    break

                # If we've seen this state before, we're in a cycle
                if state in seen:
                    break

                seen[state] = steps
                current = nodes[current][instructions[instruction_idx]]
                steps += 1

        # Calculate the least common multiple of all cycle lengths
        return lcm(*cycles)
