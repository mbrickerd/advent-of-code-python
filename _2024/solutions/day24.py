"""Day 24: Crossed Wires

This module provides the solution for Advent of Code 2024 - Day 24.

It solves a puzzle about analyzing and debugging a digital circuit composed of
boolean logic gates (AND, OR, XOR). The circuit is supposed to implement a binary
adder, but some output wires have been swapped, causing incorrect results.

The solution involves simulating the circuit to determine output values and
analyzing the circuit structure to identify misconnected wires that need to be
swapped to fix the adder implementation.

The module contains Connection and Circuit dataclasses for representing the
circuit structure, a CircuitValidator for verifying correct adder wiring, and
a Solution class that inherits from SolutionBase.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
import re

from aoc.models.base import SolutionBase


@dataclass
class Connection:
    """Represents a logic gate connection in the circuit.

    Attributes
    ----------
        input1 (str): First input wire identifier
        gate (str): Gate operation type (AND, OR, XOR)
        input2 (str): Second input wire identifier
        output (str): Output wire identifier
    """

    input1: str
    gate: str
    input2: str
    output: str

    def __str__(self) -> str:
        """Generate string representation of the connection.

        Returns
        -------
            String in format 'input1 gate input2 -> output'
        """
        return f"{self.input1} {self.gate} {self.input2} -> {self.output}"


@dataclass
class Circuit:
    """Represents a digital circuit with wires and logic gate connections.

    Attributes
    ----------
        wires (dict[str, int]): Maps wire identifiers to their values (-1 for unknown)
        connections (list[Connection]): Logic gate connections in the circuit
        operators (dict[str, Callable]): Maps gate types to their logic functions
    """

    wires: dict[str, int]
    connections: list[Connection] = field(default_factory=list)
    operators: dict[str, Callable[[int, int], int]] = field(
        default_factory=lambda: {
            "OR": lambda x, y: x | y,
            "AND": lambda x, y: x & y,
            "XOR": lambda x, y: x ^ y,
        }
    )

    def calc(self, wire: str) -> int:
        """Calculate the value of a wire recursively based on its inputs.

        Recursively evaluates the circuit by finding the gate that outputs to
        this wire and computing its inputs first.

        Args:
            wire (str): Identifier of the wire to calculate

        Returns
        -------
            Computed value for the wire (0 or 1)

        Raises
        ------
            ValueError: If no connection is found for the wire
        """
        if self.wires[wire] != -1:
            return self.wires[wire]

        for conn in self.connections:
            if conn.output == wire:
                x = self.calc(conn.input1)
                y = self.calc(conn.input2)
                self.wires[wire] = self.operators[conn.gate](x, y)
                return self.wires[wire]

        err_msg = f"No connection found for wire {wire}"
        raise ValueError(err_msg)

    def execute(self) -> list[int]:
        """Execute the circuit and return the z-wire values.

        Computes all output wires (those starting with 'z') and returns their
        values in order from most significant to least significant bit.

        Returns
        -------
            List of z-wire values in reverse order (MSB first)
        """
        z_values = []
        i = 0

        while True:
            key = f"z{i:02}"
            if key not in self.wires or all(conn.output != key for conn in self.connections):
                break

            z_values.append(self.calc(key))
            i += 1

        return z_values[::-1]  # Reverse for correct order (MSB first)


class CircuitValidator:
    """Validates circuit structure for correct binary adder implementation.

    This helper class checks that the circuit correctly implements a ripple-carry
    adder by validating that each bit position follows the expected pattern of
    XOR, AND, and OR gates.
    """

    def __init__(self, formulas: dict[str, tuple[str, str, str]]):
        """Initialize the validator with circuit formulas.

        Args:
            formulas (dict): Maps output wires to (operation, input1, input2) tuples
        """
        self.formulas = formulas

    def make_wire(self, char: str, num: int) -> str:
        """Create a wire identifier with the given character and number.

        Args:
            char (str): Character prefix for the wire ('x', 'y', or 'z')
            num (int): Wire number to append

        Returns
        -------
            Wire identifier in format 'char##'
        """
        return f"{char}{num:02}"

    def validate_z(self, wire: str, num: int) -> bool:
        """Validate that a z-wire correctly implements the sum bit.

        Args:
            wire (str): Wire identifier to validate
            num (int): Expected bit position for the wire

        Returns
        -------
            True if wire is correctly connected as an adder output
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if op != "XOR":
            return False

        if num == 0:
            return sorted([x, y]) == ["x00", "y00"]

        return (
            self.validate_intermediate_xor(x, num)
            and self.validate_carry_bit(y, num)
            or self.validate_intermediate_xor(y, num)
            and self.validate_carry_bit(x, num)
        )

    def validate_intermediate_xor(self, wire: str, num: int) -> bool:
        """Validate an intermediate XOR gate that combines input bits.

        Args:
            wire (str): Wire identifier to validate
            num (int): Expected bit position for the wire

        Returns
        -------
            True if gate correctly XORs corresponding x and y inputs
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if op != "XOR":
            return False

        return sorted([x, y]) == [self.make_wire("x", num), self.make_wire("y", num)]

    def validate_carry_bit(self, wire: str, num: int) -> bool:
        """Validate that a wire correctly implements the carry bit logic.

        Args:
            wire (str): Wire identifier to validate
            num (int): Expected bit position for the wire

        Returns
        -------
            True if carry bit logic is correctly configured
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if num == 1:
            if op != "AND":
                return False

            return sorted([x, y]) == ["x00", "y00"]

        if op != "OR":
            return False

        return (
            self.validate_direct_carry(x, num - 1)
            and self.validate_recarry(y, num - 1)
            or self.validate_direct_carry(y, num - 1)
            and self.validate_recarry(x, num - 1)
        )

    def validate_direct_carry(self, wire: str, num: int) -> bool:
        """Validate a direct carry gate (AND of input bits).

        Args:
            wire (str): Wire identifier to validate
            num (int): Expected bit position for the wire

        Returns
        -------
            True if direct carry AND gate is correctly configured
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if op != "AND":
            return False

        return sorted([x, y]) == [self.make_wire("x", num), self.make_wire("y", num)]

    def validate_recarry(self, wire: str, num: int) -> bool:
        """Validate a recarry gate (propagated carry from previous bit).

        Args:
            wire (str): Wire identifier to validate
            num (int): Expected bit position for the wire

        Returns
        -------
            True if recarry AND gate is correctly configured
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if op != "AND":
            return False

        return (
            self.validate_intermediate_xor(x, num)
            and self.validate_carry_bit(y, num)
            or self.validate_intermediate_xor(y, num)
            and self.validate_carry_bit(x, num)
        )

    def validate(self, num: int) -> bool:
        """Validate the circuit at a specific bit position.

        Args:
            num (int): Bit position to validate

        Returns
        -------
            True if bit position is correctly configured
        """
        return self.validate_z(self.make_wire("z", num), num)

    def progress(self) -> int:
        """Determine how many consecutive bits are correctly validated.

        Returns
        -------
            Number of consecutive valid bit positions starting from zero
        """
        i = 0
        while self.validate(i):
            i += 1

        return i


class Solution(SolutionBase):
    """Simulate and debug digital circuits implementing binary addition.

    This solution implements circuit analysis algorithms:
    - Part 1: Simulate the circuit to compute the decimal output value
    - Part 2: Identify swapped wires by validating adder structure

    The solution parses circuit definitions, simulates gate execution, and
    validates that the circuit correctly implements a ripple-carry adder.
    """

    def parse_data(self, data: list[str]) -> Circuit:
        """Parse input data into a Circuit object.

        Extracts initial wire values and gate connections from the input format,
        creating a complete circuit representation.

        Args:
            data (list[str]): Input lines with wire values and gate definitions

        Returns
        -------
            Circuit object with initialized wires and connections
        """
        separator_idx = data.index("")
        wires = {}

        for line in data[:separator_idx]:
            wire, val = line.split(": ")
            wires[wire] = int(val)

        connections = []
        for line in data[separator_idx + 1 :]:
            match = re.match(r"(\w+) (OR|AND|XOR) (\w+) -> (\w+)", line)
            if match:
                input1, gate, input2, output = match.groups()

                for wire in [input1, input2, output]:
                    if wire not in wires:
                        wires[wire] = -1

                connections.append(Connection(input1, gate, input2, output))

        return Circuit(wires, connections)

    def part1(self, data: list[str]) -> int:
        """Simulate the circuit and compute the decimal output value.

        Executes all gates in the circuit to determine the final values of all
        z-wires, then converts the binary representation to decimal.

        Args:
            data (list[str]): Input lines with wire values and gate definitions

        Returns
        -------
            Decimal value represented by the binary output on z-wires
        """
        circuit = self.parse_data(data)
        z_values = circuit.execute()
        return int("".join(map(str, z_values)), 2)

    def part2(self, data: list[str]) -> str:
        """Identify swapped output wires by validating adder structure.

        Analyzes the circuit to find pairs of gates with swapped outputs that
        prevent the circuit from correctly implementing a binary adder. Uses
        iterative validation and swapping to identify all four pairs.

        Args:
            data (list[str]): Input lines with gate definitions

        Returns
        -------
            Comma-separated string of sorted wire identifiers that are swapped
        """
        formulas = {}
        separator_idx = data.index("")

        for line in data[separator_idx + 1 :]:
            match = re.match(r"(\w+) (OR|AND|XOR) (\w+) -> (\w+)", line)
            if match:
                input1, gate, input2, output = match.groups()
                formulas[output] = (gate, input1, input2)

        validator = CircuitValidator(formulas)
        swaps = []

        for _ in range(4):
            baseline = validator.progress()
            for x in formulas:
                for y in formulas:
                    if x == y:
                        continue
                    formulas[x], formulas[y] = formulas[y], formulas[x]
                    if validator.progress() > baseline:
                        break
                    formulas[x], formulas[y] = formulas[y], formulas[x]
                else:
                    continue
                break
            swaps += [x, y]

        return ",".join(sorted(swaps))
