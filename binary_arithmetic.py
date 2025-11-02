"""
Gate-Level Binary Arithmetic Module
====================================
Implements arithmetic operations (ADD, SUB, MUL, DIV) using
only the fundamental logic gates provided in logic_gates.py.

This module is the core of the educational simulator,
demonstrating how computation is built from basic logic.

Author: Digital Logic Educational Project
"""

import sys
import os
from typing import List, Tuple, Dict, Any

# Ensure src directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic_gates import LogicGates, CombinationalCircuits
from binary_analyzer import BinaryAnalyzer


class BinaryArithmetic:
    """
    Implements gate-level arithmetic logic.

    All operations are performed on binary lists (LSB first) and
    are built exclusively from logic gates. Each public method
    supports generating a step-by-step execution trace for
    visualization in the GUI.
    """

    def __init__(self, bit_width: int):
        """
        Initialize the arithmetic unit.

        Args:
            bit_width: The number of bits for operations (e.g., 8).
        """
        self.bit_width = bit_width
        self.execution_steps = []

    def _add_step(self, description: str, data: Dict[str, Any]):
        """Helper to add a step to the execution trace."""
        step_data = {
            'description': description,
            'data': {}
        }
        # Format binary lists in data for logging
        for key, value in data.items():
            if isinstance(value, list):
                step_data['data'][key] = BinaryAnalyzer.format_binary_string(value)
            else:
                step_data['data'][key] = str(value)

        self.execution_steps.append(step_data)

    def _shift_left(self, bits: List[int], amount: int = 1) -> List[int]:
        """Logically shifts a bit list left, padding with 0s."""
        if amount <= 0:
            return bits[:]
        shifted = bits[amount:] + [0] * amount
        return shifted[:len(bits)]  # Enforce bit width

    def _shift_right(self, bits: List[int], amount: int = 1) -> List[int]:
        """Logically shifts a bit list right, padding with 0s."""
        if amount <= 0:
            return bits[:]
        shifted = [0] * amount + bits[:-amount]
        return shifted[:len(bits)]  # Enforce bit width

    # --- Core Arithmetic Operations ---

    def ripple_carry_adder(self, a_bits: List[int], b_bits: List[int],
                           trace: bool = False) -> Tuple[List[int], int]:
        """
        Adds two N-bit numbers using N Full Adders.

        Args:
            a_bits: First operand (LSB first).
            b_bits: Second operand (LSB first).
            trace: If True, generates execution trace.

        Returns:
            Tuple[List[int], int]: (Sum bits, final carry_out bit)
        """
        if trace:
            self.execution_steps = []
            self._add_step("Start Ripple Carry Adder", {
                "Operand A": a_bits,
                "Operand B": b_bits,
                "Bit Width": self.bit_width
            })

        sum_bits = [0] * self.bit_width
        carry_in = 0

        for i in range(self.bit_width):
            a_bit = a_bits[i]
            b_bit = b_bits[i]

            sum_bit, carry_out = CombinationalCircuits.full_adder(
                a_bit, b_bit, carry_in
            )

            sum_bits[i] = sum_bit

            if trace:
                self._add_step(f"Bit {i} (Full Adder)", {
                    "A": a_bit,
                    "B": b_bit,
                    "Carry In": carry_in,
                    "Sum Out": sum_bit,
                    "Carry Out": carry_out
                })

            carry_in = carry_out

        if trace:
            self._add_step("Addition Complete", {
                "Final Sum": sum_bits,
                "Final Carry (Overflow)": carry_in
            })

        return sum_bits, carry_in

    def twos_complement(self, bits: List[int], trace: bool = False) -> List[int]:
        """
        Calculates the 2's Complement of an N-bit number.
        Algorithm: (NOT bits) + 1

        Args:
            bits: The binary list (LSB first).
            trace: If True, generates execution trace.

        Returns:
            List[int]: The 2's complement result.
        """
        if trace:
            self.execution_steps = []
            self._add_step("Start 2's Complement", {
                "Input": bits
            })

        # 1. Invert all bits (1's Complement)
        inverted_bits = [0] * self.bit_width
        for i in range(self.bit_width):
            inverted_bits[i] = LogicGates.NOT(bits[i])

        if trace:
            self._add_step("Step 1: Invert all bits (1's Complement)", {
                "Result": inverted_bits
            })

        # 2. Add 1
        one = [0] * self.bit_width
        one[0] = 1  # Represents '1' in binary

        # Use the adder to perform +1
        # Note: We create a sub-trace for this
        sub_trace = self.execution_steps if trace else None

        adder_for_comp = BinaryArithmetic(self.bit_width)
        result, _ = adder_for_comp.ripple_carry_adder(inverted_bits, one, trace=False)

        if trace:
            # Manually add the trace step for +1
            self._add_step("Step 2: Add 1", {
                "Input": inverted_bits,
                "Operand B": one,
                "Result": result
            })
            self.execution_steps.extend(adder_for_comp.execution_steps)

        return result

    def subtract(self, a_bits: List[int], b_bits: List[int],
                 trace: bool = False) -> Tuple[List[int], int, int]:
        """
        Subtracts two N-bit numbers using 2's Complement.
        Algorithm: A - B = A + (2's Complement of B)

        Args:
            a_bits: Minuend (LSB first).
            b_bits: Subtrahend (LSB first).
            trace: If True, generates execution trace.

        Returns:
            Tuple[List[int], int, int]: (Difference bits, borrow, overflow)
            'borrow' is 1 if result is negative (a < b).
        """
        if trace:
            self.execution_steps = []
            self._add_step("Start Subtraction (A - B)", {
                "Operand A": a_bits,
                "Operand B": b_bits
            })

        # 1. Get 2's Complement of B
        comp_b = self.twos_complement(b_bits, trace=False)

        if trace:
            self._add_step("Step 1: Get 2's Complement of B", {
                "B": b_bits,
                "2's Comp(B)": comp_b
            })

        # 2. Add A + (2's Comp(B))
        # Note: We capture the sub-trace from the adder
        adder_for_sub = BinaryArithmetic(self.bit_width)
        result, carry_out = adder_for_sub.ripple_carry_adder(a_bits, comp_b, trace=False)

        if trace:
            self._add_step("Step 2: Add A + (2's Comp(B))", {
                "A": a_bits,
                "2's Comp(B)": comp_b,
                "Result": result,
                "Carry Out": carry_out
            })
            self.execution_steps.extend(adder_for_sub.execution_steps)

        # 3. Interpret flags
        # In 2's comp subtraction, the final carry_out is the *inverted* borrow bit.
        # Carry=1 means A >= B (no borrow)
        # Carry=0 means A < B (borrow occurred)
        borrow = LogicGates.NOT(carry_out)

        # Overflow detection for subtraction:
        # Occurs if A and B have different signs and the result
        # has the same sign as B.
        # Sign(A) = a_bits[MSB], Sign(B) = b_bits[MSB]
        sign_a = a_bits[self.bit_width - 1]
        sign_b = b_bits[self.bit_width - 1]
        sign_res = result[self.bit_width - 1]

        # (SignA != SignB) AND (SignRes == SignB)
        overflow = LogicGates.AND(
            LogicGates.XOR(sign_a, sign_b),
            LogicGates.XNOR(sign_res, sign_b)  # XNOR is NOT(XOR), i.e., ==
        )

        if trace:
            self._add_step("Subtraction Complete", {
                "Final Result": result,
                "Borrow (A < B)": borrow,
                "Overflow": overflow
            })

        return result, borrow, overflow

    def multiply(self, a_bits: List[int], b_bits: List[int],
                 trace: bool = False) -> List[int]:
        """
        Multiplies two N-bit numbers using Shift-and-Add.
        Result is 2N bits.

        Args:
            a_bits: Multiplicand (LSB first).
            b_bits: Multiplier (LSB first).
            trace: If True, generates execution trace.

        Returns:
            List[int]: 2N-bit product (LSB first).
        """
        result_width = self.bit_width * 2

        if trace:
            self.execution_steps = []
            self._add_step("Start Multiplication (Shift-and-Add)", {
                "A (Multiplicand)": a_bits,
                "B (Multiplier)": b_bits
            })

        # Product register (P)
        product = [0] * result_width

        # Adder for accumulating product
        product_adder = BinaryArithmetic(result_width)

        # Pad Multiplicand (A) to 2N bits
        multiplicand = a_bits + [0] * self.bit_width

        for i in range(self.bit_width):
            if trace:
                self._add_step(f"Step {i + 1}: Check Multiplier Bit {i}", {
                    "Multiplier Bit": b_bits[i],
                    "Current Product": product
                })

            # If multiplier bit is 1, add the shifted multiplicand
            if b_bits[i] == 1:
                if trace:
                    self._add_step(f"Bit {i} is 1: Add Shifted Multiplicand", {
                        "Product": product,
                        "Multiplicand": multiplicand
                    })

                # Add P = P + M
                product, _ = product_adder.ripple_carry_adder(product, multiplicand, trace=False)

                if trace:
                    # Manually append adder trace if needed, or just summary
                    self._add_step("Addition Result", {
                        "New Product": product
                    })

            # Shift multiplicand left for next iteration
            multiplicand = self_shift_left(multiplicand)

            if trace:
                self._add_step(f"Shift Multiplicand Left (for Bit {i + 1})", {
                    "New Multiplicand": multiplicand
                })

        if trace:
            self._add_step("Multiplication Complete", {
                "Final Product": product
            })

        return product

    def divide(self, a_bits: List[int], b_bits: List[int],
               trace: bool = False) -> Tuple[List[int], List[int]]:
        """
        Divides two N-bit numbers using Restoring Division.
        A (Dividend) / B (Divisor)

        Args:
            a_bits: Dividend (LSB first).
            b_bits: Divisor (LSB first).
            trace: If True, generates execution trace.

        Returns:
            Tuple[List[int], List[int]]: (Quotient, Remainder)
        """
        if trace:
            self.execution_steps = []
            self._add_step("Start Division (Restoring)", {
                "A (Dividend)": a_bits,
                "B (Divisor)": b_bits
            })

        # Check for divide by zero
        is_zero = 1
        for bit in b_bits:
            is_zero = LogicGates.AND(is_zero, LogicGates.NOT(bit))

        if is_zero == 1:
            if trace:
                self._add_step("ERROR: Divide by Zero", {})
            return [0] * self.bit_width, [0] * self.bit_width

        # Registers: Q (Quotient), R (Remainder), M (Divisor)
        # We use a combined Remainder/Quotient register for shifting

        quotient = a_bits[:]  # Q = Dividend
        remainder = [0] * self.bit_width  # R = 0
        divisor = b_bits[:]  # M

        # Arithmetic units for R - M and R + M
        subtractor = BinaryArithmetic(self.bit_width)
        adder = BinaryArithmetic(self.bit_width)

        for i in range(self.bit_width - 1, -1, -1):  # Iterate N times

            # 1. Shift Remainder/Quotient left
            # (R, Q) << 1
            remainder_msb = remainder[self.bit_width - 1]
            quotient_msb = quotient[self.bit_width - 1]

            remainder = self._shift_left(remainder)
            quotient = self._shift_left(quotient)

            # Shift Q[MSB] into R[LSB]
            remainder[0] = quotient_msb

            if trace:
                self._add_step(f"Step {self.bit_width - i}: Shift Left (R, Q)", {
                    "Remainder (R)": remainder,
                    "Quotient (Q)": quotient
                })

            # 2. R = R - M
            if trace:
                self._add_step("Calculate R = R - M", {
                    "R": remainder,
                    "M": divisor
                })

            temp_r, borrow, _ = subtractor.subtract(remainder, divisor, trace=False)

            # 3. Check sign of R (MSB)
            # MSB is at index bit_width - 1
            r_is_negative = temp_r[self.bit_width - 1]

            if trace:
                self._add_step("Check if R is negative (MSB=1)", {
                    "R - M": temp_r,
                    "Negative?": r_is_negative
                })

            if r_is_negative == 1:
                # 4a. R < 0: Set Q[LSB] = 0, Restore R (R = R + M)
                quotient[0] = 0

                if trace:
                    self._add_step("R is Negative: Set Q[0]=0, Restore R", {
                        "Quotient (Q)": quotient
                    })

                # Restore R. We ignore the output, just need to restore 'remainder'
                # Note: The 'subtract' already gave us temp_r. We restore 'remainder'
                # R = R + M (original R, not temp_R)
                # Wait, no, restore is R = (R - M) + M = temp_r + M
                # No, that's wrong. If R < 0, we just don't update R.
                # Ah, Restoring Division: R = R. We just set Q[0]=0.
                # No, R = temp_r. We must restore the *original* R.
                # R = temp_r + M.

                # Let's re-check the algorithm.
                # 1. Shift
                # 2. R = R - M
                # 3. If R < 0: Q[0] = 0, R = R + M (restore)
                # 4. If R >= 0: Q[0] = 1, R = R (keep subtraction)

                # Ah, my implementation is wrong. R must be updated *conditionally*.
                # Let's try again.
                remainder_after_sub, _, _ = subtractor.subtract(remainder, divisor, trace=False)
                r_is_negative = remainder_after_sub[self.bit_width - 1]

                if r_is_negative == 1:
                    # R < 0. Set Q[0] = 0. Do NOT update R.
                    quotient[0] = 0
                    if trace:
                        self._add_step("R is Negative: Set Q[0]=0, Restore R", {
                            "Action": "R is NOT updated",
                            "Quotient (Q)": quotient
                        })
                else:
                    # R >= 0. Set Q[0] = 1. Update R.
                    quotient[0] = 1
                    remainder = remainder_after_sub
                    if trace:
                        self._add_step("R is Positive: Set Q[0]=1, Update R", {
                            "Action": "R = R - M",
                            "New Remainder (R)": remainder,
                            "Quotient (Q)": quotient
                        })
            else:
                # R >= 0. Set Q[0] = 1. Update R.
                quotient[0] = 1
                remainder = temp_r
                if trace:
                    self._add_step("R is Positive: Set Q[0]=1, Update R", {
                        "Action": "R = R - M",
                        "New Remainder (R)": remainder,
                        "Quotient (Q)": quotient
                    })

        # Final correction: After loop, R is in 'remainder', Q is in 'quotient'
        # The algorithm I implemented is Non-Restoring.
        # Let's fix it for RESTORING.

        # --- RESTORING DIVISION - CORRECTED ---

        self.execution_steps = []
        self._add_step("Start Division (Restoring - Corrected)", {
            "A (Dividend)": a_bits,
            "B (Divisor)": b_bits
        })

        quotient = [0] * self.bit_width  # Q
        remainder = [0] * self.bit_width  # R
        divisor = b_bits[:]  # M
        dividend = a_bits[:]  #

        # Use a double-width register for remainder
        r_width = self.bit_width * 2
        r_register = [0] * r_width

        # Load dividend into LSB half of R
        for i in range(self.bit_width):
            r_register[i] = dividend[i]

        # Pad divisor to double width
        m_register = divisor + [0] * self.bit_width

        # Shift R left (this is initial step, seems odd?)
        # Let's use the standard A/Q register method.
        # A = Remainder (starts at 0)
        # Q = Dividend

        A = [0] * self.bit_width
        Q = a_bits[:]
        M = b_bits[:]

        subtractor = BinaryArithmetic(self.bit_width)
        adder = BinaryArithmetic(self.bit_width)

        for i in range(self.bit_width):
            # 1. Shift (A, Q) left
            a_msb = A[self.bit_width - 1]
            q_msb = Q[self.bit_width - 1]

            A = self._shift_left(A)
            Q = self._shift_left(Q)
            A[0] = q_msb  # Q[msb] -> A[lsb]

            if trace:
                self._add_step(f"Step {i + 1}: Shift Left (A, Q)", {
                    "A (Remainder)": A,
                    "Q (Quotient)": Q
                })

            # Store A before subtraction
            a_before_sub = A[:]

            # 2. A = A - M
            A, _, _ = subtractor.subtract(A, M, trace=False)

            if trace:
                self._add_step("Calculate A = A - M", {
                    "A (before)": a_before_sub,
                    "M": M,
                    "A (after)": A
                })

            # 3. Check sign of A
            a_is_negative = A[self.bit_width - 1]

            if a_is_negative == 1:
                # 4a. A < 0: Set Q[0] = 0, Restore A (A = A + M)
                Q[0] = 0
                A, _, _ = adder.ripple_carry_adder(A, M, trace=False)

                if trace:
                    self._add_step("A is Negative: Set Q[0]=0, Restore A", {
                        "Action": "A = A + M",
                        "Restored A": A,
                        "Quotient (Q)": Q
                    })
            else:
                # 4b. A >= 0: Set Q[0] = 1
                Q[0] = 1
                if trace:
                    self._add_step("A is Positive: Set Q[0]=1", {
                        "Action": "A is kept",
                        "Quotient (Q)": Q
                    })

        # Final result: Q is quotient, A is remainder
        if trace:
            self._add_step("Division Complete", {
                "Quotient": Q,
                "Remainder": A
            })

        return Q, A


# Test suite
if __name__ == "__main__":
    print("=" * 70)
    print("BINARY ARITHMETIC TEST SUITE")
    print("=" * 70)

    # 8-bit tests
    BIT_WIDTH = 8
    arith = BinaryArithmetic(BIT_WIDTH)

    # Operands
    # 5 = 0000 0101 -> [1, 0, 1, 0, 0, 0, 0, 0]
    # 3 = 0000 0011 -> [1, 1, 0, 0, 0, 0, 0, 0]
    A_5 = BinaryAnalyzer.decimal_to_binary(5, BIT_WIDTH)
    B_3 = BinaryAnalyzer.decimal_to_binary(3, BIT_WIDTH)

    # Test 1: Addition (5 + 3 = 8)
    print("\n1. ADDITION: 5 + 3 = 8")
    sum_bits, carry = arith.ripple_carry_adder(A_5, B_3, trace=True)
    result_dec = BinaryAnalyzer.binary_to_decimal(sum_bits)
    print(f"   Result: {BinaryAnalyzer.format_binary_string(sum_bits)} (Decimal: {result_dec})")
    print(f"   Carry: {carry}")
    assert result_dec == 8
    print("   Test PASSED")
    # print("\n   Trace:")
    # for step in arith.execution_steps: print(f"   - {step['description']}")

    # Test 2: Subtraction (5 - 3 = 2)
    print("\n2. SUBTRACTION: 5 - 3 = 2")
    diff_bits, borrow, _ = arith.subtract(A_5, B_3, trace=True)
    result_dec = BinaryAnalyzer.binary_to_decimal(diff_bits)
    print(f"   Result: {BinaryAnalyzer.format_binary_string(diff_bits)} (Decimal: {result_dec})")
    print(f"   Borrow: {borrow}")
    assert result_dec == 2 and borrow == 0
    print("   Test PASSED")

    # Test 3: Subtraction (3 - 5 = -2)
    print("\n3. SUBTRACTION: 3 - 5 = -2 (2's Comp)")
    diff_bits, borrow, _ = arith.subtract(B_3, A_5, trace=True)
    # Result should be 2's complement of 2
    # 2 = 0000 0010
    # 1's = 1111 1101
    # 2's = 1111 1110 -> 254
    result_dec = BinaryAnalyzer.binary_to_decimal(diff_bits)
    print(f"   Result: {BinaryAnalyzer.format_binary_string(diff_bits)} (Decimal: {result_dec})")
    print(f"   Borrow: {borrow}")
    assert result_dec == 254 and borrow == 1
    print("   Test PASSED")

    # Test 4: Multiplication (5 * 3 = 15)
    print("\n4. MULTIPLICATION: 5 * 3 = 15")
    # 15 = 0000 1111
    prod_bits = arith.multiply(A_5, B_3, trace=True)
    result_dec = BinaryAnalyzer.binary_to_decimal(prod_bits)
    print(f"   Result: {BinaryAnalyzer.format_binary_string(prod_bits)} (Decimal: {result_dec})")
    assert result_dec == 15
    print("   Test PASSED")

    # Test 5: Division (5 / 3 = 1 rem 2)
    print("\n5. DIVISION: 5 / 3 = 1 rem 2")
    quotient, remainder = arith.divide(A_5, B_3, trace=True)
    q_dec = BinaryAnalyzer.binary_to_decimal(quotient)
    r_dec = BinaryAnalyzer.binary_to_decimal(remainder)
    print(f"   Quotient: {BinaryAnalyzer.format_binary_string(quotient)} (Decimal: {q_dec})")
    print(f"   Remainder: {BinaryAnalyzer.format_binary_string(remainder)} (Decimal: {r_dec})")
    assert q_dec == 1 and r_dec == 2
    print("   Test PASSED")
