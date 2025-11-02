"""
Arithmetic Logic Unit (ALU) Simulator
======================================
Simulates a mini ALU and its Control Unit. The ALU performs
operations based on opcodes and sets status flags.

This module integrates the BinaryArithmetic and LogicGates
modules to create a higher-level computational unit.

Author: Digital Logic Educational Project
"""

import sys
import os
from typing import List, Dict, Any, Optional

# Ensure src directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic_gates import LogicGates
from binary_arithmetic import BinaryArithmetic
from binary_analyzer import BinaryAnalyzer


class ALUFlags:
    """
    Manages the CPU status flags (Zero, Carry, Overflow, Sign, Parity).
    """

    def __init__(self):
        """Initialize all flags to 0."""
        self.Zero: int = 0
        self.Carry: int = 0
        self.Overflow: int = 0
        self.Sign: int = 0
        self.Parity: int = 0
        self.reset()

    def reset(self):
        """Set all flags to 0."""
        self.Zero = 0
        self.Carry = 0
        self.Overflow = 0
        self.Sign = 0
        self.Parity = 0

    def update(self, result_bits: List[int],
               carry_out: int,
               overflow: int):
        """
        Update flags based on the result of an operation.

        Args:
            result_bits: The N-bit result of the operation.
            carry_out: The raw carry bit from the operation (if any).
            overflow: The overflow bit from the operation (if any).
        """
        self.reset()
        bit_width = len(result_bits)

        # 1. Zero Flag: Set if result is all zeros
        is_zero = 1
        for bit in result_bits:
            is_zero = LogicGates.AND(is_zero, LogicGates.NOT(bit))
        self.Zero = is_zero

        # 2. Carry Flag: Set if operation generated a carry/borrow
        self.Carry = carry_out

        # 3. Overflow Flag: Set if 2's complement overflow occurred
        self.Overflow = overflow

        # 4. Sign Flag: Set if MSB of result is 1
        self.Sign = result_bits[bit_width - 1]

        # 5. Parity Flag: Set if result has an odd number of 1s
        self.Parity = BinaryAnalyzer.check_parity(result_bits)

    def to_dict(self) -> Dict[str, int]:
        """Returns flags as a dictionary for the GUI."""
        return {
            "Zero": self.Zero,
            "Carry": self.Carry,
            "Overflow": self.Overflow,
            "Sign": self.Sign,
            "Parity": self.Parity
        }


class ALU:
    """
    Simulates the Arithmetic Logic Unit.

    Executes opcodes, operates on binary lists, and updates flags.
    """

    # --- Operation Opcodes ---
    OP_ADD = 0x01
    OP_SUB = 0x02
    OP_MUL = 0x03
    OP_DIV = 0x04

    OP_AND = 0x10
    OP_OR = 0x11
    OP_XOR = 0x12
    OP_NOT = 0x13

    OP_SHL = 0x20  # Logical Shift Left
    OP_SHR = 0x21  # Logical Shift Right
    OP_ROL = 0x22  # Rotate Left
    OP_ROR = 0x23  # Rotate Right

    # ---

    def __init__(self, bit_width: int):
        """
        Initialize the ALU.

        Args:
            bit_width: The number of bits for operations (e.g., 8).
        """
        self.bit_width = bit_width
        self.arithmetic = BinaryArithmetic(bit_width)
        self.flags = ALUFlags()
        self.execution_log = []

    def _add_log(self, description: str, data: Dict[str, Any]):
        """Helper to add a step to the execution log."""
        step_data = {
            'description': description,
            'data': {}
        }
        for key, value in data.items():
            if isinstance(value, list):
                step_data['data'][key] = BinaryAnalyzer.format_binary_string(value)
            else:
                step_data['data'][key] = str(value)
        self.execution_log.append(step_data)

    def execute(self, opcode: int, a_bits: List[int],
                b_bits: Optional[List[int]] = None,
                trace: bool = False) -> List[int]:
        """
        Executes a single ALU operation.

        Args:
            opcode: The operation code (e.g., ALU.OP_ADD).
            a_bits: The first operand.
            b_bits: The second operand (optional for unary ops).
            trace: If True, generates detailed trace.

        Returns:
            List[int]: The N-bit result.
        """
        self.execution_log = []
        if trace:
            self._add_log("ALU Execution Start", {
                "Opcode": hex(opcode),
                "Operand A": a_bits,
                "Operand B": b_bits if b_bits else "N/A"
            })

        # Ensure b_bits is valid for binary ops
        if b_bits is None:
            b_bits = [0] * self.bit_width

        result_bits = [0] * self.bit_width
        carry_out = 0
        overflow = 0

        # --- Arithmetic Operations ---
        if opcode == self.OP_ADD:
            result_bits, carry_out = self.arithmetic.ripple_carry_adder(
                a_bits, b_bits, trace=trace
            )
            self.execution_log.extend(self.arithmetic.execution_steps)
            # TODO: Add overflow detection for addition

        elif opcode == self.OP_SUB:
            result_bits, borrow, ovf = self.arithmetic.subtract(
                a_bits, b_bits, trace=trace
            )
            self.execution_log.extend(self.arithmetic.execution_steps)
            carry_out = borrow  # Use borrow as the "carry" flag
            overflow = ovf

        elif opcode == self.OP_MUL:
            # Note: Multiplication result is 2N bits,
            # but ALU returns N bits. We return the LSB half.
            prod_bits = self.arithmetic.multiply(a_bits, b_bits, trace=trace)
            self.execution_log.extend(self.arithmetic.execution_steps)
            result_bits = prod_bits[:self.bit_width]
            # Check if MSB half has data (overflow)
            for i in range(self.bit_width, self.bit_width * 2):
                if prod_bits[i] == 1:
                    overflow = 1
                    break

        elif opcode == self.OP_DIV:
            quotient, remainder = self.arithmetic.divide(
                a_bits, b_bits, trace=trace
            )
            self.execution_log.extend(self.arithmetic.execution_steps)
            result_bits = quotient  # Return quotient as main result
            # We could store remainder in a separate register,
            # but for now it's just in the log.

        # --- Logical Operations ---
        elif opcode == self.OP_AND:
            for i in range(self.bit_width):
                result_bits[i] = LogicGates.AND(a_bits[i], b_bits[i])
            self._add_log("Logical AND", {"Result": result_bits})

        elif opcode == self.OP_OR:
            for i in range(self.bit_width):
                result_bits[i] = LogicGates.OR(a_bits[i], b_bits[i])
            self._add_log("Logical OR", {"Result": result_bits})

        elif opcode == self.OP_XOR:
            for i in range(self.bit_width):
                result_bits[i] = LogicGates.XOR(a_bits[i], b_bits[i])
            self._add_log("Logical XOR", {"Result": result_bits})

        elif opcode == self.OP_NOT:
            for i in range(self.bit_width):
                result_bits[i] = LogicGates.NOT(a_bits[i])
            self._add_log("Logical NOT", {"Result": result_bits})

        # --- Bitwise Shift/Rotate Operations ---
        elif opcode == self.OP_SHL:
            carry_out = a_bits[self.bit_width - 1]  # MSB is shifted out
            result_bits = a_bits[1:] + [0]
            self._add_log("Logical Shift Left (SHL)", {
                "Result": result_bits, "Carry": carry_out
            })

        elif opcode == self.OP_SHR:
            carry_out = a_bits[0]  # LSB is shifted out
            result_bits = [0] + a_bits[:-1]
            self._add_log("Logical Shift Right (SHR)", {
                "Result": result_bits, "Carry": carry_out
            })

        elif opcode == self.OP_ROL:
            carry_out = a_bits[self.bit_width - 1]  # MSB
            result_bits = a_bits[1:] + [carry_out]  # MSB wraps to LSB
            self._add_log("Rotate Left (ROL)", {
                "Result": result_bits, "Carry": carry_out
            })

        elif opcode == self.OP_ROR:
            carry_out = a_bits[0]  # LSB
            result_bits = [carry_out] + a_bits[:-1]  # LSB wraps to MSB
            self._add_log("Rotate Right (ROR)", {
                "Result": result_bits, "Carry": carry_out
            })

        else:
            self._add_log("ERROR: Unknown Opcode", {"Opcode": hex(opcode)})

        # Update all flags based on the result
        self.flags.update(result_bits, carry_out, overflow)

        if trace:
            self._add_log("ALU Execution Complete", {
                "Final Result": result_bits,
                "Flags": str(self.flags.to_dict())
            })

        return result_bits


class ControlUnit:
    """
    Simulates the Control Unit.

    Receives "instructions" (simplified as opcodes and operands),
    directs the ALU to execute, and returns the result.
    """

    def __init__(self, alu: ALU):
        """
        Initialize the Control Unit, linking it to an ALU.

        Args:
            alu: The ALU instance this CU will control.
        """
        self.alu = alu

    def decode_and_execute(self, instruction: Dict,
                           trace: bool = False) -> List[int]:
        """
        Decodes an instruction and commands the ALU.

        Args:
            instruction: A dictionary containing:
                'opcode': The operation (e.g., ALU.OP_ADD)
                'operand_a': The first N-bit operand
                'operand_b': The second N-bit operand (optional)
            trace: If True, enables tracing in the ALU.

        Returns:
            List[int]: The N-bit result from the ALU.
        """
        opcode = instruction.get('opcode')
        a_bits = instruction.get('operand_a')
        b_bits = instruction.get('operand_b')

        if opcode is None or a_bits is None:
            raise ValueError("Invalid instruction: missing opcode or operand_a")

        # Command the ALU to execute
        result = self.alu.execute(
            opcode=opcode,
            a_bits=a_bits,
            b_bits=b_bits,
            trace=trace
        )

        return result


# Test suite
if __name__ == "__main__":
    print("=" * 70)
    print("ALU SIMULATOR TEST SUITE")
    print("=" * 70)

    BIT_WIDTH = 8
    alu = ALU(BIT_WIDTH)
    control = ControlUnit(alu)

    # Operands
    A_15 = BinaryAnalyzer.decimal_to_binary(15, BIT_WIDTH)  # 0000 1111
    B_7 = BinaryAnalyzer.decimal_to_binary(7, BIT_WIDTH)  # 0000 0111

    # Test 1: ADD (15 + 7 = 22)
    print("\n1. TEST: ADD (15 + 7 = 22)")
    instruction = {'opcode': ALU.OP_ADD, 'operand_a': A_15, 'operand_b': B_7}
    result = control.decode_and_execute(instruction, trace=True)
    res_dec = BinaryAnalyzer.binary_to_decimal(result)

    print(f"   Result: {BinaryAnalyzer.format_binary_string(result)} (Decimal: {res_dec})")
    print(f"   Flags: {alu.flags.to_dict()}")

    # 22 = 0001 0110. Parity = 3 (odd) = 1. Sign=0. Zero=0.
    assert res_dec == 22
    assert alu.flags.Zero == 0
    assert alu.flags.Sign == 0
    assert alu.flags.Parity == 1
    print("   Test PASSED")

    # Test 2: AND (15 & 7 = 7)
    print("\n2. TEST: AND (0000 1111 & 0000 0111 = 0000 0111)")
    instruction = {'opcode': ALU.OP_AND, 'operand_a': A_15, 'operand_b': B_7}
    result = control.decode_and_execute(instruction, trace=True)
    res_dec = BinaryAnalyzer.binary_to_decimal(result)

    print(f"   Result: {BinaryAnalyzer.format_binary_string(result)} (Decimal: {res_dec})")
    print(f"   Flags: {alu.flags.to_dict()}")

    assert res_dec == 7
    assert alu.flags.Parity == 1  # 3 ones = odd
    print("   Test PASSED")

    # Test 3: NOT (NOT 15 = 240)
    print("\n3. TEST: NOT (NOT 0000 1111 = 1111 0000)")
    instruction = {'opcode': ALU.OP_NOT, 'operand_a': A_15}
    result = control.decode_and_execute(instruction, trace=True)
    res_dec = BinaryAnalyzer.binary_to_decimal(result)

    print(f"   Result: {BinaryAnalyzer.format_binary_string(result)} (Decimal: {res_dec})")
    print(f"   Flags: {alu.flags.to_dict()}")

    # 240 = 1111 0000. Parity = 4 (even) = 0. Sign=1.
    assert res_dec == 240
    assert alu.flags.Sign == 1
    assert alu.flags.Parity == 0
    print("   Test PASSED")

    # Test 4: SHL (15 << 1 = 30)
    print("\n4. TEST: SHL (0000 1111 << 1 = 0001 1110)")
    instruction = {'opcode': ALU.OP_SHL, 'operand_a': A_15}
    result = control.decode_and_execute(instruction, trace=True)
    res_dec = BinaryAnalyzer.binary_to_decimal(result)

    print(f"   Result: {BinaryAnalyzer.format_binary_string(result)} (Decimal: {res_dec})")
    print(f"   Flags: {alu.flags.to_dict()}")

    # MSB (bit 7) was 0, so Carry=0
    assert res_dec == 30
    assert alu.flags.Carry == 0
    print("   Test PASSED")
