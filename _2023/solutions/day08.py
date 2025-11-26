"""Day 8: Haunted Wasteland

This module provides the solution for Advent of Code 2023 - Day 8.

It handles navigation through a network of labeled nodes using left/right
instructions. The puzzle involves following a repeating sequence of directions
to traverse from starting nodes to ending nodes in the network.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse the network map, navigate from node to node, and find the number
of steps required to reach destination nodes for both single-path and multi-path
scenarios.
"""

from math import lcm
import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Navigate through a network of nodes using repeating instructions.

    This solution handles two types of navigation:
    Part 1 follows a single path from node AAA to node ZZZ using the given
    left/right instructions. Part 2 simultaneously follows multiple paths
    starting from all nodes ending in 'A' until all paths reach nodes ending
    in 'Z', using cycle detection and least common multiple calculations.

    The solution uses regex parsing to extract node connections and implements
    efficient cycle detection for the multi-path scenario.
    """

    regex = r"(\w{3})\s*=\s*\((\w{3}),\s*(\w{3})\)"

    def parse_to_dict(self, data: list[str]) -> dict[str, tuple[str, str]]:
        """Parse network map into a dictionary of node connections.

        Each line is parsed using regex to extract node names and their left/right
        connections. The result maps each node to a tuple of (left_node, right_node).

        Args:
            data (list[str]): List of strings representing node connections

        Returns
        -------
            Dictionary mapping node names to (left_node, right_node) tuples
        """
        return {match[1]: (match[2], match[3]) for s in data if (match := re.match(self.regex, s))}

    def part1(self, data: list[str]) -> int:
        """Calculate steps required to navigate from AAA to ZZZ.

        Follows the left/right instructions repeatedly, starting at node AAA
        and continuing until reaching node ZZZ. Instructions are represented
        as 0 for left and 1 for right for efficient tuple indexing.

        Args:
            data (list[str]): List of strings containing instructions and node map

        Returns
        -------
            Number of steps required to reach ZZZ from AAA
        """
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
        """Calculate steps for all paths starting with 'A' to reach nodes ending with 'Z'.

        Finds all starting nodes (ending in 'A') and determines the cycle length
        for each path to reach a node ending in 'Z'. The answer is the least
        common multiple of all cycle lengths, representing when all paths
        simultaneously reach their destination nodes.

        Args:
            data (list[str]): List of strings containing instructions and node map

        Returns
        -------
            Number of steps until all paths simultaneously reach nodes ending in 'Z'
        """
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
