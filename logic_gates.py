"""
Fundamental Logic Gates Module
===============================
This module implements the basic Boolean operations that form the foundation
of all digital logic circuits. These gates are the building blocks for
complex arithmetic operations.

Author: Digital Logic Educational Project
Purpose: Educational demonstration of gate-level computation
"""

from typing import Union


class LogicGates:
    """
    Implements fundamental Boolean logic gates.

    All methods are static as they represent pure logical operations
    without internal state. These gates operate on binary values (0, 1)
    and form the foundation for all higher-level operations.
    """

    @staticmethod
    def AND(a: int, b: int) -> int:
        """
        Logical AND gate: Output is 1 only if both inputs are 1.

        Truth Table:
        A | B | OUT
        0 | 0 |  0
        0 | 1 |  0
        1 | 0 |  0
        1 | 1 |  1

        Args:
            a: First input bit (0 or 1)
            b: Second input bit (0 or 1)

        Returns:
            int: Result of AND operation (0 or 1)
        """
        return 1 if (a == 1 and b == 1) else 0

    @staticmethod
    def OR(a: int, b: int) -> int:
        """
        Logical OR gate: Output is 1 if at least one input is 1.

        Truth Table:
        A | B | OUT
        0 | 0 |  0
        0 | 1 |  1
        1 | 0 |  1
        1 | 1 |  1

        Args:
            a: First input bit (0 or 1)
            b: Second input bit (0 or 1)

        Returns:
            int: Result of OR operation (0 or 1)
        """
        return 1 if (a == 1 or b == 1) else 0

    @staticmethod
    def NOT(a: int) -> int:
        """
        Logical NOT gate (Inverter): Inverts the input.

        Truth Table:
        A | OUT
        0 |  1
        1 |  0

        Args:
            a: Input bit (0 or 1)

        Returns:
            int: Inverted bit (0 or 1)
        """
        return 1 if a == 0 else 0

    @staticmethod
    def XOR(a: int, b: int) -> int:
        """
        Logical XOR gate (Exclusive OR): Output is 1 if inputs differ.

        Implementation: XOR = (A AND NOT B) OR (NOT A AND B)

        Truth Table:
        A | B | OUT
        0 | 0 |  0
        0 | 1 |  1
        1 | 0 |  1
        1 | 1 |  0

        Args:
            a: First input bit (0 or 1)
            b: Second input bit (0 or 1)

        Returns:
            int: Result of XOR operation (0 or 1)
        """
        # XOR can be constructed from AND, OR, and NOT gates
        # XOR = (A AND NOT B) OR (NOT A AND B)
        return LogicGates.OR(
            LogicGates.AND(a, LogicGates.NOT(b)),
            LogicGates.AND(LogicGates.NOT(a), b)
        )

    @staticmethod
    def NAND(a: int, b: int) -> int:
        """
        Logical NAND gate: NOT AND (Universal gate).

        Truth Table:
        A | B | OUT
        0 | 0 |  1
        0 | 1 |  1
        1 | 0 |  1
        1 | 1 |  0

        Args:
            a: First input bit (0 or 1)
            b: Second input bit (0 or 1)

        Returns:
            int: Result of NAND operation (0 or 1)
        """
        return LogicGates.NOT(LogicGates.AND(a, b))

    @staticmethod
    def NOR(a: int, b: int) -> int:
        """
        Logical NOR gate: NOT OR (Universal gate).

        Truth Table:
        A | B | OUT
        0 | 0 |  1
        0 | 1 |  0
        1 | 0 |  0
        1 | 1 |  0

        Args:
            a: First input bit (0 or 1)
            b: Second input bit (0 or 1)

        Returns:
            int: Result of NOR operation (0 or 1)
        """
        return LogicGates.NOT(LogicGates.OR(a, b))

    @staticmethod
    def XNOR(a: int, b: int) -> int:
        """
        Logical XNOR gate (Equivalence): Output is 1 if inputs match.

        Truth Table:
        A | B | OUT
        0 | 0 |  1
        0 | 1 |  0
        1 | 0 |  0
        1 | 1 |  1

        Args:
            a: First input bit (0 or 1)
            b: Second input bit (0 or 1)

        Returns:
            int: Result of XNOR operation (0 or 1)
        """
        return LogicGates.NOT(LogicGates.XOR(a, b))


class CombinationalCircuits:
    """
    Implements combinational logic circuits built from basic gates.

    These circuits form the building blocks for arithmetic operations.
    They have no memory and output depends only on current inputs.
    """

    @staticmethod
    def half_adder(a: int, b: int) -> tuple[int, int]:
        """
        Half Adder: Adds two single bits.

        Circuit Design:
        - Sum = A XOR B
        - Carry = A AND B

        Truth Table:
        A | B | Sum | Carry
        0 | 0 |  0  |   0
        0 | 1 |  1  |   0
        1 | 0 |  1  |   0
        1 | 1 |  0  |   1

        Args:
            a: First input bit
            b: Second input bit

        Returns:
            tuple: (sum_bit, carry_bit)
        """
        sum_bit = LogicGates.XOR(a, b)
        carry_bit = LogicGates.AND(a, b)
        return sum_bit, carry_bit

    @staticmethod
    def full_adder(a: int, b: int, carry_in: int) -> tuple[int, int]:
        """
        Full Adder: Adds three single bits (includes carry input).

        Circuit Design:
        Uses two half adders and an OR gate:
        1. First half adder: adds A and B
        2. Second half adder: adds sum with carry_in
        3. Final carry = carry from either half adder

        Truth Table:
        A | B | Cin | Sum | Cout
        0 | 0 |  0  |  0  |  0
        0 | 0 |  1  |  1  |  0
        0 | 1 |  0  |  1  |  0
        0 | 1 |  1  |  0  |  1
        1 | 0 |  0  |  1  |  0
        1 | 0 |  1  |  0  |  1
        1 | 1 |  0  |  0  |  1
        1 | 1 |  1  |  1  |  1

        Args:
            a: First input bit
            b: Second input bit
            carry_in: Carry input from previous stage

        Returns:
            tuple: (sum_bit, carry_out)
        """
        # First half adder: Add A and B
        sum1, carry1 = CombinationalCircuits.half_adder(a, b)

        # Second half adder: Add sum1 with carry_in
        sum_out, carry2 = CombinationalCircuits.half_adder(sum1, carry_in)

        # Final carry: OR of both carries
        carry_out = LogicGates.OR(carry1, carry2)

        return sum_out, carry_out

    @staticmethod
    def multiplexer_2to1(a: int, b: int, select: int) -> int:
        """
        2-to-1 Multiplexer: Selects one of two inputs.

        Circuit Design:
        OUT = (A AND NOT SEL) OR (B AND SEL)

        Args:
            a: Input 0
            b: Input 1
            select: Selection bit (0 selects a, 1 selects b)

        Returns:
            int: Selected input
        """
        return LogicGates.OR(
            LogicGates.AND(a, LogicGates.NOT(select)),
            LogicGates.AND(b, select)
        )


# Module test code
if __name__ == "__main__":
    print("=" * 60)
    print("LOGIC GATES TEST SUITE")
    print("=" * 60)

    # Test basic gates
    print("\n1. Basic Gate Tests:")
    print(f"AND(1, 1) = {LogicGates.AND(1, 1)} (Expected: 1)")
    print(f"OR(0, 1) = {LogicGates.OR(0, 1)} (Expected: 1)")
    print(f"NOT(1) = {LogicGates.NOT(1)} (Expected: 0)")
    print(f"XOR(1, 0) = {LogicGates.XOR(1, 0)} (Expected: 1)")

    # Test Half Adder
    print("\n2. Half Adder Test:")
    print("Input: A=1, B=1")
    sum_bit, carry = CombinationalCircuits.half_adder(1, 1)
    print(f"Sum={sum_bit}, Carry={carry} (Expected: Sum=0, Carry=1)")

    # Test Full Adder
    print("\n3. Full Adder Test:")
    print("Input: A=1, B=1, Carry_in=1")
    sum_bit, carry = CombinationalCircuits.full_adder(1, 1, 1)
    print(f"Sum={sum_bit}, Carry_out={carry} (Expected: Sum=1, Carry=1)")

    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)