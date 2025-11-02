"""
Binary Analyzer and Utility Module
===================================
Provides utility functions for binary-decimal conversion,
binary validation, and analysis (e.g., parity, overflow).

Author: Digital Logic Educational Project
"""

from typing import List, Tuple


class BinaryAnalyzer:
    """
    Provides static methods for binary conversion and analysis.

    This module assists the simulator by converting user-friendly
    decimal inputs into binary lists (and vice-versa) and
    performing common binary analysis tasks.
    """

    @staticmethod
    def decimal_to_binary(n: int, bit_width: int) -> List[int]:
        """
        Converts a decimal integer to a binary list (LSB first).

        Args:
            n: The decimal integer.
            bit_width: The number of bits for the output.

        Returns:
            List[int]: Binary representation (LSB first).
                       Padded with zeros to match bit_width.
        """
        if n < 0:
            # For this project, we handle negative numbers
            # via 2's complement in the arithmetic module.
            # This converter assumes positive input.
            raise ValueError("Decimal to binary conversion input must be non-negative")

        bits = []
        temp_n = n

        # Extract bits using modulo and division
        while temp_n > 0:
            bits.append(temp_n % 2)
            temp_n = temp_n // 2

        # Pad with zeros to reach the desired bit width
        padding = [0] * (bit_width - len(bits))
        result = bits + padding

        # Truncate if n is too large for the bit width
        return result[:bit_width]

    @staticmethod
    def binary_to_decimal(bits: List[int]) -> int:
        """
        Converts a binary list (LSB first) to a decimal integer.

        Args:
            bits: List of bits (LSB first).

        Returns:
            int: The decimal equivalent.
        """
        decimal = 0
        for i, bit in enumerate(bits):
            if bit == 1:
                decimal += (2 ** i)
        return decimal

    @staticmethod
    def format_binary_string(bits: List[int], msb_first: bool = True) -> str:
        """
        Formats a binary list into a readable string.

        Args:
            bits: List of bits (LSB first).
            msb_first: If True, reverses the list for display.

        Returns:
            str: A string representation (e.g., "1011 0101").
        """
        display_bits = bits.copy()
        if msb_first:
            display_bits.reverse()

        s = "".join(map(str, display_bits))

        # Add spaces for readability
        if len(s) > 4:
            parts = [s[i:i + 4] for i in range(0, len(s), 4)]
            return " ".join(parts)
        return s

    @staticmethod
    def check_parity(bits: List[int]) -> int:
        """
        Checks the (even) parity of a binary list.
        Uses XOR to chain the parity check.

        Args:
            bits: List of bits (LSB first).

        Returns:
            int: 0 for even parity, 1 for odd parity.
        """
        # We must use LogicGates per the design document
        from logic_gates import LogicGates

        parity = 0
        for bit in bits:
            parity = LogicGates.XOR(parity, bit)
        return parity

    @staticmethod
    def validate_binary_list(bits: List[int], bit_width: int) -> Tuple[List[int], bool]:
        """
        Ensures a binary list is valid and matches the bit width.

        Args:
            bits: The input list of bits.
            bit_width: The target width.

        Returns:
            Tuple[List[int], bool]: (Padded/truncated list, overflow_status)
        """
        overflow = False
        if len(bits) > bit_width:
            overflow = True
            result = bits[:bit_width]
        else:
            padding = [0] * (bit_width - len(bits))
            result = bits + padding

        return result, overflow


# Test suite
if __name__ == "__main__":
    print("=" * 70)
    print("BINARY ANALYZER TEST SUITE")
    print("=" * 70)

    # Test 1: Decimal to Binary
    print("\n1. Decimal to Binary (8-bit): 42")
    bits_42 = BinaryAnalyzer.decimal_to_binary(42, 8)
    print(f"   List (LSB first): {bits_42}")
    print(f"   Format (MSB first): {BinaryAnalyzer.format_binary_string(bits_42)}")
    # 42 = 32 + 8 + 2 = 0010 1010
    # LSB first: [0, 1, 0, 1, 0, 1, 0, 0]
    assert bits_42 == [0, 1, 0, 1, 0, 1, 0, 0]
    print("   Test PASSED")

    # Test 2: Binary to Decimal
    print("\n2. Binary to Decimal: [1, 0, 1, 1, 0, 0, 0, 1]")
    # 1000 1101 (MSB) = 128 + 8 + 4 + 1 = 141
    bits_141 = [1, 0, 1, 1, 0, 0, 0, 1]
    decimal = BinaryAnalyzer.binary_to_decimal(bits_141)
    print(f"   Decimal: {decimal} (Expected: 141)")
    assert decimal == 141
    print("   Test PASSED")

    # Test 3: Parity Check
    print("\n3. Parity Check: [0, 1, 0, 1, 0, 1, 0, 0]")
    # 3 ones = Odd parity
    parity = BinaryAnalyzer.check_parity(bits_42)
    print(f"   Parity: {parity} (Expected: 1)")
    assert parity == 1
    print("   Test PASSED")

    # Test 4: Formatting
    print("\n4. Formatting (16-bit):")
    bits_16 = BinaryAnalyzer.decimal_to_binary(30000, 16)
    formatted = BinaryAnalyzer.format_binary_string(bits_16)
    print(f"   Input: {bits_16}")
    print(f"   Formatted: {formatted} (Expected: 0111 0101 0011 0000)")
    assert formatted == "0111 0101 0011 0000"
    print("   Test PASSED")