Conceptual Circuit Diagrams

This document explains how the complex arithmetic units in the simulator are built from the ground up using fundamental logic gates.

1. Fundamental Gates (The Building Blocks)

All logic originates from these basic gates.

AND Gate

Output is 1 only if A AND B are 1.

A --\
   [AND]-- OUT
B --/


OR Gate

Output is 1 if A OR B (or both) are 1.

A --\
   [OR ]-- OUT
B --/


XOR Gate (Exclusive OR)

Output is 1 only if A and B are different.

A --\
   [XOR]-- OUT
B --/


NOT Gate (Inverter)

Output is the opposite of the input.

A --[NOT]-- OUT


2. Combinational Circuits

These circuits combine basic gates to perform a specific function.

Half Adder

Adds two single bits, A and B. It outputs a Sum and a Carry.

Circuit: It is made of one XOR gate and one AND gate.

Logic:

Sum = A XOR B

Carry = A AND B

ASCII Diagram:

      +-------[XOR]-- SUM
A ----|
      |
      +-------[AND]-- CARRY
B ----|


Truth Table:
| A | B | Sum | Carry |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

Full Adder

Adds three single bits: A, B, and a Carry_In (from the previous bit). It is built using two Half Adders and an OR gate.

ASCII Diagram:

        +--------------[HA 1]--+
A ------|              |       |
        |      Sum1 ---|       +----[OR]---- CARRY_OUT
B ------|              |       |
        +--------------+       |
               Carry1 ---------+

        +--------------[HA 2]--+
C_In ---|              |       |
        |      Sum_Out(SUM)    |
Sum1 ---|                      |
        |      Carry2 ---------+
        +--------------+


3. Arithmetic Units (Conceptual)

These units chain combinational circuits to perform N-bit arithmetic.

8-Bit Ripple Carry Adder

This circuit adds two 8-bit numbers. It is simply a chain of 8 Full Adders. The Carry_Out of one Full Adder becomes the Carry_In of the next.

ASCII Diagram:

(LSB)                                                      (MSB)
A0,B0 --+      A1,B1 --+      ...      A7,B7 --+
        |             |                       |
C_in=0 ->[FA_0]-> C_out ->[FA_1]-> C_out -> ... ->[FA_7]-> C_out(FINAL CARRY)
        |             |                       |
       Sum0          Sum1                    Sum7


8-Bit Subtractor (2's Complement)

This simulator performs subtraction A - B by using the 2's Complement method. This allows us to perform subtraction by using our existing Ripple Carry Adder.

The logic is: A - B = A + (NOT B) + 1

This is achieved by:

Inverting all 8 bits of B (using 8 NOT gates). This is the 1's Complement.

Adding A and (NOT B) using our 8-bit Ripple Carry Adder.

Setting the initial Carry_In of the first Full Adder to 1. This adds the + 1 required to complete the 2's Complement.

ASCII Diagram:

     B0 ->[NOT]--+
A0 --------------+
                 |
     B1 ->[NOT]--+      ...      B7 ->[NOT]--+
A1 --------------+                       A7 --------------+
                 |                                        |
C_in=1 ->[FA_0]-> C_out ->[FA_1]-> C_out -> ... ->[FA_7]-> C_out(BORROW)
        |             |                       |
       Res0          Res1                    Res7


The final C_out is inverted to become the Borrow flag.
